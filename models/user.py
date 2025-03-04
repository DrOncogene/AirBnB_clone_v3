#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def hash_password(self):
        "hashes the password"
        self.password = md5(self.password.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
