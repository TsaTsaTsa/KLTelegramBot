from sqlalchemy import MetaData, Table, Integer, String, Column

metadata_feelings = MetaData()

feelings = Table(
    "feelings",
    metadata_feelings,
    Column("id", Integer, primary_key=True),
    Column("type", String),
)
