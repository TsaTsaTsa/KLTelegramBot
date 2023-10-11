from sqlalchemy import MetaData, Table, Integer, String, Column

metadata_learning_sections = MetaData()


learning_sections = Table(
    "learning_sections",
    metadata_learning_sections,
    Column("id", Integer, primary_key=True),
    Column("type", String),
)
