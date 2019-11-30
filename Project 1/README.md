# CPSC-531-Advanced-Database-Management-Systems

## RDBMS and Database

The RDBMS for this project is the Datalog Educational System, or DES. 
The database is Luis Rocha’s Chinook Database, modified for use with DES.

## Platforms
You may use any platform supported by DES to develop and test your queries.

Once you have downloaded DES, use the following commands to install rlwrap, which will
make it easier to interact with the DES console by providing line editing and command history:
```
$ sudo apt update
$ sudo apt install --yes rlwrap
```
Then use the following commands to extract and start DES:
```
$ unzip ~/Downloads/DES6.2Linux64SICStus.zip
$ cd des
$ chmod +x des des_start
$ rlwrap ./des
```
## Loading the Database
Download the database file Chinook_DES.ddb and place it in the same directory where you
extracted DES. The database can be loaded with the following command:
```
DES> /restore_ddb Chinook_DES.ddb
```
Note that the database will take a while to load.
You can view the database schema with /dbschema command, or by downloading and viewing
Chinook_DES.sql.

## Recreating the database
If the database does not load, you can recreate the database and save it again using the
following commands:
```
DES> /process Chinook_DES.sql
DES> /save_ddb Chinook_DES.ddb
```
but note that this process will take several minutes to complete.

## Queries

Write queries in Relational Algebra, Tuple Relational Calculus, and Domain Relational Calculus
to determine each of the following:
1. Albums by the artist “Red Hot Chili Peppers.”
2. Genres associated with the artist “U2.”
3. Names of tracks on playlist “Grunge” and their associated artists and albums.
4. Names and email addresses of customers who bought tracks in playlist “TV Shows.”
5. Names of the support representatives whose customers bought tracks in “Purchased
AAC audio file” format.

## Query Syntax
You can switch between query languages using the commands /ra, /trc, and /drc. Consult
examples/*.ra, examples/*.trc, examples/*.drc, and doc/manualDES.pdf for query
syntax.
Note in particular that per pp. 152 and 159, domain and tuple variables must begin with and
uppercase variable and the names of relations must be surrounded by single quotes. For  
example, the following TRC query should return all tuples in the Playlist relation:
```
{ P | 'Playlist'(P) }
```
