import torch

from comfyui_structured_outputs.utils.image_utils import (
    base64_to_tensor,
    tensor_to_base64,
)


def test_round_trip_uint8():
    """
    Test round-trip conversion for a uint8 image tensor.
    """
    # Create a dummy red image with shape [1, 100, 100, 3] and type uint8.
    red_image = torch.zeros((1, 100, 100, 3), dtype=torch.uint8)
    red_image[..., 0] = 255  # Set red channel to max.

    # Convert tensor -> base64 -> tensor.
    b64_str = tensor_to_base64(red_image, image_format="PNG")
    recovered_image = base64_to_tensor(b64_str)

    # Check that the recovered tensor matches the original.
    assert torch.equal(recovered_image, red_image), (
        "Recovered uint8 image tensor does not match the original."
    )


def test_round_trip_float():
    """
    Test round-trip conversion for a float image tensor.
    Since the conversion scales float values (in [0,1]) to uint8,
    compare against the expected scaled version.
    """
    # Create a dummy red image with shape [1, 100, 100, 3] and type float.
    red_image_float = torch.zeros((1, 100, 100, 3), dtype=torch.float32)
    red_image_float[..., 0] = 1.0  # Red channel at max.

    # Convert tensor -> base64 -> tensor.
    b64_str = tensor_to_base64(red_image_float, image_format="PNG")
    recovered_image = base64_to_tensor(b64_str)

    # Expected image: float image scaled to uint8.
    expected_image = (red_image_float[0] * 255).to(torch.uint8).unsqueeze(0)

    assert torch.equal(recovered_image, expected_image), (
        "Recovered image tensor from float conversion does not match the expected uint8 image."
    )
