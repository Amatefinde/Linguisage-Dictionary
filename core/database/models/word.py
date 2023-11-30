from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Literal


class Image(Base):
    img: Mapped[str]

    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"))
    sense: Mapped["Sense"] = relationship(back_populates="images")


class Sense(Base):
    lvl: Mapped[
        Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None
    ] = mapped_column(default=None, server_default=None)
    definition: Mapped[str]
    short_cut: Mapped[str | None] = mapped_column(
        default=None, server_default=None
    )
    examples: Mapped[list[str]] = mapped_column(default=[])
    row_examples: Mapped[list[str]] = mapped_column(default=[])

    images: Mapped[list["Image"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    word: Mapped["Word"] = relationship(back_populates="senses")


class Word(Base):
    word: Mapped[str]

    senses: Mapped[list["Sense"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
