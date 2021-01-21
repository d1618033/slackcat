# pylint: disable=no-member
import json
from datetime import datetime
from pathlib import Path
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .message import Message

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True, unique=True)
    value = Column(String)


class Cache:
    def __init__(self, path: Path):
        self._path = path
        self._engine = create_engine(f"sqlite:///{path}")
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)()

    def set(self, date: datetime, value: str):
        if item := self._session.query(Item).filter_by(date=date).first():
            item.value = value
        else:
            item = Item(date=date, value=value)
        self._session.add(item)

    def get(self, date: datetime) -> str:
        return self._session.query(Item).filter_by(date=date).first().value

    def get_in_range(
        self, from_date: datetime, to_date: datetime
    ) -> List[str]:
        return [
            item.value
            for item in self._session.query(Item)
            .filter(Item.date >= from_date, Item.date <= to_date)
            .order_by(Item.date)
            .all()
        ]

    def sync(self):
        self._session.commit()


class MessageCache:
    def __init__(self, cache: Cache):
        self._cache = cache

    def add(self, message: Message):
        self._cache.set(message.ts, message.json())

    def get_in_range(
        self, from_date: datetime, to_date: datetime
    ) -> List[Message]:
        return [
            Message(**json.loads(value))
            for value in self._cache.get_in_range(from_date, to_date)
        ]

    def sync(self):
        self._cache.sync()
