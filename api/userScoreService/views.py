import os
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from api.userScoreService.user_score_calculator import evaluate_singing

router = APIRouter(prefix='/score', tags=['score'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SONGS_DIR = BASE_DIR / "songs"
DEBUG_DIR = BASE_DIR / "debug"
SONGS_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/evaluate-singing/")
async def evaluate_singing_view(song_name: str, user_recording: UploadFile = File(...)):
    """
    Принимает название песни и файл с записью пользователя, возвращает оценку пения.
    Сохраняет запись пользователя для отладки.
    """
    # Путь к оригинальной песне
    original_path = os.path.join(SONGS_DIR, song_name)

    if not os.path.exists(original_path):
        raise HTTPException(status_code=404, detail="Песня не найдена на сервере")

    # Путь для сохранения записи пользователя для отладки
    debug_file_path = os.path.join(DEBUG_DIR, f"debug_{user_recording.filename}_{os.urandom(4).hex()}.wav")

    # Создаём временный файл для анализа
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_user_path = temp_file.name
        try:
            # Сохраняем файл во временный путь и копируем для отладки
            with open(temp_user_path, "wb") as temp_buffer:
                shutil.copyfileobj(user_recording.file, temp_buffer)

            # Сохраняем копию для отладки
            shutil.copy(temp_user_path, debug_file_path)
            print(f"Запись пользователя сохранена для отладки: {debug_file_path}")

            # Оцениваем пение
            score = evaluate_singing(original_path, temp_user_path)

            # Возвращаем результат
            return JSONResponse(content={"score": round(score, 2)})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_user_path):
                try:
                    os.unlink(temp_user_path)
                except PermissionError as e:
                    print(f"Не удалось удалить файл {temp_user_path}: {e}")


@router.get("/files/")
async def list_of_debugs():
    if not DEBUG_DIR.exists():
        return {"files": []}
    files = [f.name for f in DEBUG_DIR.glob("*.wav")]
    return {"files": files}


@router.get("/files/{filename}")
async def get_debug_file(filename: str):
    file_path = DEBUG_DIR / filename
    if not file_path.exists() or not file_path.suffix == ".wav":
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)