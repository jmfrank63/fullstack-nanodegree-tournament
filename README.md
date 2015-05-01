# fullstack-nanodegree-tournament
Project 2 of the fullstack developer nanodegree

To run the project install git and postgres sql database

On windows you have to use a virtual machine to run it

Make sure your user has access to the postgres default
database and has the rights to create databases

To check if your database is running use:

*sudo service postgresql status*

and start it via

*sudo service postgresql start

if necessary.

To download the project:
*git clone https://github.com/jmfrank63/fullstack-nanodegree-tournament.git*

In the sql folder you will find some files with sql queries.

To manually use them connect to the postgres sql database with:
psql postgres

and issue the command: CREATE DATABASE tournament

Then connect to the create database with:

\c tournament

Alternatively you can create the databese from the command line:
createdb tournament

and connect to it:
psql tournament

Once connected create your tables:

\i sql/tournament.sql

and insert some players with:

\i sql/register_aplayers.sql
\i sql/register_jplayers.sql

If you want an uneven number you can import a single
additional player form uneven_aplayer.sql or
uneven_jplayer.sql

You can always restart by dropping the database with:

*drop database tournament;*

The above steps can be utilized directly via
the createdb.py script:

*python createdb.py*

To run the swiss tournament simmulation type:

*python support.py*

To run the test provided by the instructors type:

*python tournament_test.py*

----------------------------------
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

Ranking by opponent match wins.

I hope you like my solution

------------------------------------------

Additonal comment for the resent:

I didn't realize that .format is nothing but an advanced %.
It won't help against sql injection. I from nowon will
never forget this.

I ran into some (this time minor) problems nevertheless. The create and drop
database commands accept only double quotes or no quotes. I couldn't find 
out how to change the quoting, but I found the AsIs method which served
the purpose.
I used the .format method only with the connect function. This command
does not accept sql thus no injection can take place.

The separation of the create tables from the database is not optimal. I must
admit this. But I would have to rewrite the way I created the database and
I do not have written a testsuite. So I will risk breaking things and I am
under heavy time pressure at the moment. 4th of May is deadline for this
project, but what is even more important I will have to finish P5 and P6 of
the front end developer to finish my first nanodegree by 18th of May.
So have my appologies for not fixing this. I did however take your
recommondation on the list comprehension.
As I mentioned: No testsuite so refacturing can break things.
I want to say thank you for the hint with bleach. I will definitely use it
on the next project.

Cheers

Johannes
