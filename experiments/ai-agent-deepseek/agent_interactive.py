"""
交互式 AI Agent
可以与 Agent 进行实时对话
"""

import os
import json
from openai import OpenAI
from tools import TOOL_DEFINITIONS, execute_tool


def create_agent(api_key: str, base_url: str = "https://api.deepseek.com"):
    """创建 DeepSeek 客户端"""
    return OpenAI(api_key=api_key, base_url=base_url)


class InteractiveAgent:
    """交互式 AI Agent"""

    def __init__(self, client: OpenAI):
        self.client = client
        self.messages = []
        self.conversation_count = 0

        # 系统提示
        system_prompt = """你是一个智能助手，可以调用工具来帮助用户。

可用工具：
1. calculator - 计算数学表达式（支持 +、-、*、/、sqrt、sin、cos 等）
2. get_current_time - 获取当前时间
3. get_weather - 查询城市天气（支持：北京、上海、深圳、杭州）
4. search_knowledge - 搜索 AI 和 Web3 知识库

使用建议：
- 当用户需要计算时，使用 calculator
- 当用户询问时间时，使用 get_current_time
- 当用户询问天气时，使用 get_weather
- 当用户询问 AI/Web3 概念时，使用 search_knowledge
- 对于普通对话，直接回答即可

请用友好、专业的方式与用户交流。"""

        self.messages.append({
            "role": "system",
            "content": system_prompt
        })

    def chat(self, user_message: str) -> str:
        """
        与 Agent 对话

        Args:
            user_message: 用户消息

        Returns:
            Agent 的回答
        """
        self.conversation_count += 1

        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # 循环处理工具调用
        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # 调用 LLM
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            # 检查是否需要调用工具
            if assistant_message.tool_calls:
                print(f"\n🔧 [Agent 正在调用工具...]")

                # 添加 Assistant 消息
                self.messages.append(assistant_message)

                # 执行所有工具调用
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"   → {tool_name}({json.dumps(tool_args, ensure_ascii=False)})")

                    # 执行工具
                    tool_result = execute_tool(tool_name, tool_args)

                    # 添加工具结果
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })

                # 继续循环
                continue

            else:
                # 返回最终回答
                final_answer = assistant_message.content
                self.messages.append(assistant_message)
                return final_answer

        return "抱歉，处理超时了。"

    def reset(self):
        """重置对话历史"""
        system_message = self.messages[0]
        self.messages = [system_message]
        self.conversation_count = 0
        print("\n✅ 对话历史已重置\n")

    def show_stats(self):
        """显示统计信息"""
        print(f"\n📊 对话统计:")
        print(f"   对话轮数: {self.conversation_count}")
        print(f"   消息数量: {len(self.messages)}")
        print()


def print_welcome():
    """打印欢迎信息"""
    print("\n" + "="*60)
    print("🤖 AI Agent 交互式演示")
    print("="*60)
    print("\n💡 可用命令:")
    print("   /help    - 显示帮助信息")
    print("   /reset   - 重置对话历史")
    print("   /stats   - 显示统计信息")
    print("   /tools   - 显示可用工具")
    print("   /exit    - 退出程序")
    print("\n💡 示例问题:")
    print("   - 计算 (123 + 456) * 789")
    print("   - 现在几点了？")
    print("   - 北京天气怎么样？")
    print("   - 什么是 RAG？")
    print("   - 先查询时间，然后计算当前小时数乘以 60")
    print("\n" + "="*60 + "\n")


def print_help():
    """打印帮助信息"""
    print("\n" + "="*60)
    print("📚 帮助信息")
    print("="*60)
    print("\n🔧 可用工具:")
    print("   1. calculator - 计算数学表达式")
    print("      示例: 计算 2 + 3 * 4")
    print("\n   2. get_current_time - 获取当前时间")
    print("      示例: 现在几点？")
    print("\n   3. get_weather - 查询城市天气")
    print("      示例: 北京天气怎么样？")
    print("      支持城市: 北京、上海、深圳、杭州")
    print("\n   4. search_knowledge - 搜索知识库")
    print("      示例: 什么是 LLM？")
    print("      支持主题: LLM、Agent、RAG、Prompt、Embedding")
    print("\n💡 提示:")
    print("   - Agent 会自动决定是否需要调用工具")
    print("   - 你可以提出需要多步推理的复杂问题")
    print("   - 对于普通对话，Agent 会直接回答")
    print("\n" + "="*60 + "\n")


def print_tools():
    """打印工具列表"""
    print("\n" + "="*60)
    print("🔧 可用工具列表")
    print("="*60)
    for i, tool_def in enumerate(TOOL_DEFINITIONS, 1):
        func = tool_def["function"]
        print(f"\n{i}. {func['name']}")
        print(f"   描述: {func['description']}")
        print(f"   参数: {', '.join(func['parameters']['properties'].keys())}")
    print("\n" + "="*60 + "\n")


def main():
    """主函数"""
    # 检查 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n❌ 错误: 请设置环境变量 DEEPSEEK_API_KEY")
        print("\n设置方法:")
        print("  export DEEPSEEK_API_KEY='your-api-key-here'")
        print("\n然后重新运行程序。\n")
        return

    # 创建 Agent
    client = create_agent(api_key)
    agent = InteractiveAgent(client)

    # 显示欢迎信息
    print_welcome()

    # 主循环
    while True:
        try:
            # 读取用户输入
            user_input = input("👤 你: ").strip()

            # 处理空输入
            if not user_input:
                continue

            # 处理命令
            if user_input.startswith("/"):
                command = user_input.lower()

                if command == "/exit":
                    print("\n👋 再见！\n")
                    break

                elif command == "/help":
                    print_help()
                    continue

                elif command == "/reset":
                    agent.reset()
                    continue

                elif command == "/stats":
                    agent.show_stats()
                    continue

                elif command == "/tools":
                    print_tools()
                    continue

                else:
                    print(f"\n❌ 未知命令: {user_input}")
                    print("   输入 /help 查看可用命令\n")
                    continue

            # 与 Agent 对话
            print()  # 空行
            response = agent.chat(user_input)
            print(f"\n🤖 Agent: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 再见！\n")
            break

        except Exception as e:
            print(f"\n❌ 错误: {e}\n")
            print("请重试或输入 /help 查看帮助\n")


if __name__ == "__main__":
    main()
