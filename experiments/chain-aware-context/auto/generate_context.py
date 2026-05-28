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