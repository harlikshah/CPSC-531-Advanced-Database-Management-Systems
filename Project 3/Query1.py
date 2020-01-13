from struct import *
from collections import namedtuple
from datetime import date
import time

format = '20s20s70s40s80s25siii12s25s50s50s'
ColumnName = namedtuple('ColumnName',['fname','lname','job','company','address','phone','day','month','year','ssn','uname','email','url'])

def ageCount(birthDate): 
    age_in_years = int((date.today() - birthDate).days / 365.25 ) 
    return age_in_years

def Result(filetype):
    blocksize=calcsize(format)
    data_block = [] 
    with open(filetype , 'rb' ) as file_data:
        while True:
            details = file_data.read(4096)
            if not details:
                break
            for i in range(0,10):
                final_output = []
                data = ColumnName._make(unpack(format,details[i*blocksize:(i+1)*blocksize]))
                if(ageCount(date(data.year, data.month, data.day))<21):
                    final_output.append(data.ssn.decode('ascii','ignore').replace('\x00',''))
                    final_output.append(data.fname.decode('ascii','ignore').replace('\x00',''))
                    final_output.append(data.lname.decode('ascii','ignore').replace('\x00',''))
                    data_block.append(final_output)
    print(data_block)

start = time.time()
Result('large.bin')
end = time.time()
print('\n Time: ' + str(end-start) +'\n')

