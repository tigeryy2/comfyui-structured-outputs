import instructor
from instructor import Instructor
from openai import OpenAI

from ..comfyui_structured_outputs import DOTENV_FILE
from ..comfyui_structured_outputs.attribute_utils import (
    BaseAttributeModel,
    BaseAttributesModel,
    attributes_to_model,
)
from ..comfyui_structured_outputs.utils.loggable import Loggable
from ..comfyui_structured_outputs.utils.utils import get_env


class StructuredOutputNode(Loggable):
    NAME: str = "StructuredOutputNode"
    RETURN_TYPES = ("ATTRIBUTE",)
    RETURN_NAMES = ("attribute",)
    CATEGORY = "structured_output"
    FUNCTION = "get_structured_output"

    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "attributes": ("ATTRIBUTE", {}),
            }
        }

    def get_structured_output(
        self, prompt: [str], attributes: [type[BaseAttributeModel]]
    ):
        prompt: str = prompt[0]
        attributes_model: type[BaseAttributesModel] = attributes_to_model(attributes)

        openai_key: str = get_env("OPENAI_KEY", DOTENV_FILE)

        instructor_client: Instructor = instructor.from_openai(
            OpenAI(api_key=openai_key)
        )

        response = instructor_client.chat.completions.create(
            model="gpt-4o",
            response_model=attributes_model,
            messages=[{"role": "user", "content": prompt}],
        )

        return [response]
