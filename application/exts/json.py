# -*- coding: utf-8 -*-
import dataclasses
import typing as t
import uuid
from flask import current_app
from flask.json.provider import DefaultJSONProvider as _DefaultJSONProvider
import decimal
from datetime import date, datetime


def _default(o: t.Any) -> t.Any:
    if o is None:
        return ''

    if isinstance(o, datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')

    if isinstance(o, date):
        return o.strftime('%Y-%m-%d')

    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)

    if dataclasses and dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)

    if hasattr(o, "__html__"):
        return str(o.__html__())

    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


class DefaultJSONProvider(_DefaultJSONProvider):
    default: t.Callable[[t.Any], t.Any] = staticmethod(
        _default
    )  # type: ignore[assignment]

    ensure_ascii = False

    sort_keys = False
