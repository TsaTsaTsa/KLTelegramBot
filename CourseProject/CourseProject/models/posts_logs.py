from sqlalchemy import MetaData, Table, Integer, ForeignKey, Column, Boolean, DateTime

from models.posts import posts

metadata_posts_logs = MetaData()

post_logs = Table(
    "post_logs",
    metadata_posts_logs,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("post_id", Integer, ForeignKey(posts.c.id)),
    Column("date_get_post", DateTime),
    Column("section_id", Integer),
)
