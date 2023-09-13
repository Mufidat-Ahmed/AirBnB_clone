#!/usr/bin/python3
"""User class defination"""
from models.base_model import BaseModel


class User(BaseModel):
    """User representation"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
