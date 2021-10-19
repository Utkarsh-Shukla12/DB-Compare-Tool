# -*- coding: utf-8 -*-
"""
Author: Utkarsh Shukla
Created Date: 19 October, 2021
This is a Prototype Script file.
"""
import pandas as pd
import ibm_db
import ibm_db_dbi
import pyodbc 


""" This is for Sql Server """
server = '10.0.0.23' 
database = 'maxdb76' 
username = 'maximo' 
password = 'maximo@123' 
sqlsrv = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sqlsrv.cursor()
sqlattDF = pd.read_sql_query('SELECT * FROM maxattribute', sqlsrv)




""" This is for DB2"""
conn_str='database=maxdb;hostname=10.0.0.18;port=50005;protocol=tcpip;uid=maximo;pwd=JLL@Maximo95'
db2 = ibm_db.connect(conn_str,'','')
#db2 = ibm_db.connect('maxdb', 'maximo', 'JLL@Maximo95')
#db2 = create_engine('ibm_db_sa://maximo:JLL@Maximo95@10.0.0.18:50005/maxdb')

#db2engine = create_engine("db2+ibm_db://10.0.0.18:50005/maxdb")
db2conn = ibm_db_dbi.Connection(db2)
asset = "select * from maxattribute"
db2attDF = pd.read_sql(asset, db2conn)
# Compare the Attributes 
#print('SQL Maxattributes are ' + str(db2attDF.shape))
#print('DB2 Maxattributes are ' + str(sqlattDF.shape))
#db2attDF.compare(sqlattDF)
# %%
db2attDF = db2attDF.drop(labels="ROWSTAMP", axis=1)
sqlattDF = sqlattDF.drop(labels="rowstamp", axis=1)

#db2attDF.info()
#sqlattDF.info()


## -> 

db2attDF.rename(columns = lambda x : x + '_file1', inplace = True)
sqlattDF.rename(columns = lambda x : x + '_file2', inplace = True)
# %%
df_join = db2attDF.merge(right = sqlattDF,
                    left_on = db2attDF.columns.to_list(),
                    right_on = sqlattDF.columns.to_list(),
                    how = 'outer')

records_present_in_db2attDF_not_in_sqlattDF = df_join.loc[df_join[sqlattDF.columns.to_list()].isnull().all(axis = 1), db2attDF.columns.to_list()]
# %%
records_present_in_sqlattDF_not_in_db2attDF = df_join.loc[df_join[db2attDF.columns.to_list()].isnull().all(axis = 1), sqlattDF.columns.to_list()]

print (records_present_in_db2attDF_not_in_sqlattDF)
print (records_present_in_sqlattDF_not_in_db2attDF)
#print (db2attDF)
#print (sqlattDF)
