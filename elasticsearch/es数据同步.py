import time, json
import etcd
from elasticsearch import Elasticsearch, helpers, exceptions

import logging
import sys
from datetime import datetime, timedelta
import pytz

import warnings
warnings.filterwarnings("ignore", category=exceptions.ElasticsearchWarning)

logging.basicConfig(
    level=logging.WARNING,  # 设置日志级别为DEBUG，记录所有级别的日志
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    filename='app.log',  # 指定日志输出文件名
    filemode='w'  # 设置文件打开模式为写入
)
logger = logging.getLogger("test")
# 设置日志级别为WARNING或更高级别，屏蔽INFO级别以下的日志消息
logger.setLevel(logging.INFO)

# 获取日志处理器列表
handlers = logger.handlers

# 禁用所有处理器的日志输出
for handler in handlers:
    print(handler)
    handler.setLevel(logging.INFO)
    
# gmt_tz = pytz.timezone('GMT')

es = Elasticsearch(['localhost:9200','localhost:9200'], http_auth=('elastic', 'elastic'), )

# hosts = ["http://127.0.0.1:2379", "http://127.0.0.1:2379", "http://127.0.0.1:2379"]
hosts = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
def create_etcd_client():
    for host in hosts:
        try:
            client = etcd.Client(host=host,  port=2379, allow_reconnect=True, protocol='http', allow_redirect=False, username=None, password=None)
            return client
        except etcd.EtcdException:
            pass
# etcd_client = etcd.Client(host='127.0.0.1', port=2379)
etcd_client = create_etcd_client()
if etcd_client is None:
    print('etcd_client is None.')
    exit()
key = '/es/user'
value = {
            "res_timestamp_begin": 0,
            "res_timestamp_end": 0,
            "res__id_begin": 0,
            "res__id_end": 0,
            "max_rows": 30,
            "return_rows": 0
        }
# 如果是第一次同步，则先在etcd中写入索引的同步配置
try:
    etcd_client.read(key).value
except etcd.EtcdKeyNotFound:
    etcd_client.write(key = key, value = value)

# 获取ES集群所有ingest节点的最小时间戳
def get_es_min_time():    
    min_time = sys.maxsize
    nodes_stats = es.nodes.stats(metric="os")["nodes"]
    for node_id,node in nodes_stats.items():
        if 'ingest' in node.get('roles'):
            if min_time > node.get('timestamp'):
                min_time = node.get('timestamp')
    return min_time

while True:
    # 获取etcd中的配置
    value = etcd_client.read(key).value
    dict = eval(value)
    etcd_res_timestamp_begin = dict.get("res_timestamp_begin")
    etcd_res_timestamp_end = dict.get("res_timestamp_end")
    etcd_res__id_begin = dict.get("res__id_begin")
    etcd_res_res__id_end = dict.get("res__id_end")
    max_rows = dict.get("max_rows")
    return_rows = dict.get("return_rows")
    
    es_min_time = get_es_min_time()
    
    query_timestamp_begin = etcd_res_timestamp_end
    query_timestamp_end = es_min_time
        
    query = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gt": query_timestamp_begin,
                        "lte": query_timestamp_end
                    }
                }
            },
            "sort": [
                {
                    "@timestamp": {
                        "order": "asc"
                    }
                }
            ],
            "size": max_rows
        }
    if return_rows >= max_rows:
        query = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": query_timestamp_begin,
                        "lte": query_timestamp_end
                    }
                }                
            },
            "sort": [
                {
                    "@timestamp": {
                        "order": "asc"
                    }
                }
            ],
            "size": max_rows
        }
    logger.info(f"query:{query}")
    res = es.search(index="cf_rfem_hist_price_bak", body=query,)    
    res_total = len(res["hits"]['hits'])
    if res_total == 0:
        time.sleep(1)
        continue
    res_timestamp_begin = res["hits"]['hits'][0]['_source']['@timestamp']
    res_timestamp_end = res["hits"]['hits'][-1]['_source']['@timestamp']
    res__id_begin = res["hits"]['hits'][0]['_id']
    res__id_end = res["hits"]['hits'][-1]['_id']
    
    actions = [
        {
            "_index": "ldc_name",
            "_id": doc["_id"],
            "_source": doc["_source"]
        }
        for doc in res["hits"]["hits"]
    ]
    
    helpers.bulk(es, actions)
    
    value = {
            "res_timestamp_begin": res_timestamp_begin,
            "res_timestamp_end": res_timestamp_end,
            "res__id_begin": res__id_begin,
            "res__id_end": res__id_end,
            "max_rows": max_rows,
            "return_rows": res_total
        }
    etcd_client.write(key = key, value = value)
    logger.info(f"res_timestamp_begin:{res_timestamp_begin} res_timestamp_end:{res_timestamp_end} res__id_begin:{res__id_begin} res__id_end:{res__id_end} return_rows:{res_total}")
    
    time.sleep(1)
