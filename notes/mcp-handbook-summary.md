# MCP (Model Context Protocol) 章节核心内容

## 什么是 MCP？

MCP (Model Context Protocol) 是 Anthropic 推出的开放协议，用于连接 AI 应用与外部数据源和工具。

**核心问题**：AI Agent 如何安全、标准化地访问外部资源？

**MCP 的解决方案**：
- **标准化协议**：统一的接口规范
- **安全隔离**：明确的权限边界
- **可扩展性**：支持任意工具和数据源

## MCP 的核心概念

### 1. MCP Server
- **定义**：提供工具和数据源的服务端
- **职责**：
  - 暴露工具（Tools）
  - 提供数据源（Resources）
  - 管理权限（Permissions）
- **示例**：
  - 文件系统 MCP Server（读写文件）
  - 数据库 MCP Server（查询数据）
  - Web3 MCP Server（链上查询、交易签名）

### 2. MCP Client
- **定义**：使用 MCP Server 的客户端（通常是 AI 应用）
- **职责**：
  - 发现可用工具
  - 调用工具
  - 处理响应
- **示例**：
  - Claude Desktop（内置 MCP Client）
  - 自定义 AI Agent

### 3. Tools（工具）
- **定义**：MCP Server 暴露的函数
- **特点**：
  - 有明确的输入输出
  - 有描述（让 LLM 理解如何使用）
  - 有权限控制
- **示例**：
  - `read_file(path)` - 读取文件
  - `query_balance(address)` - 查询余额
  - `simulate_transaction(tx)` - 模拟交易

### 4. Resources（资源）
- **定义**：MCP Server 提供的数据源
- **特点**：
  - 可以是静态数据（文件、数据库）
  - 可以是动态数据（API、链上数据）
  - 支持订阅（实时更新）
- **示例**：
  - 文件系统（`file://path/to/file`）
  - 数据库（`db://table/row`）
  - 链上数据（`chain://ethereum/address/balance`）

### 5. Prompts（提示词模板）
- **定义**：MCP Server 提供的预定义 Prompt
- **用途**：
  - 标准化常见任务
  - 提供最佳实践
  - 简化用户输入
- **示例**：
  - "分析这个合约的安全风险"
  - "总结这个地址的交易历史"

## MCP 的架构

```
┌─────────────────┐
│   AI Agent      │
│  (MCP Client)   │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────┴────────┐
│   MCP Server    │
│  ┌───────────┐  │
│  │  Tools    │  │
│  ├───────────┤  │
│  │ Resources │  │
│  ├───────────┤  │
│  │  Prompts  │  │
│  └───────────┘  │
└─────────────────┘
         │
         │
┌────────┴────────┐
│  External Data  │
│  (File, DB,     │
│   Blockchain)   │
└─────────────────┘
```

## MCP 的价值

### 优势
1. **标准化**：统一的接口，不用为每个工具写适配器
2. **安全性**：明确的权限边界，防止 Agent 滥用工具
3. **可组合性**：多个 MCP Server 可以组合使用
4. **可维护性**：工具和 Agent 解耦，独立演进

### 劣势
1. **学习成本**：需要理解 MCP 协议
2. **额外抽象**：简单场景可能不需要 MCP
3. **生态依赖**：需要等待 MCP Server 生态成熟

## MCP vs 传统 Tool Calling

### 传统 Tool Calling
```python
# Agent 直接调用工具
def get_balance(address):
    return web3.eth.get_balance(address)

tools = [
    {
        "name": "get_balance",
        "description": "Get ETH balance",
        "parameters": {...}
    }
]
```

**问题**：
- 工具和 Agent 耦合
- 没有权限控制
- 难以复用

### MCP Tool Calling
```python
# MCP Server 暴露工具
class Web3MCPServer:
    @tool
    def get_balance(self, address: str) -> float:
        """Get ETH balance of an address"""
        return web3.eth.get_balance(address)

# Agent 通过 MCP 调用
mcp_client.call_tool("get_balance", {"address": "0x..."})
```

**优势**：
- 工具和 Agent 解耦
- 统一的权限管理
- 可以跨 Agent 复用

## Web3 场景的 MCP 应用

### 1. Web3 MCP Server 设计

**核心工具**：
- `query_balance(address, token)` - 查询余额
- `query_allowance(owner, spender, token)` - 查询授权额度
- `simulate_transaction(tx)` - 模拟交易
- `get_contract_info(address)` - 获取合约信息
- `query_transaction_history(address, limit)` - 查询交易历史

**核心资源**：
- `chain://ethereum/address/{address}/balance` - 余额
- `chain://ethereum/contract/{address}/abi` - 合约 ABI
- `chain://ethereum/tx/{hash}` - 交易详情

**权限控制**：
- 只读权限：查询余额、合约信息
- 模拟权限：模拟交易（不上链）
- 签名权限：签名交易（需要用户确认）

### 2. 安全考虑

**问题 1：Agent 滥用工具**
- 解决：MCP Server 实现 Rate Limiting
- 解决：MCP Server 记录所有调用日志

**问题 2：敏感操作**
- 解决：签名交易需要 Human-in-the-loop
- 解决：MCP Server 实现权限分级（只读 vs 签名）

**问题 3：数据可信度**
- 解决：MCP Server 标注数据来源（链上 vs 第三方 API）
- 解决：结合 Day 4 的 Context 分层设计

### 3. 实时性挑战

**问题**：链上数据变化快，如何保证实时性？

**解决方案**：
- **订阅机制**：MCP Resources 支持订阅（WebSocket）
- **缓存策略**：
  - 实时查询：余额、授权状态
  - 短期缓存（1 分钟）：合约信息
  - 长期缓存（1 小时）：历史交易
- **主动推送**：链上事件触发 MCP Server 推送更新

## 何时使用 MCP？

### 适合使用
- 需要访问多种外部数据源
- 需要跨 Agent 复用工具
- 需要严格的权限控制
- 团队协作开发（工具和 Agent 分离）

### 不适合使用
- 简单的单次 API 调用
- 原型验证阶段
- 工具只用一次（不需要复用）
- 性能要求极高（MCP 有额外开销）

## 最小实践建议

1. **先手写工具**：不要直接用 MCP，先手写一遍
2. **按需引入**：只有需要复用时才用 MCP
3. **关注权限**：明确定义每个工具的权限边界
4. **标注来源**：数据来源要清晰（链上 vs 第三方）

## MCP 与 Frameworks 的关系

- **LangChain Tools** ≈ **MCP Tools**（都是工具抽象）
- **LangChain** 是应用框架，**MCP** 是协议标准
- **可以结合使用**：LangChain Agent + MCP Server

**示例**：
```python
# LangChain Agent 使用 MCP Tools
from langchain.agents import initialize_agent
from mcp_client import MCPClient

mcp_client = MCPClient("web3-mcp-server")
tools = mcp_client.get_tools()  # 获取 MCP Tools

agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
agent.run("查询 0x... 的 ETH 余额")
```

---

## 思考题

1. 你之前做的 Web3 Agent，如果用 MCP 重构，会有什么不同？
2. MCP 的权限控制如何设计？（只读 vs 模拟 vs 签名）
3. MCP 如何保证链上数据的实时性？
4. MCP 与 Day 4 的 Context 分层如何结合？
