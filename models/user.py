#!/usr/bin/python3
"""this will define the User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """this represents a User

    Attributes:
        email: this is the user's email
        password: this is the user's password
        first_name: This is the user's first name
        last_name: this is the user's last name
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
