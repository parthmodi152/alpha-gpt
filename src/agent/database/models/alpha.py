"""
Alpha model definition for AlphaGPT
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from agent.database.models.base import Base


class Alpha(Base):
    """
    SQLAlchemy model for representing an alpha factor
    """
    __tablename__ = "alphas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    checkpoint_id = Column(String, nullable=False)
    # Relationship to hypothesis
    hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"), nullable=False)
    # Alpha metadata
    alpha_id = Column(String, nullable=False)  # Unique identifier for the alpha
    expression = Column(String)  # Mathematical expression of the alpha
    description = Column(String)  # Description of the alpha
    code = Column(String)  # Code implementation of the alpha
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship
    backtest_results = relationship(
        "BacktestResult", back_populates="alpha", cascade="all, delete-orphan"
    )
