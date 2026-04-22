import neo4j
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from config.config import MYSQL_CONFIG, NEO4J_CONFIG, WEB_STATIC_DIR, EMBEDDING_MODEL_PATH, VECTOR_STORE_DIR, AGENT_WITH_MEMORY, AGENT_STREAM_OUTPUT
from langchain_neo4j import Neo4jGraph
from langchain_huggingface import HuggingFaceEmbeddings

# 尝试连接Neo4j数据库
try:
    neo4j_driver = neo4j.GraphDatabase.driver(uri=NEO4J_CONFIG["uri"], auth=NEO4J_CONFIG["auth"])
    # 测试连接
    with neo4j_driver.session() as session:
        session.run("RETURN 1")
    logging.info("Neo4j数据库连接成功！")
except Exception as e:
    neo4j_driver = None
    logging.warning(f"Neo4j数据库连接失败: {e}")
    logging.warning("项目将在没有Neo4j的情况下运行，某些功能可能不可用")

# 尝试获取Neo4j schema
try:
    neo4j_schema = Neo4jGraph(
        url=NEO4J_CONFIG["uri"],
        username=NEO4J_CONFIG["auth"][0],
        password=NEO4J_CONFIG["auth"][1],
        database="neo4j"
    ).get_schema
    logging.info("Neo4j schema获取成功！")
except Exception as e:
    neo4j_schema = lambda: "Neo4j schema unavailable"
    logging.warning(f"Neo4j schema获取失败: {e}")

# 加载嵌入模型
try:
    # 自动检测设备，优先使用 CUDA，否则使用 CPU
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedding_model = HuggingFaceEmbeddings(model_name=str(EMBEDDING_MODEL_PATH), model_kwargs={"device": device})
    logging.info(f"嵌入模型加载成功！使用设备: {device}")
except Exception as e:
    embedding_model = None
    logging.warning(f"嵌入模型加载失败: {e}")
    logging.warning("项目将在没有嵌入模型的情况下运行，某些功能可能不可用")

# 初始化 ChromaDB 客户端
try:
    import chromadb
    chroma_client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    # 获取或创建文档集合
    try:
        document_collection = chroma_client.get_collection("edu_documents")
        logging.info("文档集合加载成功！")
    except Exception:
        document_collection = chroma_client.create_collection("edu_documents")
        logging.info("文档集合创建成功！")
except Exception as e:
    chroma_client = None
    document_collection = None
    logging.warning(f"ChromaDB 初始化失败: {e}")
    logging.warning("项目将在没有文档检索的情况下运行，某些功能可能不可用")