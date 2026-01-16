from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class CredentialRes(BaseSchema):
    """
    Data Transfer Object for returning a credential.
    """

    id: int
    name: str

class ResourceRes(BaseSchema):
    """
    Data Transfer Object for returning a resource.
    """
    type: str
    details: dict
    cloud_id: int
    external_resource_id: Optional[str]
    current_resource_status: Optional[str]
    current_resource_risk: Optional[str]

class AnalysisRes(BaseSchema):
    """
    Data Transfer Object for returning a analysis.
    """

    credential_id: int
    resources: Optional[list[ResourceRes]] = []