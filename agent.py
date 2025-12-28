from langchain_siliconflow import SiliconFlowEmbeddings, ChatSiliconFlow
from config import Config, llm, embeddings, config
from store.kv_store import KeyValueMemoryStore
from store.vector_store import VectorMemoryStore
from store.writer import MemoryWriter
from store.priority import PriorityMemoryManager # 管理不同级别记忆, hierarchy
from store.version import MemoryUpdateManager # 负责处理记忆冲突, 写入不同版本
from prompts.SYSTEM_PROPT import EXTRACTION_PROMPT
from datetime import datetime
from memory import MemoryItem, MemoryType
from evaluator import MemoryValueEvaluator
import json

class SmartMemoryAgent:
    """记忆Agent"""

    def __init__(self, embeddings: SiliconFlowEmbeddings, llm: ChatSiliconFlow, config: Config):
        self.embeddings = embeddings
        self.llm = llm
        self.config = config

        # 初始化各组件
        self.evaluator = MemoryValueEvaluator()
        self.kv_store = KeyValueMemoryStore()
        self.vector_store = VectorMemoryStore(embeddings) # Vector 需要传 embedding 模型
        self.writer = MemoryWriter(self.kv_store, self.vector_store)
        self.priority_manager = PriorityMemoryManager(self.evaluator)
        self.update_manager = MemoryUpdateManager()

        print("MemoryAgent Initialized!")
    
    def process_user_input(self, user_input: str):
        """处理用户输入并提取记忆"""
        print(f"\n用户输入: {user_input}")
        print(f"分析中……")

        memories_to_store = self.extract_memories_with_llm(user_input)

        # 存储提取的记忆
        if memories_to_store:
            for memory in memories_to_store:
                self._store_memory(memory)
        else:
            print(f"! 未识别到需要存储的记忆（可能需要更明确的表达）\n")



    def extract_memories_with_llm(self, user_input: str):
        """使用 LLM 提取记忆, 判断能否由用户当前输入拿到什么有价值的东西"""

        prompt = EXTRACTION_PROMPT.format(user_input=user_input)
    
        response = self.llm.invoke(prompt)

        # 解析 JSON, 提起记忆数组
        try:
            memories_data = json.loads(response.content)
        except json.JSONDecodeError as e:
            print(f"LLM 返回格式错误, {e}")
            return []

        # 转换为 MemoryItem
        memories = []
        for mem in memories_data:
            memory = MemoryItem(
                content=mem["content"],
                memory_type=MemoryType[mem["memory_type"]],
                importance=mem["importance"],
                timestamp=datetime.now(),
                confidence=mem["confidence"],
                
                
            )
            memories.append(memory)
        return memories

    def _store_memory(self, memory: MemoryItem):
        """存储记忆"""
        # 评估并分级存储
        scores = self.evaluator.evaluate(memory)
        priority = self.priority_manager.classify_priority(memory)

        print(f"📝 记忆: {memory.content}")
        print(f"   类型: {memory.memory_type.value}")
        print(f"   优先级: {priority.value}")
        print(f"   综合得分: {scores['total_score']:.3f}")

        # 存储到各个系统
        self.priority_manager.store(memory)
        self.vector_store.add(memory) # 存到向量数据库方便语义检索
        key = f"{memory.memory_type.value}_{datetime.now().timestamp}_{memory.metadata}" # 加上 metadata 防止相同类型记忆冲突了
        self.update_manager.add_or_update(key, memory)
        print()

    def recall(self, query: str, top_k: int=3):
        """召回记忆"""
        print(f"\n🔍 查询: {query}\n")
        results = self.vector_store.semantic_search(query, top_k)

        print(f"找到 {len(results)} 条相关记忆:\n")
        for i, (memory, score) in enumerate(results, 1):
            print(f"{i}. [{memory.memory_type.value}] {memory.content}")
            print(f"   相似度: {score:.4f}")
            print()
        
        return results

    def get_report(self):
        """生成记忆系统报告"""
        print("\n" + "="*70)
        print("📊 记忆系统报告")
        print("="*70)

        # 优先级统计
        priority_stats = self.priority_manager.get_statistics()
        print("\n📈 优先级分布:")
        for layer, count in priority_stats.items():
            print(f"  {layer}: {count} 条")

        # 写入统计
        write_stats = self.writer.get_write_statistics()
        if write_stats:
            print("\n✍️  写入策略统计:")
            for strategy, count in write_stats.items():
                print(f"  {strategy}: {count} 次")

        print("\n" + "="*70)

############################### 测试部分 ###############################
agent = SmartMemoryAgent(embeddings, llm, config)

def main():
    # 创建并演示智能Agent
    print("🎬 模拟完整交互场景\n")
    print("="*70)

    # 模拟用户交互
    print("\n" + "="*70)
    agent.process_user_input("我是一名数据科学家，主要做金融数据分析。")

    print("\n" + "-"*70)
    agent.process_user_input("我喜欢用图表展示结果，不喜欢纯文字报告。")

    print("\n" + "-"*70)
    agent.process_user_input("这个月我需要完成市场分析和风险评估两个任务。")

    print("\n" + "="*70)

    # 测试召回功能
    print("\n🧠 测试记忆召回功能\n")
    print("="*70)

    agent.recall("用户的职业背景是什么？")
    agent.recall("用户对输出格式有什么偏好？")
    agent.recall("当前有哪些任务？")

    # 生成最终报告
    agent.get_report()

if __name__ == "__main__":
    main()
