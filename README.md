What is Today?
==============

Taday is a social networking site.


Building and Run Today
--------------

Today can be run on Linux. We support to choose Ubuntu as OS, and both 32 bit and 64 bit systems.

Before running TODAY, you should do:
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv
$ sudo pip install tornado 
$ sudo pip install bcrypt
$ sudo pip install futures
$ sudo pip install markdown
$ sudo pip install torndb
$ sudo pip install jieba
$ sudo pip install networkx
$ sudo apt-get install python-mysqldb

make sure you have MySQL installed:
   $ sudo apt-get install mysql-server
   $ sudo apt-get isntall mysql-client
   $ sudo apt-get install libmysqlclient-dev

Create a database and user for this app
 - Connect to MySQL as a user that can create databases and users:
   ```
      $ mysql -u root -p
   ```
 - Create a database named "today":
   ```
     mysql > CREATE DATABASE today;
   ```
 - Allow the "today" user to connect with the password "today":
   ```
      mysql > GRANT ALL PRIVILEGES ON today.* TO 'today'@'localhost' IDENTIFIED BY 'today';
   ```
 - Create prerequisite tables in your database
   ```
     $ mysql --user=today --password=today --database=today < schema.sql
   ```

Run Today:
----------

python today.py
