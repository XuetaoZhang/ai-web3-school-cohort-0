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