import rpyc
import os
import hashlib
from rpyc.core.service import SlaveService
from rpyc.utils.server import ThreadedServer

# DATA_DIR = 'datas/'

READ_DIR = 'read/'

Master = {'host':'localhost','port':'7779'}
# conn = rpyc.connect('localhost',7779)
BLOCK_SIZE = 1024*1024*2
# path = conn.root.write('a',7777)
# print(path)
# 读文件->文件名 + 目录
# 通过ID和offset定位位置
# 多线程读取
# MD5 校验

# 目录
def exist(filename):
    conn = rpyc.connect(Master['host'], Master['port'])
    blocks, hash = conn.root.read(filename)
    # print(blocks)
    if blocks == "no file":
        return 'no file'
    else:
        return 'yes'

def read(filename, offset=None):
    conn = rpyc.connect(Master['host'], Master['port'])
    blocks, hash = conn.root.read(filename)
    print(blocks)
    if blocks !="no file":
        if offset is None:
            # 读取各个块
            all = []
            for k in blocks:
                # 依此读取，读取失败就读备份
                data = None
                for b in blocks[k]:
                    try:
                        con = rpyc.connect(b['host'],port=b['port']).root
                        data = con.get(str(b['blockid']))
                        all.append(data)
                        break
                    except Exception as e:
                        print(e)
                if data==None:
                    print('read failed')
                    break
            # 拼接数据
            if len(all)!=0:
                with open(READ_DIR + filename,'wb') as f:
                    for dt in all:
                        f.write(dt)
            # 验证hash
            with open(READ_DIR + filename,'rb') as f:
                data = f.read()
                m = hashlib.md5()
                m.update(data)
                fhash = m.hexdigest()
            if hash == fhash:
                print('success')
            else:
                print('the file is not consistent')

        else:
            if len(offset)!=2:
                print('the len of offset is not two')
            else:
                block_index1 = offset[0]//BLOCK_SIZE
                block_index2 = offset[1]//BLOCK_SIZE
                all = []
                for blk in range(block_index1,block_index2 + 1):
                    start = offset[0] if offset[0]>blk*BLOCK_SIZE else None
                    end = offset[1] if offset[1]<(blk+1)*BLOCK_SIZE else None
                    print(start, end)
                    # 依此读取，读取失败就读备份
                    data = None
                    for b in blocks[blk]:
                        try:
                            con = rpyc.connect(b['host'], port=b['port']).root
                            data = con.get(str(b['blockid']),start,end)
                            all.append(data)
                            break
                        except Exception as e:
                            print(e)
                    if data == None:
                        print('read failed')
                        break
                # 拼接数据
                if len(all) != 0:
                    with open(READ_DIR + filename, 'wb') as f:
                        for dt in all:
                            f.write(dt)
                print('success')
    else:
        print("file not exists")

# 如果备份一份的话
# 3M文件最终是2*2个块

def put(filepath, name):
    size = os.path.getsize(filepath)
    conn = rpyc.connect(Master['host'], Master['port'])
    blocks, FileID = conn.root.write(name, size)
    with open(filepath,'rb') as f:
        data = f.read()
        m = hashlib.md5()
        m.update(data)
        hash = m.hexdigest()
        # 上传hash
        rpyc.connect(Master['host'], Master['port']).root.hash(name, hash)

    with open(filepath, 'rb') as f:
        for k in blocks:
            datanodes = blocks[k]
            data = f.read(BLOCK_SIZE)
            print(datanodes)
            datacon = rpyc.connect(datanodes[0]['host'],datanodes[0]['port'])
            res = datacon.root.put(datanodes[0]['blockid'],data,datanodes[1:],True)
            if res=='error':
                print(f'error when writing block:{k}')
                break
    return FileID


while True:
    try:
        inp = input("输入read\put\exist filename offset1 offset2\n").split(" ")
        if inp[0] == 'read':
            if len(inp) == 4:
                offset = [int(inp[2]), int(inp[3])]
                read(inp[1],offset)
            else:
                read(inp[1])
        elif inp[0] == 'put':
            if len(inp) == 3:
                print(put(inp[1],inp[2]))
        elif inp[0] == 'exist':
            if len(inp) == 2:
                print(exist(inp[1]))
        else:
            print('error')
    except Exception as e:
        print('error')
        break
# print(put('shakespeare.txt','shakespeare'))
# read('shakespeare',[1000,1001])
# read('shakespeare')
# print(exist('shakespeare'))

# 分片 做副本
# 返回文件ID
# def upload():
# read('a',0)
# def main(args):
