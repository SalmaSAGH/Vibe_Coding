from services.strategies.irrigation_strategy import (
    TomatoIrrigationStrategy,
    LettuceIrrigationStrategy,
    IrrigationStrategy
)

class StrategyFactory:
    """Factory for creating crop-specific strategies"""
    
    _irrigation_strategies = {
        'tomato': TomatoIrrigationStrategy,
        'lettuce': LettuceIrrigationStrategy,
    }
    
    @classmethod
    def get_irrigation_strategy(cls, crop_type: str) -> IrrigationStrategy:
        strategy_class = cls._irrigation_strategies.get(
            crop_type.lower(),
            TomatoIrrigationStrategy
        )
        return strategy_class()
