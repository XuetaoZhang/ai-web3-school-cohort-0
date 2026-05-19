# RAG 系统实验报告

**日期**: 2026-05-19  
**项目**: 基于 DeepSeek 的简单 RAG 系统  
**目标**: 理解 RAG 工作原理，构建能回答 Handbook 问题的系统

---

## 📋 项目概述

### 什么是 RAG？

RAG (Retrieval-Augmented Generation) 是一种通过检索外部知识来增强 LLM 回答能力的技术。

### 核心组件

1. **知识库** (`knowledge_base.py`)
   - 存储 AI × Web3 School Handbook 的文档摘要
   - 7 个主题文档

2. **向量数据库** (`vector_store.py`)
   - 使用 ChromaDB
   - 将文档转换为向量并存储
   - 支持语义相似度检索

3. **RAG 系统** (`rag_system.py`)
   - 集成 DeepSeek API
   - 实现完整的 RAG 工作流程

---

## 🔄 RAG 工作流程

```
用户提问
    ↓
向量数据库检索相关文档
    ↓
将文档作为上下文
    ↓
DeepSeek 基于上下文生成回答
    ↓
返回结果给用户
```

---

## 🛠️ 技术栈

- **LLM**: DeepSeek API (deepseek-chat)
- **向量数据库**: ChromaDB
- **Embedding**: ChromaDB 默认 embedding 函数
- **语言**: Python 3

---

## 📊 测试结果

### 测试问题 1
**问题**: 什么是 AI Agent？它有哪些核心组件？

**检索到的文档**:
- AI Agent 基础
- [其他相关文档]

**DeepSeek 回答**:
[待运行后填写]

---

### 测试问题 2
**问题**: RAG 的工作流程是什么？

**检索到的文档**:
- 检索增强生成（RAG）
- [其他相关文档]

**DeepSeek 回答**:
[待运行后填写]

---

### 测试问题 3
**问题**: Web3 Agent 钱包需要考虑哪些安全问题？

**检索到的文档**:
- Web3 Agent 钱包
- [其他相关文档]

**DeepSeek 回答**:
[待运行后填写]

---

## 💡 关键洞察

### 1. RAG 的优势
- ✅ 提供最新信息（知识库可更新）
- ✅ 减少幻觉（基于真实文档）
- ✅ 可追溯来源（知道信息来自哪里）
- ✅ 降低成本（无需重新训练模型）

### 2. 向量检索的重要性
- 语义相似度 > 关键词匹配
- Embedding 质量影响检索准确性
- n_results 参数需要权衡（太少信息不足，太多噪音增加）

### 3. Prompt 设计
- 明确要求基于参考资料回答
- 要求引用关键信息
- 处理参考资料不足的情况

---

## 🐛 遇到的问题

### 问题 1: sentence-transformers 依赖冲突
**现象**: pip 安装时报 torch 版本冲突

**解决方案**: 使用 ChromaDB 默认 embedding 函数，避免安装 sentence-transformers

**影响**: 无明显影响，默认 embedding 函数足够使用

---

### 问题 2: [待填写]
**现象**: 

**解决方案**: 

**影响**: 

---

## 🚀 改进思路

### 1. 提高检索质量
- [ ] 使用更好的 embedding 模型（如 BGE）
- [ ] 调整 chunk 大小
- [ ] 添加重排序（Reranking）

### 2. 扩展知识库
- [ ] 添加更多 Handbook 内容
- [ ] 支持动态更新
- [ ] 添加元数据过滤

### 3. 优化 Prompt
- [ ] 添加思维链（Chain of Thought）
- [ ] 要求引用具体段落
- [ ] 处理多跳推理

### 4. 用户体验
- [ ] 添加流式输出
- [ ] 显示检索到的文档标题
- [ ] 支持追问

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 文档数量 | 7 |
| 平均检索时间 | [待测试] |
| 平均生成时间 | [待测试] |
| 检索准确率 | [待评估] |

---

## 🎯 下一步

1. [ ] 运行完整测试
2. [ ] 记录实际输出
3. [ ] 评估检索质量
4. [ ] 尝试不同的问题
5. [ ] 优化参数

---

## 📝 使用说明

### 运行测试

```bash
cd ~/ai-web3-school-cohort-0/experiments/rag-system-deepseek
source venv/bin/activate
export DEEPSEEK_API_KEY=your_api_key
python rag_system.py
```

### 自定义问题

修改 `rag_system.py` 中的 `questions` 列表：

```python
questions = [
    "你的问题 1",
    "你的问题 2",
    "你的问题 3"
]
```

---

## 🔗 参考资源

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [ChromaDB 文档](https://docs.trychroma.com/)
- [RAG 论文](https://arxiv.org/abs/2005.11401)

---

**实验完成时间**: [待填写]  
**总耗时**: [待填写]
