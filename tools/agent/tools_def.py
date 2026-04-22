import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from .schema import CypherCheckerResponse
from .prompts import cypher_checker_prompt
from tools.entity.entity_alignment import EntityAlignment
from config.dependency import neo4j_driver,neo4j_schema,embedding_model,document_collection

import logging
logger = logging.getLogger(__file__)

# 维护当前Neo4j当中实体所对应的index的列表，每个实体存在两个Index，以list形式存储，第一个为全文索引，第二个为向量索引
# hybrid_store_list = {
#     "CourseInfo": ["course_name_index","CourseInfo_namevector_index"],
#     "ChapterInfo": ["ChapterInfoNameIndex","ChapterInfoNameVectorIndex"],
# }
hybrid_store_list=['category','subject','category','chapter']

# 设置DeepSeek API密钥
import os
os.environ["DEEPSEEK_API_KEY"] = "sk-7cfee948c73a4acfaadbedc14643818c"

# 尝试初始化ChatDeepSeek
try:
    cypher_checker_llm = ChatDeepSeek(model="deepseek-chat").with_structured_output(CypherCheckerResponse)
    logger.info("ChatDeepSeek初始化成功！")
except Exception as e:
    cypher_checker_llm = None
    logger.warning(f"ChatDeepSeek初始化失败: {e}")
    logger.warning("项目将在没有Cypher检查的情况下运行，某些功能可能不可用")

try:
    ea = EntityAlignment()
except Exception as e:
    ea = None
    logger.warning(f"EntityAlignment初始化失败: {e}")

def hybrid_search_query(query_text,full_text_index_name,vector_index_name,driver=neo4j_driver,top_k=1,alpha=0.5,threshold=0.5):
    if not embedding_model or not driver:
        logger.warning("嵌入模型或Neo4j驱动不可用，无法执行混合搜索")
        return []
    
    try:
        vector_list = embedding_model.embed_query(query_text)
        res = driver.execute_query(
            """
            CALL () {


        	CALL db.index.vector.queryNodes($vector_index_name, $top_k, $query_vector) 
        	YIELD node, score
    	WITH node, score LIMIT $top_k
    	return node, score*$alpha as score


    	UNION


    	CALL db.index.fulltext.queryNodes($fulltext_index_name, $query_text, {limit: $top_k})
    	YIELD node, score
    	WITH collect({node:node, score:score}) AS nodes, max(score) AS max_score
    	UNWIND nodes as n
    	RETURN n.node as node, n.score*(1 - $alpha) / max_score as score
    }
    WITH node, sum(score) AS score ORDER BY score DESC LIMIT $top_k
    RETURN node.`name` AS text, score, node {.*, `name`: Null, `name_embedding`: Null, id: Null } AS metadata
        """,
        parameters_={
            "vector_index_name": vector_index_name,
            "top_k": top_k,
            "query_vector": vector_list,
            "fulltext_index_name": full_text_index_name,
            "query_text": query_text,
            "alpha": alpha
        }
    )
        return [{"text":record["text"], "score":record["score"]} for record in res.records if record["score"] > threshold]
    except Exception as e:
        logger.error(f"混合搜索失败: {e}")
        return []

def entity_alignment(entitys_to_alignment:list):
    """
    当需要将用户的查询问题当中的实体对齐到图数据库当中已有的实体时，可以使用当前工具
    :param entity_to_alignment_list:
    :return:
    """
    logger.info(f"开始调用工具：entity_alignment，对齐参数为：{entitys_to_alignment}")
    if not ea:
        logger.warning("EntityAlignment不可用，无法执行实体对齐")
        return entitys_to_alignment
    
    try:
        for node in entitys_to_alignment:
            if node['label'] in hybrid_store_list:
                res = ea(node['entity'],node['label'])

                # results = hybrid_search_query(node['entity'],full_text_index_name=hybrid_store_list[node['label']][0],vector_index_name=hybrid_store_list[node['label']][1])
                if res:
                    node['entity'] = res

        return entitys_to_alignment
    except Exception as e:
        logger.error(f"实体对齐失败: {e}")
        return entitys_to_alignment

def check_syntax_error(cypher:str):
    """
    当需要检查cypher语句是否存在语句错误，或者是否不符合已有schema结构时使用
    当执行Cypher语句前，必须要使用该工具来进行检测Cypher语句的合法性
    """
    logger.info("开始调用工具：check_syntax_error")
    logger.info(f"当前需要校验的Cypher语句为:{cypher}")
    if not cypher_checker_llm:
        logger.warning("ChatDeepSeek不可用，无法执行Cypher语句检查")
        return {"is_valid": True, "error_message": "Cypher检查不可用，跳过检查"}
    
    try:
        prompt = PromptTemplate.from_template(cypher_checker_prompt)
        chain = prompt | cypher_checker_llm
        res = chain.invoke(
            {
                "neo4j_schema": neo4j_schema,
                "cypher": cypher
            }
        )
        logger.info(f"Cypher语句LLM校验结果为:{res}")
        return res
    except Exception as e:
        logger.error(f"Cypher语句检查失败: {e}")
        return {"is_valid": True, "error_message": f"Cypher检查失败: {e}"}

def neo4j_query(cypher,params=None):
    """
    当需要从neo4j数据库查询数据时使用
    :param cypher:
    :param driver:
    :param params:
    :return:
    """
    logger.info("开始调用工具：neo4j_query")
    logger.info(f"当前调用的cypher为:{cypher},当前调用的params为：{params}",)
    if not params:
        params={}

    driver = globals()['neo4j_driver']
    if not driver:
        logger.warning("Neo4j驱动不可用，无法执行查询")
        return []
    
    try:
        result = driver.execute_query(cypher,parameters_=params)
        logger.info(f"当前调用cypher结果为:{result.records}")
        return result.records
    except Exception as e:
        logger.error(f"Neo4j查询失败: {e}")
        return []


def document_retrieval(query_text: str, top_k: int = 3):
    """
    当需要从文档知识库中检索相关背景知识时使用。
    适用于获取课程详细介绍、知识点解释、学习建议等非结构化信息。
    
    :param query_text: 查询文本
    :param top_k: 返回最相关的文档数量，默认3条
    :return: 相关文档列表，包含文档内容和元数据
    """
    logger.info(f"开始调用工具：document_retrieval，查询：{query_text}")
    
    if not document_collection or not embedding_model:
        logger.warning("文档集合或嵌入模型不可用，无法执行检索")
        return []
    
    try:
        # 获取查询的嵌入向量
        query_embedding = embedding_model.embed_query(query_text)
        
        # 执行向量检索
        results = document_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        # 格式化返回结果
        documents = []
        for i in range(len(results["ids"][0])):
            doc = {
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "relevance_score": 1 - results["distances"][0][i]  # 转换为相似度分数
            }
            documents.append(doc)
        
        logger.info(f"文档检索完成，找到 {len(documents)} 条相关文档")
        return documents
    except Exception as e:
        logger.error(f"文档检索失败: {e}")
        return []


if __name__ == '__main__':
    pass