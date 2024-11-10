from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDtoModel(BaseModel):
    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class ApiRequest(BaseDtoModel):
    topic: Optional[str] = None
    text: str
    options: Dict[str, Any]


class ClassifierAttributeDto(BaseDtoModel):
    name: str
    value: Any


class ApiResponse(BaseDtoModel):
    attributes: List[ClassifierAttributeDto]
