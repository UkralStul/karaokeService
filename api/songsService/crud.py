import os
from pathlib import Path


def get_available_songs(songs_dir: Path, lyrics_dir: Path) -> list:
    """
    Возвращает список доступных песен, для которых загружены и песня, и файл слов (.lrc).

    Аргументы:
        songs_dir (str): Путь к директории с песнями
        lyrics_dir (str): Путь к директории со словами песен

    Возвращает:
        list: Список названий песен (без расширения), для которых есть и песня, и слова.
    """
    # Получаем список файлов песен (например, .mp3, .wav, .ogg)
    song_files = [f for f in os.listdir(songs_dir) if f.endswith(('.mp3', '.wav', '.ogg'))]

    # Получаем список файлов слов (.lrc)
    lyrics_files = [f for f in os.listdir(lyrics_dir) if f.endswith('.lrc')]
    print('song_files', song_files, 'lyrics_files', lyrics_files)
    # Извлекаем базовые имена (без расширения)
    song_names = {os.path.splitext(f)[0] for f in song_files}
    lyrics_names = {os.path.splitext(f)[0] for f in lyrics_files}
    print('song_names', song_names, 'lyrics_names', lyrics_names)
    # Находим пересечение — песни, для которых есть и песня, и слова
    available_songs = list(song_names.intersection(lyrics_names))
    print(available_songs)
    return available_songs

