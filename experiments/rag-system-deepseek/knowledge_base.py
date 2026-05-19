"""
简单的知识库：AI × Web3 School Handbook 摘要
"""

HANDBOOK_DOCS = [
    {
        "id": "llm-1",
        "title": "什么是大语言模型",
        "content": """
        大语言模型（LLM）是基于 Transformer 架构的深度学习模型，
        通过在海量文本数据上训练，学习语言的模式和知识。
        LLM 的核心能力包括：文本生成、理解、翻译、总结等。
        常见的 LLM 包括：GPT-4、Claude、DeepSeek、Llama 等。
        """
    },
    {
        "id": "prompt-1",
        "title": "Prompt Engineering 基础",
        "content": """
        Prompt Engineering 是设计有效提示词的技术。
        关键技巧包括：
        1. 清晰的指令
        2. 提供上下文
        3. Few-shot 示例
        4. 输出格式约束
        5. 角色设定
        """
    },
    {
        "id": "agent-1",
        "title": "AI Agent 基础",
        "content": """
        AI Agent 是能够感知环境、做出决策并执行行动的智能系统。
        Agent 的核心组件：
        1. LLM（推理引擎）
        2. Tools（工具集）
        3. Memory（记忆系统）
        4. Planning（规划能力）
        """
    },
    {
        "id": "rag-1",
        "title": "检索增强生成（RAG）",
        "content": """
        RAG 通过检索外部知识来增强 LLM 的回答能力。
        工作流程：
        1. 用户提问
        2. 检索相关文档
        3. 将文档作为上下文提供给 LLM
        4. LLM 基于上下文生成回答
        """
    },
    {
        "id": "web3-agent-1",
        "title": "Web3 Agent 钱包",
        "content": """
        Web3 Agent 需要钱包来执行链上操作。
        关键考虑：
        1. 权限管理（Session Key）
        2. 额度限制
        3. 时间限制
        4. 操作白名单
        5. 多签验证
        """
    },
    {
        "id": "context-1",
        "title": "Context 上下文窗口",
        "content": """
        Context 是 LLM 能够处理的输入文本长度。
        不同模型的 Context 长度不同：
        - GPT-4: 8K-128K tokens
        - Claude: 200K tokens
        - DeepSeek: 64K tokens
        Context 管理策略：
        1. 滑动窗口
        2. 摘要压缩
        3. 检索增强（RAG）
        """
    },
    {
        "id": "embedding-1",
        "title": "Embedding 向量嵌入",
        "content": """
        Embedding 是将文本转换为数值向量的技术。
        用途：
        1. 语义相似度计算
        2. 文档检索
        3. 聚类分析
        常见模型：
        - OpenAI text-embedding-ada-002
        - Sentence-BERT
        - BGE 系列
        """
    }
]
