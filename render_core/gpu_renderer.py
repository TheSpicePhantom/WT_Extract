"""GPU-Renderer: Swapchain Clear via Vulkan Command Buffers auf der GPU."""

from __future__ import annotations

from dataclasses import dataclass, field
import time

from collections.abc import Callable

from vulkan import *  # noqa: F403

from render_core.device import GpuDevice, create_gpu_device, destroy_gpu_device, query_swapchain_support
from render_core.frame_sync import MAX_FRAMES_IN_FLIGHT
from render_core.instance import InstanceConfig, create_instance, destroy_instance
from render_core.policy import assert_gpu_only
from render_core.render_pass import (
    SwapchainFramebuffers,
    create_swapchain_framebuffers,
    create_swapchain_render_pass,
    destroy_swapchain_framebuffers,
)
from render_core.staging import FrameStagingUploader
from render_core.gpu_timing import GpuFrameTimer
from render_core.surface import create_surface, destroy_surface
from render_core.swapchain import Swapchain, create_swapchain, destroy_swapchain
from render_core.vk_loader import VulkanKhrApi
from render_core.vk_types import (
    VkCommandBuffer,
    VkCommandPool,
    VkDevice,
    VkExtent2D,
    VkFence,
    VkFramebuffer,
    VkInstance,
    VkRenderPass,
    VkSemaphore,
    VkSurfaceKHR,
)
from wt_platform.window import Window


def _timed_pre_render(
    fn: Callable[[int, VkCommandBuffer], None] | None,
    timing_fn: Callable[[str, float], None] | None,
    frame_index: int,
    command_buffer: VkCommandBuffer,
) -> None:
    if fn is None:
        return
    t0 = time.perf_counter()
    fn(frame_index, command_buffer)
    if timing_fn is not None:
        timing_fn("pre_render_ms", (time.perf_counter() - t0) * 1000.0)


@dataclass
class FrameResources:
    command_pool: VkCommandPool
    command_buffer: VkCommandBuffer
    image_available: VkSemaphore
    render_finished: VkSemaphore
    in_flight_fence: VkFence


@dataclass
class GpuRenderer:
    """Minimaler GPU-Renderpfad — kein CPU-Fallback."""

    window: Window
    instance: VkInstance
    surface: VkSurfaceKHR
    khr: VulkanKhrApi
    device: GpuDevice
    swapchain: Swapchain
    framebuffers: SwapchainFramebuffers
    frames: list[FrameResources] = field(default_factory=list)
    staging: FrameStagingUploader | None = None
    gpu_timer: GpuFrameTimer | None = None
    current_frame: int = 0
    _last_framebuffer_size: tuple[int, int] = field(default=(-1, -1), repr=False)

    @classmethod
    def create(cls, window: Window, enable_validation: bool = False) -> GpuRenderer:
        assert_gpu_only("GpuRenderer.create")

        instance = create_instance(InstanceConfig(enable_validation=enable_validation))
        khr = VulkanKhrApi.for_instance(instance)
        surface = create_surface(instance, window)
        device = create_gpu_device(khr, instance, surface)
        khr.bind_device(device.logical)

        width, height = window.framebuffer_size
        swapchain = create_swapchain(
            khr,
            device.logical,
            device.physical,
            surface,
            device.queue_family_indices,
            width,
            height,
        )
        render_pass = create_swapchain_render_pass(device.logical, swapchain.image_format)
        framebuffers = create_swapchain_framebuffers(device.logical, render_pass, swapchain)
        frames = _create_frame_resources(device.logical, device.queue_family_indices.graphics)
        staging = FrameStagingUploader.create(device.physical, device.logical)
        gpu_timer = GpuFrameTimer.try_create(device.physical, device.logical)

        return cls(
            window=window,
            instance=instance,
            surface=surface,
            khr=khr,
            device=device,
            swapchain=swapchain,
            framebuffers=framebuffers,
            frames=frames,
            staging=staging,
            gpu_timer=gpu_timer,
            _last_framebuffer_size=swapchain.extent_size,
        )

    def draw_frame(self, clear_color: tuple[float, float, float, float] = (0.08, 0.09, 0.11, 1.0)) -> None:
        while self.draw_frame_with_record(clear_color=clear_color):
            pass

    def draw_frame_with_record(
        self,
        record_fn: Callable[[VkCommandBuffer, VkExtent2D], None] | None = None,
        clear_color: tuple[float, float, float, float] = (0.08, 0.09, 0.11, 1.0),
        prepare_fn: Callable[[int], None] | None = None,
        pre_render_fn: Callable[[int, VkCommandBuffer], None] | None = None,
        timing_fn: Callable[[str, float], None] | None = None,
    ) -> bool:
        """GPU-Frame mit optionalem Render-Pass-Recording. Gibt True zurück wenn Swapchain neu erstellt wurde."""
        assert_gpu_only("GpuRenderer.draw_frame_with_record")

        width, height = self.window.framebuffer_size
        if width < 1 or height < 1:
            return False

        if self._needs_swapchain_recreate():
            self._recreate_swapchain()
            return True

        frame_index = self.current_frame
        frame = self.frames[frame_index]

        # M25: GPU-Timing Readback (vor Fence-Wait: hier ist der Slot noch "previous frame").
        # Wir lesen nach dem Fence-Wait, damit Query-Daten garantiert fertig sind.
        t0 = time.perf_counter()
        vkWaitForFences(self.device.logical, 1, [frame.in_flight_fence], VK_TRUE, UINT64_MAX)
        if timing_fn is not None:
            timing_fn("wait_fence_ms", (time.perf_counter() - t0) * 1000.0)
        if self.gpu_timer is not None and timing_fn is not None:
            gpu_frame_ms, gpu_render_ms = self.gpu_timer.try_read_ms(frame_index)
            if gpu_frame_ms is not None:
                timing_fn("gpu_frame_ms", gpu_frame_ms)
            if gpu_render_ms is not None:
                timing_fn("gpu_renderpass_ms", gpu_render_ms)

        if prepare_fn is not None:
            prepare_fn(frame_index)

        try:
            t1 = time.perf_counter()
            image_index = self.khr.vkAcquireNextImageKHR(
                self.device.logical,
                self.swapchain.handle,
                UINT64_MAX,
                frame.image_available,
                VK_NULL_HANDLE,
            )
            if timing_fn is not None:
                timing_fn("acquire_ms", (time.perf_counter() - t1) * 1000.0)
        except VkErrorOutOfDateKhr:
            self._recreate_swapchain()
            return True

        vkResetFences(self.device.logical, 1, [frame.in_flight_fence])
        vkResetCommandBuffer(frame.command_buffer, 0)
        t_record = time.perf_counter()
        _record_render_pass_commands(
            frame.command_buffer,
            self.framebuffers.render_pass,
            self.framebuffers.framebuffers[image_index],
            self.swapchain.extent,
            clear_color,
            pre_render_fn=lambda command_buffer: (
                _timed_pre_render(pre_render_fn, timing_fn, frame_index, command_buffer)
            )
            if pre_render_fn is not None
            else None,
            record_fn=record_fn,
            gpu_timer=self.gpu_timer,
            frame_index=frame_index,
        )
        if timing_fn is not None:
            timing_fn("record_ms", (time.perf_counter() - t_record) * 1000.0)

        wait_stages = [VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT]
        submit_info = VkSubmitInfo(
            waitSemaphoreCount=1,
            pWaitSemaphores=[frame.image_available],
            pWaitDstStageMask=wait_stages,
            commandBufferCount=1,
            pCommandBuffers=[frame.command_buffer],
            signalSemaphoreCount=1,
            pSignalSemaphores=[frame.render_finished],
        )
        t_submit = time.perf_counter()
        vkQueueSubmit(self.device.graphics_queue, 1, [submit_info], frame.in_flight_fence)
        if timing_fn is not None:
            timing_fn("submit_ms", (time.perf_counter() - t_submit) * 1000.0)

        present_info = VkPresentInfoKHR(
            waitSemaphoreCount=1,
            pWaitSemaphores=[frame.render_finished],
            swapchainCount=1,
            pSwapchains=[self.swapchain.handle],
            pImageIndices=[image_index],
        )

        try:
            t_present = time.perf_counter()
            self.khr.vkQueuePresentKHR(self.device.present_queue, present_info)
            if timing_fn is not None:
                timing_fn("present_ms", (time.perf_counter() - t_present) * 1000.0)
        except VkErrorOutOfDateKhr:
            self._recreate_swapchain()
            return True
        except VkSuboptimalKhr:
            if self._needs_swapchain_recreate():
                self._recreate_swapchain()
                return True

        self.current_frame = (self.current_frame + 1) % MAX_FRAMES_IN_FLIGHT
        return False

    def recreate_swapchain_for_surface_change(self) -> None:
        """Swapchain nach Fenster-/Vollbild-Wechsel synchron neu aufbauen."""
        self._wait_until_frames_complete()
        self._recreate_swapchain(force=True)

    def _wait_until_frames_complete(self) -> None:
        for frame in self.frames:
            vkWaitForFences(self.device.logical, 1, [frame.in_flight_fence], VK_TRUE, UINT64_MAX)
        vkDeviceWaitIdle(self.device.logical)

    def _needs_swapchain_recreate(self) -> bool:
        fb = self.window.framebuffer_size
        if fb[0] < 1 or fb[1] < 1:
            return False
        return fb != self.swapchain.extent_size

    def _resolve_swapchain_size(self) -> tuple[int, int]:
        """Wartet bis GLFW-Framebuffer und Vulkan-Surface-Extent übereinstimmen."""
        for _ in range(256):
            self.window.poll_events()
            fb_w, fb_h = self.window.framebuffer_size
            if fb_w < 1 or fb_h < 1:
                continue
            support = query_swapchain_support(self.khr, self.device.physical, self.surface)
            current = support.capabilities.currentExtent
            if current.width == 0xFFFFFFFF:
                return fb_w, fb_h
            if current.width >= 1 and current.height >= 1:
                if current.width == fb_w and current.height == fb_h:
                    return fb_w, fb_h
        fb_w, fb_h = self.window.framebuffer_size
        return max(fb_w, 1), max(fb_h, 1)

    def wait_for_frame_slot(self) -> int:
        """Wartet bis der aktuelle Frame-Slot frei ist — vor GPU-Buffer-Uploads aufrufen."""
        frame = self.frames[self.current_frame]
        vkWaitForFences(self.device.logical, 1, [frame.in_flight_fence], VK_TRUE, UINT64_MAX)
        return self.current_frame

    def _recreate_swapchain(self, *, force: bool = False) -> None:
        width, height = self.window.framebuffer_size
        while width < 1 or height < 1:
            self.window.poll_events()
            if self.window.should_close:
                return
            width, height = self.window.framebuffer_size

        if not force and not self._needs_swapchain_recreate():
            return

        self._wait_until_frames_complete()

        old_swapchain = self.swapchain
        destroy_swapchain_framebuffers(self.device.logical, self.framebuffers)

        width, height = self._resolve_swapchain_size()
        self.swapchain = create_swapchain(
            self.khr,
            self.device.logical,
            self.device.physical,
            self.surface,
            self.device.queue_family_indices,
            width,
            height,
            old_swapchain=old_swapchain.handle,
        )
        destroy_swapchain(self.khr, self.device.logical, old_swapchain)

        render_pass = create_swapchain_render_pass(self.device.logical, self.swapchain.image_format)
        self.framebuffers = create_swapchain_framebuffers(
            self.device.logical,
            render_pass,
            self.swapchain,
        )
        self._last_framebuffer_size = self.swapchain.extent_size

    def destroy(self) -> None:
        if self.device.logical:
            try:
                vkDeviceWaitIdle(self.device.logical)
            except VkErrorDeviceLost:
                pass

        if self.gpu_timer is not None:
            self.gpu_timer.destroy()
            self.gpu_timer = None

        for frame in self.frames:
            vkDestroySemaphore(self.device.logical, frame.image_available, None)
            vkDestroySemaphore(self.device.logical, frame.render_finished, None)
            vkDestroyFence(self.device.logical, frame.in_flight_fence, None)
            vkDestroyCommandPool(self.device.logical, frame.command_pool, None)

        if self.staging is not None:
            self.staging.destroy()
            self.staging = None

        destroy_swapchain_framebuffers(self.device.logical, self.framebuffers)
        destroy_swapchain(self.khr, self.device.logical, self.swapchain)
        destroy_gpu_device(self.device)
        destroy_surface(self.khr, self.instance, self.surface)
        destroy_instance(self.instance)


def _create_frame_resources(device: VkDevice, graphics_queue_family: int) -> list[FrameResources]:
    frames: list[FrameResources] = []
    for _ in range(MAX_FRAMES_IN_FLIGHT):
        pool_info = VkCommandPoolCreateInfo(
            queueFamilyIndex=graphics_queue_family,
            flags=VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT,
        )
        command_pool = vkCreateCommandPool(device, pool_info, None)

        alloc_info = VkCommandBufferAllocateInfo(
            commandPool=command_pool,
            level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,
            commandBufferCount=1,
        )
        command_buffer = vkAllocateCommandBuffers(device, alloc_info)[0]

        semaphore_info = VkSemaphoreCreateInfo()
        image_available = vkCreateSemaphore(device, semaphore_info, None)
        render_finished = vkCreateSemaphore(device, semaphore_info, None)

        fence_info = VkFenceCreateInfo(flags=VK_FENCE_CREATE_SIGNALED_BIT)
        in_flight_fence = vkCreateFence(device, fence_info, None)

        frames.append(
            FrameResources(
                command_pool=command_pool,
                command_buffer=command_buffer,
                image_available=image_available,
                render_finished=render_finished,
                in_flight_fence=in_flight_fence,
            )
        )
    return frames


def _record_render_pass_commands(
    command_buffer: VkCommandBuffer,
    render_pass: VkRenderPass,
    framebuffer: VkFramebuffer,
    extent: VkExtent2D,
    clear_color: tuple[float, float, float, float],
    pre_render_fn: Callable[[VkCommandBuffer], None] | None = None,
    record_fn: Callable[[VkCommandBuffer, VkExtent2D], None] | None = None,
    gpu_timer: GpuFrameTimer | None = None,
    frame_index: int = 0,
) -> None:
    begin_info = VkCommandBufferBeginInfo(flags=VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)
    vkBeginCommandBuffer(command_buffer, begin_info)

    if gpu_timer is not None:
        gpu_timer.reset(command_buffer, frame_index)
        gpu_timer.write_start(command_buffer, frame_index)

    if pre_render_fn is not None:
        pre_render_fn(command_buffer)

    render_pass_info = VkRenderPassBeginInfo(
        renderPass=render_pass,
        framebuffer=framebuffer,
        renderArea=VkRect2D(
            offset=VkOffset2D(0, 0),
            extent=extent,
        ),
        clearValueCount=1,
        pClearValues=[VkClearValue(color=VkClearColorValue(float32=list(clear_color)))],
    )
    vkCmdBeginRenderPass(command_buffer, render_pass_info, VK_SUBPASS_CONTENTS_INLINE)
    if record_fn is not None:
        record_fn(command_buffer, extent)
    vkCmdEndRenderPass(command_buffer)

    if gpu_timer is not None:
        gpu_timer.write_after_renderpass(command_buffer, frame_index)
        gpu_timer.write_end(command_buffer, frame_index)
    vkEndCommandBuffer(command_buffer)
