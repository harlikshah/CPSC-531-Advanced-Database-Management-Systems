# CPSC-531-Advanced-Database-Management-Systems

## RDBMS and Database

The database is Luis Rocha’s Chinook Database, modified for use with Python.

## Platforms
You may use any platform supported by DES to develop and test your queries.

## Loading the Database
Download the database file Chinook_Python.py and place it in directory where you will
develop your Python code. The database can be loaded with the following command:

```
from Chinook_Python import *
```
You will find variables named Artist, Album, Customer, etc. containing sets of namedtuple
objects.

## Relational Operators

Implement the following functions in Python:

* select(relation, predicate)
* project(relation, columns)
* rename(relation, new_columns=None, new_relation=None)
* cross(relation1, relation2)
* theta_join(relation1, relation2, predicate)

The predicate for select() should be a function that takes a single namedtuple as an
argument and returns True or False.
The predicate for theta_join() should take two namedtuples and return a bool.
The new_columns and new_relation parameters to rename() are optional. if neither argument
is provided, return the original relation

## Extra Credit
Implement natural_join(relation1, relation2).

## Queries

The file queries.py contains four variations of the first query from Project 1:

1. Combining 𝜎 and  to implement 𝜃-join
2. Performing 𝜎 after 𝜃-join
3. Performing 𝜎 before 𝜃-join
4. Natural join (Run this If you did the extra credit.)

All of the queries above should return the following set:
```
{Result(Title='Blood Sugar Sex Magik'),
Result(Title='By The Way'),
Result(Title='Californication')}
```
When the relational operators are implemented and the queries above work correctly, write
code to run the last query from Project 1.

## Performance Measurement

As a rough approximation of the processing required for each query, instrument your functions
to measure the cardinality of the result set for each relational operator. When a query
completes, print the total number of tuples returned during processing.

1. What do you observe about the queries listed above?
2. Can you rewrite the last query from Project 1 to minimize the number of tuples
processed?
