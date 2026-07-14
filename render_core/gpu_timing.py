"""GPU-Timestamps (M25) — optionales Frame-Timing via VkQueryPool.

Design:
- Pro Frame-Slot ein fester Query-Index-Bereich (QUERY_COUNT Queries).
- WriteTimestamp im CommandBuffer, Readback nach Fence-Wait.
- Robust: wenn disabled oder unsupported → keine Messung, keine Crashes.
"""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403
from vulkan import ffi

from render_core.frame_sync import MAX_FRAMES_IN_FLIGHT
from render_core.vk_types import VkCommandBuffer, VkDevice, VkPhysicalDevice

QUERY_COUNT = 3  # start, after_renderpass, end


@dataclass
class GpuFrameTimer:
    physical: VkPhysicalDevice
    device: VkDevice
    query_pool: object
    timestamp_period_ns: float
    enabled: bool = True

    @classmethod
    def try_create(cls, physical: VkPhysicalDevice, device: VkDevice) -> GpuFrameTimer | None:
        props = vkGetPhysicalDeviceProperties(physical)
        period = float(getattr(props.limits, "timestampPeriod", 0.0) or 0.0)
        if period <= 0.0:
            return None

        # Note: We assume timestamp queries are supported for graphics queue. Most GPUs do.
        pool_info = VkQueryPoolCreateInfo(
            queryType=VK_QUERY_TYPE_TIMESTAMP,
            queryCount=MAX_FRAMES_IN_FLIGHT * QUERY_COUNT,
        )
        query_pool = vkCreateQueryPool(device, pool_info, None)
        return cls(
            physical=physical,
            device=device,
            query_pool=query_pool,
            timestamp_period_ns=period,
            enabled=True,
        )

    def destroy(self) -> None:
        if self.query_pool:
            vkDestroyQueryPool(self.device, self.query_pool, None)
            self.query_pool = VK_NULL_HANDLE

    def _base(self, frame_index: int) -> int:
        return int(frame_index) * QUERY_COUNT

    def reset(self, command_buffer: VkCommandBuffer, frame_index: int) -> None:
        if not self.enabled:
            return
        base = self._base(frame_index)
        vkCmdResetQueryPool(command_buffer, self.query_pool, base, QUERY_COUNT)

    def write_start(self, command_buffer: VkCommandBuffer, frame_index: int) -> None:
        if not self.enabled:
            return
        vkCmdWriteTimestamp(
            command_buffer,
            VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            self.query_pool,
            self._base(frame_index) + 0,
        )

    def write_after_renderpass(self, command_buffer: VkCommandBuffer, frame_index: int) -> None:
        if not self.enabled:
            return
        vkCmdWriteTimestamp(
            command_buffer,
            VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
            self.query_pool,
            self._base(frame_index) + 1,
        )

    def write_end(self, command_buffer: VkCommandBuffer, frame_index: int) -> None:
        if not self.enabled:
            return
        vkCmdWriteTimestamp(
            command_buffer,
            VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
            self.query_pool,
            self._base(frame_index) + 2,
        )

    def try_read_ms(self, frame_index: int) -> tuple[float | None, float | None]:
        """Returns (gpu_frame_ms, gpu_renderpass_ms) or (None, None) if unavailable."""
        if not self.enabled:
            return None, None

        base = self._base(frame_index)
        # cffi-Array + void*-Cast — PyVulkan akzeptiert kein ctypes/rohes cffi-Array als pData.
        results = ffi.new("uint64_t[]", QUERY_COUNT)
        stride = ffi.sizeof("uint64_t")
        flags = VK_QUERY_RESULT_64_BIT
        res = vkGetQueryPoolResults(
            self.device,
            self.query_pool,
            base,
            QUERY_COUNT,
            QUERY_COUNT * stride,
            ffi.cast("void*", results),
            stride,
            flags,
        )
        if res == VK_NOT_READY:
            return None, None
        if res != VK_SUCCESS:
            return None, None

        t0 = int(results[0])
        t1 = int(results[1])
        t2 = int(results[2])
        if t2 <= t0 or t1 < t0:
            return None, None

        ns_per_tick = self.timestamp_period_ns
        frame_ms = (t2 - t0) * ns_per_tick / 1_000_000.0
        render_ms = (t1 - t0) * ns_per_tick / 1_000_000.0 if t1 >= t0 else None
        return float(frame_ms), float(render_ms) if render_ms is not None else None

