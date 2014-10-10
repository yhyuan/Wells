# Required packages: arcpy from ArcGIS 10.1 and pyodbc from https://code.google.com/p/pyodbc/. 
# visit https://code.google.com/p/pyodbc/downloads/list and download pyodbc-3.0.7.win32-py2.7.exe
# Input data: 
#        1) An Access database named VW_GMAP_HTML_04.mdb contains two tables: VW_GMAP_LL_04 and VW_GMAP_HTML_04. 
#		Fields in VW_GMAP_LL_04 LL_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "X": 2, "Y": 3, "BHK": 4, "PREV_WELL_ID": 5, "DPBR_M": 6, "WELL_TYPE": 7, "DEPTH_M": 8, "YEAR_COMPLETED": 9, "WELL_COMPLETED_DATE": 10, "RECEIVED_DATE": 11, "AUDIT_NO": 12, "TAG": 13, "CONTRACTOR": 14, "SWL": 15, "FINAL_STATUS_DESCR": 16, "USE1": 17, "USE2": 18, "MOE_COUNTY_DESCR": 19, "MOE_MUNICIPALITY_DESCR": 20, "CON": 21, "LOT": 22, "STREET": 23, "CITY": 24}
#		Fields in VW_GMAP_HTML_04 HT_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "WELL_COMPLETED_DATE": 2, "RECEIVED_DATE": 3, "AUDIT_NO": 4, "TAG": 5, "CONTRACTOR": 6, "SWL": 7, "FINAL_STATUS_DESCR": 8, "USE1": 9, "USE2": 10, "MOE_COUNTY_DESCR": 11, "MOE_MUNICIPALITY_DESCR": 12, "CON": 13, "LOT": 14, "STREET": 15, "CITY": 16, "UTMZONE": 17, "EAST83": 18, "NORTH83": 19, "GEO": 20, "PLUG": 21, "HOLE": 22, "CM": 23, "CAS": 24, "SCRN": 25, "WAT": 26, "PT": 27, "PTD": 28, "DISINFECTED": 29}
#        2) An Access database named PDFpath.mdb contains one table: WellPath00
#          Fields: WELL_ID, PDF_PATH, PDF_CHANGE_DTTM          
#        3) readme_Wells.txt, Wells.msd, Wells.mxd
# Steps: 1) Use C:\Windows\SysWOW64\odbcad32.exe (The default one in control panel might not work since it is 64 bit) to create a ODBC User DSN using Wells as the name for VW_GMAP_HTML_04.mdb since the office is 32 bit.
# Use C:\Windows\SysWOW64\odbcad32.exe to create a ODBC User DSN using PDFpath as the name for PDFpath.mdb.
# Output data: 
#		A zip file named Wells.zip contains a file geodatabases named Wells.gdb, Wells.mxs, Wells.msd, readme.txt
#       Sometimes, the zipping may failed because of the files in geodatabase is still being used during zipping process. Just zip the files after the script is stopped. 
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

def createFeatureClass(featureName, featureData, featureFieldList, featureInsertCursorFields):
	print "Create " + featureName + " feature class"
	featureNameNAD83 = featureName + "_NAD83"
	featureNameNAD83Path = arcpy.env.workspace + "\\"  + featureNameNAD83
	arcpy.CreateFeatureclass_management(arcpy.env.workspace, featureNameNAD83, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# Process: Define Projection
	arcpy.DefineProjection_management(featureNameNAD83Path, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	# Process: Add Fields	
	for featrueField in featureFieldList:
		arcpy.AddField_management(featureNameNAD83Path, featrueField[0], featrueField[1], featrueField[2], featrueField[3], featrueField[4], featrueField[5], featrueField[6], featrueField[7], featrueField[8])
	# Process: Append the records
	cntr = 1
	try:
		with arcpy.da.InsertCursor(featureNameNAD83, featureInsertCursorFields) as cur:
			for rowValue in featureData:
				cur.insertRow(rowValue)
				cntr = cntr + 1
	except Exception as e:
		print "\tError: " + featureName + ": " + e.message
	# Change the projection to web mercator
	arcpy.Project_management(featureNameNAD83Path, arcpy.env.workspace + "\\" + featureName, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	#arcpy.FeatureClassToShapefile_conversion([featureNameNAD83Path], OUTPUT_PATH + "\\Shapefile")
	arcpy.Delete_management(featureNameNAD83Path, "FeatureClass")
	print "Finish " + featureName + " feature class."

print "Create Wells feature class"
featureName = "WellsBasic"
featureFieldList = [["BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["WELL_ID", "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", ""], ["DEPTH_M", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["YEAR_COMPLETED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],  ["WELL_COMPLETED_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["AUDIT_NO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],  ["TAG_NO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["CONTRACTOR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],  ["PATH", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
featureInsertCursorFields = ("SHAPE@XY", "BORE_HOLE_ID",  "WELL_ID",  "DEPTH_M",  "YEAR_COMPLETED",  "WELL_COMPLETED_DATE",  "AUDIT_NO",  "TAG_NO",  "CONTRACTOR", "PATH")

cnxn = pyodbc.connect('DSN=PDFpath')
cursor = cnxn.cursor()
cursor.execute("select WELL_ID,PDF_PATH from WellPath00")
rows = cursor.fetchall()
pathDict = {}
for row in rows:
	pathDict[row[0]] = row[1]
print "Load data to Wells feature class"
cnxn = pyodbc.connect('DSN=Wells')
cursor = cnxn.cursor()
print "Start to load WWIS_OWNER_VW_GMAP_LL_04"
cursor.execute("select X,Y,BORE_HOLE_ID,WELL_ID,DEPTH_M,YEAR_COMPLETED,WELL_COMPLETED_DATE,AUDIT_NO,TAG,CONTRACTOR, BHK from WWIS_OWNER_VW_GMAP_LL_04" + WHERE)
rows = cursor.fetchall()
print "WWIS_OWNER_VW_GMAP_LL_04 is loaded successfully"
#wellsDict = {};
#BHKwellsDict = {};
#for row in rows:
#	BHKwellsDict[row[2]] = row[10]  # use BORE_HOLE_ID (row[2]) as unique key
BHKwellsDict = {};
for row in rows:
	BHKwellsDict[str(row[2])] = row[10]  # use BORE_HOLE_ID (row[2]) as unique key
def getWellsRow(row):
	path = ""
	if (row[3] in pathDict):
		path = pathDict[row[3]]
	return [(row[0], row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], path]
rows = map(getWellsRow, rows)
createFeatureClass(featureName, rows, featureFieldList, featureInsertCursorFields)
pathDict = {}
def toSting(item):
	if not item:
		return " "
	itemStr = str(item)
	return itemStr

print "Start to load WWIS_OWNER_VW_GMAP_HTML_04"
cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2, MOE_COUNTY_DESCR, MOE_MUNICIPALITY_DESCR, CON, LOT, STREET, CITY, UTMZONE, EAST83, NORTH83, GEO, PLUG, HOLE, CM, CAS, SCRN, WAT, PT, PTD, DISINFECTED from WWIS_OWNER_VW_GMAP_HTML_04"  + WHERE)
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
f.write("Total Records: " + str(count) + "\n")
f.close()

print len(BHKwellsDict) 
#print BHKwellsDict

featureName = "WellsMore"
# , "BHK", 
featureFieldList = [["BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["WELL_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],  ["WELL_COMPLETED_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["RECEIVED_DATE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["AUDIT_NO", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["TAG", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["CONTRACTOR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["SWL", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["FINAL_STATUS_DESCR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["USE1", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["USE2", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], 	["MOE_COUNTY_DESCR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["MOE_MUNICIPALITY_DESCR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["CON", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["LOT", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["STREET", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["CITY", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["UTMZONE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["EAST83", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""],	["NORTH83", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["GEO", "TEXT", "", "", "3000", "", "NULLABLE", "NON_REQUIRED", ""],["PLUG", "TEXT", "", "", "1000", "", "NULLABLE", "NON_REQUIRED", ""],["HOLE", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["CM", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["CAS", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["SCRN", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["WAT", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["PT", "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", ""],["PTD", "TEXT", "", "", "500", "", "NULLABLE", "NON_REQUIRED", ""],["DISINFECTED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
fieldList = map(lambda fieldInfo: fieldInfo[0], featureFieldList)
#featureInsertCursorFields = ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")
featureInsertCursorFields = tuple(["SHAPE@XY"] + fieldList + ["BHK"])
#print(len(featureFieldList))
#print(len(list(featureInsertCursorFields)))
featureNameNAD83 = featureName + "_NAD83"
featureNameNAD83Path = arcpy.env.workspace + "\\"  + featureNameNAD83
arcpy.CreateFeatureclass_management(arcpy.env.workspace, featureNameNAD83, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
# Process: Define Projection
arcpy.DefineProjection_management(featureNameNAD83Path, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
# Process: Add Fields
featureFieldList = featureFieldList + [["BHK", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
for featrueField in featureFieldList:
	arcpy.AddField_management(featureNameNAD83Path, featrueField[0], featrueField[1], featrueField[2], featrueField[3], featrueField[4], featrueField[5], featrueField[6], featrueField[7], featrueField[8])

cntr = 0
cnxn = pyodbc.connect('DSN=Wells')
cursor = cnxn.cursor()
cursor.execute("select " + ", ".join(fieldList) + " from WWIS_OWNER_VW_GMAP_HTML_04")
#cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2, MOE_COUNTY_DESCR,MOE_MUNICIPALITY_DESCR,CON,LOT,STREET,CITY,UTMZONE,EAST83,NORTH83,GEO,PLUG,HOLE,CM,CAS,SCRN,WAT,PT,PTD,DISINFECTED from WWIS_OWNER_VW_GMAP_HTML_04")
try:
	with arcpy.da.InsertCursor(featureNameNAD83, featureInsertCursorFields) as cur:
		while 1:
			row = cursor.fetchone()
			if not row:
				break
			BHK = ""
			if (str(row[0]) in BHKwellsDict):
				BHK = BHKwellsDict[str(row[0])]
			cur.insertRow([(0, 0)] + map(lambda item: " " if (not item) else str(item), row) + [BHK])
			cntr = cntr + 1
except Exception as e:
	print e.message
# Change the projection to web mercator
arcpy.Project_management(featureNameNAD83Path, arcpy.env.workspace + "\\" + featureName, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(featureNameNAD83Path, "FeatureClass")
print "Finish " + featureName + " feature class."

arcpy.AddIndex_management ("WellsMore", "BORE_HOLE_ID", "BORE_HOLE_IDIndex", "UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "BORE_HOLE_ID", "BORE_HOLE_IDIndex", "UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "WELL_ID", "WELL_IDIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "DEPTH_M", "DEPTH_MIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "YEAR_COMPLETED", "YEAR_COMPLETEDIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "WELL_COMPLETED_DATE", "WELL_COMPLETED_DATEIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "AUDIT_NO", "AUDIT_NOIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "TAG_NO", "TAG_NOIndex", "NON_UNIQUE", "ASCENDING")
arcpy.AddIndex_management ("WellsBasic", "CONTRACTOR", "CONTRACTORIndex", "NON_UNIQUE", "ASCENDING")

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

print "Remvoe useless files"
os.system("del " + OUTPUT_PATH + "\\Wells.msd")
os.system("del " + OUTPUT_PATH + "\\Wells.mxd")
os.system("del " + OUTPUT_PATH + "\\readme_Wells.txt")
os.system("rmdir " + OUTPUT_PATH + "\\Wells.gdb /s /q")

elapsed_time = time.time() - start_time
print elapsed_time
