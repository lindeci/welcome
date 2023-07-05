# 收集syslog到ES的设置

Logstash配置,监听UDP协议
```
docker pull docker.elastic.co/logstash/logstash:7.17.8
docker run -d --name=logstash docker.elastic.co/logstash/logstash:7.17.8
sleep 30
docker logs -f logstash

docker cp logstash:/usr/share/logstash /data/elk7/
mkdir /data/elk7/logstash/config/conf.d
chmod 777 -R /data/elk7/logstash

vi /data/elk7/logstash/config/conf.d/syslog.conf

input {
  udp {
    port => 5044
    type => rsyslog
  }
}


filter {
  if [type] == "rsyslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["172.16.13.196:9200"]
    user => elastic
    password => elastic
  }

  stdout { codec => rubydebug }
}



cat logstash.yml
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: [ "http://172.16.13.196:9200" ]
xpack.monitoring.elasticsearch.username: "elastic"
xpack.monitoring.elasticsearch.password: "elastic"
path.config: /usr/share/logstash/config/conf.d/*.conf
path.logs: /usr/share/logstash/logs

docker run  --name=logstash --restart=always -p 5044:5044/udp -v /data/elk7/logstash:/usr/share/logstash logstash:7.17.8
```
测试：
```
logger -d -P 5044 -n 172.16.13.196 'Dec 15 20:47:42 host-172-16-13-196 systemd[1]: Stopped System Logging Service.'
```
或者
```
yum install nc –y
nc -zvu 172.16.13.196 5044
```
检查logstash日志
```
docker logs -f logstash
```
