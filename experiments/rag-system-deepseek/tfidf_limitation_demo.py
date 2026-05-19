"""
TF-IDF 局限性演示

展示为什么 "Embedding 向量嵌入有什么用途？" 和 "Embedding 向量嵌入"
相似度只有 0.3482
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

def analyze_similarity(text1, text2):
    """分析两个文本的相似度"""

    print(f"\n{'='*80}")
    print(f"文本1: {text1}")
    print(f"文本2: {text2}")
    print(f"{'='*80}")

    # 1. 分词
    words1 = list(jieba.cut(text1))
    words2 = list(jieba.cut(text2))

    print(f"\n📝 分词结果:")
    print(f"  文本1: {words1}")
    print(f"  文本2: {words2}")

    # 找出共同词和不同词
    set1 = set(words1)
    set2 = set(words2)
    common = set1 & set2
    only1 = set1 - set2
    only2 = set2 - set1

    print(f"\n🔍 词汇分析:")
    print(f"  共同词: {common}")
    print(f"  只在文本1: {only1}")
    print(f"  只在文本2: {only2}")
    print(f"  匹配率: {len(common)}/{len(set1)} = {len(common)/len(set1)*100:.1f}%")

    # 2. TF-IDF 向量化
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # 获取特征名（词汇表）
    feature_names = vectorizer.get_feature_names_out()

    print(f"\n📊 TF-IDF 向量化:")
    print(f"  词汇表大小: {len(feature_names)}")
    print(f"  词汇表: {list(feature_names)}")

    # 显示每个词的 TF-IDF 权重
    vec1 = vectors[0].toarray()[0]
    vec2 = vectors[1].toarray()[0]

    print(f"\n⚖️  TF-IDF 权重:")
    for i, word in enumerate(feature_names):
        if vec1[i] > 0 or vec2[i] > 0:
            print(f"  '{word}': 文本1={vec1[i]:.4f}, 文本2={vec2[i]:.4f}")

    # 3. 计算相似度
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    print(f"\n🎯 余弦相似度: {similarity:.4f}")

    # 解释相似度
    if similarity > 0.8:
        level = "非常高 ✅"
    elif similarity > 0.6:
        level = "高 ✅"
    elif similarity > 0.4:
        level = "中等 ⚠️"
    elif similarity > 0.2:
        level = "低 ❌"
    else:
        level = "非常低 ❌"

    print(f"  相似度等级: {level}")

    return similarity


def main():
    print("=" * 80)
    print("TF-IDF 局限性演示")
    print("=" * 80)

    # 案例1：你发现的问题
    print("\n\n【案例 1】你发现的问题")
    analyze_similarity(
        "Embedding 向量嵌入有什么用途？",
        "Embedding 向量嵌入"
    )

    print("\n\n💡 为什么相似度低？")
    print("  1. 问题有 7 个词，回答只有 3 个词")
    print("  2. '有'、'什么'、'用途' 这些词在回答中不存在")
    print("  3. TF-IDF 只看词的匹配，不理解语义")
    print("  4. 向量在不同维度上的分布差异大")

    # 案例2：完全匹配
    print("\n\n【案例 2】完全匹配（对照组）")
    analyze_similarity(
        "Embedding 向量嵌入",
        "Embedding 向量嵌入"
    )

    # 案例3：近义词
    print("\n\n【案例 3】近义词（TF-IDF 的盲区）")
    analyze_similarity(
        "Embedding 有什么用途？",
        "Embedding 有什么作用？"
    )

    print("\n\n💡 观察:")
    print("  '用途' 和 '作用' 是近义词，但 TF-IDF 认为它们完全不同！")

    # 案例4：中英文混合
    print("\n\n【案例 4】中英文翻译（TF-IDF 的盲区）")
    analyze_similarity(
        "Embedding 是什么？",
        "向量嵌入是什么？"
    )

    print("\n\n💡 观察:")
    print("  'Embedding' 和 '向量嵌入' 是同一个概念，但 TF-IDF 认为它们不相关！")

    # 案例5：长度影响
    print("\n\n【案例 5】文档长度影响")
    analyze_similarity(
        "Embedding",
        "Embedding 是一种将文本转换为向量的技术，广泛应用于自然语言处理"
    )

    print("\n\n💡 观察:")
    print("  即使都包含 'Embedding'，长度差异也会导致相似度下降！")

    # 总结
    print("\n\n" + "=" * 80)
    print("📚 TF-IDF 的局限性总结")
    print("=" * 80)
    print("""
1. ❌ 词袋模型：只看词的出现，不理解含义
   - "用途" ≠ "作用"（实际上是近义词）
   - "Embedding" ≠ "向量嵌入"（实际上是翻译）

2. ❌ 无法处理多语言：中英文混合时失效
   - 无法识别翻译关系
   - 无法跨语言匹配

3. ❌ 文档长度敏感：长短文档相似度偏低
   - 短文档向量稀疏
   - 长文档向量分散

4. ❌ 无上下文理解：不理解查询意图
   - "Embedding 用途" vs "Embedding 原理"
   - TF-IDF 认为几乎一样（都有 Embedding）

5. ✅ 优点：简单、快速、无需训练
   - 适合快速原型
   - 适合英文单语场景
   - 适合关键词检索

💡 解决方案：使用深度学习 Embedding
   - sentence-transformers
   - OpenAI Embeddings
   - 多语言预训练模型
""")

    print("\n" + "=" * 80)
    print("🎓 学习要点")
    print("=" * 80)
    print("""
你发现的问题非常关键！这正是为什么：

1. TF-IDF 适合：
   ✅ 快速原型和概念验证
   ✅ 英文单语、专业术语检索
   ✅ 关键词精确匹配场景

2. 深度学习 Embedding 适合：
   ✅ 语义理解（近义词、翻译）
   ✅ 多语言混合场景
   ✅ 生产环境的 RAG 系统

3. 你的观察说明：
   ✅ 你真正理解了向量检索的原理
   ✅ 你发现了 TF-IDF 的核心局限
   ✅ 你准备好学习更高级的 Embedding 了！
""")


if __name__ == "__main__":
    main()
