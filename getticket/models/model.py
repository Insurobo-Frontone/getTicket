from sqlalchemy import Column, DateTime, MetaData, String, Table, text

metadata = MetaData()

t_moneypin_key_statistics = Table(
    'moneypin_key_statistics', metadata,
    Column('uuid', String(36), primary_key=True, server_default=text('(uuid())')),
    Column('ip', String(15), nullable=False),
    Column('key_date', DateTime, nullable=False, server_default=text('(now())'))
)

