import rpyc
import os
import hashlib
from rpyc.core.service import SlaveService
from rpyc.utils.server import ThreadedServer

# DATA_DIR = 'data1/'
Master = {'host':'localhost','port':'7779'}

'''
file.seek(offset [,whence])
'''

class Dataserver(rpyc.Service):
    def __init__(self,DT):
        self.DATA_DIR = DT
    def exposed_get(self,block_id,start=None,end=None):
        # block_addr = os.path.join(self.DATA_DIR, block_id)
        block_addr = f'{self.DATA_DIR}/{str(block_id)}'
        if not os.path.isfile(block_addr):
            return "no exists"
        with open(block_addr,'rb') as f:
            if start!=None and end!=None:
                f.seek(start,0)
                return f.read(end-start)
            if start!=None:
                f.seek(start,0)
                return f.read()
            if end!=None:
                return f.read(end)
            return f.read()

    # 部分文件 blockid put
    def exposed_put(self, block_id, data, replica, IsPrim):
        '''
        :param block_id: 写入的结点
        :param data: 写入的数据
        :param replica: 写入其他备份结点
        :return:
        '''
        try:
            # m = hashlib.md5()
            # m.update(data)
            # hash = m.hexdigest()
            # putdir = os.path.join(self.DATA_DIR, block_id)
            # putdir = self.DATA_DIR + str(block_id)
            putdir = f'{self.DATA_DIR}/{str(block_id)}'
            with open(putdir,'wb') as f:
                f.write(data)
                # 返回给name hash值
                # rpyc.connect(Master['host'],Master['port']).root.hash(block_id,hash)
            if IsPrim and replica!=None:
                temp = self.rep(block_id, data, replica)
                if not temp:
                    return 'error'
            # 通知写成功
            return 'success'
        except Exception as e:
            print(e)
            return 'error'

    def rep(self, block_id, data, replica):
        print('Write other data nodes')
        success = True
        for datanode in replica:
            # 连接
            conn = rpyc.connect(datanode['host'],datanode['port'])
            issuccess = conn.root.put(datanode['blockid'],data,replica,False)
            if issuccess==False:
                success = False
        return success

import sys

if __name__ == "__main__":
    port = sys.argv[1]
    DATA_DIR = sys.argv[2]
    server = ThreadedServer(Dataserver(DATA_DIR), port=port, protocol_config={
        'allow_public_attrs': True,
    })
    server.start()