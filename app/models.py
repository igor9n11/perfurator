from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Fragrance(Base):
    __tablename__ = "fragrances"
    __table_args__ = (UniqueConstraint("name", "brand", "gender"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    brand: Mapped[str] = mapped_column(String(100), index=True)
    gender: Mapped[str] = mapped_column(String(10))
    year: Mapped[int | None]
    country: Mapped[str | None] = mapped_column(String(50))

    top_notes: Mapped[str | None]
    middle_notes: Mapped[str | None]
    base_notes: Mapped[str | None]
    accords: Mapped[str | None]

    source_rating: Mapped[float | None]
    source_votes: Mapped[int | None]

    ratings: Mapped[list["Rating"]] = relationship(back_populates="fragrance")


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("user_id", "fragrance_id"),
        CheckConstraint("score BETWEEN 1 AND 10", name="score_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    fragrance_id: Mapped[int] = mapped_column(ForeignKey("fragrances.id"), index=True)
    score: Mapped[int]
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="ratings")
    fragrance: Mapped["Fragrance"] = relationship(back_populates="ratings")
