from typing import List, Dict
from memory import MemoryItem, sample_memories, MemoryType
from evaluator import MemoryValueEvaluator, evaluator
from enum import Enum

class MemoryPriority(Enum):
    """记忆优先级"""
    HIGH = "高优先级"
    MEDIUM = "中优先级"
    LOW = "低优先级"

class PriorityMemoryManager:
    """优先级记忆管理器"""

    def __init__(self, evaluator: MemoryValueEvaluator):
        self.evaluator = evaluator

        # 三层存储, 所以实际上的存储是需要有评分的, 不是直接不加区分的向上 summarize 的
        self.long_term: List[MemoryItem] = []
        self.mid_term: List[MemoryItem] = []
        self.short_term: List[MemoryItem] = []

        # 优先级阈值
        self.high_threshold = 0.7
        self.medium_threshold = 0.4

    def classify_priority(self, memory: MemoryItem) -> MemoryPriority:
        """根据综合评分来分类优先级"""
        scores = self.evaluator.evaluate(memory)
        total_score = scores['total_score']

        if total_score >= self.high_threshold:
            return MemoryPriority.HIGH
        elif total_score >= self.medium_threshold:
            return MemoryPriority.MEDIUM
        else:
            return MemoryPriority.LOW

    def store(self, memory: MemoryItem):
        """存储记忆, 自动根据优先级计算位置"""
        priority = self.classify_priority(memory)
        scores = self.evaluator.evaluate(memory)

        if priority == MemoryPriority.HIGH:
            self.long_term.append(memory)
            storage = "长期记忆库"
        elif priority == MemoryPriority.MEDIUM:
            self.mid_term.append(memory)
            storage = "中期记忆库"
        else:
            self.short_term.append(memory)
            storage = "短期缓存"

        print(f"[{priority.value}] -> {storage}")
        print(f"    内容: {memory.content}")
        print(f"    综合得分: {scores['total_score']:.3f}")

    def get_statistics(self) -> Dict:
        """获取存储统计"""
        return {
            '长期记忆': len(self.long_term),
            '中期记忆': len(self.mid_term),
            '短期记忆': len(self.short_term),
            '总计': len(self.long_term) + len(self.mid_term) + len(self.short_term)
        }
    

############################### 测试部分 ###############################
priority_manager = PriorityMemoryManager(evaluator)
def main():
    # 创建优先级管理器
    print("✅ 优先级记忆管理器创建成功")
    print(f"\n优先级分类阈值：")
    print(f"  High:   ≥ {priority_manager.high_threshold}")
    print(f"  Medium: ≥ {priority_manager.medium_threshold}")
    print(f"  Low:    < {priority_manager.medium_threshold}")

    # 存储示例记忆并分类
    print("\n🔄 自动分类并存储记忆：\n")
    print("="*60)

    for i, memory in enumerate(sample_memories, 1):
        print(f"\n{i}. 处理记忆: {memory.content}")
        priority_manager.store(memory)
        print("-" * 60)


if __name__ == "__main__":
    main()