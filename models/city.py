#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
The city Module
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    The City Class

    Attributes:
        state_id (str): The UUID of the State the City belongs to
        name (str): The City name

    """
    state_id = ''
    name = ''
