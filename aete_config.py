"""
Configuration manager for the Autonomous Evolutionary Trading Engine.
Centralizes all system settings with environment variable support and validation.
"""
import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TradingMode(Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

class DataSource(Enum):
    CCXT = "ccxt"
    ALPACA = "alpaca"
    YFINANCE = "yfinance"

@dataclass
class AETEConfig:
    """Immutable configuration container for AETE system"""
    # Trading Configuration
    trading_mode: TradingMode = TradingMode.BACKTEST
    data_source: DataSource = DataSource.CCXT
    symbols: tuple = ("BTC/USDT", "ETH/USDT", "SOL/USDT")
    timeframe: str = "1h"
    
    # Evolution Parameters
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.15
    crossover_rate: float = 0.65
    
    # Firebase Configuration
    firebase_project_id: Optional[str] = None
    firestore_collection: str = "aete_strategies"
    
    # Risk Management
    max_position_size: float = 0.1  # 10% of portfolio
    stop_loss_pct: float = 0.05  # 5%
    take_profit_pct: float = 0.15  # 15%
    
    # Performance Thresholds
    min_sharpe_ratio: float = 0.5
    max_drawdown_pct: float = 0.25
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.mutation_rate < 0 or self.mutation_rate > 1:
            raise ValueError("Mutation rate must be between 0 and 1")
        if self.max_position_size <= 0 or self.max_position_size > 1:
            raise ValueError("Max position size must be between 0 and 1")
        
        # Load from environment variables if available
        self.firebase_project_id = os.getenv("FIREBASE_PROJECT_ID", self.firebase_project_id)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for Firebase storage"""
        return {
            "trading_mode": self.trading_mode.value,
            "data_source": self.data_source.value,
            "symbols": list(self.symbols),
            "timeframe": self.timeframe,
            "population_size": self.population_size,
            "generations": self.generations,
            "mutation_rate": self.mutation_rate,
            "crossover_rate": self.crossover_rate,
            "risk_params": {
                "max_position_size": self.max_position_size,
                "stop_loss_pct": self.stop_loss_pct,
                "take_profit_pct": self.take_profit_pct
            }
        }

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure structured logging for AETE system"""
    logger = logging.getLogger("AETE")
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Global logger instance
logger = setup_logging()