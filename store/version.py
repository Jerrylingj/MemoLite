from dataclasses import dataclass
from collections import defaultdict
from memory import MemoryItem, MemoryType
from datetime import datetime
from typing import List, Dict


@dataclass
class MemoryVersion:
    """记忆版本: 用于处理记忆冲突"""
    version: int
    content: str
    timestamp: datetime
    confidence: float
    source: str # 'user', 'system', 'inferred'

class MemoryUpdateManager:
    """记忆更新与冲突解决管理器"""

    def __init__(self):
        # 存储每个key的版本历史
        self.version_history: Dict[str, List[MemoryVersion]] = defaultdict(list)
        self.current_version: Dict[str, MemoryItem] = {}
        self.decay_rate = 0.1 # 每天衰减10%

    def add_or_update(self, key: str, new_memory:MemoryItem, source: str='system'):
        """添加或更新记忆(带版本控制)"""
        # 创建版本目录
        version_num = len(self.version_history[key]) + 1
        version = MemoryVersion(
            version=version_num,
            content=new_memory.content,
            timestamp=new_memory.timestamp,
            confidence=new_memory.confidence,
            source=source
        )
        self.version_history[key].append(version)

        # 判断是否冲突
        if key in self.current_version:
            old_memory = self.current_version[key]
            print(f"⚠️  检测到记忆更新: {key}")
            print(f"   旧版本: {old_memory.content}")
            print(f"   新版本: {new_memory.content}")
            print(f"   版本号: v{version_num}")

            # 解决冲突
            resolved = self._resolve_conflict(old_memory, new_memory, source)
            self.current_version[key] = resolved
            print(f"   ✅ 冲突已解决，采用: {resolved.content}")
        else:
            self.current_version[key] = new_memory
            print(f"✨ 新增记忆: {key} -> {new_memory.content}")

        
    def _resolve_conflict(self, old: MemoryItem, new: MemoryItem, source: str):
        """解决冲突策略"""
        # 1. 用户反馈优先级最高
        if source == 'user':
            print(f"   🎯 策略: 用户反馈优先")
            return new
        
        # 2. 置信度加权
        old_weight = old.confidence
        new_weight = new.confidence

        if new_weight > old_weight:
            print(f"   ⚖️  策略: 高置信度优先 (新:{new_weight:.2f} > 旧:{old_weight:.2f})")
            return new
        elif new_weight < old_weight:
            print(f"   ⚖️  策略: 保持高置信度 (旧:{old_weight:.2f} > 新:{new_weight:.2f})")
            # 增加旧记忆的频率
            old.frequency += 1
            return old
        else:
            # 3: 相同置信度，选择最新的
            print(f"   ⏰ 策略: 时间优先（置信度相同）")
            return new if new.timestamp > old.timestamp else old

    def apply_time_decay(self, days_passed: float = 1.0):
        """应用时间衰减"""
        print(f"\n⏳ 应用时间衰减 (经过{days_passed}天)...\n")

        for key, memory in self.current_version.items():
            # 某些类型不衰减
            if memory.memory_type in [MemoryType.USER_PROFILE, MemoryType.PREFERENCES]:
                print(f"    {key}: 不衰减 (类型: {memory.memory_type.value})")
                continue
            
            # 计算衰减
            old_importance = memory.importance
            # 剩余比例：每天衰减 decay_rate 比例, 衰减了 days_passed 天
            decay_factor = (1 - self.decay_rate) ** days_passed
            memory.importance = old_importance * decay_factor

            print(f"  {key}: {old_importance:.3f} -> {memory.importance:.3f}")

    def get_version_history(self, key: str) -> List[MemoryVersion]:
        """获取版本历史"""
        return self.version_history.get(key, [])
    def rollback(self, key:str, version_num: int):
        """回滚到指定版本"""
        versions = self.version_history.get(key, [])
        # 异常情况
        if not versions or version_num < 1 or version_num > len(versions):
            return False

        target_version = versions[version_num - 1]
        # 重建 MemoryItem
        rolled_back = MemoryItem(
            content=target_version.content,
            memory_type=self.current_version[key].memory_type, # vesion_history 里的是阉割版, 没存这个字段, 因为都一样没必要存
            timestamp=target_version.timestamp,
            confidence=target_version.confidence
        )
        self.current_version[key] = rolled_back # 会滚到目标版本
        print(f"🔙 已回滚 {key} 到版本 v{version_num}")
        return True


############################### 测试部分 ###############################
update_manager = MemoryUpdateManager()

def main():
    print("✅ 记忆更新管理器创建成功")    

    # 演示记忆更新与冲突解决
    print("🎬 演示记忆更新与冲突解决：\n")
    print("="*70)

    # 场景1: 初次添加
    print("\n场景1️⃣: 初次添加用户偏好\n")
    mem1 = MemoryItem(
        content="用户喜欢简洁的输出",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        confidence=0.7
    )
    update_manager.add_or_update("output_style", mem1, source='system')

    print("\n" + "="*70)

    # 场景2: 系统推断更新（置信度较低）
    print("\n场景2️⃣: 系统推断出新偏好（置信度较低）\n")
    mem2 = MemoryItem(
        content="用户可能喜欢详细的输出",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        confidence=0.5
    )
    update_manager.add_or_update("output_style", mem2, source='inferred')

    print("\n" + "="*70)

    # 场景3: 用户明确反馈（最高优先级）
    print("\n场景3️⃣: 用户明确表达偏好\n")
    mem3 = MemoryItem(
        content="用户要求输出必须包含详细图表",
        memory_type=MemoryType.PREFERENCES,
        timestamp=datetime.now(),
        confidence=1.0
    )
    update_manager.add_or_update("output_style", mem3, source='user')

    print("\n" + "="*70)
  

if __name__ == "__main__":
    main()