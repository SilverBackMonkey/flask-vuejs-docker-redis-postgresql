from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import BaseModel

from companies.types import FinancialSource

from typing import TYPE_CHECKING


class Company(BaseModel):
    """ The model describing a company """

    __tablename__ = 'companies'

    if TYPE_CHECKING:
        symbol: str
        name: str
        short_name: str
        keywords: str
        logo: str
        founded: int
        employees: int
        summary: str
        data_source: str
    else:
        symbol: Mapped[str] = mapped_column(String(length=12), index=True, unique=True, nullable=False)
        # Company symbol

        name: Mapped[str] = mapped_column(String(length=64))
        # Full name of the company

        short_name: Mapped[str] = mapped_column(String(length=64), default=None, nullable=True)
        # Short name of the company

        keywords: Mapped[str] = mapped_column(Text)
        # Keywords separated by ','

        logo: Mapped[str] = mapped_column(Text, default=None, nullable=True)
        # URL of the stored company logo

        founded: Mapped[int] = mapped_column(default=None, nullable=True)
        # The year of creation of this company

        employees: Mapped[int] = mapped_column(default=None, nullable=True)
        # Number of employees in this company

        summary: Mapped[str] = mapped_column(Text, default=None, nullable=True)
        # Full description of the company

        data_source = Column(Enum(FinancialSource), default=FinancialSource.CUSTOM)
        # The source from which the financial data will be returned


__all__ = (
    'Company',
)
