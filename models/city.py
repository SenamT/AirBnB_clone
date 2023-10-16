#!/usr/bin/python3
"""this will define the City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """this represents a city

    Attributes:
        state_id: This will be the state id
        name: this is the city's name
    """

    state_id = ""
    name = ""
