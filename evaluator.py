from memory import MemoryType, MemoryItem
from typing import Dict, Optional
from datetime import datetime
import numpy as np

class MemoryValueEvaluator:
    """
        记忆价值评估: 
        输入一个 MemoryItem 给出对应的分数, 只需要评估各维度权重以及转换到 float 的逻辑即可
        分数为 [0, 1] 之间的浮点数
    """
    def __init__(self):
        # 评估维度: 重要性, 频率, 未来可用性, 时效性, 置信度
        self.weights = {
            'importance': 0.3,
            'frequency': 0.2,
            'future_utility': 0.25,
            'temporal_validity': 0.15,
            'confidence': 0.1
        }

    # importance, confidence 是直接设置的, 不需要转换
    # frequency 和分数应有转换关系, 分数不能随频率增加无限增长, 采用对数函数来设置
    # future_utility 要根据 memory_type 来评估, 不同类型的记忆未来可用性不一样, 这里先手动设置
    # temporal_validity 则根据时间有效期来评分
    
    def calculate_frequency_score(self, frequency: int) -> float:
        """记住归一化"""
        return min(1.0, np.log1p(frequency) / np.log1p(10))

    def calculate_future_utility(self, memory_type: MemoryType) -> float:
        """根据记忆类型估算未来有效性"""
        utility_map = {
            MemoryType.USER_PROFILE: 0.95,
            MemoryType.PREFERENCES: 0.9,
            MemoryType.BEHAVIORAL_PATTERNS: 0.85,
            MemoryType.LEARNED_KNOWLEDGE: 0.8,
            MemoryType.FACTS: 0.6,
            MemoryType.TASK_CONTEXT: 0.4
        }
        return utility_map.get(memory_type, 0.5)

    def calculate_temporal_score(self, created: datetime, validity: Optional[datetime]):
        if validity is None:
            return 1.0 # 无时间限制

        now = datetime.now()
        if now > validity:
            return 0.0 # 已过期
        
        # 按照剩余时间比例得分
        total_duration = (validity - created).total_seconds()
        remaining_duration = (validity - now).total_seconds()
        return remaining_duration / total_duration if total_duration > 0 else 0.0

    def evaluate(self, memory: MemoryItem) -> Dict[str, float]:
        scores = {
            'importance': memory.importance,
            'frequency': self.calculate_frequency_score(memory.frequency),
            'future_utility': self.calculate_future_utility(memory.memory_type),
            'temporal_validity': self.calculate_temporal_score(
                memory.timestamp,
                memory.temporal_validity
            ),
            'confidence': memory.confidence
        }

        total_score = sum(
            scores[key] * self.weights[key]
            for key in scores.keys()
        )

        scores['total_score'] = total_score
        return scores

############################### 测试部分 ###############################
evaluator = MemoryValueEvaluator()
def main():
    """测试记忆评估器"""
    print(f"评估维度权重: ")
    for dim, weight in evaluator.weights.items():
        print(f"    {dim}: {weight:.2f}")

if __name__ == "__main__":
    main()

