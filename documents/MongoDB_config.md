因为写文件是的open file数量限制
在 etc/profile 里面写入
ulimit -n 25000
然后 source /etc/profile   配置环境变量

先启动 config ，再启动shard，最后启动mongos
/usr/local/mongodb/bin/mongod --port 27222 --dbpath=/home/zhanggao/mongodb/shard/config --logpath=/home/zhanggao/mongodb/shard/log/config.log --logappend --fork --configsvr --replSet rs0

/usr/local/mongodb/bin/mongod --shardsvr --port 27020 --dbpath=/home/zhanggao/mongodb/shard/s0 --logpath=/home/zhanggao/mongodb/shard/log/s0.log --logappend --fork
/usr/local/mongodb/bin/mongod --shardsvr --port 27021 --dbpath=/home/zhanggao/mongodb/shard/s1 --logpath=/home/zhanggao/mongodb/shard/log/s1.log --logappend --fork
/usr/local/mongodb/bin/mongod --shardsvr --port 27022 --dbpath=/home/zhanggao/mongodb/shard/s2 --logpath=/home/zhanggao/mongodb/shard/log/s2.log --logappend --fork
/usr/local/mongodb/bin/mongod --shardsvr --port 27023 --dbpath=/home/zhanggao/mongodb/shard/s3 --logpath=/home/zhanggao/mongodb/shard/log/s3.log --logappend --fork

/usr/local/mongodb/bin/mongos --port 40001 --configdb=rs0/127.0.0.1:27222 --fork --logpath=/home/zhanggao/mongodb/shard/log/route.log


（1）在27222  config里面
必须先配，启动mongos 40001 之前
use admin
config = {_id:"rs0", members:[

  {_id:0, host:"127.0.0.1:27222"}

  ]

};

rs.initiate(config) 

（2）在 40001里面
添加shard
use admin
db.runCommand( { addshard : "127.0.0.1:27020",name:"shard0"} )
db.runCommand( { addshard : "127.0.0.1:27021",name:"shard1"} )
db.runCommand( { addshard : "127.0.0.1:27022",name:"shard2"} )
db.runCommand( { addshard : "127.0.0.1:27023",name:"shard3"} )
db.runCommand( { listshards : 1} )
整体状态查看
mongos> sh.status();


（3） 数据库分片配置

激活数据库分片功能
语法：( { enablesharding : "数据库名称" } )

mongos> use test 
use admin
mongos> db.runCommand( { enablesharding : "test" } )
指定分片建对集合分片，范围片键--创建索引
(以上必须在mongos内做)

下面可以直接在python里面做
mongos> db.vast.ensureIndex( { _id: 1 } )
mongos> use admin
mongos> db.runCommand( { shardcollection : "test.vast",key : {_id: 1} } )
集合分片验证
mongos> use test
mongos> for(i=0;i<20000;i++){ db.vast1.insert({"id":i,"name":"clsn","age":70,"date":new Date()}); }
mongos> db.vast.stats()


（4）在pymongo 连数据库