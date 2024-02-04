from core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .word import Word
    from .example import Example


class SenseImage(Base):
    img: Mapped[str]

    is_public: Mapped[bool]
    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"))
    sense: Mapped["Sense"] = relationship(back_populates="sense_images")


class Sense(Base):
    lvl: Mapped[Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None] = mapped_column(
        default=None, server_default=None
    )
    is_public: Mapped[bool]
    definition: Mapped[str]
    short_cut: Mapped[str | None] = mapped_column(default=None, server_default=None)
    part_of_speech: Mapped[str | None] = mapped_column(default=None, server_default=None)
    sense_images: Mapped[list["SenseImage"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    examples: Mapped[list["Example"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    word: Mapped["Word"] = relationship(back_populates="senses")

    def __str__(self):
        return self.definition[:60] + ("..." if len(self.definition) > 60 else "")
