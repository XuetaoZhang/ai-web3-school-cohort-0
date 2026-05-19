"""
简化版 RAG 系统 - 不依赖向量数据库
使用简单的关键词匹配进行检索
"""

import os
from openai import OpenAI
from knowledge_base import HANDBOOK_DOCS

class SimpleRAGWithoutVectorDB:
    def __init__(self, api_key=None):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        # 直接使用知识库
        self.documents = HANDBOOK_DOCS

    def simple_search(self, query, n_results=2):
        """简单的关键词匹配检索"""
        # 计算每个文档与查询的相关性（简单的关键词匹配）
        scores = []
        query_lower = query.lower()

        for doc in self.documents:
            # 计算查询词在文档中出现的次数
            content_lower = doc['content'].lower()
            title_lower = doc['title'].lower()

            # 标题匹配权重更高
            score = content_lower.count(query_lower) + title_lower.count(query_lower) * 3

            # 也检查查询中的关键词
            keywords = ['agent', 'rag', 'prompt', 'llm', 'web3', '钱包', '上下文', 'embedding']
            for keyword in keywords:
                if keyword in query_lower:
                    score += content_lower.count(keyword) * 2

            scores.append((doc, score))

        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)

        # 返回前 n_results 个文档
        return [doc for doc, score in scores[:n_results]]

    def query(self, question):
        """RAG 查询流程"""
        print(f"\n🤔 问题: {question}")

        # 1. 检索相关文档
        print("\n🔍 检索相关文档...")
        relevant_docs = self.simple_search(question, n_results=2)

        # 2. 构建上下文
        context = "\n\n".join([f"【{doc['title']}】\n{doc['content']}" for doc in relevant_docs])
        print(f"\n📚 找到 {len(relevant_docs)} 个相关文档:")
        for doc in relevant_docs:
            print(f"  - {doc['title']}")

        # 3. 构建 Prompt
        prompt = f"""基于以下参考资料回答问题。如果参考资料中没有相关信息，请说明。

参考资料：
{context}

问题：{question}

请用中文回答，并引用参考资料中的关键信息。"""

        # 4. 调用 DeepSeek
        print("\n🤖 DeepSeek 正在思考...")
        try:
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
        except Exception as e:
            print(f"\n❌ API 调用失败: {e}")
            print("\n💡 提示: 请确保已设置 DEEPSEEK_API_KEY 环境变量")
            print("   export DEEPSEEK_API_KEY=your_api_key")
            return None

# 测试代码
if __name__ == "__main__":
    # 检查 API Key
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("⚠️  未检测到 DEEPSEEK_API_KEY 环境变量")
        print("\n请先设置 API Key:")
        print("  export DEEPSEEK_API_KEY=your_api_key")
        print("\n然后重新运行此脚本")
        exit(1)

    print("✅ 检测到 DEEPSEEK_API_KEY")
    print("🚀 启动简化版 RAG 系统...\n")

    rag = SimpleRAGWithoutVectorDB()

    # 测试问题
    questions = [
        "什么是 AI Agent？它有哪些核心组件？",
        "RAG 的工作流程是什么？",
        "Web3 Agent 钱包需要考虑哪些安全问题？"
    ]

    for q in questions:
        result = rag.query(q)
        if result:
            print("\n" + "="*80 + "\n")
