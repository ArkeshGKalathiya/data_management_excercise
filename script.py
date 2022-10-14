# %%
# pip3 install xlrd
# pip3 install mysql-connector-python


# changes done by ARKESH in database

############## Employee ##################
# added AUTO_INCREMENT to EmployeeId


############## RegionalDiv ##################
# added AUTO_INCREMENT to RegionId
# removed city
# removed state
# changed EmployeeId to ManagerId
# add UNIQUE constraint to column region


############## Created Segment Table #############
############## Created Sub Category Table #############
############## Modified Category Table Completely #############

############## Product ##################
# added AUTO_INCREMENT to ProductId
# added ProductCode : Unique Key ( for ex : FUR-BO-10001798)
# added categoryId
# added subCategoryId


##### NOTES ######

#1 There is no relation between segment and category
#2 region names are converted into lower case

import pandas as pd
import mysql.connector as connector


bootstrapFile = './bootstrap.sql'
dbName = 'sample_superstore'


connection = connector.connect(host='localhost', user="root")


def getSheet(name):
    sheet = pd.read_excel('./sample_superstore.xls', name)
    return sheet


def bootstrapDatabase():
    cursor = connection.cursor()
    cursor.execute(f'create database if not exists {dbName}')
    cursor.execute(f'use {dbName}')

    with open(bootstrapFile) as file:
        content = file.read()
        lines = content.split(';')
        for line in lines:
            cursor.execute(line)

    connection.commit()
    cursor.close()


def loadManagers():
    people = getSheet('People')
    regionManagerMap = {}
    cursor = connection.cursor()
    for index, row in people.iterrows():
        name = row['Regional Manager']
        region = row['Region']
        cursor.execute(
            'insert into Employee (Name,Designation) values(%s,%s)', (name, 'REGION_MANAGER'))
        regionManagerMap[region.lower()] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return regionManagerMap



def loadRegions(regionManagerMap):
    regionMap = {}
    cursor = connection.cursor()
    for region in regionManagerMap:
        managerId = regionManagerMap[region]
        cursor.execute('insert into RegionalDiv (ManagerId,Region) values(%s,%s)',(managerId,region))
        regionMap[region.lower()] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return regionMap


def loadSegments():
    orders = getSheet('Orders')
    segments = orders['Segment'].unique()
    cursor = connection.cursor()
    segmentMap = {}
    for segment in segments:
        cursor.execute('insert into Segment (name) values(%s)',(segment,))
        segmentMap[segment.lower()] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return segmentMap

def loadCategories():
    orders = getSheet('Orders')
    categories = orders['Category'].unique()
    cursor = connection.cursor()
    categoryMap = {}
    for category in categories:
        cursor.execute('insert into Category (name) values(%s)',(category,))
        categoryMap[category.lower()] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return categoryMap


def loadSubCategories(categoryMap):
    orders = getSheet('Orders')
    cursor = connection.cursor()
    subToMainMap = {}
    subCategoryMap = {}
    for index, row in orders.iterrows():
        category = row['Category']
        subCategory = row['Sub-Category']
        category = category.lower()
        subCategory = subCategory.lower()
        existing = subToMainMap.get(subCategory)
        if(existing is not None and existing != category):
            print(f"Previously it was {existing} but new row says it should be {category}")
        subToMainMap[subCategory] = category

    subCategories = orders['Sub-Category'].unique()
    for subCategory in subCategories:
        sub = subCategory.lower()
        category = subToMainMap[sub]
        categoryId = categoryMap[category]
        cursor.execute('insert into SubCategory (name,CategoryId) values(%s,%s)',(subCategory,categoryId))
        subCategoryMap[sub] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return subCategoryMap
        



bootstrapDatabase()


##### CREATING REGION MAP 
regionManagerMap = loadManagers()
regionMap = loadRegions(regionManagerMap)
segmentMap = loadSegments()
categoryMap = loadCategories()
subCategoryMap = loadSubCategories(categoryMap)
print(subCategoryMap)
