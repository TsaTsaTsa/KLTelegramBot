from sqlalchemy import MetaData, Table, Integer, ForeignKey, String, Column, DateTime

from models.feelings import feelings
from models.users import users

metadata_feeling_logs = MetaData()

feeling_logs = Table(
    "feeling_logs",
    metadata_feeling_logs,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("date", DateTime),
    Column("feeling_id", Integer, ForeignKey(feelings.c.id)),
    Column("feeling_str", String),
    Column("describe", String)
)
