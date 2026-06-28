from sqlalchemy import Column,Integer,String,ForeignKey,Text,DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique=True,index=True)
    password_hash = Column(String)

class Video(Base):
    __tablename__ ="videos"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    title=Column(String)
    filename=Column(String)
    storage_url=Column(String)
    status=Column(String,default="uploaded")
    user=relationship("User")
    transcripts = relationship(
                        "VideoTranscript",
                            back_populates="video"
                            )




class VideoTranscript(Base):
    __tablename__ = "video_transcripts"

    id = Column(Integer, primary_key=True, index=True)

    video_id = Column(
        Integer,
        ForeignKey("videos.id"),
        unique=True,
        nullable=False
    )

    transcript = Column(
        Text,
        nullable=False
    )

    language = Column(
        String,
        default="unknown"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    video = relationship(
        "Video",
        back_populates="transcripts",
        uselist=False
    )

class VideoSummary(Base):
    __tablename__="video_summarie"
    
    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    video_id=Column(
        Integer,
        ForeignKey("videos.id"),
        unique=True
    )

    summary=Column(Text)

    key_takeaways = Column(Text)

    topics = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    video = relationship("Video")