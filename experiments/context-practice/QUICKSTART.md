# Context 最小实践：钱包授权检查 Agent

## 项目概述

这是一个演示 **Context 分层设计**价值的实践项目。

**场景**：用户问"这个 dApp 要我 approve，可以签吗？"

**挑战**：Agent 需要基于多种来源的信息做出安全建议，但这些信息的可信度不同：
- ✅ 链上数据（高可信）
- ✅ 安全规则库（高可信）
- ⚠️ dApp 页面说明（低可信，可能被钓鱼网站伪造）
- ⚠️ 用户历史偏好（仅供参考，不能自动批准）

**解决方案**：通过 Context 分层设计，明确标注每层数据的来源和可信度，防止 LLM 被误导。

---

## Context 分层设计

### 1. 指令层（System Rules）
- 定义 Agent 的角色和边界
- 明确禁止事项（不能直接签名、不能访问私钥）
- 要求输出结构化结果

### 2. 任务层（Task Context）
- 会话信息（session_id, timestamp）
- 用户意图
- 用户地址和网络

### 3. 事实层（On-chain Facts）
- 链上数据（余额、授权额度）
- 交易模拟结果
- Spender 合约信息
- **数据来源**：RPC 节点、Etherscan API
- **刷新策略**：每次实时查询

### 4. 知识层（Reference Knowledge）
- 安全规则库
- 历史案例库
- **数据来源**：内部安全知识库
- **刷新策略**：可以缓存

### 5. 不可信输入层（Untrusted Input）
- dApp 页面说明
- **⚠️ 明确标注为不可信**
- **只做参考，不作为决策依据**

### 6. 记忆层（User Memory）
- 用户历史偏好
- **⚠️ 仅供参考，不能自动批准**
- **必须重新检查当前状态**

---

## 文件结构

```
context-practice/
├── wallet-approval-context-spec.md  # Context Spec 设计文档
├── wallet_approval_agent.py         # 主 Agent 实现
├── mock_data.py                     # 模拟数据源
├── test_agent.py                    # 测试脚本
├── QUICKSTART.md                    # 本文件
└── EXPERIMENT-REPORT.md             # 实验报告（待填写）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install openai
```

### 2. 设置 API Key

```bash
export DEEPSEEK_API_KEY="your-api-key"
```

### 3. 运行测试

```bash
cd ~/ai-web3-school-cohort-0/experiments/context-practice
python3 test_agent.py
```

### 4. 测试用例

测试脚本包含 4 个测试用例：

1. **可信合约 + 无限授权**（Uniswap V3 Router）
   - 预期：medium 风险（可信但无限授权）

2. **未知合约 + 无限授权**
   - 预期：high 风险（未知合约 + 无限授权）

3. **已知诈骗合约**
   - 预期：high 风险（在黑名单中）

4. **可信合约 + 有限授权**（100 USDC）
   - 预期：low 风险（可信 + 有限授权）

---

## 验证 Context 的价值

运行测试后，观察以下几点：

### ✅ 不可信输入是否被正确处理？

测试用例 3 中，dApp 页面说明是 "Official Uniswap Router"（假冒），但 Agent 应该：
- 识别出这是已知诈骗合约
- 不被 dApp 页面说明误导
- 给出 high 风险警告

### ✅ 记忆层是否只做参考？

用户之前批准过 Uniswap Router，但 Agent 应该：
- 提示"你之前批准过这个合约"
- 但仍然重新检查当前状态
- 不自动批准

### ✅ 输出是否结构化？

Agent 应该输出 JSON 格式的风险评估：
- risk_level: low/medium/high
- risk_factors: 风险因素列表
- recommendation: 建议
- checklist: 检查清单
- alternative_actions: 替代方案

---

## 对比：无 Context 分层的问题

如果不做分层，直接把所有信息混在一起：

❌ **问题 1：LLM 可能被 dApp 页面说明误导**
- dApp 说"这是官方 Uniswap"，LLM 可能信以为真
- 即使链上数据显示这是诈骗合约

❌ **问题 2：无法区分"事实"和"推测"**
- 链上数据是事实
- dApp 页面说明是推测
- 混在一起，LLM 无法判断

❌ **问题 3：可能基于用户历史偏好自动批准**
- 用户之前批准过 Uniswap
- LLM 可能认为"这次也可以批准"
- 但没有检查当前状态

❌ **问题 4：输出格式不可控**
- LLM 可能输出自然语言
- 难以解析和验证
- 无法集成到钱包 UI

---

## 核心收获

### 1. Context 是信息治理问题

Context 不只是"把信息塞给 LLM"，而是：
- 明确每层数据的来源和可信度
- 设计刷新策略（实时 vs 缓存）
- 设置安全边界（Agent 能做什么、不能做什么）

### 2. 不可信输入必须隔离标注

dApp 页面说明、用户输入等不可信来源：
- 必须明确标注为"untrusted"
- 只做参考，不作为决策依据
- 防止钓鱼网站误导 LLM

### 3. 记忆层只做参考，不做决策

用户历史偏好可以提升体验：
- ✅ 提示"你之前批准过这个合约"
- ❌ 不能自动批准
- ❌ 不能降低风险等级

### 4. 结构化输出便于验证

要求 LLM 输出 JSON 格式：
- 便于解析和验证
- 可以集成到钱包 UI
- 可以审计决策依据

---

## 下一步

1. 运行测试，观察结果
2. 填写 `EXPERIMENT-REPORT.md`，记录你的发现
3. 思考：如果没有 Context 分层，会出现什么问题？
4. 更新学习笔记，总结 Context 的核心价值

---

## 参考资料

- [Context Spec 设计文档](./wallet-approval-context-spec.md)
- [AI × Web3 School Handbook - Context 章节](https://aiweb3.school/handbook)
