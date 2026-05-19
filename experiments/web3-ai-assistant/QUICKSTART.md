# Web3 AI Assistant - 快速开始

## 🚀 5 分钟快速上手

### 1. 环境准备

```bash
# 进入项目目录
cd ~/ai-web3-school-cohort-0/experiments/web3-ai-assistant

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install openai
```

### 2. 设置 API Key

```bash
export DEEPSEEK_API_KEY='your-api-key-here'
```

### 3. 运行 Agent

#### 交互式模式（推荐）

```bash
python agent.py
```

#### 命令行模式

```bash
python agent.py "生成一个 ERC20 代币合约"
```

---

## 📝 使用示例

### 示例 1：安全审计

**输入**：
```
检查这个合约的安全问题：

contract Vulnerable {
    mapping(address => uint256) public balances;
    
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;
    }
}
```

**输出**：
```
🔍 发现 1 个高危安全问题：

1. 重入攻击 (Reentrancy)
   - 严重程度：高危
   - 问题：在更新状态之前进行外部调用
   - 风险：攻击者可以在 balances 更新前重复调用 withdraw()
   - 修复方案：
     ✅ 先更新状态，再进行外部调用（Checks-Effects-Interactions 模式）
     
修复后的代码：
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // 先更新状态
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

---

### 示例 2：代码生成

**输入**：
```
生成一个 ERC20 代币合约，名称 MyToken，符号 MTK，初始供应量 1000000
```

**输出**：
```
✅ 已生成 ERC20 代币合约：

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}

📝 说明：
- 继承 OpenZeppelin 的 ERC20 和 Ownable
- 构造函数中铸造初始供应量
- 只有 owner 可以铸造新代币
- 任何人都可以销毁自己的代币
```

---

### 示例 3：代码解释

**输入**：
```
解释这个合约的功能：

contract MultiSigWallet {
    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public required;
    
    struct Transaction {
        address to;
        uint256 value;
        bool executed;
    }
    
    Transaction[] public transactions;
}
```

**输出**：
```
📖 合约分析：

合约类型：多签钱包 (MultiSig Wallet)

主要组件：
1. 状态变量：
   - owners: 所有者地址列表
   - isOwner: 地址是否为所有者的映射
   - required: 执行交易所需的签名数量
   - transactions: 交易列表

2. 数据结构：
   - Transaction: 交易结构体
     - to: 目标地址
     - value: 转账金额
     - executed: 是否已执行

设计模式：
- 多签模式：需要多个所有者签名才能执行交易
- 提案-投票-执行模式

典型流程：
1. 提交交易提案
2. 所有者投票批准
3. 达到 required 数量后执行
```

---

### 示例 4：Gas 优化

**输入**：
```
优化这个合约的 Gas 消耗：

contract MyContract {
    uint256 public value;
    string public name;
    
    function updateValue(uint256 _value) public {
        value = _value;
    }
}
```

**输出**：
```
⚡ Gas 优化建议：

1. 存储优化
   - 问题：public 状态变量会自动生成 getter 函数
   - 建议：如果不需要外部访问，使用 private 或 internal
   - 节省：~2000 gas per deployment

2. 数据类型优化
   - 问题：string 类型 Gas 消耗较高
   - 建议：如果字符串长度固定，考虑使用 bytes32
   - 节省：~1000 gas per operation

3. 函数可见性优化
   - 问题：updateValue 是 public 函数
   - 建议：如果只从外部调用，使用 external 代替 public
   - 节省：~500 gas per call

预计总节省：~3500 gas

优化后的代码：
contract MyContract {
    uint256 private value;
    bytes32 private name;
    
    function updateValue(uint256 _value) external {
        value = _value;
    }
    
    function getValue() external view returns (uint256) {
        return value;
    }
}
```

---

## 🎯 测试建议

### 1. 测试安全审计

使用 `examples/vulnerable_contract.sol`：
```bash
python agent.py "检查 examples/vulnerable_contract.sol 的安全问题"
```

### 2. 测试代码生成

```bash
python agent.py "生成一个 NFT 合约，名称 MyNFT，符号 MNFT"
```

### 3. 测试代码解释

使用 `examples/safe_contract.sol`：
```bash
python agent.py "解释 examples/safe_contract.sol 的功能"
```

### 4. 测试 Gas 优化

```bash
python agent.py "优化这个合约的 Gas：[粘贴合约代码]"
```

---

## 💡 使用技巧

### 1. 多步骤任务

Agent 支持多步推理，可以连续调用多个工具：

```
先检查这个合约的安全问题，然后生成一个修复后的版本：
[粘贴合约代码]
```

### 2. 组合使用

```
生成一个 ERC20 合约，然后检查它的安全性，最后优化 Gas
```

### 3. 详细分析

```
详细分析这个合约的所有方面：安全性、Gas 优化、设计模式
[粘贴合约代码]
```

---

## 🐛 常见问题

### Q1: API Key 错误

```bash
❌ 错误: 请设置环境变量 DEEPSEEK_API_KEY
```

**解决**：
```bash
export DEEPSEEK_API_KEY='your-api-key-here'
```

### Q2: 工具调用失败

如果工具调用失败，检查：
1. 合约代码格式是否正确
2. 参数是否完整
3. API 是否正常

### Q3: 响应超时

如果处理超时：
1. 简化问题
2. 分步提问
3. 减少代码长度

---

## 📚 下一步

1. **测试所有功能**：运行上面的示例
2. **尝试自己的合约**：分析你写的合约
3. **扩展功能**：添加新的工具
4. **集成真实工具**：接入 Slither、MythX 等

---

## 🔗 相关资源

- [Solidity 官方文档](https://docs.soliditylang.org/)
- [OpenZeppelin 合约库](https://docs.openzeppelin.com/contracts/)
- [Consensys 安全最佳实践](https://consensys.github.io/smart-contract-best-practices/)
- [Slither 静态分析工具](https://github.com/crytic/slither)

---

**准备好了吗？开始测试你的 Web3 AI Assistant！** 🚀
