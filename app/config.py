import os

# Все настройки можно переопределить переменными окружения,
# иначе берутся значения по умолчанию (удобно для локального запуска).

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./perfume.db")

# Ключ для подписи cookie сессий. На сервере обязательно задать свой.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

# Сколько оценок нужно пользователю, чтобы получить прогнозы.
MIN_RATINGS = int(os.getenv("MIN_RATINGS", "10"))
