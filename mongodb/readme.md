# mogodb vs es
MOGODB比ES优势：事务、灵活备份、跨集群数据同步

# 建库、建用户、授权
use modb_func;
db.createUser({user:"modb_func",pwd:"modb_func",roles:[{role:"readWrite",db:"modb_func"}]})