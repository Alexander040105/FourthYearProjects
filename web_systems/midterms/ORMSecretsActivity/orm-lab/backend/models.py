# =====================================================================
#  Week 10 Lab — models.py
#  TODO 2: describe the projects table as a SQLAlchemy model.
#
#  Right now this file is almost empty. Your job is to define a Project
#  model that maps to a "projects" table, following the deck's example.
# =====================================================================

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean


class Base(DeclarativeBase):
    pass


# ------------------------------------------------------------------
# TODO 2 — define the Project model
#   * __tablename__ = "projects"
#   * id     : int, primary key
#   * title  : str
#   * tech   : str
#   * done   : bool, default False
# ------------------------------------------------------------------
class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    tech: Mapped[str] = mapped_column(String(100), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
