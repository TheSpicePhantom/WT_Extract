"""Render Pass und Framebuffers — GPU Clear auf Swapchain-Images."""

from __future__ import annotations

from dataclasses import dataclass

from vulkan import *  # noqa: F403

from render_core.swapchain import Swapchain
from render_core.vk_types import VkDevice, VkFormat, VkFramebuffer, VkRenderPass


@dataclass
class SwapchainFramebuffers:
    render_pass: VkRenderPass
    framebuffers: list[VkFramebuffer]


def create_swapchain_render_pass(device: VkDevice, swapchain_format: VkFormat) -> VkRenderPass:
    color_attachment = VkAttachmentDescription(
        format=swapchain_format,
        samples=VK_SAMPLE_COUNT_1_BIT,
        loadOp=VK_ATTACHMENT_LOAD_OP_CLEAR,
        storeOp=VK_ATTACHMENT_STORE_OP_STORE,
        stencilLoadOp=VK_ATTACHMENT_LOAD_OP_DONT_CARE,
        stencilStoreOp=VK_ATTACHMENT_STORE_OP_DONT_CARE,
        initialLayout=VK_IMAGE_LAYOUT_UNDEFINED,
        finalLayout=VK_IMAGE_LAYOUT_PRESENT_SRC_KHR,
    )

    color_ref = VkAttachmentReference(
        attachment=0,
        layout=VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL,
    )

    subpass = VkSubpassDescription(
        pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS,
        colorAttachmentCount=1,
        pColorAttachments=[color_ref],
    )

    dependency = VkSubpassDependency(
        srcSubpass=VK_SUBPASS_EXTERNAL,
        dstSubpass=0,
        srcStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
        srcAccessMask=0,
        dstStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
        dstAccessMask=VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT,
    )

    render_pass_info = VkRenderPassCreateInfo(
        attachmentCount=1,
        pAttachments=[color_attachment],
        subpassCount=1,
        pSubpasses=[subpass],
        dependencyCount=1,
        pDependencies=[dependency],
    )
    return vkCreateRenderPass(device, render_pass_info, None)


def create_swapchain_framebuffers(
    device: VkDevice,
    render_pass: VkRenderPass,
    swapchain: Swapchain,
) -> SwapchainFramebuffers:
    framebuffers: list[VkFramebuffer] = []
    for view in swapchain.image_views:
        framebuffer_info = VkFramebufferCreateInfo(
            renderPass=render_pass,
            attachmentCount=1,
            pAttachments=[view],
            width=swapchain.extent.width,
            height=swapchain.extent.height,
            layers=1,
        )
        framebuffers.append(vkCreateFramebuffer(device, framebuffer_info, None))

    return SwapchainFramebuffers(render_pass=render_pass, framebuffers=framebuffers)


def destroy_swapchain_framebuffers(device: VkDevice, bundle: SwapchainFramebuffers) -> None:
    for framebuffer in bundle.framebuffers:
        vkDestroyFramebuffer(device, framebuffer, None)
    vkDestroyRenderPass(device, bundle.render_pass, None)
