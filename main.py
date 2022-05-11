from fastapi import FastAPI
from users import router as users_router
from auth import router as auth_router
from posts import router as posts_router
from comments import router as comments_router

app = FastAPI(title="CoolBlogAPI", version="0.1.0")

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(posts_router.router)
app.include_router(comments_router.router)


@app.get("/")
async def root():
    return {"message": "Cool Blog Rest API"}
