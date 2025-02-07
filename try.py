
import mysql.connector

con=mysql.connector.connect(host='localhost',username='root',password='root',database='login')



my_cursor=con.cursor()
con.commit()
con.close()

print("connectins success fully created ")

# this is how you need to create server 
# SHOW DATABASES;
# use data;

# CREATE TABLE user (
#     userid INT NOT NULL AUTO_INCREMENT,
#     name VARCHAR(100),
#     email VARCHAR(100) UNIQUE,
#     password VARCHAR(100),
#     PRIMARY KEY (userid)
# );

# describe user;
# SELECT * FROM user;
  


  
