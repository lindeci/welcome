from elasticsearch import Elasticsearch, helpers

# 设置 Elasticsearch 的地址和凭证
es_host = "1.1.1.1"
es_port = 9200
es_user = "elastic"
es_pass = "elastic"

# 设置备份文件路径和索引名称模式
backup_path = "/data/es_backup"
index_list = ["device_1","device_2","device_3"]
# 创建 Elasticsearch 客户端对象
es = Elasticsearch(
    [f"http://{es_user}:{es_pass}@{es_host}:{es_port}"],
    http_auth=(es_user, es_pass),
    timeout=30,
    max_retries=10,
    retry_on_timeout=True,
)

# 备份 Elasticsearch 索引
def backup_index(index_name):
    result = es.search(
        index=index_name,
        body={"query": {"match_all": {}}},
        scroll="10m",
        size=1000,
    )
    sid = result["_scroll_id"]
    scroll_size = len(result["hits"]["hits"])
    with open(f"{backup_path}/{index_name}.json", "w") as f:
        while scroll_size > 0:
            scroll_size = len(result["hits"]["hits"])
            for doc in result["hits"]["hits"]:
                f.write(f'{doc["_source"]}\n')
            result = es.scroll(scroll_id=sid, scroll="10m")
            sid = result["_scroll_id"]
    print(f"Index {index_name} has been backed up to {backup_path}")

# 备份或恢复 Elasticsearch 索引
def main():
    # 备份索引
    for index_name in index_list:
        backup_index(index_name)

    # 恢复索引
    #for index_name in indices:
    #    restore_index(index_name)

if __name__ == "__main__":
    main()