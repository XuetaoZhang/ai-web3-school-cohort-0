import os
from openai import OpenAI
from vector_store import SimpleVectorStore
from knowledge_base import HANDBOOK_DOCS

class SimpleRAG:
    def __init__(self, api_key=None):
        # 初始化 DeepSeek 客户端（使用 OpenAI 兼容接口）
        self.client = OpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        # 初始化向量存储
        self.vector_store = SimpleVectorStore()
        self.vector_store.add_documents(HANDBOOK_DOCS)

    def query(self, question):
        """RAG 查询流程"""
        print(f"\n🤔 问题: {question}")

        # 1. 检索相关文档
        print("\n🔍 检索相关文档...")
        results = self.vector_store.search(question, n_results=2)

        # 2. 构建上下文
        context = "\n\n".join(results['documents'][0])
        print(f"\n📚 找到 {len(results['documents'][0])} 个相关文档")

        # 3. 构建 Prompt
        prompt = f"""基于以下参考资料回答问题。如果参考资料中没有相关信息，请说明。

参考资料：
{context}

问题：{question}

请用中文回答，并引用参考资料中的关键信息。"""

        # 4. 调用 DeepSeek
        print("\n🤖 DeepSeek 正在思考...")
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的 AI 助手，擅长基于参考资料回答问题。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        # 5. 返回结果
        print(f"\n💡 回答:\n{answer}")

        return {
            "question": question,
            "context": context,
            "answer": answer
        }

# 测试代码
if __name__ == "__main__":
    # 确保设置了 DEEPSEEK_API_KEY 环境变量
    # export DEEPSEEK_API_KEY=your_api_key

    rag = SimpleRAG()

    # 测试问题
    questions = [
        "什么是 AI Agent？它有哪些核心组件？",
        "RAG 的工作流程是什么？",
        "Web3 Agent 钱包需要考虑哪些安全问题？"
    ]

    for q in questions:
        rag.query(q)
        print("\n" + "="*80 + "\n")
