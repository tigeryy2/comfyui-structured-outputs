import base64
from io import BytesIO

import numpy as np
import torch
from PIL import Image


def tensor_to_pil_image(image_tensor: torch.Tensor) -> Image.Image:
    """
    Converts a torch.Tensor image of shape [B, H, W, C] to a PIL Image.
    If batch size > 1, the first image in the batch is used.

    Args:
        image_tensor (torch.Tensor): Image tensor with shape [B, H, W, C].

    Returns:
        PIL.Image.Image: The converted image.
    """
    if image_tensor.ndim != 4:
        raise ValueError("Expected image tensor with 4 dimensions [B, H, W, C]")

    # Use the first image in the batch.
    img = image_tensor[0].detach().cpu().numpy()

    # If the image has a single channel with shape (H, W, 1), squeeze it to (H, W)
    if img.shape[-1] == 1:
        img = img.squeeze(-1)

    # If the image is a float type, assume the values are in [0,1] and convert them to [0,255]
    if np.issubdtype(img.dtype, np.floating):
        img = (img * 255).clip(0, 255).astype(np.uint8)

    return Image.fromarray(img)


def pil_image_to_base64(pil_img: Image.Image, image_format: str = "PNG") -> str:
    """
    Converts a PIL Image to a base64-encoded string.

    Args:
        pil_img (PIL.Image.Image): The image to convert.
        image_format (str): The format to use when saving the image (default 'PNG').

    Returns:
        str: The base64-encoded string of the image.
    """
    buffered = BytesIO()
    pil_img.save(buffered, format=image_format)
    img_bytes = buffered.getvalue()
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return base64_str


def tensor_to_base64(image_tensor: torch.Tensor, image_format: str = "PNG") -> str:
    """
    Converts a torch.Tensor image of shape [B, H, W, C] to a base64-encoded string.

    Args:
        image_tensor (torch.Tensor): The image tensor to convert.
        image_format (str): The image format for the output (default 'PNG').

    Returns:
        str: The base64-encoded string of the image.
    """
    pil_img = tensor_to_pil_image(image_tensor)
    return pil_image_to_base64(pil_img, image_format)


def base64_to_pil(base64_str: str) -> Image.Image:
    """
    Converts a base64-encoded string back to a PIL Image.

    Args:
        base64_str (str): The base64-encoded image string.

    Returns:
        PIL.Image.Image: The decoded image.
    """
    decoded_bytes = base64.b64decode(base64_str)
    buffer = BytesIO(decoded_bytes)
    pil_img = Image.open(buffer)
    pil_img.load()  # Ensure the image is loaded.
    return pil_img


def pil_image_to_tensor(pil_img: Image.Image) -> torch.Tensor:
    """
    Converts a PIL Image to a torch.Tensor with shape [B, H, W, C].

    Args:
        pil_img (PIL.Image.Image): The PIL image to convert.

    Returns:
        torch.Tensor: The image tensor with shape [1, H, W, C].
    """
    np_img = np.array(pil_img)
    # If the image is grayscale (shape: H x W), add a channel dimension.
    if np_img.ndim == 2:
        np_img = np.expand_dims(np_img, axis=-1)
    tensor_img = torch.from_numpy(np_img)
    # Add the batch dimension.
    tensor_img = tensor_img.unsqueeze(0)
    return tensor_img


def base64_to_tensor(base64_str: str) -> torch.Tensor:
    """
    Converts a base64-encoded image string back to a torch.Tensor of shape [B, H, W, C].

    Args:
        base64_str (str): The base64-encoded image string.

    Returns:
        torch.Tensor: The decoded image tensor.
    """
    pil_img = base64_to_pil(base64_str)
    return pil_image_to_tensor(pil_img)
