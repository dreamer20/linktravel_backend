from pydantic import BaseModel


class Options(BaseModel):
    url: str
    only_root: bool = False
    without_subdomain: bool = False