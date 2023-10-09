from sqlalchemy import MetaData, Table, Integer, ForeignKey, String, Column

from models.posts import posts

metadata_photos = MetaData()

photos = Table(
    "photos",
    metadata_photos,
    Column("id", Integer, primary_key=True),
    Column("post_id", Integer, ForeignKey(posts.c.id)),
    Column("file_id", String),
)
