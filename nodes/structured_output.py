import instructor
from instructor import Instructor
from openai import OpenAI

from ..comfyui_structured_outputs import DOTENV_FILE
from ..comfyui_structured_outputs.attribute_utils import (
    BaseAttributeModel,
    BaseAttributesModel,
    attributes_to_model,
)
from ..comfyui_structured_outputs.utils.image_utils import tensor_to_base64
from ..comfyui_structured_outputs.utils.loggable import Loggable
from ..comfyui_structured_outputs.utils.utils import get_env


class StructuredOutputNode(Loggable):
    NAME: str = "StructuredOutputNode"
    RETURN_TYPES = ("ATTRIBUTE",)
    RETURN_NAMES = ("attributes",)
    CATEGORY = "structured_output"
    FUNCTION = "get_structured_output"

    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "attributes": ("ATTRIBUTE", {}),
            },
            "optional": {
                "image_in": ("IMAGE", {}),
            },
        }

    def get_structured_output(
        self, prompt: [str], attributes: [type[BaseAttributeModel]], image_in=None
    ):
        prompt: str = prompt[0]
        attributes_model: type[BaseAttributesModel] = attributes_to_model(attributes)
        image_in = image_in[0] if image_in else None

        self.log().debug("Setting up Instructor client")
        openai_key: str = get_env("OPENAI_KEY", DOTENV_FILE)
        instructor_client: Instructor = instructor.from_openai(
            OpenAI(api_key=openai_key)
        )

        image_b64 = None
        if image_in is not None:
            self.log().debug("Converting tensor to base64")
            image_b64 = tensor_to_base64(image_in)

        response = instructor_client.chat.completions.create(
            model="gpt-4o",
            response_model=attributes_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        # if an image is provided, include
                        *(
                            [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_b64}"
                                    },
                                }
                            ]
                            if image_b64 is not None
                            else []
                        ),
                    ],
                }
            ],
        )

        return [response]
