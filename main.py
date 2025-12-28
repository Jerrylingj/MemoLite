from agent import SmartMemoryAgent
from config import llm, embeddings, config
import sys

def main():
    agent = SmartMemoryAgent(embeddings=embeddings, llm=llm, config=config)

    print("\n" + "="*70)
    print("🤖 欢迎使用 MemoLite - 一个轻量的 Memory Agent")
    print("="*70)
    print("\n💡 功能说明:")
    print("  - 输入任何内容，Agent 会自动提取并记住重要信息")
    print("  - 输入 'recall <查询>' 来检索相关记忆")
    print("  - 输入 'report' 查看记忆系统报告")
    print("  - 输入 'exit' 或 'quit' 退出程序")

     # 多轮对话循环
    while True:
        try:
            user_input = input("👤 你: ").strip()
            
            # 处理特殊命令
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 再见！")
                break
            
            elif user_input.lower() == 'report':
                agent.get_report()
            
            elif user_input.lower().startswith('recall '):
                query = user_input[7:]  # 去掉 'recall ' 前缀
                agent.recall(query)
            
            else:
                # 普通输入 - 处理并提取记忆
                agent.process_user_input(user_input)
        
        except KeyboardInterrupt:
            print("\n\n👋 程序已中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 出错了: {e}")
            print("请重试或输入 'exit' 退出\n")

if __name__ == "__main__":
    main()
