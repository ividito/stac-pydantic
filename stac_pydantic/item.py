from datetime import datetime as dt
from typing import Dict, List, Optional, Union

from pydantic import Field, BaseModel, root_validator

from .geojson import Feature, FeatureCollection
from .shared import Asset, BBox, ExtensionTypes, Link
from .extensions import Extensions
from .version import STAC_VERSION


class ItemProperties(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/item-spec/item-spec.md#properties-object
    """

    datetime: Union[str, dt] = Field(..., alias="datetime")

    class Config:
        extra = "allow"


class Item(Feature):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/item-spec/item-spec.md
    """
    id: str
    stac_version: str = Field(STAC_VERSION, const=True)
    properties: ItemProperties
    assets: Dict[str, Asset]
    links: List[Link]
    bbox: BBox
    stac_extensions: Optional[List[Union[str, ExtensionTypes]]]
    collection: Optional[str]

    @root_validator(pre=True)
    def validate_extensions(cls, values):
        if "stac_extensions" in values:
            if values["stac_extensions"]:
                for ext in values["stac_extensions"]:
                    if "http" not in ext and ext != "checksum":
                        ext_model = getattr(Extensions, ext)
                        ext_model(**values["properties"])
        return values

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


class ItemCollection(FeatureCollection):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/item-spec/itemcollection-spec.md
    """

    stac_version: str = Field(STAC_VERSION, const=True)
    features: List[Item]
    stac_extensions: Optional[List[ExtensionTypes]]
    links: Optional[List[Link]]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)
