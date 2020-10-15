#Databse information

This system has been build on postgre.  
If you want to use a different database, you'll have to change the DB_URI in main.py  
If you don't know how to do this, you're fat out of luck my friend.  

The program needs a user with table creation, data read and data write privilages.
In the case of postgre this can be done with the following sql command:

create user username with password 'password';   
create database domoticcontrol;   
grant all privileges on database domoticcontrol to domotic;   

The grant all might be a bit overpowered, but I don't know because I'm not experienced with database security.
If anyone knows any better, please make an issue report with why I'm wrong and stupid. 