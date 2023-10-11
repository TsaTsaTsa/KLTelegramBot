from enum import Enum

from sqlalchemy import Column, String, MetaData, Table, Integer, ForeignKey, BigInteger

from models.posts import posts


class Status(Enum):
    coursing = "coursing"
    on_feeling_tracker = "on_feeling_tracker"
    off_feeling_tracker = "off_feeling_tracker"
    inactive = "inactive"


metadata_users = MetaData()

users = Table(
    "users",
    metadata_users,
    Column("id", Integer, primary_key=True),
    Column("user_id", BigInteger),
    Column("next_post_id", Integer, ForeignKey(posts.c.id)),
    Column("status", String),
)
