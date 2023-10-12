#!/usr/bin/python3
"""user module, contains basic user info"""
from models.base_model import BaseModel


class User(BaseModel):
    """ user class , inherits from BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
