# fullstack-nanodegree-tournament
Project 2 of the fullstack developer nanodegree

To run the project install git and postgres sql database

On windows you have to use a virtual machine to run it

Make sure your user has access to the postgres default
database and has the rights to create databases

To download the project:
git clone https://github.com/jmfrank63/fullstack-nanodegree-tournament.git

To run the swiss tournament simmulation type:
python support.py

To run the test provided by the instructors type:
python tournament_test.py

All files should be pep8 compliant

The tests provided are not complete. They do not cover cases
where the last pair already played against each other.

Unfortunately it was not exactly specified what had to be in python
and what in sql. Getting the player standings could have been done
in sql as well. I decided to use a very simple structure
and using medium complex sql statements to get some values
as proof of concept. I hope this is sufficient. Solving the
conflict problem that sometimes can happen in pure sql is hopefully
something we do not have to do. It was hard enough in python.

Two of the extra credits are supported: 
Odd number of players
and ranking by opponent match wins.
I hope you like my solution
