from fastapi import FastAPI
from api.songsService import router as songs_router
from api.userScoreService import router as user_score_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],    # Разрешённые методы (GET, POST и т.д.)
    allow_headers=["*"],    # Разрешённые заголовки
)
app.include_router(songs_router)
app.include_router(user_score_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
