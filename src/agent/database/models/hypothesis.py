"""
Hypothesis model definition for AlphaGPT
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from agent.database.models.base import Base


class Hypothesis(Base):
    """
    SQLAlchemy model for representing a trading hypothesis
    """

    __tablename__ = "hypotheses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    checkpoint_id = Column(String, nullable=False)
    # Hypothesis data
    trading_idea = Column(String, nullable=False)
    hypothesis = Column(String, nullable=False)
    reason = Column(String)
    concise_reason = Column(String)
    concise_observation = Column(String)
    concise_justification = Column(String)
    concise_knowledge = Column(String)
    # Iteration tracking
    iteration = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
