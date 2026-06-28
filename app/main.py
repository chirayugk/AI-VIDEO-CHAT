from fastapi import FastAPI,Header,UploadFile,File
from .database import engine
from .models import Base
from .database import SessionLocal
from .models import User,Video
from .schemas import UserCreate,UserLogin
from .auth import hash_password,create_access_token,verify_password,verify_token
from .models import Video, VideoTranscript,VideoSummary
from .services.transcription import transcribe_video
from .services.summary import generate_summary



Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"running"}

@app.post("/signup")
def signup(user:UserCreate):
    db = SessionLocal()

    existing_user=db.query(User).filter(User.email==user.email).first()

    if existing_user:
        return {"error":"email already exists"}
    
    new_user=User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    return {"message":"user created"}   

@app.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {"error": "Invalid credentials"}

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        return {"error": "Invalid credentials"}

    token = create_access_token(
        {
            "user_id": db_user.id,
            "email": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(authorization:str=Header(None)):
    if not authorization:
        return {"error":"token missing"}
    
    token=authorization.split(" ")[1]

    payload=verify_token(token)

    if not payload:
        return {"error":"invalid token"}
    
    return {
        "user_id":payload["user_id"],
        "email":payload["email"]
    }

@app.get("/videos")
def get_videos():

    db = SessionLocal()

    videos = db.query(Video).all()

    return [
        {
            "id": video.id,
            "title": video.title,
            "filename": video.filename,
            "status": video.status
        }
        for video in videos

    ]
@app.post("/videos/upload")
async def upload_video(file: UploadFile=File(...)):
    file_path = f"uploads/{file.filename}"
    db =SessionLocal()
    with open(file_path, "wb") as buffer: 
        content = await file.read() 
        buffer.write(content) 

    new_video = Video(
        title=file.filename,
        filename=file.filename,
        storage_url=file_path,
        status="uploaded",
        user_id=1
    )

    db.add(new_video)
    db.commit()    
    db.refresh(new_video)
    return {"video_id": new_video.id,
            "filename":new_video.filename,
            "status":new_video.status}    

@app.post("/videos/{video_id}/process")
def process_video(video_id: int):

    db = SessionLocal()

    video = db.query(Video).filter(
        Video.id == video_id
    ).first()

    if not video:
        return {"error": "Video not found"}
    existing = db.query(VideoTranscript).filter(VideoTranscript.video_id == video.id).first()

    if existing:
            return {
        "message": "Transcript already exists"
    }
    video.status="processing"
    db.commit()

    try :
        result = transcribe_video(
        video.storage_url
        )

        transcript = VideoTranscript(
        video_id=video.id,
        transcript=result["transcript"],
        language=result["language"]
        )

        db.add(transcript)

        video.status = "completed"

        db.commit()

        return {
        "video_id": video.id,
    "status": video.status,
        "language":result["language"]
        }
    except Exception as e:
        video.status="failed"
        db.commit()
        return {
            "error":str(e)
        }

@app.get("/videos/{video_id}/transcript")
def get_transcript(video_id: int):

  db = SessionLocal()
  try:
    transcript = db.query(
        VideoTranscript
    ).filter(
        VideoTranscript.video_id == video_id
    ).first()

    if not transcript:
         return {"error": "Transcript not found"}

    return {
 "video_id": transcript.video_id,
        "language": transcript.language,
            "created_at": transcript.created_at,
        "transcript": transcript.transcript    }
  finally:
    db.close()


@app.post("/videos/{video_id}/summary")
def create_summary(video_id: int):
        db =SessionLocal()
        video=db.query(Video).filter(Video.id==video_id).first()

        if not video:
            return {
                "error":"video not found"
            }
        transcript = db.query(VideoTranscript).filter(
        VideoTranscript.video_id == video_id
    ).first()

        if not transcript:
          return {"error": "Transcript not found"}
        existing_summary = db.query(VideoSummary).filter(
                   VideoSummary.video_id == video_id
                     ).first()

        if existing_summary:
          return {
            "message": "Summary already exists"
         }

        result = generate_summary(
        transcript.transcript
             )
        summary = VideoSummary(
        video_id=video.id,
        summary=result["summary"],
        key_takeaways=str(result["key_takeaways"]),
        topics=str(result["topics"])
    )

        db.add(summary)
        db.commit()

        return {
        "message": "Summary generated successfully"
    }

@app.get("/videos/{video_id}/summary")
def get_summary(video_id: int):

    db = SessionLocal()

    summary = db.query(VideoSummary).filter(
        VideoSummary.video_id == video_id
    ).first()

    if not summary:
        return {
            "error": "Summary not found"
        }

    return {
        "summary": summary.summary,
        "key_takeaways": summary.key_takeaways,
        "topics": summary.topics
    }