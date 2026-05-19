# Web3 基础知识复习

## 📚 目录

1. [区块链基础](#区块链基础)
2. [智能合约](#智能合约)
3. [Solidity 核心概念](#solidity-核心概念)
4. [DeFi 生态](#defi-生态)
5. [AI × Web3 结合点](#ai--web3-结合点)

---

## 区块链基础

### 核心概念

**区块链（Blockchain）**：
- 分布式账本技术（Distributed Ledger Technology, DLT）
- 由区块（Block）按时间顺序链接而成
- 每个区块包含：区块头（Header）+ 交易数据（Transactions）

**区块结构**：
```
Block N:
├── Block Header
│   ├── Previous Block Hash  # 前一个区块的哈希
│   ├── Timestamp            # 时间戳
│   ├── Nonce                # 工作量证明的随机数
│   ├── Merkle Root          # 交易树根哈希
│   └── Difficulty           # 挖矿难度
└── Transactions             # 交易列表
    ├── Transaction 1
    ├── Transaction 2
    └── ...
```

### 核心特性

1. **去中心化（Decentralization）**
   - 没有单一控制点
   - 节点平等参与
   - 抗审查

2. **不可篡改（Immutability）**
   - 通过密码学哈希链接
   - 修改历史需要重新计算所有后续区块
   - 计算成本极高

3. **透明性（Transparency）**
   - 所有交易公开可查
   - 任何人都可以验证
   - 匿名但可追溯

4. **安全性（Security）**
   - 密码学保护
   - 共识机制保证
   - 分布式存储

### 共识机制

#### 1. PoW (Proof of Work) - 工作量证明

**代表**：Bitcoin, Ethereum (旧版)

**原理**：
- 矿工竞争解决数学难题
- 第一个找到解的矿工获得记账权
- 其他节点验证并接受

**优点**：
- 安全性高
- 经过长期验证

**缺点**：
- 能源消耗大
- 交易速度慢（Bitcoin: ~7 TPS）

#### 2. PoS (Proof of Stake) - 权益证明

**代表**：Ethereum 2.0, Cardano

**原理**：
- 验证者质押代币
- 根据质押量和时间选择验证者
- 恶意行为会被罚没质押

**优点**：
- 能源效率高
- 交易速度快
- 更环保

**缺点**：
- 富者愈富
- 相对较新

#### 3. 其他共识机制

- **DPoS** (Delegated PoS)：委托权益证明，如 EOS
- **PBFT** (Practical Byzantine Fault Tolerance)：实用拜占庭容错
- **PoA** (Proof of Authority)：权威证明，用于联盟链

### 区块链类型

1. **公链（Public Blockchain）**
   - 完全开放
   - 任何人可参与
   - 例：Bitcoin, Ethereum

2. **联盟链（Consortium Blockchain）**
   - 部分开放
   - 授权节点参与
   - 例：Hyperledger Fabric

3. **私链（Private Blockchain）**
   - 完全封闭
   - 单一组织控制
   - 例：企业内部链

---

## 智能合约

### 定义

**智能合约（Smart Contract）**：
- 运行在区块链上的程序
- 自动执行、不可篡改
- 无需第三方信任

### 特点

1. **确定性（Deterministic）**
   - 相同输入 → 相同输出
   - 所有节点执行结果一致

2. **自动执行（Automatic Execution）**
   - 条件满足自动触发
   - 无需人工干预

3. **不可篡改（Immutable）**
   - 部署后无法修改
   - 需要升级机制（Proxy Pattern）

4. **透明性（Transparent）**
   - 代码公开可审计
   - 执行过程可追溯

### 应用场景

- **DeFi**：去中心化金融（借贷、交易、稳定币）
- **NFT**：非同质化代币（艺术品、游戏道具）
- **DAO**：去中心化自治组织
- **供应链**：溯源、防伪
- **身份认证**：DID（去中心化身份）

---

## Solidity 核心概念

### 基础语法

#### 1. 合约结构

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyContract {
    // 状态变量
    uint256 public value;
    address public owner;
    
    // 事件
    event ValueChanged(uint256 newValue);
    
    // 修饰符
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    // 构造函数
    constructor() {
        owner = msg.sender;
    }
    
    // 函数
    function setValue(uint256 _value) public onlyOwner {
        value = _value;
        emit ValueChanged(_value);
    }
}
```

#### 2. 数据类型

**值类型**：
```solidity
// 布尔
bool public isActive = true;

// 整数
uint256 public count = 100;      // 无符号整数
int256 public balance = -50;     // 有符号整数

// 地址
address public user = 0x123...;
address payable public recipient;

// 字节
bytes32 public hash;
bytes public data;

// 枚举
enum Status { Pending, Active, Completed }
Status public status = Status.Pending;
```

**引用类型**：
```solidity
// 数组
uint[] public numbers;
address[] public users;

// 映射
mapping(address => uint256) public balances;
mapping(address => mapping(address => uint256)) public allowances;

// 结构体
struct User {
    string name;
    uint256 age;
    bool isActive;
}
User public user;
```

#### 3. 函数可见性

```solidity
// public: 内外部都可调用
function publicFunc() public {}

// external: 只能外部调用
function externalFunc() external {}

// internal: 只能内部和继承合约调用
function internalFunc() internal {}

// private: 只能内部调用
function privateFunc() private {}
```

#### 4. 函数修饰符

```solidity
// view: 只读，不修改状态
function getValue() public view returns (uint256) {
    return value;
}

// pure: 不读取也不修改状态
function add(uint256 a, uint256 b) public pure returns (uint256) {
    return a + b;
}

// payable: 可以接收 ETH
function deposit() public payable {
    balances[msg.sender] += msg.value;
}
```

### 常见模式

#### 1. 所有权模式

```solidity
contract Ownable {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}
```

#### 2. 暂停模式

```solidity
contract Pausable {
    bool public paused = false;
    
    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }
    
    function pause() public {
        paused = true;
    }
    
    function unpause() public {
        paused = false;
    }
}
```

#### 3. 提款模式

```solidity
contract Withdrawal {
    mapping(address => uint256) public pendingWithdrawals;
    
    function withdraw() public {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "No funds");
        
        pendingWithdrawals[msg.sender] = 0;  // 先更新状态
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### 安全问题

#### 1. 重入攻击（Reentrancy）

**问题**：
```solidity
// ❌ 不安全
function withdraw() public {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    balances[msg.sender] = 0;  // 状态更新在转账之后
}
```

**解决**：
```solidity
// ✅ 安全
function withdraw() public {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // 先更新状态
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

#### 2. 整数溢出（Integer Overflow）

**问题**：
```solidity
// Solidity < 0.8.0
uint8 x = 255;
x = x + 1;  // 溢出变成 0
```

**解决**：
- Solidity >= 0.8.0 自动检查
- 或使用 SafeMath 库

#### 3. 访问控制（Access Control）

**问题**：
```solidity
// ❌ 缺少权限检查
function withdraw() public {
    // 任何人都可以调用
}
```

**解决**：
```solidity
// ✅ 添加权限检查
function withdraw() public onlyOwner {
    // 只有 owner 可以调用
}
```

---

## DeFi 生态

### 核心协议

#### 1. DEX (去中心化交易所)

**Uniswap**：
- AMM (自动做市商) 模型
- 恒定乘积公式：x * y = k
- 无需订单簿

**工作原理**：
```
流动性池：ETH/USDT
- ETH 数量：x
- USDT 数量：y
- 恒定乘积：k = x * y

交易时：
- 用户用 Δx 个 ETH 换 USDT
- 池子收到 Δx，输出 Δy
- 保持 (x + Δx) * (y - Δy) = k
```

#### 2. 借贷协议

**Aave / Compound**：
- 超额抵押借贷
- 利率由供需决定
- 清算机制

**流程**：
```
1. 用户存入 ETH 作为抵押
2. 根据抵押率借出 USDT
3. 支付利息
4. 如果抵押率不足，触发清算
```

#### 3. 稳定币

**类型**：
- **法币抵押**：USDT, USDC（1:1 美元储备）
- **加密货币抵押**：DAI（超额抵押 ETH）
- **算法稳定币**：UST（已崩盘）

#### 4. 衍生品

- **期权**：Opyn, Hegic
- **期货**：dYdX, Perpetual Protocol
- **合成资产**：Synthetix

### DeFi 风险

1. **智能合约风险**：代码漏洞、黑客攻击
2. **流动性风险**：无常损失、挤兑
3. **预言机风险**：价格操纵
4. **监管风险**：政策不确定性

---

## AI × Web3 结合点

### 1. AI 辅助智能合约开发

**应用**：
- **代码生成**：根据需求生成 Solidity 代码
- **安全审计**：自动检测常见漏洞
- **代码优化**：Gas 优化建议

**示例**：
```
用户：生成一个 ERC20 代币合约
AI：生成完整的 ERC20 代码，包括 mint、burn、transfer 等功能
```

### 2. AI 驱动的 DeFi 策略

**应用**：
- **收益优化**：自动寻找最佳收益策略
- **风险管理**：预测清算风险
- **套利机器人**：跨 DEX 套利

**示例**：
```
AI Agent 监控多个 DEX 价格
发现套利机会 → 自动执行交易
```

### 3. RAG 增强的区块链知识库

**应用**：
- **智能合约文档问答**：快速理解复杂合约
- **DeFi 协议解释**：解释协议工作原理
- **安全最佳实践**：提供安全建议

**示例**：
```
用户：Uniswap V3 的集中流动性是什么？
RAG：检索 Uniswap 文档 → 生成详细解释
```

### 4. AI Agent 与区块链交互

**应用**：
- **链上数据查询**：查询余额、交易历史
- **智能合约调用**：自动执行链上操作
- **多链操作**：跨链桥接、资产转移

**示例**：
```
用户：查询我的 ETH 余额
Agent：调用 Etherscan API → 返回余额

用户：将 100 USDT 从 Ethereum 转到 Polygon
Agent：调用跨链桥合约 → 执行转账
```

### 5. 链上 AI 模型

**应用**：
- **预测市场**：基于 AI 的价格预测
- **信用评分**：链上行为分析
- **NFT 生成**：AI 生成艺术品

**挑战**：
- Gas 成本高
- 计算能力有限
- 隐私问题

### 6. 去中心化 AI

**应用**：
- **联邦学习**：多方协作训练模型
- **模型市场**：买卖 AI 模型
- **计算资源共享**：去中心化 GPU 网络

**项目**：
- Ocean Protocol：数据市场
- Fetch.ai：AI Agent 网络
- SingularityNET：AI 服务市场

---

## 🎯 学习检查点

### 区块链基础
- [ ] 理解区块结构和链接方式
- [ ] 掌握 PoW 和 PoS 的区别
- [ ] 了解区块链的核心特性

### 智能合约
- [ ] 理解智能合约的工作原理
- [ ] 掌握 Solidity 基础语法
- [ ] 了解常见安全问题

### DeFi
- [ ] 理解 AMM 工作原理
- [ ] 了解借贷协议机制
- [ ] 认识 DeFi 风险

### AI × Web3
- [ ] 思考 AI 如何辅助智能合约开发
- [ ] 理解 RAG 在区块链领域的应用
- [ ] 探索 AI Agent 与链上交互的可能性

---

## 📚 推荐资源

### 学习资源
- [Ethereum 官方文档](https://ethereum.org/zh/developers/docs/)
- [Solidity 官方文档](https://docs.soliditylang.org/)
- [OpenZeppelin 合约库](https://docs.openzeppelin.com/contracts/)
- [DeFi Llama](https://defillama.com/) - DeFi 数据

### 开发工具
- **Remix**：在线 Solidity IDE
- **Hardhat**：智能合约开发框架
- **Foundry**：快速的 Solidity 测试框架
- **Etherscan**：区块链浏览器

### 安全审计
- [Consensys Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [Slither](https://github.com/crytic/slither) - 静态分析工具
- [MythX](https://mythx.io/) - 安全分析平台

---

**下一步**：
1. 对照 Handbook 补充遗漏内容
2. 编写一个简单的 Solidity 合约
3. 思考一个 AI × Web3 的实践项目
