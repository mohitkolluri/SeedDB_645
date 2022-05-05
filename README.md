# SeedDB_645
CICS645 Final Project

INSTRUCTIONS FOR SETTING UP DB:
---------------------------------------
Download postgres: 
---------------------------------------
Windows: https://www.postgresql.org/download/windows/
---------------------------------------
Macbook: https://wiki.postgresql.org/wiki/Homebrew
---------------------------------------
Enter postgres CLI using 'psql postgres'
---------------------------------------
--> CREATE DATABASE seeddb
---------------------------------------
--> create user team_645_seeddb
---------------------------------------
--> ALTER USER team_645_seeddb WITH SUPERUSER;
------------------------------------------
Place adult.data in this directory downloaded from 
https://archive.ics.uci.edu/ml/machine-learning-databases/adult/
-------------------------------------------
--> Run 'pip install -r requirements.txt'
---------------------------------------
--> Run 'python3 seeddb.py'
---------------------------------------
