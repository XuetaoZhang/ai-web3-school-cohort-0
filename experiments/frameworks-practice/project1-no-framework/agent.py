"""
项目1：不使用 Frameworks 的 Agent 实现
手动实现 Function Calling 流程
"""

from openai import OpenAI
import os
import json
import requests

# 工具定义（OpenAI 格式）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_eth_balance",
            "description": "获取以太坊地址的余额。输入一个以太坊地址，返回该地址在 Sepolia 测试网上的 ETH 余额。",
            "parameters": {
                "type": "object",
                "properties": {
                    "eth_address": {
                        "type": "string",
                        "description": "以太坊地址，例如：0x1234567890abcdef1234567890abcdef12345678"
                    }
                },
                "required": ["eth_address"]
            }
        }
    }
]

def get_eth_balance(eth_address: str) -> str:
    """
    调用 Sepolia RPC 接口获取地址余额
    """
    rpc_url = "https://sepolia.infura.io/v3/a741720a2c33491da85d6f877f3cc1ba"

    # 构造 JSON-RPC 请求
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [eth_address, "latest"],
        "id": 1
    }

    try:
        response = requests.post(rpc_url, json=payload)
        result = response.json()

        if "result" in result:
            # 将 Wei 转换为 ETH
            balance_wei = int(result["result"], 16)
            balance_eth = balance_wei / 10**18
            return f"{balance_eth} ETH"
        else:
            return f"错误：{result.get('error', '未知错误')}"
    except Exception as e:
        return f"请求失败：{str(e)}"

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    手动执行工具调用
    """
    if tool_name == "get_eth_balance":
        return get_eth_balance(tool_input["eth_address"])
    else:
        return f"未知工具：{tool_name}"

def run_agent(user_question: str):
    """
    手动实现 Agent 循环
    """
    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

    messages = [
        {
            "role": "user",
            "content": user_question
        }
    ]

    print(f"\n{'='*60}")
    print(f"用户问题：{user_question}")
    print(f"{'='*60}\n")

    # Agent 循环
    while True:
        # 步骤1：调用 LLM
        print("📤 调用 LLM...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        print(f"✅ LLM 响应类型：{response.choices[0].finish_reason}")

        # 步骤2：检查是否需要调用工具
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            tool_id = tool_call.id

            print(f"\n🔧 LLM 请求调用工具：{tool_name}")
            print(f"   参数：{json.dumps(tool_input, ensure_ascii=False)}")

            # 步骤3：手动执行工具
            print(f"⚙️  执行工具...")
            tool_result = process_tool_call(tool_name, tool_input)
            print(f"✅ 工具返回：{tool_result}")

            # 步骤4：将工具结果返回给 LLM
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": tool_result
            })

            # 继续循环，让 LLM 处理工具结果
            continue

        # 步骤5：LLM 返回最终答案
        else:
            final_answer = message.content

            print(f"\n{'='*60}")
            print(f"🤖 最终答案：")
            print(f"{'='*60}")
            print(final_answer)
            print(f"{'='*60}\n")
            break

if __name__ == "__main__":
    # 测试问题
    question = "0x1234567890abcdef1234567890abcdef12345678这个地址的余额是多少？"
    run_agent(question)
