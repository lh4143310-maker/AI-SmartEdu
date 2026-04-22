from config.config import NEO4J_CONFIG
import neo4j

try:
    print("正在连接Neo4j...")
    # 尝试使用bolt协议
    uri = NEO4J_CONFIG["uri"].replace("neo4j://", "bolt://")
    print(f"使用URI: {uri}")
    driver = neo4j.GraphDatabase.driver(
        uri=uri,
        auth=NEO4J_CONFIG["auth"]
    )
    
    # 测试连接
    with driver.session() as session:
        result = session.run("RETURN 1")
        print(f"✅ Neo4j连接成功！结果: {result.single()}")
    
    driver.close()
except Exception as e:
    print(f"❌ Neo4j连接失败: {e}")
