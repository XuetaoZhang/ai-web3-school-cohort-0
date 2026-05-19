# 快速开始指南

## 🚀 运行 RAG 系统

### 选择版本

我们提供了三个版本，从简单到完整：

| 版本 | 文件 | 检索方式 | 推荐度 |
|------|------|---------|--------|
| **简化版** | `rag_simple.py` | 关键词匹配 | ⭐⭐ 理解概念 |
| **向量版** | `rag_vector.py` | TF-IDF + 余弦相似度 | ⭐⭐⭐⭐⭐ **强烈推荐** |
| **完整版** | `rag_system.py` | 深度学习 Embedding | ⭐⭐⭐ 需要 ChromaDB |

**推荐使用 `rag_vector.py`**：体验真正的向量检索流程！

详细对比请查看：[RETRIEVAL-COMPARISON.md](./RETRIEVAL-COMPARISON.md)

---

### 1. 获取 DeepSeek API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并登录
3. 进入 **API Keys** 页面
4. 点击 **创建新的 API Key**
5. 复制 API Key（只显示一次，请妥善保存）

### 2. 设置环境变量

在终端中运行：

```bash
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

**提示**：将 `sk-xxxxxxxxxxxxxxxx` 替换为你的实际 API Key

### 3. 运行 RAG 系统

#### 推荐：向量版本（体验真正的 RAG）

```bash
cd ~/ai-web3-school-cohort-0/experiments/rag-system-deepseek
source venv/bin/activate
python rag_vector.py
```

**你会看到**：
- 🔄 文档向量化过程
- 📊 每个文档的相似度分数
- 🎯 检索结果排序
- 💡 DeepSeek 的回答

#### 或者：简化版本（快速理解概念）

```bash
python rag_simple.py
```

### 4. 预期输出

#### 向量版本输出示例

```
🔄 正在向量化知识库...
✅ 向量化完成！文档数量: 7, 向量维度: 1000

================================================================================
🤔 问题: 什么是 AI Agent？它有哪些核心组件？
================================================================================

🔍 检索流程:
  1️⃣ 向量化查询: '什么是 AI Agent？它有哪些核心组件？'
     查询向量维度: (1, 1000)
  2️⃣ 计算与所有文档的余弦相似度...
     相似度分数: [0.1234 0.8523 0.2341 0.1567 0.0892 0.1123 0.1890]
  3️⃣ 按相似度排序...

📊 检索结果:
  #1 [AI Agent 基础] 相似度: 0.8523
  #2 [检索增强生成（RAG）] 相似度: 0.2341

🤖 DeepSeek 正在思考...

💡 回答:
根据参考资料，AI Agent 是能够感知环境、做出决策并执行行动的智能系统...
```

**关键信息**：
- ✅ 看到向量维度（1000 维）
- ✅ 看到每个文档的相似度分数
- ✅ 理解为什么选择这些文档
- ✅ 体验完整的向量检索流程

#### 简化版本输出

系统会自动测试 3 个问题：

1. **什么是 AI Agent？它有哪些核心组件？**
2. **RAG 的工作流程是什么？**
3. **Web3 Agent 钱包需要考虑哪些安全问题？**

每个问题的输出包括：
- 🔍 检索到的相关文档
- 🤖 DeepSeek 的回答

---

## 📝 自定义测试

### 修改测试问题

编辑 `rag_simple.py` 文件，找到 `questions` 列表：

```python
questions = [
    "你的问题 1",
    "你的问题 2",
    "你的问题 3"
]
```

### 添加更多文档

编辑 `knowledge_base.py` 文件，在 `HANDBOOK_DOCS` 列表中添加：

```python
{
    "id": "your-doc-id",
    "title": "文档标题",
    "content": """
    文档内容...
    """
}
```

---

## 🐛 常见问题

### 问题 1: ModuleNotFoundError: No module named 'openai'

**原因**: 虚拟环境未激活或依赖未安装

**解决方案**:
```bash
cd ~/ai-web3-school-cohort-0/experiments/rag-system-deepseek
source venv/bin/activate
pip install openai
```

### 问题 2: API 调用失败

**原因**: API Key 未设置或无效

**解决方案**:
1. 检查 API Key 是否正确
2. 确保已设置环境变量：`echo $DEEPSEEK_API_KEY`
3. 检查 API Key 是否有余额

### 问题 3: 网络连接错误

**原因**: 无法访问 DeepSeek API

**解决方案**:
1. 检查网络连接
2. DeepSeek API 在国内可直接访问，无需代理

---

## 📊 项目结构

```
rag-system-deepseek/
├── venv/                    # 虚拟环境
├── knowledge_base.py        # 知识库（7个文档）
├── rag_simple.py           # 简化版 RAG 系统（推荐）
├── vector_store.py         # 向量数据库（需要 ChromaDB）
├── rag_system.py           # 完整版 RAG 系统（需要 ChromaDB）
├── README.md               # 实验报告
└── QUICKSTART.md           # 本文件
```

**推荐使用**: `rag_simple.py` - 无需安装 ChromaDB，使用简单的关键词匹配

---

## 🎯 下一步

完成 RAG 系统测试后：

1. ✅ 记录测试结果到 `README.md`
2. ✅ 更新学习笔记 `daily/2026-05-19.md`
3. ✅ 提交代码到 GitHub
4. ✅ 继续实践 3：创建 AI Agent

---

## 💡 学习要点

### RAG 的核心流程

1. **检索** (Retrieval)
   - 根据用户问题检索相关文档
   - 使用向量相似度或关键词匹配

2. **增强** (Augmented)
   - 将检索到的文档作为上下文
   - 构建完整的 Prompt

3. **生成** (Generation)
   - LLM 基于上下文生成回答
   - 减少幻觉，提高准确性

### 为什么使用 RAG？

- ✅ **最新信息**: 知识库可随时更新
- ✅ **减少幻觉**: 基于真实文档回答
- ✅ **可追溯**: 知道信息来源
- ✅ **成本低**: 无需重新训练模型

---

## 📚 参考资源

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [RAG 论文](https://arxiv.org/abs/2005.11401)
- [实践指南](./PRACTICE-GUIDE-DEEPSEEK.md)

---

**祝学习愉快！** 🎉
