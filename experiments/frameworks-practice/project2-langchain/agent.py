"""
项目2：使用 LangChain Framework 的 Agent 实现
使用 LangGraph 自动处理工具调用流程
"""

import os
import requests
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def get_eth_balance(eth_address: str) -> str:
    """
    获取以太坊地址的余额。输入一个以太坊地址，返回该地址在 Sepolia 测试网上的 ETH 余额。

    Args:
        eth_address: 以太坊地址，例如：0x1234567890abcdef1234567890abcdef12345678

    Returns:
        该地址的 ETH 余额
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

def run_agent(user_question: str):
    """
    使用 LangGraph 运行 Agent
    """
    print(f"\n{'='*60}")
    print(f"用户问题：{user_question}")
    print(f"{'='*60}\n")

    # 初始化 LLM（使用 DeepSeek）
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com",
        temperature=0
    )

    # 定义工具列表
    tools = [get_eth_balance]

    print("🤖 LangGraph 自动处理：")
    print("   ✅ 自动调用 LLM")
    print("   ✅ 自动解析工具调用")
    print("   ✅ 自动执行工具")
    print("   ✅ 自动把结果给 LLM")
    print("   ✅ 自动生成最终答案")
    print("   ✅ 自动处理循环逻辑\n")

    # 使用 LangGraph 创建 ReAct Agent（一行代码！）
    agent_executor = create_react_agent(llm, tools)

    # 执行 Agent（Framework 自动处理所有步骤）
    result = agent_executor.invoke({"messages": [("user", user_question)]})

    # 获取最终答案
    final_message = result["messages"][-1]

    print(f"\n{'='*60}")
    print(f"🤖 最终答案：")
    print(f"{'='*60}")
    print(final_message.content)
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # 测试问题
    question = "0x1234567890abcdef1234567890abcdef12345678这个地址的余额是多少？"
    run_agent(question)
