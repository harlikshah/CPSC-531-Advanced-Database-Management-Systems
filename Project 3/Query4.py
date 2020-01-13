from struct import *
from collections import namedtuple
from datetime import date
import itertools
import json
import time
import shelve

format = '20s20s70s40s80s25siii12s25s50s50s'
Result = namedtuple('Result',['fName','lName','job','company','address','phone','day','month','year','ssn','uname','email','url'])

def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age

def createIndexShelve(fileName):
    record_read =0
    bytes_read = 0
    dbindexmem = {}
    dbindex = open('birthdateindex.db' , 'w')
    with open(fileName,'rb') as file:
        while True:
            len_to_be_read = calcsize(format)
            record_read +=1
            fileContent = file.read(len_to_be_read)
            if not fileContent:
                break
            if(len(fileContent) == calcsize(format)):
                result = Result._make(unpack(format,fileContent))
                birthdate= date(result.year, result.month, result.day)
                if str(birthdate) in dbindexmem:
                    dbindexmem["{}".format(birthdate)].append(bytes_read)
                else:
                    dbindexmem["{}".format(birthdate)] = [bytes_read]
                bytes_read+=calcsize(format)
            if(record_read%10==0):
                file.read(46)
                bytes_read+=46
    json.dump(dbindexmem , dbindex)
    dbindex.close()

def sortdatafile(filename):
    createIndexShelve(filename)
    dbreadindex = open('birthdateindex.db' , 'r')
    dbreadindmem = json.load(dbreadindex)
    dbreadindex.close()
    finalrows = []
    for i in dbreadindmem:
        year  = int(i.split('-')[0])
        month = int(i.split('-')[1])
        day   = int(i.split('-')[2])
        datev = date(year,month,day)
        finalrows.append((datev,dbreadindmem[i]))
    finalrows = sorted(finalrows, key=lambda x : x[0] , reverse=True)
    #dbreadindex.close()
    sorteddatafile = open('sorteddatafile.bin','wb')
    records =  0
    with open(filename,'rb') as file:
        for k,offsets in finalrows:
            result = []
            for offset in offsets :
                records = records + 1
                file.seek(offset,0)
                fileContent = file.read(calcsize(format))
                if fileContent:
                    sorteddatafile.write(fileContent)
                if records%10 == 0 :
                    sorteddatafile.write(pack('46s',b' '*46))
    sorteddatafile.close()

def createClusterIndex():
    records_read = 0
    block_pos = 0
    dbindex = {}
    dbfile = open('clustered.db' , 'w')
    block_size = 4096
    prevbirthdate = ''
    with open('sorteddatafile.bin' , 'rb') as file:
        while True:
            fileContent = file.read(calcsize(format))
            records_read +=1
            if not fileContent:
                break
            if(len(fileContent) == calcsize(format)):
                result = Result._make(unpack(format,fileContent))
                currbirthdate = date(result.year, result.month, result.day)
                if currbirthdate != prevbirthdate :
                    dbindex["{}".format(currbirthdate)] = block_pos
                if(records_read%10 == 0):
                    file.read(46)
                    block_pos = int(block_size * (records_read/10))
                prevbirthdate = currbirthdate
    json.dump(dbindex,dbfile)
    dbfile.close()

def runningClusterIndex():
    dbindex = open('clustered.db' , 'r')
    dbindexread = json.load(dbindex)
    dbindex.close()
    records_read =0 
    finalResult = []
    prev_location =-4096
    with open('sorteddatafile.bin' , 'rb') as file:
        for i in dbindexread:
            year  = int(i.split('-')[0])
            month = int(i.split('-')[1])
            day   = int(i.split('-')[2])
            #print(dbindexread[i], i )
            if(calculateAge(date(year,month,day))<21):
                records_to_be_read=(dbindexread[i]-prev_location)/4096
                if prev_location != dbindexread[i]:
                    while records_to_be_read>=0:
                        records_read = 0 
                        file.seek(dbindexread[i])
                        while records_read <10:
                            result = []
                            fileContent = file.read(calcsize(format))
                            records_read+=1
                            if not fileContent:
                                break
                            if(len(fileContent) == calcsize(format)):
                                record = Result._make(unpack(format,fileContent))
                                #print(record)
                                if(calculateAge(date(record.year,record.month,record.day))<21):
                                    result.append(record.ssn.decode('ascii','ignore').replace('\x00',''))
                                    result.append(record.fName.decode('ascii','ignore').replace('\x00',''))
                                    result.append(record.lName.decode('ascii','ignore').replace('\x00',''))
                                    finalResult.append(result)
                                else:
                                    break
                        records_to_be_read-=1
                    prev_location =dbindexread[i]
            else:
                break
    print(finalResult)

fileName = 'small.bin'

print ('\n--- Fourth Query output ---\n')
start = time.time()
sortdatafile(fileName)
createClusterIndex()
runningClusterIndex()
end = time.time()
print('\n--- Time taken for query ' + str(end-start))
