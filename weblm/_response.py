from pydantic import BaseModel, HttpUrl
from typing import List


class ConvertResponse(BaseModel):
    markdown: str
    url: HttpUrl
    token_count: int | None = None
    model_name: str | None = None

class ScrapeLinksResponse(BaseModel):
    urls: List[HttpUrl]

