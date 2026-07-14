"""Wiederverwendbare Frame-Staging-Buffer — Copy + Barrier im Frame-Command-Buffer."""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403

from render_core.buffer import create_buffer, destroy_buffer, upload_to_buffer
from render_core.frame_sync import MAX_FRAMES_IN_FLIGHT
from render_core.vk_types import VkBuffer, VkCommandBuffer, VkDevice, VkDeviceMemory, VkPhysicalDevice

INITIAL_STAGING_CAPACITY = 512 * 1024


@dataclass
class _StagingSlot:
    buffer: VkBuffer
    memory: VkDeviceMemory
    capacity: int


@dataclass
class FrameStagingUploader:
    """Pro Frame-Slot ein HOST_VISIBLE Staging-Buffer — CPU schreibt, Copy per vkCmdCopyBuffer."""

    physical: VkPhysicalDevice
    device: VkDevice
    slots: tuple[_StagingSlot, ...]

    @classmethod
    def create(
        cls,
        physical: VkPhysicalDevice,
        device: VkDevice,
        initial_capacity: int = INITIAL_STAGING_CAPACITY,
    ) -> FrameStagingUploader:
        slots: list[_StagingSlot] = []
        size = max(initial_capacity, 1)
        for _ in range(MAX_FRAMES_IN_FLIGHT):
            buffer, memory = create_buffer(
                physical,
                device,
                size,
                VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
            )
            slots.append(_StagingSlot(buffer=buffer, memory=memory, capacity=size))
        return cls(physical=physical, device=device, slots=tuple(slots))

    def destroy(self) -> None:
        for slot in self.slots:
            destroy_buffer(self.device, slot.buffer, slot.memory)

    def _ensure_slot_capacity(self, frame_index: int, size: int) -> None:
        slot = self.slots[frame_index]
        if size <= slot.capacity:
            return

        vkDeviceWaitIdle(self.device)
        destroy_buffer(self.device, slot.buffer, slot.memory)
        new_size = max(size, slot.capacity * 2)
        buffer, memory = create_buffer(
            self.physical,
            self.device,
            new_size,
            VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
        )
        new_slot = _StagingSlot(buffer=buffer, memory=memory, capacity=new_size)
        slots = list(self.slots)
        slots[frame_index] = new_slot
        self.slots = tuple(slots)

    def write(self, frame_index: int, data: bytes) -> None:
        if not data:
            return
        if not (0 <= frame_index < MAX_FRAMES_IN_FLIGHT):
            raise ValueError(
                f"frame_index muss 0..{MAX_FRAMES_IN_FLIGHT - 1} sein, erhalten {frame_index}."
            )
        self._ensure_slot_capacity(frame_index, len(data))
        upload_to_buffer(self.device, self.slots[frame_index].memory, data)

    def record_copy_to_vertex_buffer(
        self,
        command_buffer: VkCommandBuffer,
        frame_index: int,
        dst_buffer: VkBuffer,
        size: int,
    ) -> None:
        """Staging → DEVICE_LOCAL Vertex-Buffer, inkl. Transfer→Vertex-Input Barrier."""
        if size <= 0:
            return

        src_buffer = self.slots[frame_index].buffer
        copy_region = VkBufferCopy(srcOffset=0, dstOffset=0, size=size)
        vkCmdCopyBuffer(command_buffer, src_buffer, dst_buffer, 1, [copy_region])

        barrier = VkBufferMemoryBarrier(
            srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,
            dstAccessMask=VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT,
            srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            buffer=dst_buffer,
            offset=0,
            size=size,
        )
        vkCmdPipelineBarrier(
            command_buffer,
            VK_PIPELINE_STAGE_TRANSFER_BIT,
            VK_PIPELINE_STAGE_VERTEX_INPUT_BIT,
            0,
            0,
            None,
            1,
            [barrier],
            0,
            None,
        )
