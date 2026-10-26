from src.utils.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Boolean, index=True)

    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))  # Foreign key to UserModel (assuming user_id is an integer)