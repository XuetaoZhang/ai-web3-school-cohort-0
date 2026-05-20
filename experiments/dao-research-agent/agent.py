"""
DAO Research Agent - Main Program
实现标准的 Agentic Loop
"""

import os
import json
from openai import OpenAI
from typing import List, Dict, Any

from tools import (
    read_proposal,
    search_forum,
    analyze_sentiment,
    check_risks,
    generate_checklist,
    TOOLS_DEFINITION
)
from prompts import SYSTEM_PROMPT


# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),
    base_url="https://api.deepseek.com"
)


def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> Any:
    """
    执行工具函数

    Args:
        tool_name: 工具名称
        tool_args: 工具参数

    Returns:
        工具执行结果
    """
    print(f"\n🔧 执行工具: {tool_name}")
    print(f"   参数: {json.dumps(tool_args, ensure_ascii=False)}")

    if tool_name == "read_proposal":
        result = read_proposal(**tool_args)
    elif tool_name == "search_forum":
        result = search_forum(**tool_args)
    elif tool_name == "analyze_sentiment":
        result = analyze_sentiment(**tool_args)
    elif tool_name == "check_risks":
        result = check_risks(**tool_args)
    elif tool_name == "generate_checklist":
        result = generate_checklist(**tool_args)
    else:
        result = {"error": f"未知的工具: {tool_name}"}

    print(f"   ✓ 完成")
    return result


def run_agent(user_input: str, max_iterations: int = 10, verbose: bool = True) -> str:
    """
    运行 Agent，实现 Agentic Loop

    Args:
        user_input: 用户输入
        max_iterations: 最大迭代次数（防止无限循环）
        verbose: 是否显示详细过程

    Returns:
        Agent 的最终输出
    """
    # 初始化消息列表
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    if verbose:
        print("\n" + "=" * 60)
        print("🤖 DAO Research Agent 启动")
        print("=" * 60)
        print(f"📝 用户请求: {user_input}")
        print("=" * 60)

    # Agentic Loop
    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n🔄 第 {iteration} 轮")

        try:
            # 1. 调用 LLM
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=TOOLS_DEFINITION,
                tool_choice="auto",  # 让 LLM 自己决定是否调用工具
                temperature=0.7
            )

            assistant_message = response.choices[0].message

            # 2. 将 LLM 的响应添加到消息列表
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })

            # 3. 检查是否需要调用工具
            if assistant_message.tool_calls:
                if verbose:
                    print(f"   LLM 决定调用 {len(assistant_message.tool_calls)} 个工具")

                # 4. 执行所有工具调用
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # 执行工具
                    result = execute_tool(function_name, function_args)

                    # 5. 将工具结果返回给 LLM
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

                # 6. 继续循环，让 LLM 处理工具结果
                continue

            # 7. 如果没有工具调用，说明任务完成
            if verbose:
                print(f"   ✓ LLM 完成分析，生成最终报告")

            return assistant_message.content

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            return f"执行过程中发生错误: {e}"

    # 达到最大迭代次数
    return f"⚠️ 达到最大迭代次数（{max_iterations}），任务可能未完成"


def main():
    """
    主程序 - 交互式命令行界面
    """
    print("\n" + "=" * 60)
    print("🤖 DAO Research Agent - 提案研究助手")
    print("=" * 60)
    print("\n功能：")
    print("  - 分析 DAO 提案")
    print("  - 搜索论坛讨论")
    print("  - 评估风险")
    print("  - 生成投票前检查清单")
    print("\n命令：")
    print("  /help  - 显示帮助")
    print("  /quit  - 退出程序")
    print("  /list  - 列出可用的提案")
    print("\n示例：")
    print("  分析提案 #123")
    print("  研究提案 124")
    print("\n" + "=" * 60)

    while True:
        try:
            user_input = input("\n👤 你: ").strip()

            if not user_input:
                continue

            # 处理命令
            if user_input == "/quit":
                print("\n👋 再见！")
                break

            elif user_input == "/help":
                print("\n📖 帮助信息")
                print("-" * 60)
                print("使用方法：")
                print("  1. 输入 '分析提案 #123' 来分析提案")
                print("  2. Agent 会自动执行以下步骤：")
                print("     - 读取提案内容")
                print("     - 搜索论坛讨论")
                print("     - 分析支持/反对理由")
                print("     - 检查风险")
                print("     - 生成检查清单")
                print("  3. 最终输出完整的分析报告")
                continue

            elif user_input == "/list":
                print("\n📋 可用的提案")
                print("-" * 60)
                print("提案 #123: 为 DeFi 教育项目拨款 50,000 USDC")
                print("提案 #124: 修改治理参数 - 降低提案门槛")
                continue

            # 运行 Agent
            result = run_agent(user_input, verbose=True)

            # 输出结果
            print("\n" + "=" * 60)
            print("📊 分析报告")
            print("=" * 60)
            print(result)
            print("\n" + "=" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break

        except EOFError:
            print("\n\n👋 再见！")
            break

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # 检查 API Key
    if os.getenv("DEEPSEEK_API_KEY") == "your-api-key-here" or not os.getenv("DEEPSEEK_API_KEY"):
        print("\n⚠️  警告: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("请设置环境变量：")
        print("  export DEEPSEEK_API_KEY='your-api-key'")
        print("\n或者在代码中直接设置 api_key")
        print()

    main()
