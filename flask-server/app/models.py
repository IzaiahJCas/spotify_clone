from . import db
from sqlalchemy.orm import Mapped, mapped_column

class SongBook(db.Model):
    __tablename__ = 'videos_included'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_name: Mapped[str] = mapped_column(unique=True)
    video_path: Mapped[str] = mapped_column(unique=True)
    video_name: Mapped[str] = mapped_column(unique=True)
    file_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)