#!/usr/bin/python3
"""this will define the Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """this represents a review

    Attributes:
        place_id: this is the id of the place
        user_id: this is the id of the user
        text: this will be the reviews text
    """

    place_id = ""
    user_id = ""
    text = ""
