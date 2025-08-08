from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class DailyLog(Base):
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    foods = relationship("Food", back_populates="log_date")
    workouts = relationship("Workout", back_populates="log_date")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    calories = Column(Integer)
    log_id = Column(Integer, ForeignKey("daily_logs.id"))
    log_date = relationship("DailyLog", back_populates="foods")

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    duration_minutes = Column(Integer)
    log_id = Column(Integer, ForeignKey("daily_logs.id"))
    log_date = relationship("DailyLog", back_populates="workouts")
