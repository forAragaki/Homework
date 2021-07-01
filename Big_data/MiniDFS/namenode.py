from rpyc import Service
from rpyc.core.service import SlaveService
from rpyc.utils.server import ThreadedServer
import uuid
import hashlib

# 2MB
BLOCK_SIZE = 1024*1024*2
REPLICATION = 1
CONF_DATA = {
    0: {'host':'localhost','port':'7777'},
    1: {'host':'localhost','port':'7778'},
    2: {'host':'localhost','port':'7776'},
    3: {'host':'localhost','port':'7775'},
    4: {'host':'localhost','port':'7774'},
}

class TestService(Service):
    def __init__(self):
        # ID从0开始
        self.FileID = 0
        # {FileID:{block:[datanode1,datanode2],md5:MD5}}
        self.Name_ID = {}
        self.Metadata = {}
        self.md5s = {}

    def exposed_test(self,num):
        return num

    def exposed_read(self,filename):
        # 查表找出每个结点文件的块
        if filename not in self.Name_ID.keys():
            return 'no file',None
        fileID = self.Name_ID[filename]
        print(self.Name_ID)
        if fileID not in self.Metadata.keys():
            return "no file",None
        return self.Metadata[fileID],self.md5s[filename]

    # fileID —> {blockid:[id:0,host:host,port:port]}
    def exposed_write(self, file, size):
        self.Name_ID[file] = self.FileID
        self.Metadata[self.FileID] = {}
        # add block
        tempp = {}
        numblock = size//BLOCK_SIZE + 1
        for k in range(numblock):
            tempblock = []
            for r in range(REPLICATION+1):
                ind = (r+k) % len(CONF_DATA)
                tem = CONF_DATA[ind].copy()
                Ids = uuid.uuid1()
                tem['blockid'] = Ids
                tempblock.append(tem)
            tempp[k] = tempblock
        self.Metadata[self.FileID] = tempp
        self.FileID += 1
        return tempp, self.FileID

    # 数据结点结束写入后得到hash值
    def exposed_hash(self,name, hash):
        self.md5s[name] = hash

server = ThreadedServer(TestService(),auto_register=False,hostname='localhost',port=7779)
server.start()