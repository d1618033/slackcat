# pylint: disable=no-member
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    def set(self, date: datetime, value):
        if item := self._session.query(Item).filter_by(date=date).first():
            item.value = value
        else:
            item = Item(date=date, value=value)
        self._session.add(item)

    def get(self, date: datetime):
        return self._session.query(Item).filter_by(date=date).first().value

    def get_in_range(self, from_date: datetime, to_date: datetime):
        return [
            item.value
            for item in self._session.query(Item)
            .filter(Item.date >= from_date, Item.date <= to_date)
            .all()
        ]

    def sync(self):
        self._session.commit()
