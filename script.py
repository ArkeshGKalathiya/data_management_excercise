# %%
# pip3 install xlrd
# pip3 install mysql-connector-python


# changes done


# EXCEL
# ADDED 05401 as ZIPCODE FOR VERMONT CITY ( IT WAS EMPTY )

############## GENERAL NOTES ##################
# added AUTO_INCREMENT to every table's primary key
# added unique id for column such as CustomerCode, ProductCode, OrderCode ( in excel it's referred as Customer ID, Product ID)


# 1. There is no relation between segment and category
# 2. Region names are converted into lower case
# 3. There is conflict in Product ID and Product Name (i.e. same product id contains multiple names, we have saved rows with first occurrence of the name)
#
#       FUR-CH-10001146
#       ["Global Value Mid-Back Manager's Chair, Gray", 'Global Task Chair, Black']
#       OFF-PA-10001970
#       ['Xerox 1881', 'Xerox 1908']
#       OFF-ST-10001228
#       ['Fellowes Personal Hanging Folder Files, Navy', 'Personal File Boxes with Fold-Down Carry Handle']
#       TEC-AC-10003832
#       ['Logitech\xa0P710e Mobile Speakerphone', 'Imation\xa016GB Mini TravelDrive USB 2.0\xa0Flash Drive']
#       OFF-PA-10002377
#       ['Xerox 1916', 'Adams Telephone Message Book W/Dividers/Space For Phone Numbers, 5 1/4"X8 1/2", 200/Messages']
#       TEC-PH-10001530
#       ['Cisco Unified IP Phone 7945G VoIP phone', 'Plantronics Voyager Pro Legend']
#       OFF-AP-10000576
#       ['Belkin 7 Outlet SurgeMaster II', "Belkin 325VA UPS Surge Protector, 6'"]
#       OFF-BI-10004632
#       ['Ibico Hi-Tech Manual Binding System', 'GBC Binding covers']
#       FUR-FU-10004091
#       ['Howard Miller 13" Diameter Goldtone Round Wall Clock', 'Eldon 200 Class Desk Accessories, Black']
#       TEC-AC-10002049
#       ['Logitech G19 Programmable Gaming Keyboard', 'Plantronics Savi W720 Multi-Device Wireless Headset System']
#       OFF-PA-10000357
#       ['White Dual Perf Computer Printout Paper, 2700 Sheets, 1 Part, Heavyweight, 20 lbs., 14 7/8 x 11', 'Xerox 1888']
#       FUR-FU-10001473
#       ['DAX Wood Document Frame', 'Eldon Executive Woodline II Desk Accessories, Mahogany']
#       OFF-PA-10000477
#       ['Xerox 1952', 'Xerox 22']
#       OFF-PA-10000659
#       ['Adams Phone Message Book, Professional, 400 Message Capacity, 5 3/6” x 11”', 'TOPS Carbonless Receipt Book, Four 2-3/4 x 7-1/4 Money Receipts per Page']
#       FUR-FU-10004848
#       ['Howard Miller 13-3/4" Diameter Brushed Chrome Round Wall Clock', 'DAX Solid Wood Frames']
#       FUR-BO-10002213
#       ['DMI Eclipse Executive Suite Bookcases', 'Sauder Forest Hills Library, Woodland Oak Finish']
#       TEC-PH-10002310
#       ['Panasonic KX T7731-B Digital phone', 'Plantronics Calisto P620-M USB Wireless Speakerphone System']
#       FUR-FU-10004270
#       ['Eldon Image Series Desk Accessories, Burgundy', 'Executive Impressions 13" Clairmont Wall Clock']
#       TEC-PH-10004531
#       ['OtterBox Commuter Series Case - iPhone 5 & 5s', 'AT&T CL2909']
#       OFF-BI-10004654
#       ['Avery Binding System Hidden Tab Executive Style Index Sets', 'VariCap6 Expandable Binder']
#       TEC-PH-10002200
#       ['Samsung Galaxy Note 2', 'Aastra 6757i CT Wireless VoIP phone']
#       OFF-ST-10004950
#       ['Acco Perma 3000 Stacking Storage Drawers', 'Tenex Personal Filing Tote With Secure Closure Lid, Black/Frost']
#       TEC-MA-10001148
#       ['Swingline SM12-08 MicroCut Jam Free Shredder', 'Okidata MB491 Multifunction Printer']
#       OFF-AR-10001149
#       ['Sanford Colorific Colored Pencils, 12/Box', 'Avery Hi-Liter Comfort Grip Fluorescent Highlighter, Yellow Ink']
#       TEC-AC-10002550
#       ['Maxell 4.7GB DVD-RW 3/Pack', 'Memorex 25GB 6X Branded Blu-Ray Recordable Disc, 30/Pack']
#       OFF-PA-10002195
#       ['RSVP Cards & Envelopes, Blank White, 8-1/2" X 11", 24 Cards/25 Envelopes/Set', 'Xerox 1966']
#       FUR-FU-10004017
#       ['Tenex Contemporary Contur Chairmats for Low and Medium Pile Carpet, Computer, 39" x 49"', 'Executive Impressions 13" Chairman Wall Clock']
#       OFF-PA-10001166
#       ['Xerox 2', 'Xerox 1932']
#       FUR-FU-10004864
#       ['Howard Miller 14-1/2" Diameter Chrome Round Wall Clock', 'Eldon 500 Class Desk Accessories']
#       OFF-PA-10003022
#       ['Xerox 1992', 'Standard Line “While You Were Out” Hardbound Telephone Message Book']
#       TEC-PH-10001795
#       ['ClearOne CHATAttach 160 -\xa0speaker phone', 'RCA H5401RE1 DECT 6.0 4-Line Cordless Handset With Caller ID/Call Waiting']
#       OFF-BI-10002026
#       ['Avery Arch Ring Binders', 'Ibico Recycled Linen-Style Covers']
#
#
#
#
#
# 4. WE ARE DELETING CUSTOMER ADDRESS TABLE, AND PUTTING EVERYTHING RELATED TO THAT IN SHIPMENT TABLEs
#    Please see function "loadCustomers()"", and there are each conflict checking steps and respected outcome
#    to summarize we were unable to derive unique relationship, so city, state, postal code will now belong to the Order table


from datetime import datetime
import pandas as pd
import mysql.connector as connector


bootstrapFile = './bootstrap.sql'
dbName = 'sample_superstore'


connection = connector.connect(host='localhost', user="root")


class ConflictMap:

    def __init__(self):
        self.conflictMap = {}
        self.conflictArrayMap = {}

    def injectConflict(self, key, value):
        if self.conflictArrayMap.get(key) is None:
            self.conflictArrayMap[key] = []

        if value not in self.conflictArrayMap[key]:
            self.conflictArrayMap[key].append(value)

    def inject(self, key, value):
        existing = self.conflictMap.get(key)
        if (existing is not None and existing != value):
            self.injectConflict(key, existing)
            self.injectConflict(key, value)
        self.conflictMap[key] = value

    def describeConflicts(self):
        if len(self.conflictArrayMap) == 0:
            return False
        for key in self.conflictArrayMap:
            print(key)
            print(self.conflictArrayMap[key])
        return True


def getSheet(name):
    sheet = pd.read_excel('./sample_superstore.xls', name)
    return pd.DataFrame(sheet)


def checkConflict(mainColumn, subColumns):
    orders = getSheet('Orders')
    conflictMap = ConflictMap()
    for index, row in orders.iterrows():
        key = row[mainColumn]
        values = []
        for column in subColumns:
            value = row[column]
            values.append(f"{value}")
        conflictMap.inject(key, '|'.join(values))
    return conflictMap.describeConflicts()


def getDifference(date1, date2):
    diff = date1 - date2
    seconds = abs(diff.total_seconds())
    return seconds / (3600 * 24)


########################################################################## DATABASE LOADING FUNCTIONS BELOW ##########################################################################


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
        cursor.execute(
            'insert into RegionalDiv (ManagerId,Region) values(%s,%s)', (managerId, region))
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
        cursor.execute('insert into Segment (name) values(%s)', (segment,))
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
        cursor.execute('insert into Category (name) values(%s)', (category,))
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
        if (existing is not None and existing != category):
            print(
                f"Previously it was {existing} but new row says it should be {category}")
        subToMainMap[subCategory] = category

    subCategories = orders['Sub-Category'].unique()
    for subCategory in subCategories:
        sub = subCategory.lower()
        category = subToMainMap[sub]
        categoryId = categoryMap[category]
        cursor.execute(
            'insert into SubCategory (name,CategoryId) values(%s,%s)', (subCategory, categoryId))
        subCategoryMap[sub] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return subCategoryMap


def loadProducts(categoryMap, subCategoryMap):

    # checkConflict('Product ID',['Category','Sub-Category'])
    # OUTCOME : NO CONFLICT

    # checkConflict('Product ID',['Product Name'])
    # OUTCOME : Same product ID can have multiple product names, so while entering rows into the db, we are just prioritizing first row
    # and save that name for the specific product id

    orders = getSheet('Orders')
    cursor = connection.cursor()
    productCodeMap = {}

    for index, row in orders.iterrows():
        productCode = row['Product ID']
        name = row['Product Name']
        category = row['Category'].lower()
        subCategory = row['Sub-Category'].lower()
        categoryId = categoryMap[category]
        subCategoryId = subCategoryMap[subCategory]
        cursor.execute('insert into Product (ProductName,ProductCode,CategoryId,SubCategoryId) values(%s,%s,%s,%s) ON DUPLICATE KEY update ProductCode=ProductCode',
                       (name, productCode, categoryId, subCategoryId))
        lastrowid = cursor.lastrowid
        if (lastrowid > 0):
            productCodeMap[productCode] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return productCodeMap


def loadCustomers():

    # checkConflict('Customer ID',['Customer Name'])
    # OUTCOME : NO CONFLICTS BETWEEN CustomerId and CustomerName

    # checkConflict('Customer ID',['City','State','Postal Code'])
    # OUTCOME : Same customer can have multiple address

    # checkConflict('Postal Code',['Customer ID'])
    # OUTCOME : Same postal code can have multiple customers

    # checkConflict('Postal Code',['City','State'])
    # OUTCOME : 92024 belongs to following city and state ['San Diego, California', 'Encinitas, California']

    # checkConflict('Postal Code',['Region'])
    # OUTCOME : no conflict

    orders = getSheet('Orders')
    cursor = connection.cursor()
    customerCodeMap = {}

    for index, row in orders.iterrows():
        customerCode = row['Customer ID']
        name = row['Customer Name']
        cursor.execute('insert into Customer (CustomerCode,CustomerName) values(%s,%s) ON DUPLICATE KEY update CustomerCode=CustomerCode',
                       (customerCode, name))
        lastrowid = cursor.lastrowid
        if (lastrowid > 0):
            customerCodeMap[customerCode] = cursor.lastrowid
    connection.commit()
    cursor.close()
    return customerCodeMap


def loadOrdersAndShipments(segmentMap, regionalMap, customerMap):

    # checkConflict('Order ID',['Order Date','Ship Date'])
    # OUTCOME : no conflict, meaning: single order id does not have multiple (order date + ship date)

    # checkConflict('Order ID',['Segment'])
    # OUTCOME : no conflict, that's why we can store segment id inside order table

    # checkConflict('Order ID',['Postal Code'])
    # OUTCOME : no conflict, meaning: single order id does not have multiple postal mode

    # checkConflict('Order ID',['Ship Mode'])
    # OUTCOME : no conflict, meaning: single order id does not have multiple ship mode

    orders = getSheet('Orders')
    orderShipmentMap = {}
    orderMap = {}
    cursor = connection.cursor()

    for index, row in orders.iterrows():
        orderCode = row['Order ID']
        orderDate = row['Order Date']
        customerCode = row['Customer ID']
        customerId = customerMap[customerCode]
        segment = row['Segment']
        segmentId = segmentMap[segment.lower()]
        region = row['Region']
        regionId = regionalMap[region.lower()]

        isShipmentAdded = orderShipmentMap.get(orderCode) != None
        if (isShipmentAdded == False):
            shipmentDate = row['Ship Date']
            shipmentMode = row['Ship Mode']
            city = row['City']
            state = row['State']
            postalCode = row['Postal Code']
            days = getDifference(shipmentDate, orderDate)

            cursor.execute(
                'insert into Shipment'
                ' (ShipmentDate,ShipmentMode,City,State,PostalCode,Days)'
                ' values(%s,%s,%s,%s,%s,%s)',
                (shipmentDate, shipmentMode, city, state, postalCode, days)
            )
            shipmentId = cursor.lastrowid
            orderShipmentMap[orderCode] = shipmentId

        shipmentId = orderShipmentMap[orderCode]
        cursor.execute(
            'insert into Orders'
            ' (OrderCode,OrderDate,CustomerId,ShipmentId,RegionId,SegmentId)'
            ' values(%s,%s,%s,%s,%s,%s)',
            (orderCode,orderDate,customerId,shipmentId,regionId,segmentId)
        )

        # print(parseDate(row['Order Date']).isoformat())


# checkConflict('Customer ID',['Segment'])
    # OUTCOME : no conflict


bootstrapDatabase()


# CREATING REGION MAP
regionManagerMap = loadManagers()
regionMap = loadRegions(regionManagerMap)
segmentMap = loadSegments()
categoryMap = loadCategories()
subCategoryMap = loadSubCategories(categoryMap)
productCodeMap = loadProducts(
    categoryMap=categoryMap,
    subCategoryMap=subCategoryMap,
)
customerMap = loadCustomers()
loadOrdersAndShipments(
    segmentMap=segmentMap,
    regionalMap=regionMap,
    customerMap=customerMap,
)
# %%
