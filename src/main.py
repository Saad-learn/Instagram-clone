from fastapi import FastAPI
from src.database import Base, engine
from src.routes.auth_route import router as auth_router
from src.routes.user_route import router as user_router
from src.routes.post_route import router as post_router
from src.routes.follow_route import router as follow_router
from src.routes.like_route import router as like_router
from src.routes.comment_route import router as comment_router
from src.routes.story_route import router as story_router
from src.routes.search_route import router as search_router

# import cloudinary

# cloudinary.config(
#     cloud_name = "dfnqxqxhh",
#     api_key = "985451642451868",
#     api_secret = "T44Sm_Wtp7UngbAtWolk0ZmczEE",
# )

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Instagram Clone API",
    version="1.0.0",
    description="Backend API for Instagram Clone"
)

@app.get("/")
def home():
    return {
        "message": "Instagram Clone API is running successfully!",
        "status": True
    }

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(follow_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(story_router)
app.include_router(search_router)

