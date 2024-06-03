from __future__ import annotations

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from core.db.base import BaseModel

from users.models import User

from .company import Company

from datetime import datetime
from typing import TYPE_CHECKING


class Forecast(BaseModel):
    """ Forecast of the company's financial indicators """

    __tablename__ = 'forecasts'

    if TYPE_CHECKING:
        company_id: int
        company: Company
        user_id: int
        user: User
        name: str
        updated_at: datetime
    else:
        company_id: Mapped[int] = mapped_column(ForeignKey(f'{Company.__tablename__}.id', ondelete='CASCADE'))
        company: Mapped[Company] = relationship(backref='forecasts')
        # The company to which this forecast is linked

        name: Mapped[str] = mapped_column(Text)
        # The name of this forecast

        user_id: Mapped[int] = mapped_column(ForeignKey(f'{User.__tablename__}.id', ondelete='CASCADE'))
        user: Mapped[User] = relationship(backref='forecasts')
        # Forecast creator (user)

        updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.current_timestamp())
        # Last update date


class ForecastField(BaseModel):
    __tablename__ = 'forecasts_fields'

    if TYPE_CHECKING:
        forecast_id: int
        forecast: Forecast
        column: str
        field: str
        value: float
    else:
        forecast_id: Mapped[int] = mapped_column(ForeignKey(f'{Forecast.__tablename__}.id', ondelete='CASCADE'))
        forecast: Mapped[Forecast] = relationship(backref='fields')
        # The forecast for which this field is saved

        column: Mapped[str] = mapped_column(Text)
        # Column name

        field: Mapped[str] = mapped_column(Text)
        # Field name

        value: Mapped[float] = mapped_column()
        # The value stored for this field


__all__ = (
    'Forecast',
    'ForecastField',
)
