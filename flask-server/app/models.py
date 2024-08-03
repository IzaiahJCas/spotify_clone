from . import db
from sqlalchemy.orm import Mapped, mapped_column

class SongBook(db.Model):
    __tablename__ = 'test_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_name: Mapped[str] = mapped_column(unique=True)
    file_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)