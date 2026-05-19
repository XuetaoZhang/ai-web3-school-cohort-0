import chromadb

class SimpleVectorStore:
    def __init__(self):
        # 初始化 ChromaDB（使用内存模式）
        self.client = chromadb.Client()

        # 创建或获取集合（使用默认的 embedding 函数，避免依赖 sentence-transformers）
        self.collection = self.client.get_or_create_collection(
            name="handbook"
        )

    def add_documents(self, documents):
        """添加文档到向量数据库"""
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [{"title": doc["title"]} for doc in documents]

        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )
        print(f"✅ 已添加 {len(documents)} 个文档到向量数据库")

    def search(self, query, n_results=2):
        """检索相关文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results

# 测试代码
if __name__ == "__main__":
    from knowledge_base import HANDBOOK_DOCS

    # 创建向量存储
    store = SimpleVectorStore()

    # 添加文档
    store.add_documents(HANDBOOK_DOCS)

    # 测试检索
    query = "什么是 AI Agent？"
    results = store.search(query)

    print(f"\n🔍 查询: {query}")
    print(f"\n📄 检索到的文档:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\n--- 文档 {i+1} ---")
        print(doc)
