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

    def __str__(self):
        return self.alias


class Word(Base):
    word: Mapped[str]

    aliases: Mapped[list["Alias"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
    senses: Mapped[list["Sense"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
    sound_uk: Mapped[str | None]
    sound_us: Mapped[str | None]

    word_images: Mapped[list["WordImage"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.word


class WordImage(Base):
    img: Mapped[str]
    is_public: Mapped[bool]

    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    word: Mapped["Word"] = relationship(back_populates="word_images")
