from langchain_siliconflow import SiliconFlowEmbeddings
from config import embeddings
from memory import MemoryItem, sample_memories
from typing import List, Dict, Tuple
import numpy as np

class VectorMemoryStore:
    """向量化记忆存储： embedding, 添加, 检索"""

    def __init__(self, embeddings: SiliconFlowEmbeddings):
        """embedding模型, 原记忆, 向量池"""
        self.embedding_model = embeddings
        self.memories: List[MemoryItem] = []
        self.embeddings: List[np.ndarray] = []

    def get_embedding(self, text: str) -> np.ndarray:
        """获取文本的embedding"""
        embedding = self.embedding_model.embed_query(text)
        return np.array(embedding)

    def add(self, memory: MemoryItem):
        """添加记忆, 自动向量化"""
        embedding = self.get_embedding(memory.content)
        self.memories.append(memory)
        self.embeddings.append(embedding)
        print(f"向量化存储: {memory.content}")

    def semantic_search(self, query: str, top_k: int=3) -> List[Tuple[MemoryItem, float]]:
        """语义检索"""
        q_embedding = self.get_embedding(query)
        similarities = []
        for i, mem_embedding in enumerate(self.embeddings):
            # 相似度: 点乘 / 模乘
            similarity = np.dot(mem_embedding, q_embedding) / (
                np.linalg.norm(mem_embedding) * np.linalg.norm(q_embedding)
            )
            similarities.append((self.memories[i], similarity))

        # 降序排序, .sort 直接原地排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

        
############################### 测试部分 ###############################
vec_store = VectorMemoryStore(embeddings)

def main():
    print("向量化 记忆存储示例: ")
    for mem in sample_memories:
        vec_store.add(mem)
    print(f"\n存储统计: 共 {len(vec_store.memories)} 条记忆")

    print("\n语义检索示例: ")
    queries = [
        "用户的职业是什么?",
        "用户喜欢什么样的输出格式?",
        "当前有什么任务在进行中?"
    ]


    for q in queries:
        print(f"\n查询: {q}")
        results = vec_store.semantic_search(q, 2)
        print("相关记忆（top-2）:")
        for i, (memory, score) in enumerate(results, 1):
            print(f"    {i}. [{memory.memory_type.value}] {memory.content}")
            print(f"       相似度: {score:.4f}")

if __name__ == "__main__":
    main()