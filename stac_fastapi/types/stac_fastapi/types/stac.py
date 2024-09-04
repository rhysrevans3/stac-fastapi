"""STAC types."""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from stac_pydantic.shared import BBox
from typing_extensions import TypedDict

NumType = Union[float, int]


class Catalog(TypedDict, total=False):
    """STAC Catalog."""

    type: str
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    title: Optional[str]
    description: str
    links: List[Dict[str, Any]]


class LandingPage(Catalog, total=False):
    """STAC Landing Page."""

    conformsTo: List[str]


class Conformance(TypedDict):
    """STAC Conformance Classes."""

    conformsTo: List[str]


class Collection(Catalog, total=False):
    """STAC Collection."""

    keywords: List[str]
    license: str
    providers: List[Dict[str, Any]]
    extent: Dict[str, Any]
    summaries: Dict[str, Any]
    assets: Dict[str, Any]


class Item(TypedDict, total=False):
    """STAC Item."""

    type: Literal["Feature"]
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    geometry: Dict[str, Any]
    bbox: BBox
    properties: Dict[str, Any]
    links: List[Dict[str, Any]]
    assets: Dict[str, Any]
    collection: str


class ItemCollection(TypedDict, total=False):
    """STAC Item Collection."""

    type: Literal["FeatureCollection"]
    features: List[Item]
    links: List[Dict[str, Any]]
    context: Optional[Dict[str, int]]


class Collections(TypedDict, total=False):
    """All collections endpoint.
    https://github.com/radiantearth/stac-api-spec/tree/master/collections
    """

    collections: List[Collection]
    links: List[Dict[str, Any]]


class PartialCollection(TypedDict, total=False):
    """Partial STAC Collection."""

    type: Optional[str]
    stac_version: Optional[str]
    stac_extensions: Optional[List[str]]
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    links: List[Dict[str, Any]]
    keywords: Optional[List[str]]
    license: Optional[str]
    providers: Optional[List[Dict[str, Any]]]
    extent: Optional[Dict[str, Any]]
    summaries: Optional[Dict[str, Any]]
    assets: Optional[Dict[str, Any]]


class PartialItem(TypedDict, total=False):
    """Partial STAC Item."""

    type: Optional[Literal["Feature"]]
    stac_version: Optional[str]
    stac_extensions: Optional[List[str]]
    id: Optional[str]
    geometry: Optional[Dict[str, Any]]
    bbox: Optional[BBox]
    properties: Optional[Dict[str, Any]]
    links: Optional[List[Dict[str, Any]]]
    assets: Optional[Dict[str, Any]]
    collection: Optional[str]


class PatchAddReplaceTest(BaseModel):
    """Add, Replace or Test Operation."""

    path: str
    op: Literal["add", "replace", "test"]
    value: Any


class PatchRemove(BaseModel):
    """Remove Operation."""

    path: str
    op: Literal["remove"]


class PatchMoveCopy(BaseModel):
    """Move or Copy Operation."""

    model_config = ConfigDict(populate_by_name=True)

    path: str
    op: Literal["move", "copy"]
    from_: str = Field(alias="from")

    def model_dump(self, by_alias=True, **kwargs) -> Dict[str, Any]:
        """Override by_alias default to True"""
        return super().model_dump(by_alias=by_alias, **kwargs)


PatchOperation = Union[PatchAddReplaceTest, PatchMoveCopy, PatchRemove]
