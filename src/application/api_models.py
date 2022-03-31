"""Module with api models for REST."""
from typing import List

from pydantic import BaseModel


class Comments(BaseModel):
    """Comments for prediction."""

    comments: List[str]
