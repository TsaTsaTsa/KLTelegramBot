from sqlalchemy import MetaData, Table, Integer, ForeignKey, Column, Boolean, DateTime

from models.posts import posts

metadata_exercise_logs = MetaData()

exercise_logs = Table(
    "exercise_logs",
    metadata_exercise_logs,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("exercise_id", Integer, ForeignKey(posts.c.id)),
    Column("date_get_exercise", DateTime),
    Column("is_done", Boolean),
    Column("is_done_last_month", Boolean),
    Column("date_change_status", DateTime)
)
