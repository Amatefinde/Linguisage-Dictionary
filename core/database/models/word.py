from core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sense import Sense


class Alias(Base):
    alias: Mapped[str] = mapped_column(unique=True)

    word: Mapped["Word"] = relationship(back_populates="aliases")
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))


class Word(Base):
    word: Mapped[str]

    aliases: Mapped[list["Alias"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
    senses: Mapped[list["Sense"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
