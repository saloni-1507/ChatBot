from sqlalchemy.orm import Mapped

from models.base import Base


class Case(Base):
    __tablename__ = "cases"

    thread_id: Mapped[str]
    issue_summary: Mapped[str]
    feature: Mapped[str]
    severity: Mapped[str]
    repro_steps: Mapped[str]
    email: Mapped[str]