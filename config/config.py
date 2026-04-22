from pathlib import Path
import dotenv
dotenv.load_dotenv() # 加载环境变量，通过langsmith来记录每次调用数据
# 数据库配置
MYSQL_CONFIG = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"123456",
    "database":"smart_edu"
}

NEO4J_CONFIG = {
    "uri":"neo4j://localhost",
    "auth":("neo4j","abc123456")
}

# 路径配置
ROOT_DIR = Path(__file__).parent.parent
WEB_STATIC_DIR = ROOT_DIR / "frontend" / "templates"
EMBEDDING_MODEL_PATH = ROOT_DIR / "model" / "pretrained" / "bge-base-zh-v1.5"
VECTOR_STORE_DIR = ROOT_DIR / 'data' / 'vectorstore'
# 其他配置
AGENT_WITH_MEMORY = True
AGENT_STREAM_OUTPUT = True