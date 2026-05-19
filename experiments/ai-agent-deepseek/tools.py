"""
AI Agent 工具定义
定义 Agent 可以调用的工具函数
"""

import json
from datetime import datetime
import math


# ============================================
# 工具函数定义
# ============================================

def calculator(expression: str) -> str:
    """
    计算数学表达式

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"

    Returns:
        计算结果
    """
    try:
        # 安全的数学计算（只允许基本运算）
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow, 'sqrt': math.sqrt,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'pi': math.pi, 'e': math.e
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return json.dumps({"result": result, "expression": expression}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """
    获取当前时间

    Args:
        timezone: 时区，默认 "Asia/Shanghai"

    Returns:
        当前时间信息
    """
    now = datetime.now()
    return json.dumps({
        "timezone": timezone,
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "timestamp": int(now.timestamp())
    }, ensure_ascii=False)


def get_weather(city: str) -> str:
    """
    获取城市天气（模拟数据）

    Args:
        city: 城市名称

    Returns:
        天气信息
    """
    # 模拟天气数据
    weather_data = {
        "北京": {"temperature": 15, "condition": "晴", "humidity": 45, "wind": "北风3级"},
        "上海": {"temperature": 18, "condition": "多云", "humidity": 60, "wind": "东风2级"},
        "深圳": {"temperature": 25, "condition": "阴", "humidity": 75, "wind": "南风1级"},
        "杭州": {"temperature": 20, "condition": "小雨", "humidity": 80, "wind": "东南风2级"},
    }

    if city in weather_data:
        data = weather_data[city]
        return json.dumps({
            "city": city,
            "temperature": data["temperature"],
            "condition": data["condition"],
            "humidity": data["humidity"],
            "wind": data["wind"],
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "error": f"未找到城市 {city} 的天气数据",
            "available_cities": list(weather_data.keys())
        }, ensure_ascii=False)


def search_knowledge(query: str) -> str:
    """
    搜索知识库（简化版，连接到 RAG 系统）

    Args:
        query: 搜索查询

    Returns:
        搜索结果
    """
    # 简化的知识库
    knowledge_base = {
        "LLM": "大语言模型（Large Language Model）是基于 Transformer 架构的深度学习模型，通过在海量文本数据上预训练，学习语言的统计规律和知识。",
        "Agent": "AI Agent 是能够感知环境、做出决策并采取行动的智能系统。它可以调用工具、执行任务、与环境交互。",
        "RAG": "检索增强生成（Retrieval-Augmented Generation）通过检索外部知识库来增强 LLM 的回答能力，减少幻觉。",
        "Prompt": "Prompt Engineering 是设计和优化输入提示词的技术，通过清晰的指令、示例和约束来引导 LLM 生成期望的输出。",
        "Embedding": "Embedding 是将文本转换为高维向量的技术，使得语义相似的文本在向量空间中距离更近。",
    }

    # 简单的关键词匹配
    results = []
    query_lower = query.lower()
    for topic, content in knowledge_base.items():
        if topic.lower() in query_lower or query_lower in content.lower():
            results.append({"topic": topic, "content": content})

    if results:
        return json.dumps({
            "query": query,
            "results": results,
            "count": len(results)
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "query": query,
            "message": "未找到相关知识",
            "available_topics": list(knowledge_base.keys())
        }, ensure_ascii=False)


# ============================================
# 工具注册表（供 Agent 使用）
# ============================================

TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "search_knowledge": search_knowledge,
}


# ============================================
# OpenAI Function Calling 格式的工具定义
# ============================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持基本运算（+、-、*、/）和常用函数（sqrt、sin、cos等）",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如：'2 + 3 * 4' 或 'sqrt(16)'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间信息，包括日期、时间、星期等",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，默认为 'Asia/Shanghai'",
                        "default": "Asia/Shanghai"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息（模拟数据）",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：'北京'、'上海'、'深圳'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "搜索 AI 和 Web3 相关的知识库",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询，例如：'什么是 LLM'、'RAG 的原理'"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def execute_tool(tool_name: str, tool_args: dict) -> str:
    """
    执行工具函数

    Args:
        tool_name: 工具名称
        tool_args: 工具参数

    Returns:
        工具执行结果（JSON 字符串）
    """
    if tool_name not in TOOLS:
        return json.dumps({"error": f"未知工具: {tool_name}"}, ensure_ascii=False)

    try:
        tool_func = TOOLS[tool_name]
        result = tool_func(**tool_args)
        return result
    except Exception as e:
        return json.dumps({"error": f"工具执行失败: {str(e)}"}, ensure_ascii=False)
