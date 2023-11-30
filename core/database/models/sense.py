from core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .word import Word
    from .example import Example
    from .row_example import RowExample


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

    images: Mapped[list["Image"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    examples: Mapped[list["Example"]] = relationship(back_populates="sense")
    row_examples: Mapped[list["RowExample"]] = relationship(
        back_populates="sense"
    )

    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    word: Mapped["Word"] = relationship(back_populates="senses")
