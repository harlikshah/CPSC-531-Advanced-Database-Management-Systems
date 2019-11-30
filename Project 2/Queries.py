'''
ADBMS Project 2

'''


import pprint
import collections
from Chinook_Python import *
from collections import namedtuple
import time

total_tuples = 0
'''
Project function - First, it has an empty set and 1 empty array list. 
It runs 2 loops and check the conditions for relation in colums.
If condition satisfy then it adds to empty list and retuen the set.
'''
def project(relation, columns):
    projectTuple = collections.namedtuple('project', columns)
    projectSet = set()
    for i in relation:
        projectList = []
        for j in columns:
            projectList.append(getattr(i, j))
        object = projectTuple(*projectList)
        projectSet.add(object)
    print('project', len(projectSet))
    global total_tuples
    total_tuples += len(projectSet)
    return projectSet

'''
Select function - First, it has an empty set. It checks condition for attr in every relation.
If its satisfy then it adds attr to set.

'''
def select(relation, predicate):
    selectSet = {attr for attr in relation if (predicate(attr))}
    print('select', len(selectSet))
    global total_tuples
    total_tuples += len(selectSet)
    return selectSet

'''
Rename function - First, it has an empty set. It checks the length of column and compare with fields in relation.
If condition satisfy then it new name to empty set and retuen the set.
'''
def rename(relation, new_columns=None, new_relation=None):
    renameTuple = collections.namedtuple('Rename', new_columns)
    renameSet = set()
    for i in relation:
        if (len(new_columns) == len(i._fields)):
            object = renameTuple(*i)
            renameSet.add(object)
    print('rename', len(renameSet))
    global total_tuples
    total_tuples += len(renameSet)
    return renameSet

'''
Cross function - First, it has an empty set. It matches fields in relation1 with fields in relation2.
It adds fields in set.
'''
def cross(relation1, relation2):
    ansSet = collections.namedtuple("cross",list(next(iter(relation1))._fields) + list(next(iter(relation2))._fields))
    crossSet = set()
    for i in relation1:
        for j in relation2:
            crossSet.add(ansSet(*i, *j))
    print('cross', len(crossSet))
    global total_tuples
    total_tuples += len(crossSet)
    return crossSet
 
'''
Theta function - First, it has an empty set. It checks fields in both the relation.
If tuples matches then it adds into empty set.
'''
def theta_join(relation1, relation2, predicate):
    thetaTuple = collections.namedtuple('theta_join', list(next(iter(relation1))._fields) + list(next(iter(relation2))._fields))
    thetaSet = set()
    for i in relation1:
        for j in relation2:
            if (predicate(i, j)):
                thetaSet.add(thetaTuple(*i, *j))
    print('theta', len(thetaSet))
    global total_tuples
    total_tuples += len(thetaSet)
    return thetaSet

'''
Theta function - First, it has an empty set. It checks fields in both the relation.
If tuples matches then it adds into empty set.
'''
def natural_join(relation1, relation2):
    t1 = list(next(iter(relation1))._fields)
    t2 = list(next(iter(relation2))._fields)
    temp = list(next(iter(relation2))._fields)
    #Delete comman column and make new relation with all columns
    sameColumn = list(set(t1) & set(t2))
    del temp[temp.index(sameColumn[0])]
    ansCol = t1 + temp
    records = [] 
    naturalSet = collections.namedtuple('Natural',ansCol)
    for i in relation1:
        for j in relation2:
            if i[t1.index(sameColumn[0]) ] == j[t2.index(sameColumn[0]) ]:
                list1 = list(j)
                #Delete the columns of second list
                del list1[t2.index(sameColumn[0])]
                list2 = list(i) + list1
                #Adding the final list into the result
                records.append(naturalSet(*list2))
    naturalSet = set(records)
    print('Natural', len(naturalSet))
    global total_tuples
    total_tuples += len(naturalSet)
    return naturalSet

print('\n1st Query\n')
start_time = 0
start_time = time.time()
pprint.pprint(
    project(
        select(
            select(
                cross(
                    Album,
                    rename(Artist, ['Id', 'Name'])
                ),
                lambda t: t.ArtistId == t.Id
            ),
            lambda t: t.Name == 'Red Hot Chili Peppers'
        ),
        ['Title']
    )
)
print((time.time() - start_time))
print('Total tuples in 1st query :',total_tuples)

total_tuples = 0

print('\n2nd Query\n')
start_time = time.time()
pprint.pprint(
    project(
        select(
            theta_join(
                Album,
                rename(Artist, ['Id', 'Name']),
                lambda t1, t2: t1.ArtistId == t2.Id
            ),
            lambda t: t.Name == 'Red Hot Chili Peppers'
        ),
        ['Title']
    )
)
print((time.time() - start_time))
print('Total tuples in 2nd query :',total_tuples)

total_tuples = 0
print('\n3rd Query\n')
start_time = time.time()
pprint.pprint(
    project(
        theta_join(
            Album,
            rename(
                select(Artist, lambda t: t.Name == 'Red Hot Chili Peppers'),
                ['Id', 'Name']
            ),
            lambda t1, t2: t1.ArtistId == t2.Id
        ),
        ['Title']
    )
)
print((time.time() - start_time))
print('Total tuples in 3rd query :',total_tuples)

total_tuples = 0
print('\n4th Query\n')
start_time = time.time()
pprint.pprint(
    project(
        natural_join(
            Album,
            select(Artist, lambda t: t.Name == 'Red Hot Chili Peppers')
        ),
        ['Title']
    )
)
print((time.time() - start_time))
print('Total tuples in 4th query :',total_tuples)


'''
project Employee.FirstName ((project MediaTypeId (select Name='Purchased AAC audio file' 
(MediaType))) njoin Track njoin InvoiceLine njoin Invoice njoin Customer zjoin Customer.SupportRepId=Employee.EmployeeId Employee);

'''

total_tuples = 0
print('\nLast query of project 1 using NATURAL JOIN\n')
start_time = time.time()
pprint.pprint(
    project(
        theta_join(
            natural_join(
                natural_join(
                    natural_join(
                        natural_join(
                            project(
                                select(
                                    MediaType,
                                    lambda t: t.Name == 'Purchased AAC audio file'
                                )
                                ,['MediaTypeId']
                            ),
                            Track
                        ),
                        rename(InvoiceLine,['InvoiceLineId', 'InvoiceId', 'TrackId', 'ILUnitPrice', 'Quantity'])
                    ),
                    Invoice
                ),
                Customer
            ),
            rename(Employee,['EmployeeId', 'ELastName', 'EFirstName', 'Title', 'ReportsTo', 'BirthDate', 'HireDate', 'EAddress', 'ECity', 'EState', 'ECountry', 'EPostalCode', 'EPhone', 'EFax', 'EEmail']),
            lambda t1, t2: t1.SupportRepId == t2.EmployeeId
        ),
        ['EFirstName']
    )
)
print((time.time() - start_time))
print('Last query of project 1 using NATURAL JOIN :',total_tuples)

print('\nLast query of project 1 using THETA JOIN\n')
total_tuples = 0
start_time = time.time()
pprint.pprint(
    project(
        theta_join(
            theta_join(
                theta_join(
                    theta_join(
                        theta_join(
                            project(
                                select(
                                    MediaType,
                                    lambda t: t.Name == 'Purchased AAC audio file'
                                )
                                ,['MediaTypeId']
                            ),
                            rename(Track,['TrackId', 'Name', 'AlbumId', 'MId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice']),
                            lambda t1, t2: t1.MediaTypeId == t2.MId
                        ),
                        rename(InvoiceLine,['InvoiceLineId', 'IId', 'TId', 'UPrice', 'Quantity']),
                        lambda t2, t3: t2.TrackId == t3.TId
                    ),
                    rename(Invoice,['InvoiceId', 'CId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total']),
                    lambda t3, t4: t3.IId == t4.InvoiceId
                ),
                rename(Customer,['CustomerId', 'FName', 'LName', 'Company', 'CAddress', 'CCity', 'CState', 'CCountry', 'CPostalCode', 'CPhone', 'CFax', 'CEmail', 'SupportRepId']),
                lambda t4, t5: t4.CId == t5.CustomerId
            ),
            rename(Employee,['EmployeeId', 'LastName', 'FirstName', 'Title', 'ReportsTo', 'BirthDate', 'HireDate', 'Address', 'City', 'State', 'Country', 'PostalCode', 'Phone', 'Fax', 'Email']),
            lambda t5, t6: t5.SupportRepId == t6.EmployeeId
        ),
        ['FirstName']
    )
)
print((time.time() - start_time))
print('Last query of project 1 using THETA JOIN :',total_tuples)


'''
1. What do you observe about the queries listed above?
    ● First query runs 96053 tuples approximately and takes 0.27 seconds to run the query.
    ● Second query runs 628 tuples approximately and takes 0.02 seconds to run the query.
    ● Third query runs 8 tuples approximately and takes 0.001 seconds to run the query.
    ● Fourth query runs 7 tuples approximately and takes 0.0009 seconds to run the query.
    ● Fifth query using Natural Join runs 2275 tuples approximately and takes 0.03 seconds to run the query.
      and using Theta Join runs 6249 tuples approximately and takes 0.04 seconds to run the query.
    ● We observe that natural join is more optimized then cross and theta join
      function. If we perform functions such as select or project before theta join,
      then it takes less tuples and time.
    ● We can see that in the above queries, forth query is doing select first so as a
      result we will get less tuples which will satisfy the condition and then we will
      do join in that so, ultimately it will reduce the number of tuples to process and
      give results in minimum time.
    ● We observe that fourth query is more optimized as it takes approximately
      0.0009 seconds to perform.

2. Can you rewrite the last query from Project 1 to minimize the number of tuples processed?
    ● To minimize the last query from project 1, firstly we have to do selection with
      predicate MediaType.Name = 'Purchased AAC audio file' so that it gives us
      less tuples instead of writing select at the first and then we are doing natural join 
      instead of theta join as theta join will not take the same field name for both relations. 
      That way we are saving time by not doing rename. 
    ● If we do this query with theta join, then it will process approximately 6249
      tuples and take 25 seconds to run the query.
    ● Using natural join, this query will process approximately 2275 tuples and take
      approximately 0.071 seconds to run the query.
     
'''