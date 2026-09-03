from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Escalation(Base):
    __tablename__ = "escalations"

    thread_id: Mapped[str]
    reason: Mapped[str]
    email: Mapped[str]
    status: Mapped[str] = mapped_column(default="open")