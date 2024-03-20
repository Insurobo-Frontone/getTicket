from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR, DATETIME, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy import BigInteger, CHAR, Column, DECIMAL, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, LargeBinary, MetaData, String, TIMESTAMP, Table, Text, text
from sqlalchemy.orm.base import Mapped

metadata = MetaData()

t_moneypin_key_statistics = Table(
    'moneypin_key_statistics', metadata,
    Column('uuid', String(36), primary_key=True, server_default=text('(uuid())')),
    Column('ip', String(15), nullable=False),
    Column('key_date', DateTime, nullable=False, server_default=text('(now())'))
)

