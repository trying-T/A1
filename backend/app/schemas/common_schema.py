from pydantic import BaseModel


class SourceItem(BaseModel):
    title: str
    snippet: str
    source_type: str
