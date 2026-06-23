from fastapi import FastAPI,Header,UploadFile,File
from .database import engine
from .models import Base
from .database import SessionLocal
from .models import User,Video
from .schemas import UserCreate,UserLogin
from .auth import hash_password,create_access_token,verify_password,verify_token

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
def get_me(autherization:str=Header(None)):
    if not autherization:
        return {"error":"token missing"}
    
    token=autherization.split(" ")[1]

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
    return {"message": "uploaded"}    

