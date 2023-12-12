# 压测命令

```
./loadgen-linux-amd64  -d 15 -c 3000 –compress
```

# 批量插入压测

```
cat loadgen.yml
variables:
  - name: id
    type: sequence
  - name: uuid
    type: uuid
  - name: now_local
    type: now_local
  - name: now_utc
    type: now_utc
  - name: now_unix
    type: now_unix
  - name: suffix
    type: range
    from: 11
    to: 15
requests:
  - request:
      method: POST
      runtime_variables:
        batch_no: id
      runtime_body_line_variables:
        routing_no: uuid
      basic_auth:
        username: elastic
        password: elastic
      #url: http://localhost:8000/_search?q=$[[id]]
      url: http://172.1.116:9200/_bulk
      body_repeat_times: 1000
      body: "{ \"create\" : { \"_index\" : \"test-$[[suffix]]\",\"_type\":\"doc\", \"_id\" : \"$[[uuid]]\" , \"routing\" : \"$[[routing_no]]\" } }\n{ \"id\" : \"$[[uuid]]\",\"routing_no\" : \"$[[routing_no]]\",\"batch_number\" : \"$[[batch_no]]\", \"random_no\" : \"$[[suffix]]\",\"ip\" : \"$[[ip]]\",\"now_local\" : \"$[[now_local]]\",\"now_unix\" : \"$[[now_unix]]\" }\n"
```

# 查询压测

```
requests:
  - request:
      method: GET
      basic_auth:
        username: elastic
        password: elastic
      url: http://172.1.117:9200/test-10/_search?q=id:chq7404dh6tkkdmmhrcg
```
