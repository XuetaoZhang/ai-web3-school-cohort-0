"""
简单的 AI Agent 实现
演示单次工具调用的完整流程
"""

import os
import json
from openai import OpenAI
from tools import TOOL_DEFINITIONS, execute_tool


def create_agent(api_key: str, base_url: str = "https://api.deepseek.com"):
    """创建 DeepSeek 客户端"""
    return OpenAI(api_key=api_key, base_url=base_url)


def run_agent(client: OpenAI, user_message: str, verbose: bool = True):
    """
    运行 Agent，处理单次对话

    Args:
        client: OpenAI 客户端
        user_message: 用户消息
        verbose: 是否打印详细信息

    Returns:
        Agent 的最终回答
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"👤 用户: {user_message}")
        print(f"{'='*60}\n")

    # 第一步：发送用户消息，让 Agent 决定是否需要调用工具
    messages = [
        {
            "role": "system",
            "content": "你是一个智能助手，可以调用工具来帮助用户。当需要计算、查询时间、天气或搜索知识时，请使用相应的工具。"
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    if verbose:
        print("🤖 Agent 思考中...")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto"  # 让模型自动决定是否调用工具
    )

    assistant_message = response.choices[0].message

    # 第二步：检查 Agent 是否决定调用工具
    if assistant_message.tool_calls:
        if verbose:
            print(f"🔧 Agent 决定调用工具:\n")

        # 将 Agent 的响应添加到对话历史
        messages.append(assistant_message)

        # 执行所有工具调用
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"   工具名称: {tool_name}")
                print(f"   工具参数: {json.dumps(tool_args, ensure_ascii=False)}")

            # 执行工具
            tool_result = execute_tool(tool_name, tool_args)

            if verbose:
                print(f"   工具结果: {tool_result}\n")

            # 将工具结果添加到对话历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

        # 第三步：将工具结果发送给 Agent，生成最终回答
        if verbose:
            print("🤖 Agent 根据工具结果生成回答...\n")

        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        final_answer = final_response.choices[0].message.content

        if verbose:
            print(f"{'='*60}")
            print(f"✅ Agent 最终回答:\n{final_answer}")
            print(f"{'='*60}\n")

        return final_answer

    else:
        # Agent 决定不需要调用工具，直接回答
        if verbose:
            print("💬 Agent 直接回答（无需工具）\n")
            print(f"{'='*60}")
            print(f"✅ Agent 回答:\n{assistant_message.content}")
            print(f"{'='*60}\n")

        return assistant_message.content


def main():
    """主函数：演示 Agent 的使用"""
    print("\n" + "="*60)
    print("🤖 AI Agent 演示 - 简单版本")
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

    # 测试案例
    test_cases = [
        "计算 (123 + 456) * 789 的结果",
        "现在几点了？",
        "北京今天天气怎么样？",
        "什么是 RAG？",
        "你好，介绍一下你自己"  # 不需要工具的问题
    ]

    print("\n📋 测试案例:")
    for i, case in enumerate(test_cases, 1):
        print(f"  {i}. {case}")

    print("\n" + "="*60)
    print("开始测试...")
    print("="*60)

    # 运行测试
    for test_case in test_cases:
        try:
            run_agent(client, test_case, verbose=True)
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")

        # 暂停一下，避免请求过快
        import time
        time.sleep(1)

    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)


if __name__ == "__main__":
    main()
