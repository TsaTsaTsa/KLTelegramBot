from sqlalchemy import MetaData, Table, Integer, Column, String, Boolean, ForeignKey

from models.learning_sections import learning_sections

metadata_posts = MetaData()


posts = Table(
    "posts",
    metadata_posts,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("next_post_id", Integer),
    Column("prev_post_id", Integer),
    Column("is_exercise", Boolean),
    Column("learning_section", Integer, ForeignKey(learning_sections.c.id)),
)
