# DAO Research Agent - 架构详解

本文档详细拆解 DAO Research Agent 的架构设计，对照 AI × Web3 School Handbook 的标准实现。

## 📚 理论基础

### 什么是 AI Agent？

**AI Agent = LLM + Tools + Agentic Loop**

- **LLM (Large Language Model)**: 大语言模型，负责理解、推理、决策
- **Tools**: 工具函数，Agent 可以调用的外部能力
- **Agentic Loop**: 循环执行流程，直到完成任务

### Agent vs 简单的 LLM 调用

| 特性 | 简单 LLM 调用 | AI Agent |
|------|--------------|----------|
| **交互方式** | 单次问答 | 多轮对话 |
| **能力** | 只能生成文本 | 可以调用工具、执行操作 |
| **工作流程** | 一次性输出 | 循环执行直到完成 |
| **决策能力** | 无 | 可以自主决策调用哪些工具 |

### 为什么需要 Agent？

单纯的 LLM 只能基于训练数据生成文本，无法：
- ❌ 获取实时信息（如最新的提案内容）
- ❌ 执行计算（如分析投票结果）
- ❌ 与外部系统交互（如查询区块链数据）

通过 **Tool Use (Function Calling)**，Agent 可以：
- ✅ 调用 API 获取实时数据
- ✅ 执行复杂计算
- ✅ 与区块链、数据库等系统交互

---

## 🏗️ 架构设计

### 1. 整体架构

```
┌────────────────────────────────────────────────────────────────┐
│                    DAO Research Agent                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    System Prompt                          │ │
│  │  定义 Agent 的角色、能力、工作流程、输出要求              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    User Input                             │ │
│  │  "分析提案 #123"                                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    LLM (DeepSeek)                         │ │
│  │                                                            │ │
│  │  1. 理解用户意图                                           │ │
│  │  2. 规划执行步骤                                           │ │
│  │  3. 决策调用哪些工具                                       │ │
│  │  4. 综合分析结果                                           │ │
│  │  5. 生成最终报告                                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Tool Selection                         │ │
│  │  LLM 决定调用哪个工具                                      │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Tools (5 个工具)                        │ │
│  │                                                            │ │
│  │  1. read_proposal(proposal_id)                            │ │
│  │     - 读取提案的完整内容                                   │ │
│  │     - 返回：标题、描述、提议者、投票截止时间等             │ │
│  │                                                            │ │
│  │  2. search_forum(proposal_id, keywords)                   │ │
│  │     - 搜索论坛中关于该提案的讨论                           │ │
│  │     - 返回：讨论帖列表、评论内容                           │ │
│  │                                                            │ │
│  │  3. analyze_sentiment(discussions)                        │ │
│  │     - 分析讨论的情感倾向                                   │ │
│  │     - 返回：支持理由、反对理由、中立观点                   │ │
│  │                                                            │ │
│  │  4. check_risks(proposal)                                 │ │
│  │     - 检查提案的潜在风险                                   │ │
│  │     - 返回：治理风险、资金风险、技术风险                   │ │
│  │                                                            │ │
│  │  5. generate_checklist(analysis)                          │ │
│  │     - 生成投票前检查清单                                   │ │
│  │     - 返回：需要人工确认的事项列表                         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Tool Execution                         │ │
│  │  执行工具函数，获取结果                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Result Processing                      │ │
│  │  LLM 处理工具返回的结果                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Agentic Loop                           │ │
│  │  是否需要调用更多工具？                                    │ │
│  │  - 是 → 返回 Tool Selection                               │ │
│  │  - 否 → 生成最终输出                                       │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    Final Output                           │ │
│  │                                                            │ │
│  │  📊 提案分析报告                                           │ │
│  │  ├─ 提案概述                                               │ │
│  │  ├─ 支持理由（附来源）                                     │ │
│  │  ├─ 反对理由（附来源）                                     │ │
│  │  ├─ 风险评估                                               │ │
│  │  ├─ 缺失信息                                               │ │
│  │  └─ 投票前检查清单                                         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### 2. 核心组件详解

#### 2.1 System Prompt

System Prompt 是 Agent 的"大脑"，定义了：

```python
SYSTEM_PROMPT = """
你是一个 DAO 提案研究助手。你的任务是帮助 DAO 成员分析提案并做出明智的投票决策。

## 你的能力

你可以调用以下工具：
1. read_proposal - 读取提案内容
2. search_forum - 搜索论坛讨论
3. analyze_sentiment - 分析情感倾向
4. check_risks - 检查风险
5. generate_checklist - 生成检查清单

## 工作流程

当用户请求分析提案时，你必须按照以下步骤执行：

1. **读取提案正文**
   - 调用 read_proposal(proposal_id)
   - 理解提案的核心内容

2. **检索论坛讨论**
   - 调用 search_forum(proposal_id)
   - 收集社区的讨论内容

3. **分析支持和反对理由**
   - 调用 analyze_sentiment(discussions)
   - 总结正反方观点

4. **检查风险**
   - 调用 check_risks(proposal)
   - 识别治理、资金、技术风险

5. **生成检查清单**
   - 调用 generate_checklist(analysis)
   - 列出需要人工确认的事项

## 输出要求

你的最终报告必须包含：

1. **信息来源**
   - 明确列出所有使用的数据来源
   - 标注哪些信息来自提案、哪些来自论坛

2. **证据不足的结论**
   - 明确指出哪些结论缺乏充分证据
   - 说明需要补充哪些信息

3. **风险评估**
   - 是否发现治理风险（如权限过大、流程不当）
   - 是否发现资金风险（如预算过高、资金流向不明）

4. **人工检查事项**
   - 如果用户要投票，还需要人工检查什么
   - 哪些信息需要进一步验证

## 重要约束

❌ 你不能直接投票
❌ 你不能代替用户做决策
✅ 你只提供分析和建议
✅ 你必须保持中立和客观
"""
```

**关键点**：
- ✅ 明确定义角色和能力
- ✅ 详细说明工作流程（5 个步骤）
- ✅ 规定输出格式和要求
- ✅ 设置安全约束（不能投票）

#### 2.2 Tools (工具函数)

每个工具函数都有：
1. **函数签名** - 定义输入参数
2. **函数描述** - 告诉 LLM 这个工具的作用
3. **参数描述** - 说明每个参数的含义
4. **返回值** - 返回结构化数据

示例：

```python
def read_proposal(proposal_id: str) -> dict:
    """
    读取 DAO 提案的完整内容
    
    Args:
        proposal_id: 提案 ID（如 "123" 或 "#123"）
    
    Returns:
        {
            "id": "123",
            "title": "提案标题",
            "description": "提案描述",
            "proposer": "0x...",
            "status": "active",
            "voting_end": "2026-05-25",
            "votes_for": 1000,
            "votes_against": 500
        }
    """
    # 实现逻辑
    pass
```

**工具定义（给 LLM 的）**：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_proposal",
            "description": "读取 DAO 提案的完整内容，包括标题、描述、提议者、投票状态等",
            "parameters": {
                "type": "object",
                "properties": {
                    "proposal_id": {
                        "type": "string",
                        "description": "提案 ID，如 '123' 或 '#123'"
                    }
                },
                "required": ["proposal_id"]
            }
        }
    },
    # ... 其他工具
]
```

#### 2.3 Agentic Loop (循环执行)

这是 Agent 的核心机制：

```python
def run_agent(user_input: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    max_iterations = 10  # 防止无限循环
    
    for i in range(max_iterations):
        # 1. 调用 LLM
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto"  # 让 LLM 自己决定是否调用工具
        )
        
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        
        # 2. 检查是否需要调用工具
        if assistant_message.tool_calls:
            # 3. 执行工具调用
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # 调用对应的工具函数
                if function_name == "read_proposal":
                    result = read_proposal(**function_args)
                elif function_name == "search_forum":
                    result = search_forum(**function_args)
                # ... 其他工具
                
                # 4. 将工具结果返回给 LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
            
            # 5. 继续循环，让 LLM 处理工具结果
            continue
        
        # 6. 如果没有工具调用，说明任务完成
        return assistant_message.content
    
    return "达到最大迭代次数"
```

**关键点**：
- ✅ 多轮对话（messages 列表）
- ✅ 自动决策（tool_choice="auto"）
- ✅ 循环执行（直到不需要调用工具）
- ✅ 防止无限循环（max_iterations）

---

## 🔄 工作流程示例

### 用户输入
```
"分析提案 #123"
```

### 执行过程

**第 1 轮**：
- LLM 理解：用户想分析提案 #123
- LLM 决策：需要先读取提案内容
- LLM 输出：调用 `read_proposal("123")`

**第 2 轮**：
- 工具执行：返回提案内容
- LLM 理解：已获取提案内容
- LLM 决策：需要搜索论坛讨论
- LLM 输出：调用 `search_forum("123")`

**第 3 轮**：
- 工具执行：返回论坛讨论
- LLM 理解：已获取讨论内容
- LLM 决策：需要分析情感倾向
- LLM 输出：调用 `analyze_sentiment(discussions)`

**第 4 轮**：
- 工具执行：返回情感分析结果
- LLM 理解：已获取支持/反对理由
- LLM 决策：需要检查风险
- LLM 输出：调用 `check_risks(proposal)`

**第 5 轮**：
- 工具执行：返回风险评估
- LLM 理解：已完成所有分析
- LLM 决策：生成最终报告
- LLM 输出：结构化的分析报告（不调用工具）

**完成**：返回最终报告给用户

---

## 📊 与 Web3 AI Assistant 的对比

### Web3 AI Assistant（之前的实现）

```python
# 简单的工具调用
def main():
    user_input = input("你: ")
    
    # 直接调用 LLM，一次性完成
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是智能合约助手"},
            {"role": "user", "content": user_input}
        ],
        tools=tools
    )
    
    # 执行工具调用（只执行一次）
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        result = execute_tool(tool_call)
        print(result)
```

**特点**：
- ❌ 单次工具调用
- ❌ 没有循环执行
- ❌ 无法处理多步骤任务
- ✅ 简单直接

### DAO Research Agent（标准实现）

```python
# Agentic Loop
def run_agent(user_input):
    messages = [...]
    
    for i in range(max_iterations):
        response = client.chat.completions.create(...)
        
        if response.tool_calls:
            # 执行所有工具调用
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call)
                messages.append(result)
            continue  # 继续循环
        
        return response.content  # 完成
```

**特点**：
- ✅ 多轮工具调用
- ✅ 循环执行直到完成
- ✅ 可以处理复杂的多步骤任务
- ✅ LLM 自主决策执行流程

---

## 🎯 关键设计原则

### 1. 只读优先

Agent 只执行只读操作，不直接修改状态：
- ✅ 读取提案
- ✅ 搜索讨论
- ✅ 分析数据
- ❌ 不投票
- ❌ 不转账
- ❌ 不修改合约

### 2. 透明性

输出必须明确：
- ✅ 数据来源
- ✅ 证据充分性
- ✅ 风险评估
- ✅ 需要人工确认的事项

### 3. 可验证性

所有结论都可以追溯：
- ✅ 引用具体的论坛帖子
- ✅ 标注提案的具体条款
- ✅ 说明分析的逻辑

### 4. 安全性

多层安全保障：
- ✅ System Prompt 约束（不能投票）
- ✅ 工具函数限制（只读 API）
- ✅ 输出检查清单（提醒人工确认）

---

## 🚀 下一步：权限升级版本

完成只读版本后，可以实现权限升级版本：

### 新增功能

1. **投票模拟**
   ```python
   def simulate_vote(proposal_id: str, vote: str) -> dict:
       """模拟投票交易，不实际执行"""
       pass
   ```

2. **生成投票交易**
   ```python
   def generate_vote_tx(proposal_id: str, vote: str) -> dict:
       """生成投票交易草稿"""
       pass
   ```

3. **用户确认**
   ```python
   def request_user_approval(tx_data: dict) -> bool:
       """请求用户确认交易"""
       pass
   ```

### 工作流程

```
分析提案 → 生成建议 → 用户决定投票 → 模拟交易 → 用户确认 → 执行投票
```

### 安全要求

- ✅ 必须经过模拟验证
- ✅ 必须用户明确授权
- ✅ 显示交易详情（Gas、影响等）
- ✅ 支持取消操作

---

## 📚 总结

### 标准 Agent 架构的核心

1. **System Prompt** - 定义角色和工作流程
2. **Tools** - 提供外部能力
3. **Agentic Loop** - 循环执行直到完成
4. **安全约束** - 只读优先、透明性、可验证性

### 与简单工具调用的区别

| 特性 | 简单工具调用 | Agent |
|------|-------------|-------|
| 执行次数 | 1 次 | 多次（循环） |
| 决策能力 | 无 | 自主决策 |
| 任务复杂度 | 简单 | 复杂多步骤 |
| 适用场景 | 单一操作 | 研究、分析、规划 |

### 学习路径

1. ✅ Day 1: Prompt Engineering - 学习如何与 LLM 交互
2. ✅ Day 2: RAG + 简单 Agent - 理解工具调用
3. ✅ Day 3: Web3 AI Assistant - 实现专业工具
4. 🔄 Day 3+: DAO Research Agent - 掌握标准 Agent 架构

下一步：实现完整的 DAO Research Agent！
