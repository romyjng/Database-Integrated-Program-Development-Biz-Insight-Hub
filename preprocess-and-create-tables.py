#!/usr/bin/env python
# coding: utf-8

# In[52]:


# Connect DB
import mysql.connector

mydb = mysql.connector.connect(
    host= "localhost",
    user = "root",
    passwd = "" # put your PW
  )
print(mydb)


# In[53]:


# Create financial DB and Show Databases
myCursor = mydb.cursor()
myCursor.execute("CREATE DATABASE IF NOT EXISTS financial")
myCursor.execute("SHOW DATABASES")
for db in myCursor:
    print(db)


# In[54]:


# Use financial DB
myCursor.execute("USE financial")


# In[75]:


# Create company_info table
myCursor.execute("CREATE TABLE company_info( \
                 id int NOT NULL PRIMARY KEY, \
                 code int UNIQUE NOT NULL, \
                 name varchar(100) UNIQUE NOT NULL, \
                 industry varchar(100) NOT NULL, \
                 current_assets float NOT NULL, \
                 current_liability float NOT NULL, \
                 net_profit float NOT NULL, \
                 fama_french_3factors float NOT NULL, \
                 carhart_4factors float NOT NULL,\
                 fama_french_5factors float NOT NULL)");


# In[79]:


# Import company_info file
import pandas as pd
info = pd.read_csv('',index_col=0) #put company_info file dir
info


# In[81]:


# Insert data into company_info table
columns = info.columns
for index, row in info.iterrows():
    # SQL 쿼리 실행
    query = "INSERT INTO company_info (id, code, name, industry, current_assets, current_liability, \
    net_profit, fama_french_3factors, carhart_4factors, fama_french_5factors )\
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (row[columns[0]],row[columns[1]],row[columns[2]],row[columns[3]],row[columns[4]],row[columns[5]],
                row[columns[6]],row[columns[7]],row[columns[8]],row[columns[9]])
    myCursor.execute(query, values)


# In[82]:


mydb.commit()


# In[83]:


# Create sep_trading table
myCursor.execute("CREATE TABLE sep_trading( \
                 id int NOT NULL PRIMARY KEY, \
                 company_code int NOT NULL, \
                 date timestamp NOT NULL, \
                 open float NOT NULL, \
                 close float NOT NULL, \
                 high float NOT NULL, \
                 low float NOT NULL, \
                 volume int NOT NULL, \
                 amount float NOT NULL,\
                 change_ratio float NOT NULL, \
                 FOREIGN KEY (company_code) REFERENCES company_info(code) ON DELETE CASCADE)");


# In[84]:


# Import sep_trading file
trd = pd.read_csv('', index_col=0) #put sep_trading file dir
trd


# In[86]:


# Insert data into sep_trading table
columns = trd.columns
for index, row in trd.iterrows():
    # SQL 쿼리 실행
    query = "INSERT INTO sep_trading (id, company_code, date, open, close, high, low, volume, amount, change_ratio) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (row[columns[0]],row[columns[1]],row[columns[2]],row[columns[3]],row[columns[4]],row[columns[5]],
                row[columns[6]],row[columns[7]],row[columns[8]],row[columns[9]])
    myCursor.execute(query, values)


# In[87]:


mydb.commit()


# In[88]:


# Create description table
myCursor.execute("CREATE TABLE description( \
                 id int NOT NULL PRIMARY KEY, \
                 content varchar(100) NOT NULL, \
                 explanation text NOT NULL)");


# In[8]:


# Import description file
import pandas as pd
des = pd.read_csv('', index_col=0) #put description file dir
des


# In[90]:


# Insert data into description table
columns = des.columns
for index, row in des.iterrows():
    # SQL 쿼리 실행
    query = "INSERT INTO description (id, content, explanation) \
    VALUES (%s, %s, %s)"
    values = (row[columns[0]],row[columns[1]],row[columns[2]])
    myCursor.execute(query, values)


# In[91]:


mydb.commit()


# In[92]:


# Create review table
myCursor.execute("CREATE TABLE review( \
                 id int AUTO_INCREMENT PRIMARY KEY, \
                 company_name varchar(100) NOT NULL, \
                 comment text NOT NULL, \
                 FOREIGN KEY (company_name) REFERENCES company_info(name) ON DELETE CASCADE)");

