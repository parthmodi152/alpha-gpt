"""
Backtest result model definition for AlphaGPT
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Float, JSON, DateTime
)
from sqlalchemy.orm import relationship
from agent.database.models.base import Base


class BacktestResult(Base):
    """
    SQLAlchemy model for representing backtest results for an alpha factor
    """
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    checkpoint_id = Column(String, nullable=False)
    # Relationship to alpha
    alpha_id = Column(Integer, ForeignKey("alphas.id"), nullable=False)
    # Backtest metrics
    is_sota = Column(Boolean, default=False)  # Is this state of the art result?
    information_ratio = Column(Float)
    annualized_return = Column(Float)
    max_drawdown = Column(Float)
    ic = Column(Float)  # Information coefficient
    # Full backtest data
    backtest_data = Column(JSON)
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship
    alpha = relationship("Alpha", back_populates="backtest_results")
