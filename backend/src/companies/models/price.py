from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db.base import BaseModel

from .company import Company

from datetime import datetime
from typing import TYPE_CHECKING


class Price(BaseModel):
    """ Data on the value of shares """

    __tablename__ = 'prices'

    if TYPE_CHECKING:
        company_id: int
        company: Company
        open: float
        high: float
        low: float
        close: float
        volume: float
        timestamp: datetime
    else:
        company_id: Mapped[int] = mapped_column(ForeignKey(f'{Company.__tablename__}.id', ondelete='CASCADE'))
        company: Mapped[Company] = relationship(backref='prices')
        # Information about the company to which the data is linked

        open: Mapped[float] = mapped_column()
        # The opening price of the auction

        high: Mapped[float] = mapped_column()
        # Maximum value of shares

        low: Mapped[float] = mapped_column()
        # Minimum value of shares

        close: Mapped[float] = mapped_column()
        # Closing price

        volume: Mapped[int] = mapped_column(BigInteger)
        # Trading volume for this period

        timestamp: Mapped[datetime] = mapped_column()
        # The day for which the trading data is saved


__all__ = (
    'Price',
)
