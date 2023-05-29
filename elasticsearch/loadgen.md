# 压测命令

```
./loadgen-linux-amd64  -d 15 -c 3000 –compress
```

# 批量插入压测

```
cat loadgen.yml
variables:name: id
type: sequencename: uuid
type: uuidname: now_local
type: now_localname: now_utc
type: now_utcname: now_unix
type: now_unixname: suffix
type: range
from: 10
to: 15
requests:request:
method: POST
runtime_variables:
batch_no: id
runtime_body_line_variables:
routing_no: uuid
basic_auth:
username: elastic
password: elastic
#url: http://localhost:8000/_search?q=$[[id]]
url: http://172.21.227.16:9200/_bulk
body_repeat_times: 1000
body: "{ \"create\" : { \"_index\" : \"test-[[suffix]]\",\"_type\":\"doc\", \"_id\" : \"[[suffix]]\",\"_type\":\"doc\", \"_id\" : \"[[uuid]]\" , \"routing\" : \"[[routing_no]]\" } }\n{ \"id\" : \"[[routing_no]]\" } }\n{ \"id\" : \"[[uuid]]\",\"routing_no\" : \"[[routing_no]]\",\"batch_number\" : \"[[routing_no]]\",\"batch_number\" : \"[[batch_no]]\", \"random_no\" : \"[[suffix]]\",\"ip\" : \"[[suffix]]\",\"ip\" : \"[[ip]]\",\"now_local\" : \"[[now_local]]\",\"now_unix\" : \"[[now_local]]\",\"now_unix\" : \"[[now_unix]]\" }\n"
```

# 查询压测

```
requests:
  - request:
      method: GET
      basic_auth:
        username: elastic
        password: elastic
      url: http://172.21.227.17:9200/test-10/_search?q=id:chq7404dh6tkkdmmhrcg
```
