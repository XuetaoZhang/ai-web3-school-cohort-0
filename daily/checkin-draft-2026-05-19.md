# Day 2 打卡 - RAG 系统与 AI Agent 实践

## 📅 基本信息

- **日期**: 2026-05-19
- **Day**: 2/42
- **阶段**: Phase 1 - AI 基础强化

---

## 📚 今日学习内容

### 1. RAG (Retrieval-Augmented Generation) 系统

**核心概念**：
- RAG = 检索（Retrieval）+ 增强（Augmented）+ 生成（Generation）
- 通过检索外部知识库增强 LLM 的回答能力
- 解决 LLM 的知识时效性和幻觉问题

**实践成果**：
- ✅ 创建了 3 个版本的 RAG 系统：
  1. **关键词匹配版**：快速理解 RAG 流程
  2. **TF-IDF 向量版**：体验真正的向量检索（⭐ 推荐）
  3. **深度学习版**：生产级方案（需要 ChromaDB）
- ✅ 构建了 7 个 AI × Web3 主题知识库
- ✅ 实现了完整的检索→增强→生成流程

**技术栈**：
- DeepSeek API（国内可直接访问）
- scikit-learn（TF-IDF 向量化）
- Python 虚拟环境

---

### 2. AI Agent 与 Tool Use

**核心概念**：
- **Agent 公式**：Agent = LLM + Tools + Loop
- **Tool Use 流程**：定义工具 → LLM 决策 → 执行工具 → 整合结果
- **多步推理**：Agent 可以连续调用多个工具完成复杂任务

**实践成果**：
- ✅ 实现了 4 个工具：
  - `calculator` - 数学计算
  - `get_current_time` - 时间查询
  - `get_weather` - 天气查询
  - `search_knowledge` - 知识库搜索
- ✅ 创建了 3 个版本的 Agent：
  - **简单版**：演示单次工具调用
  - **多轮版**：支持连续调用多个工具
  - **交互式版**：实时对话体验
- ✅ 测试通过，工具调用准确

---

## 💡 关键洞察

### 🔥 重要发现：TF-IDF 的局限性

在测试向量检索时，我发现了一个重要问题：

**案例**：
```
查询："Embedding 向量嵌入有什么用途？"
文档："Embedding 向量嵌入"
TF-IDF 相似度：0.3482（很低！）
```

**更极端的案例**：
```
"Embedding 是什么" vs "向量嵌入是什么"
TF-IDF 相似度：0.15（几乎不相关！）
实际含义：完全相同
```

**原因分析**：
1. **词袋模型**：TF-IDF 只看字符匹配，不理解语义
2. **无法识别近义词**："用途" vs "作用"
3. **无法识别翻译关系**："Embedding" vs "向量嵌入"
4. **文档长度敏感**：长短文档相似度偏低

**解决方案**：
- 生产环境需要深度学习 Embedding（如 sentence-transformers）
- 深度学习模型可以理解语义，相似度可达 0.85+

**收获**：
- 培养了批判性思维：不盲目接受结果，质疑"为什么"
- 通过实验验证假设
- 理解算法的工作原理和局限性

---

### Agent 的工作原理

**核心机制**：
```
用户提问
    ↓
LLM 分析意图
    ↓
决定是否调用工具
    ↓
执行工具函数
    ↓
LLM 整合结果
    ↓
返回最终答案
```

**关键点**：
1. **必须提前告诉 Agent 有哪些工具**：LLM 无法主动发现工具
2. **工具定义很重要**：清晰的描述决定 LLM 的决策准确性
3. **多步推理**：通过循环机制实现连续工具调用

---

## 🛠️ 技术实践

### 项目结构

```
experiments/
├── PRACTICE-GUIDE-DEEPSEEK.md      # DeepSeek 版本实践指南
├── rag-system-deepseek/            # RAG 系统
│   ├── knowledge_base.py           # 知识库定义
│   ├── rag_simple.py               # 关键词匹配版
│   ├── rag_vector.py               # TF-IDF 向量版 ⭐
│   ├── rag_system.py               # 深度学习版
│   ├── QUICKSTART.md               # 快速开始
│   ├── RETRIEVAL-COMPARISON.md     # 检索方式对比
│   └── tfidf_limitation_simple.py  # TF-IDF 局限性演示
└── ai-agent-deepseek/              # AI Agent 系统
    ├── tools.py                    # 工具定义
    ├── agent_simple.py             # 简单版 Agent
    ├── agent_multi.py              # 多轮对话版
    ├── agent_interactive.py        # 交互式版
    ├── QUICKSTART.md               # 快速开始
    └── README.md                   # 实验报告
```

### 代码亮点

**1. TF-IDF 向量检索实现**：
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 向量化
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1,3))
doc_vectors = vectorizer.fit_transform(documents)

# 计算相似度
query_vector = vectorizer.transform([query])
similarities = cosine_similarity(query_vector, doc_vectors)[0]

# 排序检索
top_indices = similarities.argsort()[-top_k:][::-1]
```

**2. Agent 多步推理实现**：
```python
while True:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOL_DEFINITIONS
    )
    
    if response.choices[0].message.tool_calls:
        # 执行工具
        for tool_call in response.choices[0].message.tool_calls:
            result = execute_tool(tool_call)
            messages.append(result)
        continue  # 继续循环
    else:
        return response.choices[0].message.content  # 返回最终答案
```

---

## 🎯 完成情况

- [x] 构建 RAG 系统（3 个版本）
- [x] 创建 AI Agent（3 个版本，4 个工具）
- [x] 理解 Tool Use 工作流程
- [x] 发现并分析 TF-IDF 局限性
- [x] 测试 Agent 系统（工具调用准确）
- [x] 更新学习笔记
- [x] 提交代码到 GitHub

**代码统计**：
- 创建文件：17 个
- 代码行数：1500+ 行
- Git 提交：4 次

---

## 🤔 思考与问题

### 已解决的问题

1. **向量检索 vs 关键词匹配**：
   - ✅ 通过实验发现 TF-IDF 无法识别近义词和翻译关系
   - ✅ 理解了深度学习 Embedding 的必要性

2. **Agent 的工具发现机制**：
   - ✅ 必须提前告诉 Agent 有哪些工具
   - ✅ LLM 无法主动发现工具（安全性和可控性考虑）

### 待探索的问题

1. **Embedding 模型选择**：不同模型对检索质量的影响？
2. **RAG 优化**：文档切片策略、Top-K 选择、重排序？
3. **Agent 决策机制**：LLM 如何选择工具？工具描述的影响？
4. **RAG + Agent**：如何结合使用？

---

## 📈 学习收获

### 技术能力

1. ✅ 掌握了 RAG 的完整工作流程
2. ✅ 理解了向量检索的原理和局限性
3. ✅ 掌握了 AI Agent 的核心机制
4. ✅ 学会了 Tool Use (Function Calling)
5. ✅ 熟悉了 DeepSeek API 的使用

### 思维方式

1. ✅ **批判性思维**：质疑不合理的结果，通过实验验证
2. ✅ **问题解决能力**：遇到依赖冲突，用简化方案替代
3. ✅ **渐进式学习**：从简单到复杂，逐步理解核心概念
4. ✅ **实践优先**：不被工具阻塞，先实现核心功能

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/XuetaoZhang/ai-web3-school-cohort-0
- **学习笔记**: `daily/2026-05-19.md`
- **RAG 快速开始**: `experiments/rag-system-deepseek/QUICKSTART.md`
- **Agent 快速开始**: `experiments/ai-agent-deepseek/QUICKSTART.md`
- **检索方式对比**: `experiments/rag-system-deepseek/RETRIEVAL-COMPARISON.md`

---

## 💭 今日反思

今天完成了两个重要的实践：RAG 系统和 AI Agent。

**最大的收获**是发现了 TF-IDF 的局限性。当我看到 "Embedding 向量嵌入有什么用途？" 和 "Embedding 向量嵌入" 的相似度只有 0.35 时，我的第一反应是"这不对"。通过深入分析和实验验证，我理解了 TF-IDF 作为词袋模型的本质局限：它只看字符匹配，不理解语义。这让我深刻体会到**批判性思维**的重要性——不盲目接受结果，而是质疑、验证、理解。

**Agent 的实践**让我理解了 LLM 的能力边界。LLM 本身只能基于训练数据回答问题，但通过 Tool Use，它可以调用外部工具获取实时信息、执行计算、查询数据库。这种"LLM + Tools + Loop"的模式，让 AI 从"知识库"变成了"行动者"。

**技术选型的灵活性**也是重要的一课。遇到 ChromaDB 依赖冲突时，我没有死磕，而是用 TF-IDF 实现了向量检索的核心流程。虽然 TF-IDF 有局限性，但它帮助我理解了向量检索的本质：向量化 → 相似度计算 → 排序。理解原理后，再升级到深度学习方案就水到渠成了。

明天计划深入学习 Embedding 模型和 RAG 优化技术，同时开始思考如何将 RAG 和 Agent 结合起来，构建更强大的 AI 应用。

---

**Time Spent / 时间投入**: 约 4 小时
- RAG 系统：2 小时
- AI Agent：1.5 小时
- 文档整理：0.5 小时
