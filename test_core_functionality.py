# 测试核心功能
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试核心功能...")

# 测试配置模块
try:
    from config.config import MYSQL_CONFIG, NEO4J_CONFIG, WEB_STATIC_DIR, EMBEDDING_MODEL_PATH, VECTOR_STORE_DIR, AGENT_WITH_MEMORY, AGENT_STREAM_OUTPUT
    print("✅ 配置模块导入成功")
except Exception as e:
    print(f"❌ 配置模块导入失败: {e}")

# 测试依赖模块
try:
    from config.dependency import neo4j_driver, neo4j_schema, embedding_model
    print("✅ 依赖模块导入成功")
    print(f"  - Neo4j驱动: {'可用' if neo4j_driver else '不可用'}")
    print(f"  - 嵌入模型: {'可用' if embedding_model else '不可用'}")
except Exception as e:
    print(f"❌ 依赖模块导入失败: {e}")

# 测试工具模块
try:
    from tools.agent.tools_def import check_syntax_error, neo4j_query, entity_alignment, hybrid_search_query
    print("✅ 工具模块导入成功")
except Exception as e:
    print(f"❌ 工具模块导入失败: {e}")

# 测试后端模块
try:
    from backend.service import ChatService
    print("✅ 后端模块导入成功")
except Exception as e:
    print(f"❌ 后端模块导入失败: {e}")

# 测试Web模块
try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from starlette.responses import HTMLResponse
    print("✅ Web模块导入成功")
except Exception as e:
    print(f"❌ Web模块导入失败: {e}")

print("\n测试完成！")
