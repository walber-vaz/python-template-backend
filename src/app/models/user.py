from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry
from app.models.base import TimestampedTable, UUIDTable


@table_registry.mapped_as_dataclass
class User(UUIDTable, TimestampedTable):
    __tablename__ = 'tb_users'

    email: Mapped[str] = mapped_column(
        String(200), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(
        nullable=False, server_default=text('TRUE'), default=True
    )
