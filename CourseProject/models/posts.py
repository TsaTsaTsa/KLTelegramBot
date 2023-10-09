from sqlalchemy import MetaData, Table, Integer, Column, String, Boolean

metadata_posts = MetaData()


posts = Table(
    "posts",
    metadata_posts,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("next_post_id", Integer),
    Column("prev_post_id", Integer),
    Column("is_exercise", Boolean),
)
