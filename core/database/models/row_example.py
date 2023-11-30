from core.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sense import Sense


class RowExample(Base):
    __tablename__ = "row_example"
    sense: Mapped["Sense"] = relationship(back_populates="row_examples")
    sense_id: Mapped["int"] = mapped_column(ForeignKey("sense.id"))
