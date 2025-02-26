import librosa
import numpy as np


def evaluate_singing(song_file: str, user_file: str) -> float:
    # Загружаем оригинальный трек и исполнение пользователя
    y_song, sr_song = librosa.load(song_file, sr=None)
    y_user, sr_user = librosa.load(user_file, sr=None)

    # Проверяем, совпадает ли частота дискретизации
    if sr_song != sr_user:
        raise ValueError("Sampling rates do not match!")

    # Вычисляем огибающую громкости
    rms_song = librosa.feature.rms(y=y_song)[0]
    rms_user = librosa.feature.rms(y=y_user)[0]

    # Выравниваем длины массивов (берём минимальную длину)
    min_len = min(len(rms_song), len(rms_user))
    rms_song = rms_song[:min_len]
    rms_user = rms_user[:min_len]

    # Оцениваем схожесть громкости как корреляцию
    similarity = np.corrcoef(rms_song, rms_user)[0, 1]

    # Приводим оценку к шкале 0-100
    score = (similarity + 1) / 2 * 100
    return round(score, 2)

