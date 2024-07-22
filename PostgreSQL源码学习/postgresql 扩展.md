# pg_cron 安装配置
pg_cron下载地址https://github.com/citusdata/pg_cron

注意：pg_cron一定不要yum安装，安装后找不到pg_config！！！！
## 安装
```sh
#解压源码包
unzip pg_cron-main.zip
#声明环境变量
export PATH=/opt/postgresql/bin:$PATH
#编译安装
make && make install
```
## 设置
```
shared_preload_libraries = ‘pg_cron,pg_stat_statements’
#在哪个数据库做定时任务，就配置成哪个数据库
cron.database_name = ‘test’
#开启跟踪I/O消耗时间
track_io_timing = on
```
## 使用
```sql
#创建扩展pg_cron
create extension pg_cron;
#查询已创建的定时任务
select * from cron.job;
#创建定时任务，语法与crontab一样
SELECT cron.schedule('*/3 * * * *', $$REFRESH MATERIALIZED VIEW v_wuhua;$$);
```
# pg_stat_statements 安装配置
pg_stat_statements在编译程序的contrib/pg_stat_statments目录下
## 安装
cd /opt/software/postgresql-15.3/contrib/pg_stat_statements
make && make install
## 设置
```
shared_preload_libraries = ‘pg_cron,pg_stat_statements’
```
## 使用
```sql
#创建扩展pg_stat_statements
create extension pg_stat_statements
#常用的统计sql参考

#最耗IO SQL，单次调用最耗IO SQL TOP 5
select userid::regrole, dbid, query from pg_stat_statements order by (blk_read_time+blk_write_time)/calls desc limit 5;  

#总最耗IO SQL TOP 5
select userid::regrole, dbid, query from pg_stat_statements order by (blk_read_time+blk_write_time) desc limit 5;  

#最耗时 SQL，单次调用最耗时 SQL TOP 5
select userid::regrole, dbid, query from pg_stat_statements order by mean_time desc limit 5;  

#总最耗时 SQL TOP 5
select userid::regrole, dbid, query from pg_stat_statements order by total_time desc limit 5;  


#最耗共享内存 SQL
select userid::regrole, dbid, query from pg_stat_statements order by (shared_blks_hit+shared_blks_dirtied) desc limit 5;  

#最耗临时空间 SQL
select userid::regrole, dbid, query from pg_stat_statements order by temp_blks_written desc limit 5;
EOF
```

# 地理空间数据处理
```sql
-- 安装PostGIS扩展
CREATE EXTENSION postgis;
-- 创建地理空间数据表
CREATE TABLE buildings (id SERIAL PRIMARY KEY, name TEXT, location GEOMETRY(Point, 4326)); -- 定义了一个点的空间类型，其中的“4326”是EPSG代码，代表WGS 84坐标系统
-- 性能优化
CREATE INDEX idx_places_location ON places USING GIST(location); -- PostGIS提供了多种类型的空间索引，如GiST、SP-GiST和BRIN等
-- 插入地理空间数据
INSERT INTO buildings (name, location) VALUES ('Building A', ST_SetSRID(ST_MakePoint(12.34, 56.78), 4326));
-- 进行地理空间查询
SELECT * FROM buildings WHERE ST_Within(location, ST_GeomFromText('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'));
```