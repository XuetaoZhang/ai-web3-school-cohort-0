# AI 基础动手实践方案

**日期**: 2026-05-18  
**目标**: 通过三个递进式实践，掌握 Prompt Engineering、RAG 和 Agent 的核心概念

---

## 📋 实践概览

| 实践 | 难度 | 时间 | 核心技能 |
|------|------|------|----------|
| 1. Prompt Engineering 基础 | ⭐ | 30-45分钟 | 提示词设计、Few-shot Learning |
| 2. 构建简单 RAG 系统 | ⭐⭐ | 45-60分钟 | 向量检索、上下文增强 |
| 3. 创建第一个 AI Agent | ⭐⭐⭐ | 60-90分钟 | Tool Use、Agent 工作流 |

---

## 🎯 实践 1: Prompt Engineering 基础实践

### 目标
掌握编写有效 Prompt 的技巧，理解如何引导 LLM 生成期望的输出。

### 准备工作
- 使用 Claude.ai 或 ChatGPT（你已经有账号）
- 准备一个文本编辑器记录实验结果

### 实践步骤

#### Step 1: 基础 Prompt 对比（15分钟）

**任务**: 对比不同 Prompt 的效果

**实验 1.1: 模糊 vs 清晰**

❌ **模糊 Prompt**:
```
写一个智能合约
```

✅ **清晰 Prompt**:
```
请用 Solidity 编写一个 ERC20 代币合约，要求：
1. 代币名称：MyToken
2. 代币符号：MTK
3. 总供应量：1,000,000
4. 包含 mint 和 burn 功能
5. 添加详细的注释说明每个函数的作用
```

**观察**: 记录两个 Prompt 的输出差异

**实验 1.2: 无示例 vs Few-shot**

❌ **Zero-shot**:
```
将这个交易哈希分类：0x1234...
```

✅ **Few-shot**:
```
请根据以下示例，对交易进行分类：

示例 1:
交易: 0xabc...def (调用 transfer 函数)
分类: Token Transfer

示例 2:
交易: 0x123...456 (调用 swap 函数)
分类: DEX Swap

示例 3:
交易: 0x789...012 (调用 mint 函数)
分类: NFT Mint

现在请分类这个交易：
交易: 0x345...678 (调用 addLiquidity 函数)
分类: ?
```

**观察**: Few-shot 是否提高了准确性？

#### Step 2: 角色设定与上下文（15分钟）

**实验 2.1: 添加角色**

```
你是一位资深的 Solidity 安全审计专家，拥有 5 年以上的智能合约审计经验。

请审查以下合约代码，找出潜在的安全漏洞：

[粘贴一段简单的合约代码]

请按以下格式输出：
1. 漏洞类型
2. 严重程度（高/中/低）
3. 具体位置
4. 修复建议
```

**实验 2.2: 添加约束条件**

```
请用 Python 编写一个函数，从以太坊节点获取最新区块信息。

要求：
- 使用 web3.py 库
- 包含错误处理
- 添加类型注解
- 代码不超过 30 行
- 包含使用示例
```

#### Step 3: 输出格式控制（15分钟）

**实验 3.1: 结构化输出**

```
分析以下 DeFi 协议的风险，并以 JSON 格式输出：

协议：Uniswap V3

输出格式：
{
  "protocol": "协议名称",
  "risks": [
    {
      "category": "风险类别",
      "severity": "严重程度",
      "description": "风险描述",
      "mitigation": "缓解措施"
    }
  ],
  "overall_score": "1-10分"
}
```

**实验 3.2: Markdown 表格输出**

```
比较以下三个 Layer 2 方案，以 Markdown 表格形式输出：

方案：Optimism, Arbitrum, zkSync

对比维度：
- TPS（每秒交易数）
- 最终确认时间
- 安全模型
- Gas 费用
- 生态系统规模

输出格式：Markdown 表格
```

### 实践产出

在 `~/ai-web3-school-cohort-0/experiments/` 创建文件：
```bash
prompt-engineering-practice.md
```

记录：
1. 每个实验的 Prompt
2. LLM 的输出
3. 你的观察和总结
4. 哪些技巧最有效

---

## 🎯 实践 2: 构建简单的 RAG 系统

### 目标
理解如何为 LLM 提供外部知识，构建一个能回答 Handbook 问题的 RAG 系统。

### 准备工作

#### Step 1: 创建项目目录（5分钟）

```bash
cd ~/ai-web3-school-cohort-0/experiments
mkdir rag-system
cd rag-system
```

#### Step 2: 安装依赖（5分钟）

创建 `requirements.txt`:
```txt
anthropic
chromadb
sentence-transformers
```

安装：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 实践步骤

#### Step 3: 准备知识库（10分钟）

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
        常见的 LLM 包括：GPT-4、Claude、Llama 等。
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

#### Step 4: 构建向量数据库（15分钟）

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

#### Step 5: 集成 Claude API（20分钟）

创建 `rag_system.py`:

```python
import os
from anthropic import Anthropic
from vector_store import SimpleVectorStore
from knowledge_base import HANDBOOK_DOCS

class SimpleRAG:
    def __init__(self, api_key=None):
        # 初始化 Claude
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        
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
        
        # 4. 调用 Claude
        print("\n🤖 Claude 正在思考...")
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        answer = message.content[0].text
        
        # 5. 返回结果
        print(f"\n💡 回答:\n{answer}")
        
        return {
            "question": question,
            "context": context,
            "answer": answer
        }

# 测试代码
if __name__ == "__main__":
    # 确保设置了 ANTHROPIC_API_KEY 环境变量
    # export ANTHROPIC_API_KEY=your_api_key
    
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

#### Step 6: 运行和测试（10分钟）

1. **设置 API Key**:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

2. **运行 RAG 系统**:
```bash
python rag_system.py
```

3. **测试不同问题**:
- 修改 `questions` 列表
- 观察检索结果和回答质量
- 尝试添加更多文档到 `knowledge_base.py`

### 实践产出

创建实验报告：`~/ai-web3-school-cohort-0/experiments/rag-system/README.md`

记录：
1. RAG 系统架构图
2. 检索效果分析
3. 遇到的问题和解决方案
4. 改进思路

---

## 🎯 实践 3: 创建第一个 AI Agent

### 目标
使用 Claude SDK 创建一个能调用工具的 Agent，理解 Tool Use 和 Agent 工作流。

### 准备工作

#### Step 1: 创建项目（5分钟）

```bash
cd ~/ai-web3-school-cohort-0/experiments
mkdir simple-agent
cd simple-agent
```

创建 `requirements.txt`:
```txt
anthropic
requests
```

安装：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 实践步骤

#### Step 2: 定义工具（15分钟）

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

# 工具定义（Claude Tool Use 格式）
TOOLS = [
    {
        "name": "get_eth_price",
        "description": "获取以太坊当前的 USD 价格",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_gas_price",
        "description": "获取以太坊当前的 Gas 价格（slow, standard, fast）",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "calculate_transaction_cost",
        "description": "计算以太坊交易的成本",
        "input_schema": {
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
]

# 工具执行函数映射
TOOL_FUNCTIONS = {
    "get_eth_price": get_eth_price,
    "get_gas_price": get_gas_price,
    "calculate_transaction_cost": calculate_transaction_cost
}
```

#### Step 3: 创建 Agent（30分钟）

创建 `agent.py`:

```python
import os
import json
from anthropic import Anthropic
from tools import TOOLS, TOOL_FUNCTIONS

class SimpleAgent:
    def __init__(self, api_key=None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
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
            
            # 调用 Claude
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=self.tools,
                messages=self.conversation_history
            )
            
            print(f"\n🤖 Claude 响应类型: {response.stop_reason}")
            
            # 检查是否需要调用工具
            if response.stop_reason == "tool_use":
                # 添加 Assistant 响应到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # 执行所有工具调用
                tool_results = []
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_result = self.execute_tool(
                            content_block.name,
                            content_block.input
                        )
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": json.dumps(tool_result)
                        })
                
                # 添加工具结果到历史
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                
            elif response.stop_reason == "end_turn":
                # Agent 完成任务
                final_response = ""
                for content_block in response.content:
                    if hasattr(content_block, "text"):
                        final_response += content_block.text
                
                print(f"\n💡 Agent 最终回答:\n{final_response}")
                
                return final_response
            
            else:
                print(f"\n⚠️ 未预期的停止原因: {response.stop_reason}")
                break
        
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

#### Step 4: 运行和测试（15分钟）

1. **设置 API Key**:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

2. **运行 Agent**:
```bash
python agent.py
```

3. **观察 Agent 行为**:
- Agent 如何选择工具
- 工具调用的顺序
- 如何组合多个工具的结果

#### Step 5: 扩展 Agent（15分钟）

**挑战任务**: 添加新工具

在 `tools.py` 中添加：

```python
def get_token_info(token_address: str) -> Dict[str, Any]:
    """
    获取 ERC20 代币信息（模拟）
    
    Args:
        token_address: 代币合约地址
    
    Returns:
        包含代币信息的字典
    """
    # 模拟数据
    mock_tokens = {
        "0x6b175474e89094c44da98b954eedeac495271d0f": {
            "name": "Dai Stablecoin",
            "symbol": "DAI",
            "decimals": 18,
            "total_supply": "5000000000"
        },
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {
            "name": "USD Coin",
            "symbol": "USDC",
            "decimals": 6,
            "total_supply": "30000000000"
        }
    }
    
    token_info = mock_tokens.get(token_address.lower())
    
    if token_info:
        return {
            "success": True,
            **token_info
        }
    else:
        return {
            "success": False,
            "error": "Token not found"
        }
```

更新 `TOOLS` 和 `TOOL_FUNCTIONS`，然后测试新问题：
```
"DAI 代币的合约地址是 0x6b175474e89094c44da98b954eedeac495271d0f，请告诉我它的详细信息"
```

### 实践产出

创建实验报告：`~/ai-web3-school-cohort-0/experiments/simple-agent/README.md`

记录：
1. Agent 架构图
2. Tool Use 工作流程
3. 不同问题的执行轨迹
4. 改进思路（如何添加更多工具）

---

## 📊 实践总结

完成所有实践后，创建总结文档：

`~/ai-web3-school-cohort-0/experiments/practice-summary.md`

### 总结内容

1. **关键学习**
   - Prompt Engineering 的核心技巧
   - RAG 如何增强 LLM 能力
   - Agent 的工作原理

2. **遇到的挑战**
   - 技术问题
   - 概念理解
   - 如何解决

3. **下一步计划**
   - 想深入的方向
   - 想构建的项目
   - 需要补充的知识

---

## 🎯 提交你的实践成果

完成后，提交到 GitHub：

```bash
cd ~/ai-web3-school-cohort-0
git add experiments/
git add daily/2026-05-18.md
git commit -m "Complete Day 1 hands-on practice: Prompt Engineering, RAG, and Agent"
git push
```

---

## 💡 额外挑战（可选）

如果你还有时间和精力：

1. **组合实践**: 创建一个带 RAG 能力的 Agent
2. **Web3 集成**: 让 Agent 能查询真实的链上数据
3. **UI 界面**: 用 Streamlit 为你的 Agent 创建简单界面

---

**准备好开始动手实践了吗？从实践 1 开始，逐步完成！** 🚀

有任何问题随时问我！
