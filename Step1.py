# Required packages: arcpy from ArcGIS 10.1 and pyodbc from https://code.google.com/p/pyodbc/. 
# visit https://code.google.com/p/pyodbc/downloads/list and download pyodbc-3.0.7.win32-py2.7.exe
# Input data: An Access database contains two tables: VW_GMAP_LL_04 and VW_GMAP_HTML_04. 
#		Fields in VW_GMAP_LL_04 LL_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "X": 2, "Y": 3, "BHK": 4, "PREV_WELL_ID": 5, "DPBR_M": 6, "WELL_TYPE": 7, "DEPTH_M": 8, "YEAR_COMPLETED": 9, "WELL_COMPLETED_DATE": 10, "RECEIVED_DATE": 11, "AUDIT_NO": 12, "TAG": 13, "CONTRACTOR": 14, "SWL": 15, "FINAL_STATUS_DESCR": 16, "USE1": 17, "USE2": 18, "MOE_COUNTY_DESCR": 19, "MOE_MUNICIPALITY_DESCR": 20, "CON": 21, "LOT": 22, "STREET": 23, "CITY": 24}
#		Fields in VW_GMAP_HTML_04 HT_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "WELL_COMPLETED_DATE": 2, "RECEIVED_DATE": 3, "AUDIT_NO": 4, "TAG": 5, "CONTRACTOR": 6, "SWL": 7, "FINAL_STATUS_DESCR": 8, "USE1": 9, "USE2": 10, "MOE_COUNTY_DESCR": 11, "MOE_MUNICIPALITY_DESCR": 12, "CON": 13, "LOT": 14, "STREET": 15, "CITY": 16, "UTMZONE": 17, "EAST83": 18, "NORTH83": 19, "GEO": 20, "PLUG": 21, "HOLE": 22, "CM": 23, "CAS": 24, "SCRN": 25, "WAT": 26, "PT": 27, "PTD": 28, "DISINFECTED": 29}
# Steps: 1) Use C:\Windows\SysWOW64\odbcad32.exe (The default one in control panel might not work) to create a ODBC User DSN using Wells as the name.
# Output data: 
#		A zip file contains a file geodatabases named Wells, Wells.mxs, Wells.msd, readme.txt

import sys, string, os, time, zipfile
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import pyodbc

start_time = time.time()
DEBUG = False
WHERE = ""
if DEBUG:
	WHERE = " WHERE BORE_HOLE_ID = 1000055771"

PATH = "."
OUTPUT_PATH = "output"
INPUT_PATH = "input"
if arcpy.Exists(OUTPUT_PATH + "\\Wells.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\Wells.gdb /s /q")
os.system("del " + OUTPUT_PATH + "\\*Wells*.*")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "Wells", "9.3")
arcpy.env.workspace = OUTPUT_PATH + "\\Wells.gdb"
WellsPoints = "Wells"
Wells = arcpy.env.workspace + "\\"  + WellsPoints
#if not arcpy.Exists(Wells):
# Process: Create Feature Class
print "Create Wells feature class"
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsPoints, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
# Process: Define Projection
arcpy.DefineProjection_management(Wells, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
# Process: Add Fields	
arcpy.AddField_management(Wells, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
arcpy.AddField_management(Wells, "WELL_ID", "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "DEPTH_M", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "YEAR_COMPLETED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "WELL_COMPLETED_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "AUDIT_NO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "TAG_NO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Wells, "CONTRACTOR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#arcpy.AddField_management(Wells, "PATH", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#arcpy.AddField_management(Wells, "URL_EN", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#arcpy.AddField_management(Wells, "URL_FR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#else:
#	arcpy.DeleteRows_management(Wells)

print "Load data to Wells feature class"
cnxn = pyodbc.connect('DSN=Wells')
cursor = cnxn.cursor()
print "Start to load WWIS_OWNER_VW_GMAP_LL_04"
cursor.execute("select X,Y,BORE_HOLE_ID,WELL_ID,DEPTH_M,YEAR_COMPLETED,WELL_COMPLETED_DATE,AUDIT_NO,TAG,CONTRACTOR, BHK from WWIS_OWNER_VW_GMAP_LL_04" + WHERE)
rows = cursor.fetchall()
print "WWIS_OWNER_VW_GMAP_LL_04 is loaded successfully"
#wellsDict = {};
BHKwellsDict = {};
try:
	#with arcpy.da.InsertCursor(WellsPoints, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "DEPTH_M", "YEAR_COMPLETED", "WELL_COMPLETED_DATE", "AUDIT_NO", "TAG_NO", "CONTRACTOR", "URL_EN", "URL_FR")) as cur:
	with arcpy.da.InsertCursor(WellsPoints, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "DEPTH_M", "YEAR_COMPLETED", "WELL_COMPLETED_DATE", "AUDIT_NO", "TAG_NO", "CONTRACTOR", "PATH")) as cur:
		cntr = 1
		for row in rows:
			#wellsDict[row[2]] = row  # use BORE_HOLE_ID (row[2]) as unique key
			BHKwellsDict[row[2]] = row[10]  # use BORE_HOLE_ID (row[2]) as unique key
			#rowValue = [(row[0], row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", ""]
			rowValue = [(row[0], row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]
			cur.insertRow(rowValue)
			#print "Record number " + str(cntr) + " was written to feature class " + WellsPoints
			cntr = cntr + 1
			#if cntr > 1000:
			#	break
except Exception as e:
	print e.message

def toSting(item):
	if not item:
		return " "
	itemStr = str(item)
	#while "\r\n" in itemStr:
	#	itemStr = itemStr.replace("\r\n", "")		
	return itemStr

print "Start to load WWIS_OWNER_VW_GMAP_HTML_04"
cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2, MOE_COUNTY_DESCR, MOE_MUNICIPALITY_DESCR, CON, LOT, STREET, CITY, UTMZONE, EAST83, NORTH83, GEO, PLUG, HOLE, CM, CAS, SCRN, WAT, PT, PTD, DISINFECTED from WWIS_OWNER_VW_GMAP_HTML_04"  + WHERE)
#rows = cursor.fetchall()
f = open ("rows_contaion_enter.txt","w")
count = 0
while 1:
	row = cursor.fetchone()
	if not row:
		break
	line = "\t".join(map(toSting, row))
	count = count + 1
	if ("\r\n" in line):
		f.write(line + "\n")		
print "WWIS_OWNER_VW_GMAP_HTML_04 is loaded successfully"
f.write(str(count) + "\n")
f.close()

print "Create WellsReport0 feature class"
WellsReports = "WellsReport0"
WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReports
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReports, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
arcpy.DefineProjection_management(WellsReportsLayer, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.AddField_management(WellsReportsLayer, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
#fields = ["WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83"]
fields = ["WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2"]
for field in fields:
	arcpy.AddField_management(WellsReportsLayer, field, "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

'''arcpy.AddField_management(WellsReportsLayer, "GEO", "TEXT", "", "", "3000", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WellsReportsLayer, "PLUG", "TEXT", "", "", "1000", "", "NULLABLE", "NON_REQUIRED", "")
fields = ["HOLE", "CM", "CAS", "SCRN", "WAT", "PT"]
for field in fields:
	arcpy.AddField_management(WellsReportsLayer, field, "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WellsReportsLayer, "PTD", "TEXT", "", "", "500", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WellsReportsLayer, "DISINFECTED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
'''	
cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2 from WWIS_OWNER_VW_GMAP_HTML_04"  + WHERE)
rows = cursor.fetchall()
cntr = 0
try:
	#with arcpy.da.InsertCursor(WellsReports, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")) as cur:
	with arcpy.da.InsertCursor(WellsReports, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2")) as cur:
		for row in rows:
			#bRow = wellsDict[row[0]]  # use BORE_HOLE_ID (row[0]) as unique key
			BHK = BHKwellsDict[row[0]]
			row = map(toSting, row)			
			#rowValue = [(0, 0), row[0], row[1], " ", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			#rowValue = [(bRow[0], bRow[1]), row[0], row[1], bRow[10], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			#print rowValue
			#rowValue = [(bRow[0], bRow[1]), row[0], row[1], bRow[10], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
			rowValue = [(0, 0), row[0], row[1], BHK, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == count):
	print "WellsReport0 is created successfully!"
else:
	print "WellsReport0 is NOT created successfully!"

print "Create WellsReport1 feature class"
WellsReport1 = "WellsReport1"
#WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReport1
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReport1, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
arcpy.DefineProjection_management(arcpy.env.workspace + "\\"  + WellsReport1, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport1, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")
fields = ["MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83"]
for field in fields:
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport1, field, "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	
cursor.execute("select BORE_HOLE_ID, MOE_COUNTY_DESCR, MOE_MUNICIPALITY_DESCR, CON, LOT, STREET, CITY, UTMZONE, EAST83, NORTH83 from WWIS_OWNER_VW_GMAP_HTML_04"  + WHERE)
rows = cursor.fetchall()

cntr = 0
try:
	with arcpy.da.InsertCursor(WellsReport1, ("SHAPE@XY", "BORE_HOLE_ID", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83")) as cur:
		for row in rows:
			row = map(toSting, row)			
			rowValue = [(0, 0), row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == count):
	print "WellsReport1 is created successfully!"
else:
	print "WellsReport1 is NOT created successfully!"

print "Create WellsReport2 feature class"	
WellsReport2 = "WellsReport2"
#WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReport2
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReport2, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
arcpy.DefineProjection_management(arcpy.env.workspace + "\\"  + WellsReport2, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "NON_REQUIRED", "")

arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "GEO", "TEXT", "", "", "3000", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "PLUG", "TEXT", "", "", "1000", "", "NULLABLE", "NON_REQUIRED", "")
fields = ["HOLE", "CM", "CAS", "SCRN", "WAT", "PT"]
for field in fields:
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, field, "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "PTD", "TEXT", "", "", "500", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "DISINFECTED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

cursor.execute("select BORE_HOLE_ID, GEO, PLUG, HOLE, CM, CAS, SCRN, WAT, PT, PTD, DISINFECTED from WWIS_OWNER_VW_GMAP_HTML_04"  + WHERE)
rows = cursor.fetchall()

cntr = 0
try:
	with arcpy.da.InsertCursor(WellsReport2, ("SHAPE@XY", "BORE_HOLE_ID", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")) as cur:
		for row in rows:
			row = map(toSting, row)			
			rowValue = [(0, 0), row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == count):
	print "WellsReport2 is created successfully!"
else:
	print "WellsReport2 is NOT created successfully!"

'''
print "Calculate the fields from WellsReport1"
WellsReport0 = "WellsReport0"
fields = ["MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83"]
for field in fields:
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, field, "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
print "Make Layer for WellsReport0"
arcpy.MakeFeatureLayer_management(arcpy.env.workspace + "\\"  + WellsReport0, WellsReport0 + "_Layer1", "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;BORE_HOLE_ID BORE_HOLE_ID VISIBLE NONE;WELL_ID WELL_ID VISIBLE NONE;BHK BHK VISIBLE NONE;WELL_COMPLETED_DATE WELL_COMPLETED_DATE VISIBLE NONE;RECEIVED_DATE RECEIVED_DATE VISIBLE NONE;AUDIT_NO AUDIT_NO VISIBLE NONE;TAG TAG VISIBLE NONE;CONTRACTOR CONTRACTOR VISIBLE NONE;SWL SWL VISIBLE NONE;FINAL_STATUS_DESCR FINAL_STATUS_DESCR VISIBLE NONE;USE1 USE1 VISIBLE NONE;USE2 USE2 VISIBLE NONE;MOE_COUNTY_DESCR MOE_COUNTY_DESCR VISIBLE NONE;MOE_MUNICIPALITY_DESCR MOE_MUNICIPALITY_DESCR VISIBLE NONE;CON CON VISIBLE NONE;LOT LOT VISIBLE NONE;STREET STREET VISIBLE NONE;CITY CITY VISIBLE NONE;UTMZONE UTMZONE VISIBLE NONE;EAST83 EAST83 VISIBLE NONE;NORTH83 NORTH83 VISIBLE NONE;")
print "Make Layer for WellsReport1"
arcpy.MakeFeatureLayer_management(arcpy.env.workspace + "\\"  + WellsReport1, WellsReport1 + "_Layer1", "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;BORE_HOLE_ID BORE_HOLE_ID VISIBLE NONE;MOE_COUNTY_DESCR MOE_COUNTY_DESCR VISIBLE NONE;MOE_MUNICIPALITY_DESCR MOE_MUNICIPALITY_DESCR VISIBLE NONE;CON CON VISIBLE NONE;LOT LOT VISIBLE NONE;STREET STREET VISIBLE NONE;CITY CITY VISIBLE NONE;UTMZONE UTMZONE VISIBLE NONE;EAST83 EAST83 VISIBLE NONE;NORTH83 NORTH83 VISIBLE NONE")
print "Add Join between WellsReport0 and WellsReport1"
arcpy.AddJoin_management(WellsReport0 + "_Layer1", "BORE_HOLE_ID", WellsReport1 + "_Layer1", "BORE_HOLE_ID", "KEEP_ALL")
print "Start Calculating fields"
for field in fields:
	print "Calculate field: " + field
	arcpy.CalculateField_management(WellsReport0 + "_Layer1", WellsReport0 + "." + field, "[" + WellsReport1 + "." + field + "]", "VB", "")
arcpy.RemoveJoin_management(WellsReport0 + "_Layer", "")

print "Calculate the fields from WellsReport2"
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, "GEO", "TEXT", "", "", "3000", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, "PLUG", "TEXT", "", "", "1000", "", "NULLABLE", "NON_REQUIRED", "")
fields = ["HOLE", "CM", "CAS", "SCRN", "WAT", "PT"]
for field in fields:
	print "Calculate field: " + field
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, field, "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, "PTD", "TEXT", "", "", "500", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport0, "DISINFECTED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.MakeFeatureLayer_management(arcpy.env.workspace + "\\"  + WellsReport2, WellsReport2 + "_Layer", "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;BORE_HOLE_ID BORE_HOLE_ID VISIBLE NONE;GEO GEO VISIBLE NONE;PLUG PLUG VISIBLE NONE;HOLE HOLE VISIBLE NONE;CM CM VISIBLE NONE;CAS CAS VISIBLE NONE;SCRN SCRN VISIBLE NONE;WAT WAT VISIBLE NONE;PT PT VISIBLE NONE;PTD PTD VISIBLE NONE;DISINFECTED DISINFECTED VISIBLE NONE")
arcpy.AddJoin_management(WellsReport0 + "_Layer", "BORE_HOLE_ID", WellsReport2 + "_Layer", "BORE_HOLE_ID", "KEEP_ALL")
fields = ["GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]
for field in fields:
	arcpy.CalculateField_management(WellsReport0 + "_Layer", WellsReport0 + "." + field, "[" + WellsReport2 + "." + field + "]", "VB", "")
arcpy.RemoveJoin_management(WellsReport0 + "_Layer", "")

arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport1" , "FeatureClass")
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport2" , "FeatureClass")
#arcpy.DeleteField_management(arcpy.env.workspace + "\\WellsReport0", "OBJECTID_1;BORE_HOLE_ID_1;OBJECTID_12;BORE_HOLE_ID_12")

arcpy.Project_management(arcpy.env.workspace + "\\WellsReport0", arcpy.env.workspace + "\\WellsMore", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Project_management(arcpy.env.workspace + "\\" + WellsPoints, arcpy.env.workspace + "\\WellsBasic", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(arcpy.env.workspace + "\\WellsReport0", "FeatureClass")
arcpy.Delete_management(arcpy.env.workspace + "\\" + WellsPoints, "FeatureClass")

print "Copy mxd, msd and create readme file"
# Prepare the msd, mxd, and readme.txt
os.system("copy " + INPUT_PATH + "\\Wells.msd " + OUTPUT_PATH)
os.system("copy " + INPUT_PATH + "\\Wells.mxd " + OUTPUT_PATH)
f = open (INPUT_PATH + "\\readme_Wells.txt","r")
data = f.read()
f.close()
#import time
dateString = time.strftime("%Y/%m/%d", time.localtime())
data = data.replace("[DATE]", dateString)
f = open (OUTPUT_PATH + "\\readme_Wells.txt","w")
f.write(data)
f.close()


print "Compress and create Wells.zip file"
# Compress the files together into a zip file
#from zipfile_infolist import print_info
target_dir = OUTPUT_PATH + '\\Wells.gdb'
zip = zipfile.ZipFile(OUTPUT_PATH + '\\Wells.zip', 'w', zipfile.ZIP_DEFLATED)
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
	for file in files:
		#print file[-4:]
		fn = os.path.join(base, file)
		#if file[-4:] != "lock":
		zip.write(fn, "Wells.gdb\\" + fn[rootlen:])
zip.write(OUTPUT_PATH + '\\Wells.msd', "Wells.msd")
zip.write(OUTPUT_PATH + '\\Wells.mxd', "Wells.mxd")
zip.write(OUTPUT_PATH + '\\readme_Wells.txt', "readme_Wells.txt")
zip.close()
'''
elapsed_time = time.time() - start_time
print elapsed_time