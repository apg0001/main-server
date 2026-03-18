from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    context_type: Mapped[str] = mapped_column(String(30), nullable=False, default="GENERAL")
    external_conversation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_message_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )