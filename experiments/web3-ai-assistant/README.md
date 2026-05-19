# Web3 AI Assistant - 智能合约助手

## 📋 项目简介

这是一个结合 AI 和 Web3 的实践项目，创建一个智能合约助手 Agent，可以：
- ✅ 分析 Solidity 代码，检测安全问题
- ✅ 生成简单的智能合约代码
- ✅ 解释智能合约的功能
- ✅ 提供 Gas 优化建议

## 🎯 学习目标

1. 将 AI Agent 应用到 Web3 领域
2. 理解智能合约的常见安全问题
3. 学习如何用 AI 辅助智能合约开发
4. 实践 Tool Use 在垂直领域的应用

## 🛠️ 功能列表

### 1. 安全审计工具
- 检测重入攻击
- 检测整数溢出
- 检测访问控制问题
- 检测未检查的外部调用

### 2. 代码生成工具
- 生成 ERC20 代币合约
- 生成简单的 NFT 合约
- 生成多签钱包合约

### 3. 代码解释工具
- 解释合约功能
- 分析合约结构
- 识别使用的设计模式

### 4. Gas 优化工具
- 分析 Gas 消耗
- 提供优化建议

## 📁 项目结构

```
web3-ai-assistant/
├── README.md                    # 项目说明
├── tools.py                     # 工具定义
├── agent.py                     # AI Agent 主程序
├── security_checker.py          # 安全检查工具
├── code_generator.py            # 代码生成工具
├── contract_explainer.py        # 合约解释工具
├── gas_optimizer.py             # Gas 优化工具
├── examples/                    # 示例合约
│   ├── vulnerable_contract.sol  # 有漏洞的合约
│   ├── safe_contract.sol        # 安全的合约
│   └── erc20_example.sol        # ERC20 示例
└── tests/                       # 测试用例
    └── test_security.py
```

## 🚀 快速开始

### 1. 环境准备

```bash
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

```bash
python agent.py
```

## 💡 使用示例

### 示例 1：安全审计

```
用户：检查这个合约的安全问题

contract Vulnerable {
    mapping(address => uint256) public balances;
    
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;
    }
}

Agent：
🔍 发现安全问题：
1. 重入攻击风险
   - 位置：withdraw() 函数
   - 问题：在更新状态之前进行外部调用
   - 建议：先更新 balances，再进行转账
```

### 示例 2：代码生成

```
用户：生成一个简单的 ERC20 代币合约，名称 MyToken，符号 MTK

Agent：
✅ 已生成 ERC20 合约：

contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
```

### 示例 3：合约解释

```
用户：解释这个合约的功能

Agent：
📖 合约分析：
- 合约类型：ERC20 代币
- 主要功能：
  1. transfer(): 转账功能
  2. approve(): 授权功能
  3. transferFrom(): 代理转账
- 设计模式：标准 ERC20 实现
```

## 🔧 工具详解

### 1. security_check(code)
检查 Solidity 代码的安全问题

**检测项**：
- 重入攻击
- 整数溢出
- 访问控制
- 未检查的外部调用
- tx.origin 使用
- 时间戳依赖

### 2. generate_contract(type, params)
生成智能合约代码

**支持类型**：
- erc20: ERC20 代币
- erc721: NFT 合约
- multisig: 多签钱包
- simple: 简单合约

### 3. explain_contract(code)
解释智能合约功能

**分析内容**：
- 合约类型
- 主要功能
- 状态变量
- 事件
- 修饰符
- 设计模式

### 4. optimize_gas(code)
提供 Gas 优化建议

**优化方向**：
- 存储优化
- 循环优化
- 函数可见性
- 数据类型选择

## 📚 相关资源

- [Solidity 官方文档](https://docs.soliditylang.org/)
- [OpenZeppelin 合约库](https://docs.openzeppelin.com/contracts/)
- [Consensys 安全最佳实践](https://consensys.github.io/smart-contract-best-practices/)
- [Slither 静态分析工具](https://github.com/crytic/slither)

## 🎯 扩展方向

1. **集成真实的静态分析工具**
   - 调用 Slither API
   - 集成 MythX

2. **链上数据查询**
   - 查询合约代码
   - 分析交易历史
   - 监控事件

3. **多链支持**
   - Ethereum
   - Polygon
   - BSC
   - Arbitrum

4. **可视化**
   - 合约调用图
   - Gas 消耗图表
   - 安全评分

## 📝 学习笔记

在这个项目中，你将学到：
- 如何将 AI Agent 应用到垂直领域
- 智能合约的常见安全问题
- Solidity 代码分析技巧
- AI 辅助开发的实践经验
