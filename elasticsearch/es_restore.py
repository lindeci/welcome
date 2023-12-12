from elasticsearch import Elasticsearch, helpers
import json

# 设置 Elasticsearch 的地址和凭证
es_host = "1.1.1.1"
es_port = 9200
es_user = "elastic"
es_pass = "elastic"

# 设置备份文件路径和索引名称模式
backup_path = "/tmp"
index_list = ["device_cmd_elastic"]
# 创建 Elasticsearch 客户端对象
es = Elasticsearch(
    [f"http://{es_user}:{es_pass}@{es_host}:{es_port}"],
    http_auth=(es_user, es_pass),
    timeout=30,
    max_retries=10,
    retry_on_timeout=True,
)

data=[
{'id': '51244eac-e1f3-478a-972b-e50eccff2f36', 'createTime': '2022-09-09T16:49:17+08:00', 'lastReportTime': None, 'returnCodeNum': 1},
{'id': '51278bb9-dbe4-447f-99e0-504e834b789e', 'createTime': '2022-09-22T14:03:10+08:00', 'lastReportTime': '2022-10-08T09:57:52+08:00', 'returnCodeNum': 5}
]

def restore_index(index_name):
    for record in data:
        es.index(index=index_name, body=json.dumps(record))
def main():
  for i in range(100):
    for index_name in index_list:
        restore_index(index_name)
if __name__ == "__main__":
    main()