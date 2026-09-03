from sqlalchemy.orm import Mapped

from models.base import Base


class Lead(Base):
    __tablename__ = "leads"

    thread_id: Mapped[str]
    company_size: Mapped[int]
    current_tool: Mapped[str]
    use_case: Mapped[str]
    timeline: Mapped[str]
    email: Mapped[str]