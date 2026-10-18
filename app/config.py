import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./perfume.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
MIN_RATINGS = int(os.getenv("MIN_RATINGS", "10"))
