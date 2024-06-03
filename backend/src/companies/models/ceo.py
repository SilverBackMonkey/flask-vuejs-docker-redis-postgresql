from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db.base import BaseModel

from .company import Company

from typing import TYPE_CHECKING


class CEO(BaseModel):
    """ Company Director model """

    __tablename__ = 'ceo'

    if TYPE_CHECKING:
        company_id: int
        company: Company
        full_name: str
        start_year: int
        end_year: int
    else:
        company_id: Mapped[int] = mapped_column(ForeignKey(f'{Company.__tablename__}.id', ondelete='CASCADE'))
        company: Mapped[Company] = relationship(backref='ceo')
        # Information about the company to which the data is linked

        full_name: Mapped[str] = mapped_column()
        # Full name of the company director

        start_year: Mapped[int] = mapped_column()
        # Year of taking office

        end_year: Mapped[int] = mapped_column(default=None, nullable=True)
        # Year of removal from office


__all__ = (
    'CEO',
)
