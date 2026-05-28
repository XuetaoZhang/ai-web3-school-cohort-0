# 自动化获取交易数据 - 最小版本

## 🎯 目标

写 Python 脚本自动获取交易数据并生成 Context 文档。

## 📋 实现步骤

### 步骤 1：安装依赖

```bash
cd experiments/chain-aware-context/auto
python3 -m venv venv
source venv/bin/activate
pip install web3
```

### 步骤 2：创建配置文件

创建 `config.py`：

```python
# Infura 配置
INFURA_PROJECT_ID = "your-infura-project-id"
INFURA_URL = "https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"

# 交易哈希
TX_HASH = "0xa40162ed6da4c2fdc7645f381600a185c0ed7efe45e98ffae54449148ff01f81"
```

### 步骤 3：获取交易数据

创建 `fetch_transaction.py`：

```python
from web3 import Web3
from config import INFURA_URL, TX_HASH

# 连接到 Infura
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# 检查连接
if not w3.is_connected():
    print("❌ Failed to connect to Infura")
    exit(1)

print("✅ Connected to Ethereum Mainnet")

# 获取交易数据
tx = w3.eth.get_transaction(TX_HASH)
receipt = w3.eth.get_transaction_receipt(TX_HASH)

# 打印基本信息
print(f"\n📋 Transaction Data:")
print(f"Block Number: {tx['blockNumber']}")
print(f"From: {tx['from']}")
print(f"To: {tx['to']}")
print(f"Value: {w3.from_wei(tx['value'], 'ether')} ETH")
print(f"Gas Used: {receipt['gasUsed']}")
print(f"Gas Price: {w3.from_wei(tx['gasPrice'], 'gwei')} Gwei")
print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")

# 打印 Logs 数量
print(f"\n📝 Logs: {len(receipt['logs'])} events")
```

### 步骤 4：生成 Context 文档

创建 `generate_context.py`：

```python
from web3 import Web3
from config import INFURA_URL, TX_HASH

def generate_context(tx_hash: str) -> str:
    """生成交易的 Context 文档"""
    
    # 连接到 Infura
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    
    if not w3.is_connected():
        raise Exception("Failed to connect to Infura")
    
    # 获取交易数据
    tx = w3.eth.get_transaction(tx_hash)
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    
    # 计算交易费用
    tx_fee = tx['gasPrice'] * receipt['gasUsed']
    
    # 生成 Markdown
    context = f"""# Transaction Context: {tx_hash}

## 1. 指令层（System Rules）
- Agent 角色：交易分析助手
- 输出格式：结构化分析报告
- 安全原则：只分析链上数据，不做投资建议

## 2. 任务层（Task Context）
- 用户意图：理解这笔交易做了什么
- 分析目标：解释交易的业务逻辑

## 3. 事实层（On-chain Facts）⛓️
**标记说明**：⛓️ = 链上可验证事实

- ⛓️ Chain ID: {tx['chainId']} (Ethereum Mainnet)
- ⛓️ Block Number: {tx['blockNumber']}
- ⛓️ Transaction Hash: {tx_hash}
  - 🔗 Explorer: https://etherscan.io/tx/{tx_hash}
- ⛓️ From: {tx['from']}
- ⛓️ To: {tx['to']}
- ⛓️ Value: {w3.from_wei(tx['value'], 'ether')} ETH
- ⛓️ Gas Used: {receipt['gasUsed']:,}
- ⛓️ Gas Price: {w3.from_wei(tx['gasPrice'], 'gwei'):.9f} Gwei
- ⛓️ Transaction Fee: {w3.from_wei(tx_fee, 'ether'):.10f} ETH
- ⛓️ Status: {'✅ Success' if receipt['status'] == 1 else '❌ Failed'}
- ⛓️ Logs: {len(receipt['logs'])} events
  - 🔗 View Logs: https://etherscan.io/tx/{tx_hash}#eventlog

## 4. 知识层（Knowledge Base）📚
**标记说明**：📚 = 外部知识

- 📚 Contract: {tx['to']}
  - 🔗 View Contract: https://etherscan.io/address/{tx['to']}
- 📚 Transaction Type: Contract Interaction

## 5. 解释层（Interpretation）💭
**标记说明**：💭 = 基于事实的解释

- 💭 Transaction Status: {'Successful' if receipt['status'] == 1 else 'Failed'}
- 💭 Gas Efficiency: {(receipt['gasUsed'] / tx['gas'] * 100):.2f}% of gas limit used
- 💭 Transaction Cost: {w3.from_wei(tx_fee, 'ether'):.10f} ETH

## 6. 来源追溯（Source Tracing）
- 所有 ⛓️ 数据来源：Ethereum Mainnet via Infura RPC
- 所有 📚 知识来源：Etherscan
- 所有 💭 解释基于：⛓️ 事实层数据的逻辑推导
- 数据获取时间：{w3.eth.get_block(tx['blockNumber'])['timestamp']}
"""
    
    return context

if __name__ == "__main__":
    # 生成 Context
    context = generate_context(TX_HASH)
    
    # 保存到文件
    with open("transaction-context.md", "w") as f:
        f.write(context)
    
    print("✅ Context document generated: transaction-context.md")
    print(context)
```

### 步骤 5：运行脚本

```bash
# 1. 测试连接和数据获取
python fetch_transaction.py

# 2. 生成 Context 文档
python generate_context.py
```

---

## 🎯 预期输出

运行 `fetch_transaction.py` 应该看到：
```
✅ Connected to Ethereum Mainnet

📋 Transaction Data:
Block Number: 25192498
From: 0xfAe9Fd9c87e2Da9199FD2Df4659d4a0d3880F23d
To: 0xE592427A0AEce92De3Edee1F18E0157C05861564
Value: 0 ETH
Gas Used: 131,448
Gas Price: 0.203002067 Gwei
Status: Success

📝 Logs: 3 events
```

运行 `generate_context.py` 应该生成 `transaction-context.md` 文件。

---

## 💡 实现提示

### 提示 1：Web3.py 基础

```python
# 连接到 Infura
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# 获取交易
tx = w3.eth.get_transaction(tx_hash)

# 获取交易回执
receipt = w3.eth.get_transaction_receipt(tx_hash)

# 单位转换
eth_value = w3.from_wei(wei_value, 'ether')  # Wei → ETH
gwei_value = w3.from_wei(wei_value, 'gwei')  # Wei → Gwei
```

### 提示 2：处理大数字

```python
# Gas Used 格式化（添加千位分隔符）
gas_used = f"{receipt['gasUsed']:,}"  # 131448 → 131,448
```

### 提示 3：计算交易费用

```python
# Transaction Fee = Gas Used × Gas Price
tx_fee = tx['gasPrice'] * receipt['gasUsed']  # 单位：Wei
tx_fee_eth = w3.from_wei(tx_fee, 'ether')     # 转换为 ETH
```

### 提示 4：错误处理

```python
try:
    tx = w3.eth.get_transaction(tx_hash)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
```

---

## ✋ 现在开始

1. **创建项目目录**：
   ```bash
   mkdir -p experiments/chain-aware-context/auto
   cd experiments/chain-aware-context/auto
   ```

2. **创建虚拟环境**：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**：
   ```bash
   pip install web3
   ```

4. **创建文件**：
   - `config.py`（填入你的 Infura Project ID）
   - `fetch_transaction.py`
   - `generate_context.py`

5. **运行测试**

完成后告诉我结果，我会帮你 review 和改进 👋
