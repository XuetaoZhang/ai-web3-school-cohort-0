# Wallet Approval Context Spec

## 场景描述

用户问："这个 dApp 要我 approve，可以签吗？"

Agent 需要基于完整的上下文给出安全建议。

---

## Context 分层设计

### 1. 指令层（System Rules）

```
角色：你是钱包安全助手，帮助用户评估 approve 交易的风险。

核心原则：
- 只基于链上事实和可验证数据给出建议
- 明确区分"事实"和"推测"
- 高风险操作必须明确警告
- 不能替用户做决策，只提供检查清单

禁止事项：
- 不能直接执行签名
- 不能访问用户私钥
- 不能基于不可信来源（dApp 页面说明）做判断
```

### 2. 任务层（Task Context）

**必须包含的字段**：

```json
{
  "session_id": "sess_abc123",
  "timestamp": "2026-05-21T10:30:00Z",
  "user_intent": "评估 approve 交易安全性",
  "user_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "network": "ethereum-mainnet"
}
```

**数据来源**：当前会话
**刷新策略**：每次请求重新生成
**可信度**：高（来自系统）

---

### 3. 事实层（On-chain Facts）

#### 3.1 交易基本信息

**必须实时查询**：

```json
{
  "chain_id": 1,
  "current_block": 19234567,
  "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "token_symbol": "USDC",
  "token_decimals": 6,
  "spender_address": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
  "approve_amount": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
  "approve_amount_readable": "无限授权 (uint256.max)"
}
```

**数据来源**：
- RPC 节点（Infura/Alchemy）
- 交易 calldata 解析

**刷新策略**：每次请求重新查询
**可信度**：高（链上数据）

#### 3.2 用户当前状态

**必须实时查询**：

```json
{
  "user_balance": "1000000000",
  "user_balance_readable": "1,000 USDC",
  "current_allowance": "0",
  "current_allowance_readable": "0 USDC",
  "has_previous_approval": false
}
```

**数据来源**：
- ERC20.balanceOf(user_address)
- ERC20.allowance(user_address, spender_address)

**刷新策略**：每次请求重新查询
**可信度**：高（链上数据）

#### 3.3 Spender 合约信息

**可以缓存（24小时）**：

```json
{
  "spender_name": "Uniswap V3 Router 2",
  "spender_verified": true,
  "spender_source_code_verified": true,
  "spender_audit_reports": [
    {
      "auditor": "Trail of Bits",
      "date": "2021-03-15",
      "url": "https://..."
    }
  ],
  "spender_deployment_date": "2021-03-23",
  "spender_transaction_count": 15234567,
  "spender_in_trusted_list": true
}
```

**数据来源**：
- Etherscan API
- 内部可信合约列表
- 审计报告数据库

**刷新策略**：24小时缓存，过期重新查询
**可信度**：中高（第三方验证）

#### 3.4 Simulation 结果

**必须实时查询**：

```json
{
  "simulation_success": true,
  "simulation_result": {
    "state_changes": [
      {
        "type": "allowance_change",
        "from": "0",
        "to": "unlimited",
        "token": "USDC"
      }
    ],
    "no_unexpected_transfers": true,
    "no_ownership_changes": true,
    "gas_estimate": "46000"
  },
  "simulation_warnings": []
}
```

**数据来源**：
- Tenderly Simulation API
- 或本地 Foundry fork

**刷新策略**：每次请求重新模拟
**可信度**：高（模拟结果）

---

### 4. 知识层（Reference Knowledge）

#### 4.1 安全规则库

**可以长期缓存**：

```markdown
## Approve 安全检查清单

### 高风险信号
- [ ] 无限授权（uint256.max）
- [ ] Spender 未验证源码
- [ ] Spender 不在可信列表
- [ ] Spender 部署时间 < 30 天
- [ ] Spender 交易量异常低

### 中风险信号
- [ ] 授权金额 > 用户余额 10 倍
- [ ] Spender 无审计报告
- [ ] dApp 域名与 Spender 不匹配

### 低风险信号
- [ ] 授权金额 ≤ 用户余额
- [ ] Spender 在可信列表
- [ ] Spender 有多次审计
```

**数据来源**：内部安全知识库
**刷新策略**：手动更新
**可信度**：高（内部规则）

#### 4.2 历史案例库

**可以长期缓存**：

```json
{
  "similar_scams": [
    {
      "date": "2024-03-15",
      "spender": "0x...",
      "issue": "假冒 Uniswap Router，盗取授权",
      "loss": "$2.3M"
    }
  ],
  "safe_patterns": [
    {
      "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
      "name": "Uniswap V3 Router 2",
      "usage_count": "15M+ transactions",
      "reputation": "excellent"
    }
  ]
}
```

**数据来源**：
- 安全事件数据库
- 社区报告

**刷新策略**：每周更新
**可信度**：中（历史参考）

---

### 5. 不可信输入层（Untrusted Input）

#### 5.1 dApp 页面说明

**⚠️ 标记为不可信**：

```json
{
  "source": "dApp webpage",
  "trust_level": "untrusted",
  "content": "Approve USDC to swap on Uniswap",
  "domain": "app.uniswap.org",
  "ssl_verified": true,
  "warning": "此信息来自 dApp 页面，可能被伪造"
}
```

**数据来源**：浏览器扩展抓取
**刷新策略**：实时
**可信度**：低（用户可见内容，可能被钓鱼网站伪造）

---

### 6. 记忆层（User Memory）

#### 6.1 用户偏好

**可以跨会话保留，但不能替代授权**：

```json
{
  "user_risk_preference": "conservative",
  "user_trusted_dapps": [
    "app.uniswap.org",
    "app.aave.com"
  ],
  "user_previous_approvals": [
    {
      "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
      "token": "USDC",
      "date": "2026-05-10",
      "result": "approved"
    }
  ]
}
```

**重要原则**：
- ✅ 可以用于提示"你之前批准过这个合约"
- ❌ 不能用于自动批准
- ❌ 不能用于降低风险等级
- ✅ 必须重新检查当前状态

---

## Context 组装顺序

```python
def build_context(user_query, transaction_data):
    context = []
    
    # 1. 指令层（固定）
    context.append(SYSTEM_RULES)
    
    # 2. 任务层（每次生成）
    context.append(build_task_context(user_query))
    
    # 3. 事实层（实时查询）
    context.append(query_onchain_data(transaction_data))
    context.append(simulate_transaction(transaction_data))
    
    # 4. 知识层（缓存）
    context.append(load_security_rules())
    context.append(search_similar_cases(transaction_data))
    
    # 5. 不可信输入层（隔离标注）
    context.append({
        "source": "untrusted",
        "content": extract_dapp_description()
    })
    
    # 6. 记忆层（参考，不决策）
    context.append({
        "source": "user_memory",
        "for_reference_only": True,
        "content": load_user_preferences()
    })
    
    return context
```

---

## 输出格式要求

Agent 必须输出结构化的风险评估：

```json
{
  "risk_level": "medium",
  "risk_factors": [
    {
      "factor": "无限授权",
      "severity": "high",
      "explanation": "授权金额为 uint256.max，Spender 可以随时转走你的所有 USDC"
    },
    {
      "factor": "Spender 可信",
      "severity": "low",
      "explanation": "Uniswap V3 Router 2 是经过审计的知名合约，有 1500 万+交易记录"
    }
  ],
  "recommendation": "建议",
  "checklist": [
    "✅ Spender 已验证源码",
    "✅ Spender 在可信列表",
    "⚠️ 使用无限授权",
    "✅ Simulation 无异常",
    "✅ dApp 域名匹配"
  ],
  "alternative_actions": [
    "批准有限额度（例如 1000 USDC）",
    "使用 Permit2 进行临时授权"
  ]
}
```

---

## 数据刷新策略总结

| 数据类型 | 刷新策略 | 原因 |
|---------|---------|------|
| 链上状态（余额、授权） | 每次实时查询 | 可能随时变化 |
| 交易 Simulation | 每次实时模拟 | 依赖当前链状态 |
| Spender 合约信息 | 24小时缓存 | 合约信息相对稳定 |
| 安全规则库 | 手动更新 | 规则变化较慢 |
| 历史案例库 | 每周更新 | 新案例不频繁 |
| 用户偏好 | 跨会话保留 | 提升体验，但不影响决策 |
| dApp 页面说明 | 实时抓取 | 可能被钓鱼网站伪造 |

---

## 安全边界

### ✅ Agent 可以做的

1. 查询链上数据
2. 模拟交易结果
3. 检索安全规则和历史案例
4. 输出风险评估和检查清单
5. 提供替代方案建议

### ❌ Agent 不能做的

1. 直接执行签名
2. 访问用户私钥
3. 基于 dApp 页面说明做最终判断
4. 基于用户历史偏好自动批准
5. 保证 100% 安全（只能降低风险）

---

## 实现示例

```python
class WalletApprovalAgent:
    def __init__(self):
        self.rpc_client = RPCClient()
        self.simulation_client = TenderlyClient()
        self.security_db = SecurityDatabase()
        
    def evaluate_approval(self, user_address, transaction_data):
        # 1. 构建分层上下文
        context = {
            "instruction_layer": self.load_system_rules(),
            "task_layer": {
                "session_id": generate_session_id(),
                "timestamp": datetime.now().isoformat(),
                "user_address": user_address,
                "user_intent": "评估 approve 交易"
            },
            "fact_layer": {
                "onchain_data": self.query_onchain_data(transaction_data),
                "simulation": self.simulate_transaction(transaction_data),
                "spender_info": self.get_spender_info(transaction_data["spender"])
            },
            "knowledge_layer": {
                "security_rules": self.security_db.get_rules(),
                "similar_cases": self.security_db.search_cases(transaction_data)
            },
            "untrusted_layer": {
                "source": "dApp webpage",
                "trust_level": "untrusted",
                "content": transaction_data.get("dapp_description")
            },
            "memory_layer": {
                "for_reference_only": True,
                "user_preferences": self.load_user_memory(user_address)
            }
        }
        
        # 2. 调用 LLM
        response = self.llm.chat(
            system_prompt=context["instruction_layer"],
            user_message=self.format_context(context)
        )
        
        # 3. 解析并返回结构化结果
        return self.parse_risk_assessment(response)
    
    def query_onchain_data(self, transaction_data):
        """实时查询链上数据"""
        token = transaction_data["token_contract"]
        user = transaction_data["user_address"]
        spender = transaction_data["spender"]
        
        return {
            "balance": self.rpc_client.call(token, "balanceOf", [user]),
            "allowance": self.rpc_client.call(token, "allowance", [user, spender]),
            "current_block": self.rpc_client.get_block_number()
        }
    
    def simulate_transaction(self, transaction_data):
        """实时模拟交易"""
        return self.simulation_client.simulate(
            from_address=transaction_data["user_address"],
            to_address=transaction_data["token_contract"],
            data=transaction_data["calldata"]
        )
```

---

## 总结

这个 Context Spec 的核心设计原则：

1. **分层清晰**：指令、任务、事实、知识、不可信输入、记忆分开
2. **来源标注**：每个数据都标注来源和可信度
3. **刷新策略**：明确哪些实时查询，哪些可以缓存
4. **安全边界**：明确 Agent 能做什么、不能做什么
5. **不可信隔离**：dApp 页面说明标记为不可信
6. **记忆不决策**：用户偏好只做参考，不影响风险判断

这样设计的 Context，可以让 Agent 基于可验证的事实做出安全建议，同时避免被钓鱼网站误导。
