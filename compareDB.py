# -*- coding: utf-8 -*-
"""
#
# Author : Utkarsh Shukla
# Created date: 20 October, 2021
# Last Update: 1 November,2021
# Version: 1.0
# Description: Quick POC to Compare content in two different DB even if DBMS is different
# LANGUAGE: Pyhton
# Script: CompareDB

This is a Prototype Script file.
"""
import pandas as pd
import ibm_db
import ibm_db_dbi
import pyodbc 
import datetime


begin_time = datetime.datetime.now()
###-----------------------------Define your Variables------------------------------------#
missing_Target = None
missing_Source = None

#----------------------------------------------------------------------------------------# 
###-----------------------------Define your functions------------------------------------#

def writeExcel(fileName, dataFrame):
    # determining the name of the file
    file_name = fileName + '.xlsx'
  
    # saving the excel
    dataFrame.to_excel(file_name)
    print(  'Missing Entries is written to '+ str(file_name)+' successfully.')
  
def missingEntries(source, traget):
    diff_df = pd.merge(source, traget, how='outer', indicator='Exist')
    diff_df = diff_df.loc[diff_df['Exist'] != 'both']
    missing_Target = diff_df.loc[diff_df['Exist'] != 'right_only']
    missing_Source = diff_df.loc[diff_df['Exist'] != 'left_only']
    writeExcel('missing_entries_from_SQL_Server', missing_Target)
    writeExcel('missing_entries_from_DB2', missing_Source)
    return missing_Source,missing_Target
    
def dataCorrection(source, traget):
    source.columns= source.columns.str.strip().str.upper()
    traget.columns= source.columns.str.strip().str.upper()

def dropNonColumns(source, traget):
    source = source.drop(labels="ROWSTAMP", axis=1)
    traget = traget.drop(labels="ROWSTAMP", axis=1)
    source = source.drop(labels="MAXOBJECTID", axis=1)
    traget = traget.drop(labels="MAXOBJECTID", axis=1)

def compareTables(source, missing_Source, traget,missing_Target):
    #print(source.info())
    #print(traget.info())
    sourceClean = pd.merge(source, missing_Target, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
    targetClean = pd.merge(traget, missing_Source, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
    # sort Brand in an ascending order
    sourceClean.sort_values(by=['OBJECTNAME'], inplace=True)
    targetClean.sort_values(by=['OBJECTNAME'], inplace=True)
    sourceClean.reset_index(drop=True, inplace=True)
    targetClean.reset_index(drop=True, inplace=True)
    #writeExcel('CleanDB2', sourceClean)
    #writeExcel('CleanSQL', targetClean)
    comparisionDF = sourceClean.compare(targetClean, keep_equal=False)
    if comparisionDF.shape[0] == 0:
        print('There are no disparity in source and Table to display')
    else:
        writeExcel('comparisionDF', comparisionDF)
        
    


#-----------------------------------------------------------------------------------------#   

""" This is for Sql Server """
server = '10.0.0.23' 
database = 'maxdb76' 
username = 'maximo' 
password = 'maximo@123' 
sqlsrv = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sqlsrv.cursor()
sqlattDF = pd.read_sql_query('SELECT * FROM maxobject order by objectname desc', sqlsrv)




""" This is for DB2"""
conn_str='database=maxdb;hostname=10.0.0.18;port=50005;protocol=tcpip;uid=maximo;pwd=JLL@Maximo95'
db2 = ibm_db.connect(conn_str,'','')


#db2engine = create_engine("db2+ibm_db://10.0.0.18:50005/maxdb")
db2conn = ibm_db_dbi.Connection(db2)
asset = "select * from maxobject order by objectname desc"
db2attDF = pd.read_sql(asset, db2conn)
# Compare the Attributes 

# %%

#------------------------------------------ Main Program -----------------------------------#
    
dataCorrection(db2attDF, sqlattDF)
###--------------------- Drop Non-Usefull Columns ------------------------------------------#
db2attDF = db2attDF.drop(labels="ROWSTAMP", axis=1)
sqlattDF = sqlattDF.drop(labels="ROWSTAMP", axis=1)
db2attDF = db2attDF.drop(labels="MAXOBJECTID", axis=1)
sqlattDF = sqlattDF.drop(labels="MAXOBJECTID", axis=1)
#-------------------------------------------------------------------------------------------# 

missing_Source,missing_Target = missingEntries(db2attDF, sqlattDF)

compareTables(db2attDF, missing_Source, sqlattDF, missing_Target)

execution_time = datetime.datetime.now() - begin_time

print (execution_time)
## -> 
