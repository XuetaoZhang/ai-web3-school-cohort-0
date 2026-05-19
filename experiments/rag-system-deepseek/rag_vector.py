"""
真正的 RAG 系统 - 使用 TF-IDF 向量化
体验完整的 RAG 流程：文档切片 → 向量化 → 相似度匹配 → 排序
"""

import os
import numpy as np
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import HANDBOOK_DOCS

class VectorRAG:
    def __init__(self, api_key=None):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        # 初始化向量化器（TF-IDF）
        self.vectorizer = TfidfVectorizer(
            max_features=1000,  # 最多保留 1000 个特征
            ngram_range=(1, 2),  # 使用 1-gram 和 2-gram
            stop_words=None  # 不过滤停用词（中文需要分词）
        )

        # 存储文档
        self.documents = HANDBOOK_DOCS
        self.doc_contents = [doc['content'] for doc in self.documents]
        self.doc_titles = [doc['title'] for doc in self.documents]

        # 向量化所有文档
        print("🔄 正在向量化知识库...")
        self.doc_vectors = self.vectorizer.fit_transform(self.doc_contents)
        print(f"✅ 向量化完成！文档数量: {len(self.documents)}, 向量维度: {self.doc_vectors.shape[1]}")

    def search(self, query, n_results=2):
        """
        向量检索流程：
        1. 将查询向量化
        2. 计算与所有文档的余弦相似度
        3. 排序并返回最相关的文档
        """
        print(f"\n🔍 检索流程:")

        # Step 1: 向量化查询
        print(f"  1️⃣ 向量化查询: '{query}'")
        query_vector = self.vectorizer.transform([query])
        print(f"     查询向量维度: {query_vector.shape}")

        # Step 2: 计算余弦相似度
        print(f"  2️⃣ 计算与所有文档的余弦相似度...")
        similarities = cosine_similarity(query_vector, self.doc_vectors)[0]
        print(f"     相似度分数: {similarities}")

        # Step 3: 排序
        print(f"  3️⃣ 按相似度排序...")
        top_indices = np.argsort(similarities)[::-1][:n_results]

        # Step 4: 返回结果
        results = []
        print(f"\n📊 检索结果:")
        for rank, idx in enumerate(top_indices, 1):
            doc = self.documents[idx]
            score = similarities[idx]
            results.append({
                'document': doc,
                'score': score
            })
            print(f"  #{rank} [{doc['title']}] 相似度: {score:.4f}")

        return results

    def query(self, question):
        """完整的 RAG 查询流程"""
        print(f"\n{'='*80}")
        print(f"🤔 问题: {question}")
        print(f"{'='*80}")

        # 1. 向量检索
        results = self.search(question, n_results=2)

        # 2. 构建上下文
        context_parts = []
        for i, result in enumerate(results, 1):
            doc = result['document']
            score = result['score']
            context_parts.append(f"【文档 {i}: {doc['title']}】(相似度: {score:.4f})\n{doc['content']}")

        context = "\n\n".join(context_parts)

        # 3. 构建 Prompt
        prompt = f"""基于以下参考资料回答问题。参考资料按相关性排序，相似度分数越高越相关。

参考资料：
{context}

问题：{question}

请用中文回答，并引用参考资料中的关键信息。如果参考资料不足以回答问题，请说明。"""

        # 4. 调用 DeepSeek
        print(f"\n🤖 DeepSeek 正在思考...")
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
            print(f"\n💡 回答:")
            print(f"{answer}")
            print(f"\n{'='*80}\n")

            return {
                "question": question,
                "retrieved_docs": results,
                "answer": answer
            }
        except Exception as e:
            print(f"\n❌ API 调用失败: {e}")
            print("\n💡 提示: 请确保已设置 DEEPSEEK_API_KEY 环境变量")
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
    print("🚀 启动向量化 RAG 系统...\n")

    # 创建 RAG 系统
    rag = VectorRAG()

    print("\n" + "="*80)
    print("📚 RAG 系统说明")
    print("="*80)
    print("本系统使用 TF-IDF 向量化 + 余弦相似度进行文档检索")
    print("虽然不是深度学习的 embedding，但能体验完整的 RAG 流程：")
    print("  1️⃣ 文档向量化（TF-IDF）")
    print("  2️⃣ 查询向量化")
    print("  3️⃣ 相似度计算（余弦相似度）")
    print("  4️⃣ 排序和检索")
    print("  5️⃣ LLM 生成回答")
    print("="*80)

    # 测试问题
    questions = [
        "什么是 AI Agent？它有哪些核心组件？",
        "RAG 的工作流程是什么？",
        "Web3 Agent 钱包需要考虑哪些安全问题？",
        "什么是 Context 上下文窗口？",
        "Embedding 向量嵌入有什么用途？"
    ]

    for q in questions:
        result = rag.query(q)
        if not result:
            break
