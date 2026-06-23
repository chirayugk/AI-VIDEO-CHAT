from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique=True,index=True)
    password_hash = Column(String)

class Video(Base):
    __tablename__ ="vidoes"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    title=Column(String)
    filename=Column(String)
    storage_url=Column(String)
    status=Column(String,default="uploaded")
    user=relationship("User")