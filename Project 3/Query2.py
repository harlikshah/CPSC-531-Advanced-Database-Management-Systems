from struct import *
from collections import namedtuple
from datetime import date
import shelve
import time

format = '20s20s70s40s80s25siii12s25s50s50s'
ColumnName = namedtuple('ColumnName',['fname','lname','job','company','address','phone','day','month','year','ssn','uname','email','url'])

def IndexSSN(fileType):
    block_size =0
    blocks = 0
    indexing = shelve.open('index.db' , 'n')
    with open(fileType,'rb') as file_data:
        while True:
            total_size = calcsize(format)
            block_size +=1
            details = file_data.read(total_size)
            if not details:
                break
            if(len(details) == calcsize(format)):
                data = ColumnName._make(unpack(format,details))
                ssn_details = data.ssn.decode('ascii','ignore').replace('\x00','')
                
                if str(ssn_details) in indexing:
                    key = "{}".format(ssn_details)
                    value = indexing[key]
                    indexing[key] = value+1
                else:
                    indexing["{}".format(ssn_details)] = 1
                blocks+=calcsize(format)
            if(block_size%10==0):
                file_data.read(46)
                blocks+=46
    indexing.close()

def Result(fileType):
    indexing = shelve.open('index.db' , 'r')
    data_block = []
    for i in indexing:
        if(indexing[i] > 1):
            data_block.append(i)
    print(data_block)

start = time.time()
IndexSSN('large.bin')
Result('large.bin')
end = time.time()
print('\n Time: ' + str(end-start)+'\n')
