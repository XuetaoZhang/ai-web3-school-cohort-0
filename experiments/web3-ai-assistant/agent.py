"""
Web3 AI Assistant - 智能合约助手
结合 AI 和 Web3 的实践项目
"""

import os
import json
from openai import OpenAI
from tools import TOOL_DEFINITIONS, AVAILABLE_TOOLS


def create_client():
    """创建 DeepSeek API 客户端"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )


def run_agent(user_message: str, verbose: bool = True):
    """
    运行 Web3 AI Assistant Agent

    Args:
        user_message: 用户消息
        verbose: 是否显示详细信息

    Returns:
        Agent 的最终回答
    """
    client = create_client()

    # 系统提示词
    system_prompt = """你是一个专业的 Web3 智能合约助手，精通 Solidity 和区块链安全。

你的能力：
1. 安全审计：检测智能合约的安全漏洞
2. 代码生成：生成标准的智能合约代码
3. 代码解释：分析和解释合约功能
4. Gas 优化：提供 Gas 优化建议

你的特点：
- 专业：使用准确的技术术语
- 详细：提供具体的代码示例和建议
- 安全：始终关注安全问题
- 实用：给出可操作的建议

当用户提供合约代码时，你应该：
1. 先理解用户的需求
2. 调用相应的工具进行分析
3. 基于工具结果给出专业的建议
4. 如果发现安全问题，务必详细说明风险和修复方案
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    if verbose:
        print("🤖 Web3 AI Assistant 正在分析...")
        print()

    # 多步推理循环
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # 检查是否需要调用工具
        if assistant_message.tool_calls:
            if verbose:
                print(f"🔧 调用工具 (第 {iteration} 轮):")
                print()

            # 将 assistant 消息添加到历史
            messages.append(assistant_message)

            # 执行所有工具调用
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                if verbose:
                    print(f"  📌 工具: {tool_name}")
                    print(f"  📝 参数: {json.dumps(tool_args, ensure_ascii=False, indent=4)}")

                # 执行工具
                if tool_name in AVAILABLE_TOOLS:
                    tool_function = AVAILABLE_TOOLS[tool_name]
                    try:
                        # 根据工具参数调用
                        if tool_name == "generate_contract":
                            result = tool_function(
                                tool_args.get("contract_type"),
                                tool_args.get("params", "{}")
                            )
                        else:
                            result = tool_function(tool_args.get("code", ""))

                        if verbose:
                            print(f"  ✅ 执行成功")
                            print()

                    except Exception as e:
                        result = json.dumps({"error": str(e)}, ensure_ascii=False)
                        if verbose:
                            print(f"  ❌ 执行失败: {e}")
                            print()
                else:
                    result = json.dumps({"error": f"未知工具: {tool_name}"}, ensure_ascii=False)

                # 将工具结果添加到消息历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # 继续循环，让 LLM 处理工具结果
            continue

        else:
            # 没有工具调用，返回最终答案
            final_answer = assistant_message.content

            if verbose:
                print("=" * 60)
                print("💬 最终回答:")
                print("=" * 60)
                print()

            return final_answer

    # 达到最大迭代次数
    return "抱歉，处理超时。请简化您的问题或分步提问。"


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("🤖 Web3 AI Assistant - 智能合约助手")
    print("=" * 60)
    print()
    print("功能：")
    print("  1. 安全审计 - 检测合约安全问题")
    print("  2. 代码生成 - 生成标准合约代码")
    print("  3. 代码解释 - 分析合约功能")
    print("  4. Gas 优化 - 提供优化建议")
    print()
    print("命令：")
    print("  /help  - 显示帮助")
    print("  /quit  - 退出程序")
    print("  /clear - 清空屏幕")
    print()
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("👤 你: ").strip()

            if not user_input:
                continue

            if user_input == "/quit" or user_input == "/exit":
                print("👋 再见！")
                break

            if user_input == "/help":
                print()
                print("📖 使用示例：")
                print()
                print("1. 安全审计：")
                print("   检查这个合约的安全问题：[粘贴合约代码]")
                print()
                print("2. 代码生成：")
                print("   生成一个 ERC20 代币合约，名称 MyToken，符号 MTK")
                print()
                print("3. 代码解释：")
                print("   解释这个合约的功能：[粘贴合约代码]")
                print()
                print("4. Gas 优化：")
                print("   优化这个合约的 Gas 消耗：[粘贴合约代码]")
                print()
                continue

            if user_input == "/clear":
                os.system('clear' if os.name != 'nt' else 'cls')
                continue

            # 运行 Agent
            print()
            response = run_agent(user_input, verbose=True)
            print(response)
            print()
            print("-" * 60)
            print()

        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print()


def main():
    """主函数"""
    import sys

    # 检查 API Key
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("❌ 错误: 请设置环境变量 DEEPSEEK_API_KEY")
        print()
        print("设置方法:")
        print("  export DEEPSEEK_API_KEY='your-api-key-here'")
        print()
        sys.exit(1)

    # 检查命令行参数
    if len(sys.argv) > 1:
        # 非交互模式
        user_message = " ".join(sys.argv[1:])
        response = run_agent(user_message, verbose=True)
        print(response)
    else:
        # 交互模式
        interactive_mode()


if __name__ == "__main__":
    main()
