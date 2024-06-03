from pydantic.functional_serializers import PlainSerializer

from typing_extensions import Annotated


Percentage = Annotated[float, PlainSerializer(lambda x: x * 100, return_type=float, when_used='json')]


__all__ = (
    'Percentage',
)
