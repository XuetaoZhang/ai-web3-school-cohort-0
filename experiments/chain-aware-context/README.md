# Chain-aware Context 实践

## 🎯 实践目标

给一笔 Uniswap 交易做上下文包，验证 Chain-aware Context 的设计。

## 📋 选择的交易

**真实的 Uniswap V3 Swap 交易示例**：

你可以选择以下任一交易进行分析：

### 选项 1：简单的 USDC → WETH Swap
- 去 https://etherscan.io/
- 搜索 Uniswap V3: SwapRouter 合约地址：`0xE592427A0AEce92De3Edee1F18E0157C05861564`
- 点击 "Transactions" 标签
- 选择最近的一笔 `exactInputSingle` 或 `exactInput` 交易

### 选项 2：使用我提供的示例交易
如果你想快速开始，可以分析这笔交易：
- **交易哈希**: `0xa40162ed6da4c2fdc7645f381600a185c0ed7efe45e98ffae54449148ff01f81`
- **说明**: 这是一笔历史 Uniswap 交易（示例）
- **Etherscan**: https://etherscan.io/tx/0xa40162ed6da4c2fdc7645f381600a185c0ed7efe45e98ffae54449148ff01f81

---

## 🚀 开始实践

### 阶段 1：手动收集数据（1 小时）

**步骤 1：选择交易**
1. 去 Etherscan 找一笔 Uniswap 交易
2. 或者使用我提供的示例交易
3. 记录交易哈希

**步骤 2：收集数据**
在 Etherscan 上查看交易详情，收集：
- Chain ID
- Block Number
- From / To
- Method
- Value
- Token Transfers（在 "Tokens Transferred" 部分）
- Logs（在 "Logs" 标签）

**步骤 3：设计 Context 文档**
创建 `experiments/chain-aware-context/manual/transaction-context.md`

使用这个模板：

```markdown
# Transaction Context: [交易哈希]

## 1. 指令层（System Rules）
- Agent 角色：交易分析助手
- 输出格式：结构化分析报告
- 安全原则：只分析链上数据，不做投资建议

## 2. 任务层（Task Context）
- 用户意图：理解这笔交易做了什么
- 分析目标：解释交易的业务逻辑

## 3. 事实层（On-chain Facts）⛓️
**标记说明**：⛓️ = 链上可验证事实

- ⛓️ Chain ID: 1 (Ethereum Mainnet)
- ⛓️ Block Number: [从 Etherscan 复制]
- ⛓️ Transaction Hash: [交易哈希]
  - 🔗 Explorer: https://etherscan.io/tx/[哈希]
- ⛓️ From: [地址]
- ⛓️ To: [合约地址]
- ⛓️ Method: [函数名]
- ⛓️ Value: [ETH 数量]
- ⛓️ Gas Used: [Gas 数量]
- ⛓️ Gas Price: [Gwei]
- ⛓️ Token Transfers:
  - [从 Etherscan "Tokens Transferred" 复制]
- ⛓️ Logs:
  - [从 Etherscan "Logs" 标签复制关键事件]

## 4. 知识层（Knowledge Base）📚
**标记说明**：📚 = 外部知识

- 📚 Uniswap V3 SwapRouter: 去中心化交易所的路由合约
- 📚 相关代币信息：
  - USDC: 稳定币，1 USDC ≈ 1 USD
  - WETH: Wrapped ETH，ERC20 版本的 ETH
- 📚 Swap 机制：通过流动性池进行代币兑换

## 5. 解释层（Interpretation）💭
**标记说明**：💭 = 基于事实的解释

- 💭 交易类型：Uniswap V3 Swap
- 💭 交易路径：[代币 A] → Pool → [代币 B]
- 💭 兑换结果：用 [数量 A] 换得 [数量 B]
- 💭 交易成本：Gas 费用 = [Gas Used] × [Gas Price]

## 6. 来源追溯（Source Tracing）
- 所有 ⛓️ 数据来源：Ethereum Mainnet（通过 Etherscan 查询）
- 所有 📚 知识来源：Uniswap 官方文档
- 所有 💭 解释基于：⛓️ 事实层数据的逻辑推导
```

---

## 💡 实现提示

### 提示 1：如何找到 Method 名称
在 Etherscan 交易详情页：
- 查看 "Input Data" 部分
- 如果合约已验证，会显示函数名（比如 `exactInputSingle`）

### 提示 2：如何理解 Token Transfers
在 "Tokens Transferred" 部分：
- 看清楚方向：From → To
- 注意数量和代币符号
- 可能有多个 Transfer（比如 USDC out, WETH in）

### 提示 3：如何解析 Logs
在 "Logs" 标签：
- 找到 Swap 事件
- 找到 Transfer 事件
- 记录关键参数

### 提示 4：标记系统的使用
- ⛓️ 只用于可以在区块链上验证的数据
- 📚 用于外部知识（文档、常识）
- 💭 用于你的分析和解释
- 🔗 用于 explorer 链接

---

## ✋ 现在开始

1. **去 Etherscan 找一笔交易**（或使用我提供的示例）
2. **创建项目目录**：`experiments/chain-aware-context/`
3. **开始手动收集数据**
4. **填写 Context 文档**

完成手动阶段后回来告诉我，我会帮你进入自动化阶段 👋
