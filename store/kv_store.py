from typing import Dict

from memory import MemoryItem, MemoryType, sample_memories
class KeyValueMemoryStore:
    """Key-Value 记忆存储"""

    def __init__(self):
        self.store: Dict[str, MemoryItem] = {}

    def set(self, key: str, memory: MemoryItem):
        self.store[key] = memory
        print(f"✅ 已存储: {key} -> {memory.content}")

    def get(self, key: str):
        return self.store.get(key)

    def get_by_type(self, memory_type: MemoryType):
        return [
            mem for mem in self.store.values()
            if mem.memory_type == memory_type
        ]

    def list_all(self):
        return list(self.store.items())

############################### 测试部分 ###############################
# 1. 创建KV存储并添加示例
kv_store = KeyValueMemoryStore()

def main():
    print("🗂️ Key-Value 记忆存储示例：\n")
    kv_store.set("user_profession", sample_memories[0])
    kv_store.set("last_meeting_date", sample_memories[1])
    kv_store.set("output_preference", sample_memories[2])

    print(f"\n📋 存储统计: 共 {len(kv_store.store)} 条记忆")

if __name__ == "__main__":
    main()