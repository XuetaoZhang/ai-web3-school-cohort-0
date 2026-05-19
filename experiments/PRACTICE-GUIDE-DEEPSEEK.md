# AI 基础动手实践方案 - DeepSeek 版本

**日期**: 2026-05-19  
**目标**: 使用 DeepSeek API 完成 RAG 和 Agent 实践（适合国内用户）

---

## 📋 为什么选择 DeepSeek？

- ✅ **国内可用**: 无需代理，访问稳定
- ✅ **性能优秀**: DeepSeek V3 性能接近 GPT-4
- ✅ **价格友好**: 比国际 API 更便宜
- ✅ **完整支持**: 支持 Chat、Function Calling（Tool Use）
- ✅ **兼容 OpenAI**: API 格式兼容，易于迁移

---

## 🔑 准备工作

### 1. 获取 DeepSeek API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册账号并登录
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制并保存（只显示一次）

### 2. 设置环境变量

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export DEEPSEEK_API_KEY="your_api_key_here"

# 立即生效
source ~/.bashrc  # 或 source ~/.zshrc
```

---

## 🎯 实践 2: 构建 RAG 系统（DeepSeek 版本）

### Step 1: 创建项目目录

```bash
cd ~/ai-web3-school-cohort-0/experiments
mkdir rag-system-deepseek
cd rag-system-deepseek
```

### Step 2: 安装依赖

创建 `requirements.txt`:
```txt
openai
chromadb
sentence-transformers
```

安装：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: 准备知识库

创建 `knowledge_base.py`:

```python
"""
简单的知识库：AI × Web3 School Handbook 摘要
"""

HANDBOOK_DOCS = [
    {
        "id": "llm-1",
        "title": "什么是大语言模型",
        "content": """
        大语言模型（LLM）是基于 Transformer 架构的深度学习模型，
        通过在海量文本数据上训练，学习语言的模式和知识。
        LLM 的核心能力包括：文本生成、理解、翻译、总结等。
        常见的 LLM 包括：GPT-4、Claude、DeepSeek、Llama 等。
        """
    },
    {
        "id": "prompt-1",
        "title": "Prompt Engineering 基础",
        "content": """
        Prompt Engineering 是设计有效提示词的技术。
        关键技巧包括：
        1. 清晰的指令
        2. 提供上下文
        3. Few-shot 示例
        4. 输出格式约束
        5. 角色设定
        """
    },
    {
        "id": "agent-1",
        "title": "AI Agent 基础",
        "content": """
        AI Agent 是能够感知环境、做出决策并执行行动的智能系统。
        Agent 的核心组件：
        1. LLM（推理引擎）
        2. Tools（工具集）
        3. Memory（记忆系统）
        4. Planning（规划能力）
        """
    },
    {
        "id": "rag-1",
        "title": "检索增强生成（RAG）",
        "content": """
        RAG 通过检索外部知识来增强 LLM 的回答能力。
        工作流程：
        1. 用户提问
        2. 检索相关文档
        3. 将文档作为上下文提供给 LLM
        4. LLM 基于上下文生成回答
        """
    },
    {
        "id": "web3-agent-1",
        "title": "Web3 Agent 钱包",
        "content": """
        Web3 Agent 需要钱包来执行链上操作。
        关键考虑：
        1. 权限管理（Session Key）
        2. 额度限制
        3. 时间限制
        4. 操作白名单
        5. 多签验证
        """
    }
]
```

### Step 4: 构建向量数据库

创建 `vector_store.py`:

```python
import chromadb
from chromadb.utils import embedding_functions

class SimpleVectorStore:
    def __init__(self):
        # 初始化 ChromaDB
        self.client = chromadb.Client()
        
        # 使用默认的 embedding 函数
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name="handbook",
            embedding_function=self.embedding_fn
        )
    
    def add_documents(self, documents):
        """添加文档到向量数据库"""
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [{"title": doc["title"]} for doc in documents]
        
        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )
        print(f"✅ 已添加 {len(documents)} 个文档到向量数据库")
    
    def search(self, query, n_results=2):
        """检索相关文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results

# 测试代码
if __name__ == "__main__":
    from knowledge_base import HANDBOOK_DOCS
    
    # 创建向量存储
    store = SimpleVectorStore()
    
    # 添加文档
    store.add_documents(HANDBOOK_DOCS)
    
    # 测试检索
    query = "什么是 AI Agent？"
    results = store.search(query)
    
    print(f"\n🔍 查询: {query}")
    print(f"\n📄 检索到的文档:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\n--- 文档 {i+1} ---")
        print(doc)
```

运行测试：
```bash
python vector_store.py
```

### Step 5: 集成 DeepSeek API

创建 `rag_system.py`:

```python
import os
from openai import OpenAI
from vector_store import SimpleVectorStore
from knowledge_base import HANDBOOK_DOCS

class SimpleRAG:
    def __init__(self, api_key=None):
        # 初始化 DeepSeek 客户端（使用 OpenAI 兼容接口）
        self.client = OpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        
        # 初始化向量存储
        self.vector_store = SimpleVectorStore()
        self.vector_store.add_documents(HANDBOOK_DOCS)
    
    def query(self, question):
        """RAG 查询流程"""
        print(f"\n🤔 问题: {question}")
        
        # 1. 检索相关文档
        print("\n🔍 检索相关文档...")
        results = self.vector_store.search(question, n_results=2)
        
        # 2. 构建上下文
        context = "\n\n".join(results['documents'][0])
        print(f"\n📚 找到 {len(results['documents'][0])} 个相关文档")
        
        # 3. 构建 Prompt
        prompt = f"""基于以下参考资料回答问题。如果参考资料中没有相关信息，请说明。

参考资料：
{context}

问题：{question}

请用中文回答，并引用参考资料中的关键信息。"""
        
        # 4. 调用 DeepSeek
        print("\n🤖 DeepSeek 正在思考...")
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的 AI 助手，擅长基于参考资料回答问题。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        # 5. 返回结果
        print(f"\n💡 回答:\n{answer}")
        
        return {
            "question": question,
            "context": context,
            "answer": answer
        }

# 测试代码
if __name__ == "__main__":
    # 确保设置了 DEEPSEEK_API_KEY 环境变量
    # export DEEPSEEK_API_KEY=your_api_key
    
    rag = SimpleRAG()
    
    # 测试问题
    questions = [
        "什么是 AI Agent？它有哪些核心组件？",
        "RAG 的工作流程是什么？",
        "Web3 Agent 钱包需要考虑哪些安全问题？"
    ]
    
    for q in questions:
        rag.query(q)
        print("\n" + "="*80 + "\n")
```

### Step 6: 运行和测试

1. **设置 API Key**:
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

2. **运行 RAG 系统**:
```bash
python rag_system.py
```

3. **测试不同问题**:
- 修改 `questions` 列表
- 观察检索结果和回答质量
- 尝试添加更多文档到 `knowledge_base.py`

---

## 🎯 实践 3: 创建 AI Agent（DeepSeek 版本）

### Step 1: 创建项目

```bash
cd ~/ai-web3-school-cohort-0/experiments
mkdir simple-agent-deepseek
cd simple-agent-deepseek
```

创建 `requirements.txt`:
```txt
openai
requests
```

安装：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: 定义工具

创建 `tools.py`:

```python
import requests
from typing import Dict, Any

def get_eth_price() -> Dict[str, Any]:
    """
    获取以太坊当前价格
    
    Returns:
        包含价格信息的字典
    """
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": "ethereum",
                "vs_currencies": "usd"
            }
        )
        data = response.json()
        price = data["ethereum"]["usd"]
        
        return {
            "success": True,
            "price": price,
            "currency": "USD"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_gas_price() -> Dict[str, Any]:
    """
    获取以太坊当前 Gas 价格（模拟）
    
    Returns:
        包含 Gas 价格信息的字典
    """
    # 实际应该调用 Etherscan API 或 RPC 节点
    # 这里用模拟数据
    return {
        "success": True,
        "slow": 20,
        "standard": 25,
        "fast": 30,
        "unit": "gwei"
    }

def calculate_transaction_cost(gas_limit: int, gas_price: int) -> Dict[str, Any]:
    """
    计算交易成本
    
    Args:
        gas_limit: Gas 限制
        gas_price: Gas 价格（gwei）
    
    Returns:
        包含成本信息的字典
    """
    try:
        # 计算成本（ETH）
        cost_eth = (gas_limit * gas_price) / 1e9
        
        return {
            "success": True,
            "gas_limit": gas_limit,
            "gas_price": gas_price,
            "cost_eth": cost_eth,
            "cost_usd": None  # 需要 ETH 价格才能计算
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 工具定义（OpenAI Function Calling 格式）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_eth_price",
            "description": "获取以太坊当前的 USD 价格",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_gas_price",
            "description": "获取以太坊当前的 Gas 价格（slow, standard, fast）",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_transaction_cost",
            "description": "计算以太坊交易的成本",
            "parameters": {
                "type": "object",
                "properties": {
                    "gas_limit": {
                        "type": "integer",
                        "description": "交易的 Gas 限制"
                    },
                    "gas_price": {
                        "type": "integer",
                        "description": "Gas 价格（单位：gwei）"
                    }
                },
                "required": ["gas_limit", "gas_price"]
            }
        }
    }
]

# 工具执行函数映射
TOOL_FUNCTIONS = {
    "get_eth_price": get_eth_price,
    "get_gas_price": get_gas_price,
    "calculate_transaction_cost": calculate_transaction_cost
}
```

### Step 3: 创建 Agent

创建 `agent.py`:

```python
import os
import json
from openai import OpenAI
from tools import TOOLS, TOOL_FUNCTIONS

class SimpleAgent:
    def __init__(self, api_key=None):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.tools = TOOLS
        self.conversation_history = []
    
    def execute_tool(self, tool_name: str, tool_input: dict):
        """执行工具调用"""
        print(f"\n🔧 执行工具: {tool_name}")
        print(f"📥 输入: {json.dumps(tool_input, indent=2, ensure_ascii=False)}")
        
        # 获取工具函数
        tool_fn = TOOL_FUNCTIONS.get(tool_name)
        if not tool_fn:
            return {"error": f"Unknown tool: {tool_name}"}
        
        # 执行工具
        result = tool_fn(**tool_input)
        print(f"📤 输出: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        return result
    
    def run(self, user_message: str, max_iterations=5):
        """运行 Agent"""
        print(f"\n👤 用户: {user_message}\n")
        
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # 调用 DeepSeek
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.conversation_history,
                tools=self.tools,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message
            print(f"\n🤖 DeepSeek 响应类型: {response.choices[0].finish_reason}")
            
            # 检查是否需要调用工具
            if assistant_message.tool_calls:
                # 添加 Assistant 响应到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # 执行所有工具调用
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)
                    
                    tool_result = self.execute_tool(tool_name, tool_input)
                    
                    # 添加工具结果到历史
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result, ensure_ascii=False)
                    })
                
            else:
                # Agent 完成任务
                final_response = assistant_message.content
                print(f"\n💡 Agent 最终回答:\n{final_response}")
                
                return final_response
        
        print(f"\n⚠️ 达到最大迭代次数 ({max_iterations})")
        return None

# 测试代码
if __name__ == "__main__":
    agent = SimpleAgent()
    
    # 测试问题
    questions = [
        "以太坊现在的价格是多少？",
        "当前的 Gas 价格是多少？推荐使用哪个档位？",
        "如果我要发送一笔 21000 gas limit 的交易，使用 standard gas price，需要多少 ETH？折合多少美元？"
    ]
    
    for q in questions:
        print("\n" + "="*80)
        agent.run(q)
        print("="*80 + "\n")
        
        # 重置对话历史
        agent.conversation_history = []
```

### Step 4: 运行和测试

1. **设置 API Key**:
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

2. **运行 Agent**:
```bash
python agent.py
```

3. **观察 Agent 行为**:
- Agent 如何选择工具
- 工具调用的顺序
- 如何组合多个工具的结果

---

## 📊 DeepSeek vs Claude 对比

| 特性 | DeepSeek | Claude |
|------|----------|--------|
| **国内访问** | ✅ 直接访问 | ❌ 需要代理 |
| **API 格式** | OpenAI 兼容 | Anthropic 格式 |
| **Tool Use** | Function Calling | Tool Use |
| **模型** | deepseek-chat | claude-sonnet-4 |
| **价格** | 更便宜 | 较贵 |
| **性能** | 优秀 | 优秀 |

---

## 🔄 从 Claude 迁移到 DeepSeek

### 主要差异

1. **客户端初始化**:
```python
# Claude
from anthropic import Anthropic
client = Anthropic(api_key=api_key)

# DeepSeek
from openai import OpenAI
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
```

2. **Chat API 调用**:
```python
# Claude
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
answer = response.content[0].text

# DeepSeek
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=1024
)
answer = response.choices[0].message.content
```

3. **Tool Use 格式**:
```python
# Claude Tool Schema
{
    "name": "get_eth_price",
    "description": "获取以太坊价格",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

# DeepSeek Function Schema
{
    "type": "function",
    "function": {
        "name": "get_eth_price",
        "description": "获取以太坊价格",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
```

---

## 💡 实践建议

### 1. API Key 安全

```bash
# 不要在代码中硬编码 API Key
# ❌ 错误
api_key = "sk-xxxxx"

# ✅ 正确
api_key = os.environ.get("DEEPSEEK_API_KEY")
```

### 2. 错误处理

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"API 调用失败: {e}")
```

### 3. 成本控制

```python
# 设置 max_tokens 限制输出长度
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    max_tokens=1024  # 限制输出
)
```

---

## 🎯 下一步

完成 DeepSeek 版本的实践后：

1. ✅ 对比 DeepSeek 和 Claude 的输出质量
2. ✅ 记录两者的差异和优劣
3. ✅ 更新学习笔记
4. ✅ 提交代码到 GitHub

---

## 📚 参考资源

- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

---

**准备好开始了吗？从 RAG 系统开始吧！** 🚀

有任何问题随时问我！
