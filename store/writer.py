from memory import MemoryItem, MemoryType
from store.kv_store import KeyValueMemoryStore, kv_store
from store.vector_store import VectorMemoryStore, vec_store
from datetime import datetime
from enum import Enum
from typing import Dict
from collections import defaultdict

class WriteStrategy(Enum):
    """写入策略类型"""
    REALTIME = "实时写入"
    BATCH = "周期写入"
    EVENT_BASED = "事件触发"
    FEEDBACK_BASED = "用户反馈"

class MemoryWriter:
    """记忆写入管理器"""

    def __init__(self, kv_store: KeyValueMemoryStore, vector_store: VectorMemoryStore):
        self.kv_store = kv_store
        self.vector_store = vector_store
        self.batch_buffer: List[MemoryItem] = []
        self.write_log: List[Dict] = []

    def write_realtime(self, key: str, memory: MemoryItem):
        """实时写入 - 立即存储关键信息"""
        print(f"⚡ [实时写入] 触发")
        self.kv_store.set(key, memory)
        self.vector_store.add(memory)
        self._log_write(WriteStrategy.REALTIME, memory)

    def add_to_batch(self, memory: MemoryItem):
        """添加到批处理缓冲区"""
        self.batch_buffer.append(memory)
        print(f"📦 [批处理] 已加入缓冲区，当前缓冲: {len(self.batch_buffer)} 条")

    def flush_batch(self):
        """批量写入"""
        if not self.batch_buffer:
            print("📦 [批处理] 缓冲区为空，无需写入")
            return

        print(f"\n📦 [批处理] 开始写入 {len(self.batch_buffer)} 条记忆...")
        for i, memory in enumerate(self.batch_buffer, 1):
            key = f"batch_{datetime.now().timestamp()}_{i}"
            self.kv_store.set(key, memory)
            self.vector_store.add(memory)
            self._log_write(WriteStrategy.BATCH, memory)

        count = len(self.batch_buffer)
        self.batch_buffer.clear()
        print(f"✅ [批处理] 完成，已写入 {count} 条记忆")

    def write_on_event(self, event_type: str, memory: MemoryItem):
        """事件触发写入"""
        print(f"🎯 [事件触发] 事件: {event_type}")
        key = f"event_{event_type}_{datetime.now().timestamp()}"
        self.kv_store.set(key, memory)
        self.vector_store.add(memory)
        self._log_write(WriteStrategy.EVENT_BASED, memory, {'event': event_type})

    def write_from_feedback(self, user_command: str, memory: MemoryItem):
        """用户反馈触发写入"""
        print(f"💬 [用户反馈] 指令: {user_command}")
        key = f"feedback_{datetime.now().timestamp()}"
        self.kv_store.set(key, memory)
        self.vector_store.add(memory)
        self._log_write(WriteStrategy.FEEDBACK_BASED, memory, {'command': user_command})

    def _log_write(self, strategy: WriteStrategy, memory: MemoryItem, extra: Dict = None):
        """记录写入日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy.value,
            'memory_type': memory.memory_type.value,
            'content': memory.content[:50],
            'extra': extra or {}
        }
        self.write_log.append(log_entry)

    def get_write_statistics(self) -> Dict:
        """获取写入统计"""
        stats = defaultdict(int)
        for log in self.write_log:
            stats[log['strategy']] += 1
        return dict(stats)


############################### 测试部分 ###############################
writer = MemoryWriter(kv_store, vec_store)

def main():
    # 创建写入管理器
    print("✅ 记忆写入管理器创建成功")

    # 演示不同的写入策略
    print("🎬 演示不同写入策略：\n")
    print("="*60)

    # 1. 实时写入
    print("\n1️⃣ 实时写入示例：")
    urgent_memory = MemoryItem(
        content="用户要求紧急修改报告格式",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        importance=0.95
    )
    writer.write_realtime("urgent_format_change", urgent_memory)

    # 2. 批处理写入
    print("\n" + "="*60)
    print("\n2️⃣ 批处理写入示例：")
    batch_memories = [
        MemoryItem(
            content="会话开始时间: 14:30",
            memory_type=MemoryType.FACTS,
            timestamp=datetime.now(),
            importance=0.3
        ),
        MemoryItem(
            content="讨论了季度财报",
            memory_type=MemoryType.FACTS,
            timestamp=datetime.now(),
            importance=0.4
        ),
        MemoryItem(
            content="提到了三个竞争对手",
            memory_type=MemoryType.FACTS,
            timestamp=datetime.now(),
            importance=0.5
        )
    ]

    for mem in batch_memories:
        writer.add_to_batch(mem)

    print("\n准备执行批量写入...")
    writer.flush_batch()

    # 3. 事件触发
    print("\n" + "="*60)
    print("\n3️⃣ 事件触发写入示例：")
    task_complete_memory = MemoryItem(
        content="财务分析任务已完成",
        memory_type=MemoryType.TASK_CONTEXT,
        timestamp=datetime.now(),
        importance=0.8
    )
    writer.write_on_event("task_completed", task_complete_memory)

    # 4. 用户反馈
    print("\n" + "="*60)
    print("\n4️⃣ 用户反馈写入示例：")
    feedback_memory = MemoryItem(
        content="记住：我不喜欢被称呼'老板'",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        importance=0.9,
        confidence=1.0
    )
    writer.write_from_feedback("记住这个", feedback_memory)

    print("\n" + "="*60)
    # 查看写入统计
    print("\n📊 写入策略统计：\n")
    stats = writer.get_write_statistics()
    for strategy, count in stats.items():
        print(f"  {strategy}: {count} 次")

    print(f"\n总写入次数: {sum(stats.values())} 次")



if __name__ == "__main__":
    main()
