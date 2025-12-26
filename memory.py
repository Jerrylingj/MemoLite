from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict

class MemoryType(Enum):
    """记忆类型枚举"""
    USER_PROFILE = "用户画像信息"
    FACTS = "对话事实"
    PREFERENCES = "偏好信息"
    BEHAVIORAL_PATTERNS = "行为模式"
    TASK_CONTEXT = "任务状态"
    LEARNED_KNOWLEDGE = "知识与经验"

@dataclass
class MemoryItem:
    """
        记忆项: 
        - 记忆内容
        - 记忆类型
        - 创建时间
        - 重要性
        - 出现频率
        - 置信度
        - 有效期
        - 额外元数据
    """
    content: str
    memory_type: MemoryType
    timestamp: datetime
    importance: float = 0.5 # [0, 1]
    frequency: int = 1
    confidence: float = 0.8 # [0, 1]
    temporal_validity: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
            
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        data = asdict(self)

        data['memory_type'] = self.memory_type.value
        data['timestamp'] = self.timestamp.isoformat()
        if self.temporal_validity:
            data['temporal_validity'] = self.temporal_validity.isoformat()
        return data

    

############################### 测试部分 ###############################
# 导出给其他模块测试用
sample_memories = [
    MemoryItem(
        content="用户是金融分析师",
        memory_type=MemoryType.USER_PROFILE,
        timestamp=datetime.now(),
        importance=0.9,
        confidence=1.0
    ),
    MemoryItem(
        content="上次会议时间是11月3日",
        memory_type=MemoryType.FACTS,
        timestamp=datetime.now(),
        importance=0.6,
        temporal_validity=datetime.now() + timedelta(days=30)
    ),
    MemoryItem(
        content="喜欢用表格展示结果",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        importance=0.8,
        frequency=3
    ),
    MemoryItem(
        content="经常在任务结束后要求总结",
        memory_type=MemoryType.BEHAVIORAL_PATTERNS,
        timestamp=datetime.now(),
        importance=0.7,
        frequency=5
    ),
    MemoryItem(
        content="数据清洗完成，但尚未生成报告",
        memory_type=MemoryType.TASK_CONTEXT,
        timestamp=datetime.now(),
        importance=0.9,
        temporal_validity=datetime.now() + timedelta(days=7)
    ),
    MemoryItem(
        content="如果用户提到'改进'，往往指的是文案优化",
        memory_type=MemoryType.LEARNED_KNOWLEDGE,
        timestamp=datetime.now(),
        importance=0.75,
        frequency=4,
        confidence=0.85
    )
]

def main():
    # 1. 测试记忆类型
    print("支持的记忆类型: ")
    for mem_type in MemoryType:
        print(f"    - {mem_type.value}")


    # 2. 测试记忆项
    print("\n测试记忆项: ")
    # 创建示例记忆项


    print("📝 创建了6个示例记忆项：\n")
    for i, mem in enumerate(sample_memories, 1):
        print(f"{i}. [{mem.memory_type.value}] {mem.content}")
        print(f"   重要性: {mem.importance:.2f} | 频率: {mem.frequency} | 置信度: {mem.confidence:.2f}")
        if mem.temporal_validity:
            print(f"   有效期至: {mem.temporal_validity.strftime('%Y-%m-%d')}")
        print()

if __name__ == "__main__":
    main()

