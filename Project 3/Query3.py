from struct import *
from collections import namedtuple
from datetime import date
import shelve
import time
import itertools

format = '20s20s70s40s80s25siii12s25s50s50s' 
ColumnName = namedtuple('ColumnName',['fname','lname','job','company','address','phone','day','month','year','ssn','uname','email','url'])

def ageCount(birthDate): 
    age_in_years = int((date.today() - birthDate).days / 365.25 ) 
    return age_in_years

def IndexBirthdate(fileType):
    block_size =0
    blocks = 0
    indexing = shelve.open('index3.db' , 'n')
    with open(fileType,'rb') as file_data:
        while True:
            total_size = calcsize(format)
            block_size +=1
            details = file_data.read(total_size)
            if not details:
                break
            if(len(details) == calcsize(format)):
                data = ColumnName._make(unpack(format,details)) 
                birthdate= date(data.year, data.month, data.day)
                if str(birthdate) in indexing:
                    indexing["{}".format(birthdate)].append(blocks)
                else:
                    indexing["{}".format(birthdate)] = [blocks]
                blocks+=calcsize(format)
            if(block_size%10==0):
                file_data.read(46)
                blocks+=46
    indexing.close()

def Result(fileType):
    indexing = shelve.open('index3.db' , 'r')
    birthdate_input = []
    for i in indexing:
        year  = int(i.split('-')[0])
        month = int(i.split('-')[1])
        day   = int(i.split('-')[2])
        if(ageCount(date(year,month,day))<21):
            birthdate_input.append(indexing[i])
    final_data = list(itertools.chain(*birthdate_input))
    data_block = []
    with open(fileType,'rb') as file_data:
        for offset in final_data:
            final_output = []
            file_data.seek(offset,0)
            details = file_data.read(calcsize(format))
            if details:
                record = ColumnName._make(unpack(format,details))
                final_output.append(record.ssn.decode('ascii','ignore').replace('\x00',''))
                final_output.append(record.fname.decode('ascii','ignore').replace('\x00',''))
                final_output.append(record.lname.decode('ascii','ignore').replace('\x00',''))
                data_block.append(final_output)
    indexing.close()
    print(data_block)

start = time.time()
IndexBirthdate('small.bin')
Result('small.bin')
end = time.time()
print('\n Time: ' + str(end-start) + '\n')
