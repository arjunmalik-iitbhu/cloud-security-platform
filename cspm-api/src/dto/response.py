from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class CredentialRes(BaseSchema):
    """
    Data Transfer Object for returning a actor.
    """

    id: int
    name: str


class AnalysisRes(BaseSchema):
    """
    Data Transfer Object for returning a director.
    """

    id: int
    name: str
