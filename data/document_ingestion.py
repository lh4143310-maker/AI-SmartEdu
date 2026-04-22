"""
文档数据导入脚本
将课程介绍、知识点解释等非结构化内容导入 ChromaDB，用于 RAG 检索
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from tqdm import tqdm
from config.config import MYSQL_CONFIG, VECTOR_STORE_DIR
from config.dependency import embedding_model
import chromadb


def get_mysql_connection():
    """获取MySQL连接"""
    return pymysql.connect(**MYSQL_CONFIG)


def fetch_course_documents():
    """从MySQL获取课程文档数据"""
    documents = []
    
    with get_mysql_connection() as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 获取课程详细信息
            cursor.execute("""
                SELECT 
                    c.id as course_id,
                    c.course_name,
                    c.course_introduce,
                    c.teacher,
                    s.subject_name,
                    cat.category_name
                FROM smart_edu.course_info c
                LEFT JOIN smart_edu.base_subject_info s ON c.subject_id = s.id
                LEFT JOIN smart_edu.base_category_info cat ON s.category_id = cat.id
                WHERE c.course_introduce IS NOT NULL AND c.course_introduce != ''
            """)
            
            for row in cursor.fetchall():
                # 构建课程文档
                doc_content = f"""课程名称：{row['course_name']}
所属分类：{row['category_name']}
所属学科：{row['subject_name']}
授课教师：{row['teacher']}
课程介绍：{row['course_introduce']}"""
                
                documents.append({
                    "id": f"course_{row['course_id']}",
                    "content": doc_content,
                    "metadata": {
                        "type": "course_introduction",
                        "course_id": row['course_id'],
                        "course_name": row['course_name'],
                        "subject": row['subject_name'],
                        "category": row['category_name']
                    }
                })
            
            print(f"获取到 {len(documents)} 条课程文档")
            
            # 获取章节信息作为补充文档
            cursor.execute("""
                SELECT 
                    ch.id as chapter_id,
                    ch.chapter_name,
                    c.course_name,
                    c.id as course_id
                FROM smart_edu.chapter_info ch
                JOIN smart_edu.course_info c ON ch.course_id = c.id
            """)
            
            chapter_count = 0
            for row in cursor.fetchall():
                doc_content = f"课程《{row['course_name']}》的章节：{row['chapter_name']}"
                documents.append({
                    "id": f"chapter_{row['chapter_id']}",
                    "content": doc_content,
                    "metadata": {
                        "type": "chapter_info",
                        "chapter_id": row['chapter_id'],
                        "chapter_name": row['chapter_name'],
                        "course_id": row['course_id'],
                        "course_name": row['course_name']
                    }
                })
                chapter_count += 1
            
            print(f"获取到 {chapter_count} 条章节文档")
            
    return documents


def ingest_documents_to_chroma(documents, batch_size=32):
    """将文档导入ChromaDB"""
    
    # 初始化ChromaDB客户端
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    
    # 获取或创建集合
    try:
        collection = client.get_collection("edu_documents")
        print("使用已存在的文档集合")
    except Exception:
        collection = client.create_collection("edu_documents")
        print("创建新的文档集合")
    
    # 获取已存在的文档ID
    existing_ids = set(collection.get()["ids"])
    
    # 过滤掉已存在的文档
    new_documents = [doc for doc in documents if doc["id"] not in existing_ids]
    
    if not new_documents:
        print("没有新文档需要导入")
        return
    
    print(f"准备导入 {len(new_documents)} 条新文档")
    
    # 批量处理
    for i in tqdm(range(0, len(new_documents), batch_size), desc="导入文档"):
        batch = new_documents[i:i + batch_size]
        
        ids = [doc["id"] for doc in batch]
        contents = [doc["content"] for doc in batch]
        metadatas = [doc["metadata"] for doc in batch]
        
        # 生成嵌入向量
        embeddings = embedding_model.embed_documents(contents)
        
        # 添加到集合
        collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas,
            embeddings=embeddings
        )
    
    print(f"成功导入 {len(new_documents)} 条文档")
    print(f"文档集合当前共有 {collection.count()} 条文档")


def search_documents(query, top_k=3):
    """测试文档检索"""
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    collection = client.get_collection("edu_documents")
    
    query_embedding = embedding_model.embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    print(f"\n查询：{query}")
    print(f"找到 {len(results['ids'][0])} 条相关文档：\n")
    
    for i in range(len(results["ids"][0])):
        doc = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        similarity = 1 - distance
        
        print(f"[{i+1}] 相似度: {similarity:.4f}")
        print(f"类型: {metadata['type']}")
        print(f"内容: {doc[:200]}...")
        print("-" * 50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="文档数据导入和检索工具")
    parser.add_argument("--ingest", action="store_true", help="导入文档数据")
    parser.add_argument("--search", type=str, help="测试检索，传入查询文本")
    parser.add_argument("--top_k", type=int, default=3, help="检索返回数量")
    
    args = parser.parse_args()
    
    if args.ingest:
        print("开始导入文档数据...")
        documents = fetch_course_documents()
        ingest_documents_to_chroma(documents)
    
    elif args.search:
        search_documents(args.search, args.top_k)
    
    else:
        print("请指定操作：--ingest 导入数据 或 --search '查询文本' 测试检索")
