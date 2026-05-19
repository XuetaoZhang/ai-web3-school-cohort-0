"""
多轮对话 AI Agent
演示 Agent 如何进行多轮工具调用和对话
"""

import os
import json
from openai import OpenAI
from tools import TOOL_DEFINITIONS, execute_tool


def create_agent(api_key: str, base_url: str = "https://api.deepseek.com"):
    """创建 DeepSeek 客户端"""
    return OpenAI(api_key=api_key, base_url=base_url)


class Agent:
    """AI Agent 类，支持多轮对话"""

    def __init__(self, client: OpenAI, system_prompt: str = None):
        self.client = client
        self.messages = []

        # 设置系统提示
        if system_prompt is None:
            system_prompt = """你是一个智能助手，可以调用工具来帮助用户。

可用工具：
1. calculator - 计算数学表达式
2. get_current_time - 获取当前时间
3. get_weather - 查询城市天气
4. search_knowledge - 搜索 AI 和 Web3 知识库

当用户需要计算、查询时间、天气或搜索知识时，请主动使用相应的工具。
如果一个问题需要多个步骤，可以多次调用工具。"""

        self.messages.append({
            "role": "system",
            "content": system_prompt
        })

    def chat(self, user_message: str, verbose: bool = True) -> str:
        """
        与 Agent 对话

        Args:
            user_message: 用户消息
            verbose: 是否打印详细信息

        Returns:
            Agent 的回答
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"👤 用户: {user_message}")
            print(f"{'='*60}\n")

        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # 循环处理，直到 Agent 不再调用工具
        max_iterations = 5  # 防止无限循环
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            if verbose and iteration > 1:
                print(f"🔄 第 {iteration} 轮处理...\n")

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
                if verbose:
                    print(f"🔧 Agent 调用工具:\n")

                # 添加 Assistant 消息
                self.messages.append(assistant_message)

                # 执行所有工具调用
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    if verbose:
                        print(f"   工具: {tool_name}")
                        print(f"   参数: {json.dumps(tool_args, ensure_ascii=False)}")

                    # 执行工具
                    tool_result = execute_tool(tool_name, tool_args)

                    if verbose:
                        print(f"   结果: {tool_result}\n")

                    # 添加工具结果
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })

                # 继续循环，让 Agent 处理工具结果
                continue

            else:
                # Agent 不再调用工具，返回最终回答
                final_answer = assistant_message.content
                self.messages.append(assistant_message)

                if verbose:
                    print(f"{'='*60}")
                    print(f"✅ Agent 回答:\n{final_answer}")
                    print(f"{'='*60}\n")

                return final_answer

        # 达到最大迭代次数
        if verbose:
            print("⚠️ 达到最大迭代次数，停止处理")

        return "抱歉，处理超时了。"

    def reset(self):
        """重置对话历史（保留系统提示）"""
        system_message = self.messages[0]
        self.messages = [system_message]


def main():
    """主函数：演示多轮对话 Agent"""
    print("\n" + "="*60)
    print("🤖 AI Agent 演示 - 多轮对话版本")
    print("="*60)

    # 检查 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n❌ 错误: 请设置环境变量 DEEPSEEK_API_KEY")
        print("\n设置方法:")
        print("  export DEEPSEEK_API_KEY='your-api-key-here'")
        return

    # 创建 Agent
    client = create_agent(api_key)
    agent = Agent(client)

    # 测试案例：需要多步推理的问题
    test_cases = [
        {
            "name": "复杂计算",
            "message": "先计算 100 * 50，然后用结果除以 25"
        },
        {
            "name": "多个查询",
            "message": "告诉我现在的时间，以及北京和上海的天气"
        },
        {
            "name": "知识搜索 + 计算",
            "message": "搜索一下什么是 Embedding，然后计算 256 * 768"
        }
    ]

    print("\n📋 测试案例:")
    for i, case in enumerate(test_cases, 1):
        print(f"  {i}. {case['name']}: {case['message']}")

    print("\n" + "="*60)
    print("开始测试...")
    print("="*60)

    # 运行测试
    for test_case in test_cases:
        print(f"\n\n{'#'*60}")
        print(f"# 测试: {test_case['name']}")
        print(f"{'#'*60}")

        try:
            agent.chat(test_case['message'], verbose=True)
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")

        # 重置对话历史
        agent.reset()

        # 暂停一下
        import time
        time.sleep(1)

    print("\n\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)

    # 交互式对话（可选）
    print("\n💡 提示: 你可以修改代码，添加交互式对话功能")
    print("   只需在 main() 函数中添加一个循环，不断读取用户输入即可")


if __name__ == "__main__":
    main()
