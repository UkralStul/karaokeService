from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import logging

from api.songsService.crud import get_available_songs

router = APIRouter(prefix='/songs', tags=['songs'])

# Настройка логирования для диагностики
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Установка абсолютных путей
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SONGS_DIR = BASE_DIR / "songs"
LYRICS_DIR = BASE_DIR / "lyrics"
SONGS_DIR.mkdir(parents=True, exist_ok=True)
LYRICS_DIR.mkdir(parents=True, exist_ok=True)

# Эндпоинт для загрузки песни
@router.post("/upload-song/")
async def upload_song(song_file: UploadFile = File(...)):
    """
    Загружает файл песни на сервер.

    Args:
        song_file (UploadFile): Файл песни для загрузки

    Returns:
        JSONResponse: Сообщение об успешной загрузке

    Raises:
        HTTPException: Если произошла ошибка при сохранении файла
    """
    song_path = os.path.join(SONGS_DIR, song_file.filename)
    try:
        with open(song_path, "wb") as buffer:
            shutil.copyfileobj(song_file.file, buffer)
        return JSONResponse(content={"message": "Песня успешно загружена", "file": song_file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке песни: {str(e)}")


# Эндпоинт для загрузки слов песни
@router.post("/upload-lyrics/")
async def upload_lyrics(lyrics_file: UploadFile = File(...)):
    """
    Загружает файл слов песни в формате .lrc на сервер.

    Args:
        lyrics_file (UploadFile): Файл слов в формате .lrc

    Returns:
        JSONResponse: Сообщение об успешной загрузке

    Raises:
        HTTPException: Если файл не в формате .lrc или произошла ошибка
    """
    if not lyrics_file.filename.endswith(".lrc"):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате .lrc")

    lyrics_path = os.path.join(LYRICS_DIR, lyrics_file.filename)
    try:
        with open(lyrics_path, "wb") as buffer:
            shutil.copyfileobj(lyrics_file.file, buffer)
        return JSONResponse(content={"message": "Слова песни успешно загружены", "file": lyrics_file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке слов: {str(e)}")


# Эндпоинт для получения песни
@router.get("/get-song/{song_name}")
async def get_song(song_name: str):
    """
    Возвращает файл песни по его названию для фронтенда.

    Args:
        song_name (str): Название файла песни

    Returns:
        FileResponse: Файл песни

    Raises:
        HTTPException: Если файл не найден
    """
    song_path = os.path.join(SONGS_DIR, song_name)
    if not os.path.exists(song_path):
        raise HTTPException(status_code=404, detail="Песня не найдена")
    return FileResponse(song_path)


# Эндпоинт для получения слов песни
@router.get("/get-lyrics/{lyrics_name}")
async def get_lyrics(lyrics_name: str):
    """
    Возвращает файл слов песни по его названию для фронтенда.

    Args:
        lyrics_name (str): Название файла слов

    Returns:
        FileResponse: Файл слов песни

    Raises:
        HTTPException: Если файл не найден
    """
    lyrics_path = os.path.join(LYRICS_DIR, lyrics_name)
    if not os.path.exists(lyrics_path):
        raise HTTPException(status_code=404, detail="Слова песни не найдены")
    return FileResponse(lyrics_path)

@router.get("/")
async def get_songs():
    try:
        songs = []
        for song_file in SONGS_DIR.iterdir():
            if song_file.is_file():
                song_name = song_file.name
                lyrics_file = LYRICS_DIR / f"{song_name.rsplit('.', 1)[0]}.lrc"
                songs.append({
                    "name": song_name,
                    "audio": f"/get-song/{song_name}",
                    "lyrics": f"/get-lyrics/{song_name.rsplit('.', 1)[0]}.lrc" if lyrics_file.exists() else None
                })
        return {"songs": songs}
    except Exception as e:
        logger.error(f"Ошибка при получении списка песен: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении списка песен: {str(e)}")

