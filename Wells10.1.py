# Install pyodbc from https://code.google.com/p/pyodbc/
# Pick pyodbc-3.0.6.win32-py2.5.exe since ArcGIS 9.3 only 
# support python 2.5
# Use C:\Windows\SysWOW64\odbcad32.exe (The default one in control panel might not work)
# to create a ODBC User DSN with Wells as the name. 
import sys, string, os
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import pyodbc


# Local variables...
PATH = "C:\\Users\\yuanje\\Downloads"
arcpy.env.workspace = PATH + "\\Wells.gdb"
WellsPoints = "Wells"
Wells = arcpy.env.workspace + "\\"  + WellsPoints
if not arcpy.Exists(Wells):
	# Process: Create Feature Class
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
	arcpy.AddField_management(Wells, "URL_EN", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(Wells, "URL_FR", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
else:
	arcpy.DeleteRows_management(Wells)
	
#LL_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "X": 2, "Y": 3, "BHK": 4, "PREV_WELL_ID": 5, "DPBR_M": 6, "WELL_TYPE": 7, "DEPTH_M": 8, "YEAR_COMPLETED": 9, "WELL_COMPLETED_DATE": 10, "RECEIVED_DATE": 11, "AUDIT_NO": 12, "TAG": 13, "CONTRACTOR": 14, "SWL": 15, "FINAL_STATUS_DESCR": 16, "USE1": 17, "USE2": 18, "MOE_COUNTY_DESCR": 19, "MOE_MUNICIPALITY_DESCR": 20, "CON": 21, "LOT": 22, "STREET": 23, "CITY": 24}
#HT_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "WELL_COMPLETED_DATE": 2, "RECEIVED_DATE": 3, "AUDIT_NO": 4, "TAG": 5, "CONTRACTOR": 6, "SWL": 7, "FINAL_STATUS_DESCR": 8, "USE1": 9, "USE2": 10, "MOE_COUNTY_DESCR": 11, "MOE_MUNICIPALITY_DESCR": 12, "CON": 13, "LOT": 14, "STREET": 15, "CITY": 16, "UTMZONE": 17, "EAST83": 18, "NORTH83": 19, "GEO": 20, "PLUG": 21, "HOLE": 22, "CM": 23, "CAS": 24, "SCRN": 25, "WAT": 26, "PT": 27, "PTD": 28, "DISINFECTED": 29}


cnxn = pyodbc.connect('DSN=Wells')
cursor = cnxn.cursor()

cursor.execute("select X,Y,BORE_HOLE_ID,WELL_ID,DEPTH_M,YEAR_COMPLETED,WELL_COMPLETED_DATE,AUDIT_NO,TAG,CONTRACTOR, BHK from VW_GMAP_LL_04")
rows = cursor.fetchall()
wellsDict = {};
try:
	with arcpy.da.InsertCursor(WellsPoints, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "DEPTH_M", "YEAR_COMPLETED", "WELL_COMPLETED_DATE", "AUDIT_NO", "TAG_NO", "CONTRACTOR", "URL_EN", "URL_FR")) as cur:
		cntr = 1
		for row in rows:
			wellsDict[row[2]] = row  # use BORE_HOLE_ID (row[2]) as unique key
			rowValue = [(row[0], row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", ""]
			cur.insertRow(rowValue)
			print "Record number " + str(cntr) + " was written to feature class " + WellsPoints
			cntr = cntr + 1
			#if cntr > 1000:
			#	break
except Exception as e:
	print e.message

def toSting(item):
	if not item:
		return " "
	itemStr = str(item)
	while "\r\n" in itemStr:
		itemStr = itemStr.replace("\r\n", "")		
	return itemStr

WellsReports = "WellsReport"
WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReports
if not arcpy.Exists(WellsReportsLayer):
	# Process: Create Feature Class
	arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReports, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# Process: Define Projection
	arcpy.DefineProjection_management(WellsReportsLayer, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	# Process: Add Fields	
	arcpy.AddField_management(WellsReportsLayer, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
	fields = ["WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]
	for field in fields:
		arcpy.AddField_management(WellsReportsLayer, field, "TEXT", "", "", "5000", "", "NULLABLE", "NON_REQUIRED", "")
else:
	arcpy.DeleteRows_management(WellsReportsLayer)	

cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2, MOE_COUNTY_DESCR, MOE_MUNICIPALITY_DESCR, CON, LOT, STREET, CITY, UTMZONE, EAST83, NORTH83, GEO, PLUG, HOLE, CM, CAS, SCRN, WAT, PT, PTD, DISINFECTED from VW_GMAP_HTML_04")
rows = cursor.fetchall()
try:
	with arcpy.da.InsertCursor(WellsReports, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")) as cur:
		cntr = 1
		for row in rows:			
			bRow = wellsDict[row[0]]  # use BORE_HOLE_ID (row[0]) as unique key
			row = map(toSting, row)
			#rowValue = [(0, 0), row[0], row[1], " ", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			rowValue = [(bRow[0], bRow[1]), row[0], row[1], bRow[10], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			cur.insertRow(rowValue)
			print "Record number " + str(cntr) + " was written to feature class " + WellsReports
			cntr = cntr + 1
			#if cntr > 1000:
			#	break
except Exception as e:
	print e.message
