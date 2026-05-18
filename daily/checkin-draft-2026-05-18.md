# Day 1 打卡 - AI × Web3 School

**日期**: 2026-05-18  
**学员**: XuetaoZhang  
**阶段**: Phase 1 - AI 基础

---

## 📚 今日学习内容

### 理论学习
- ✅ 阅读 AI 基础章节
  - 大语言模型（LLM）
  - 提示词（Prompt）
  - 上下文（Context）
  - 检索增强生成（RAG）
  - 智能体（Agent）

### 动手实践
- ✅ 完成 Prompt Engineering 基础实践
  - 模糊 vs 清晰 Prompt 对比
  - Zero-shot vs Few-shot 学习
  - 角色设定实验
  - 约束条件控制
  - 结构化输出（JSON、Markdown）

---

## 💡 关键收获

### 1. Prompt Engineering 核心技巧

**清晰度的重要性**
- 模糊提示词让 LLM 只能输出训练数据中最常见的内容
- 清晰的提示词能够精确引导 LLM 输出符合要求的结果
- 实例：智能合约生成，清晰提示词能生成完整的 ERC20 合约

**Few-shot Learning 的威力**
- Zero-shot 只能依赖训练数据中的分类
- Few-shot 通过示例能显著提升分类准确性
- 适用场景：交易分类、代码生成、数据标注

**约束条件的作用**
- 明确的约束（如代码行数、输出格式）能减少发散
- 结构化输出（JSON、Markdown）便于程序解析
- 适合需要自动化处理的场景

### 2. 对 AI × Web3 的理解

通过今天的学习，我认识到：
- Prompt Engineering 是与 AI 有效沟通的基础
- 在 Web3 场景中，清晰的提示词对于智能合约生成、安全审计等任务至关重要
- Few-shot 学习特别适合链上交易分类、DeFi 协议分析等场景

---

## 🛠️ 实践成果

### 完成的实验
1. **基础 Prompt 对比**
   - 模糊 vs 清晰：效果差异显著
   - Zero-shot vs Few-shot：Few-shot 明显更准确

2. **角色与约束**
   - 角色设定：定义了 Solidity 安全审计专家角色
   - 约束条件：限制代码行数和输出格式，减少发散

3. **输出格式控制**
   - JSON 格式：适合程序解析
   - Markdown 表格：适合文档展示

### 代码仓库
- GitHub: https://github.com/XuetaoZhang/ai-web3-school-cohort-0
- 实践文件: `experiments/prompt-engineering-practice.md`

---

## 🤔 遇到的问题与思考

### 问题
1. 角色设定的效果不够明显，可能需要更多对比实验
2. 如何在实际项目中系统化应用这些技巧？

### 思考
1. Prompt Engineering 不是一次性的，需要持续迭代优化
2. 不同场景需要不同的提示词策略
3. 结构化输出对于构建 AI × Web3 应用非常重要

---

## 📝 明日计划

### 学习目标
- 完成 RAG 系统实践
- 完成 AI Agent 实践
- 深入理解 Agent 工作流

### 实践任务
- 构建简单的 RAG 系统（检索增强生成）
- 创建第一个 AI Agent（能调用工具）
- 尝试将 RAG 和 Agent 结合

---

## 📊 学习统计

- **学习时间**: 约 3 小时
  - 理论学习: 1.5 小时
  - 动手实践: 1.5 小时
- **完成进度**: Day 1 / 42 天
- **实践产出**: 1 个实验文档

---

## 🎯 个人感悟

今天是 AI × Web3 School 的第一天，通过系统学习 AI 基础和 Prompt Engineering 实践，我深刻体会到：

1. **Prompt Engineering 是基础技能**：作为一个前端开发者，我已经在使用 AI 工具辅助开发，但今天的系统学习让我意识到，精心设计的提示词能让 AI 的输出质量提升数倍。

2. **理论与实践结合**：光看理论不够，动手实验才能真正理解。通过对比实验，我清楚地看到了不同技巧的效果差异。

3. **Web3 + AI 的潜力**：作为一个有 DeFi 开发经验的开发者，我看到了 AI 在智能合约生成、安全审计、交易分析等场景的巨大潜力。

期待明天的 RAG 和 Agent 实践，特别想看看如何让 AI Agent 与链上数据交互！

---

**#AIWeb3School #Day1 #PromptEngineering #LearningInPublic**
