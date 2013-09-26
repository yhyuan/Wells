# Required packages: arcpy from ArcGIS 10.1 and pyodbc from https://code.google.com/p/pyodbc/
# Input data: An Access database contains two tables: VW_GMAP_LL_04 and VW_GMAP_HTML_04. 
#		Fields in VW_GMAP_LL_04 LL_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "X": 2, "Y": 3, "BHK": 4, "PREV_WELL_ID": 5, "DPBR_M": 6, "WELL_TYPE": 7, "DEPTH_M": 8, "YEAR_COMPLETED": 9, "WELL_COMPLETED_DATE": 10, "RECEIVED_DATE": 11, "AUDIT_NO": 12, "TAG": 13, "CONTRACTOR": 14, "SWL": 15, "FINAL_STATUS_DESCR": 16, "USE1": 17, "USE2": 18, "MOE_COUNTY_DESCR": 19, "MOE_MUNICIPALITY_DESCR": 20, "CON": 21, "LOT": 22, "STREET": 23, "CITY": 24}
#		Fields in VW_GMAP_HTML_04 HT_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "WELL_COMPLETED_DATE": 2, "RECEIVED_DATE": 3, "AUDIT_NO": 4, "TAG": 5, "CONTRACTOR": 6, "SWL": 7, "FINAL_STATUS_DESCR": 8, "USE1": 9, "USE2": 10, "MOE_COUNTY_DESCR": 11, "MOE_MUNICIPALITY_DESCR": 12, "CON": 13, "LOT": 14, "STREET": 15, "CITY": 16, "UTMZONE": 17, "EAST83": 18, "NORTH83": 19, "GEO": 20, "PLUG": 21, "HOLE": 22, "CM": 23, "CAS": 24, "SCRN": 25, "WAT": 26, "PT": 27, "PTD": 28, "DISINFECTED": 29}
# Steps: 1) Use C:\Windows\SysWOW64\odbcad32.exe (The default one in control panel might not work) to create a ODBC User DSN using Wells as the name.
# Output data: 
#		A zip file contains a file geodatabases named Wells, Wells.mxs, Wells.msd, readme.txt

import sys, string, os
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import pyodbc


# Local variables...
#PATH = "C:\\Users\\yuanje\\Downloads"
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
#else:
#	arcpy.DeleteRows_management(Wells)
	


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

cursor.execute("select BORE_HOLE_ID, WELL_ID, WELL_COMPLETED_DATE, RECEIVED_DATE, AUDIT_NO, TAG, CONTRACTOR, SWL, FINAL_STATUS_DESCR, USE1, USE2, MOE_COUNTY_DESCR, MOE_MUNICIPALITY_DESCR, CON, LOT, STREET, CITY, UTMZONE, EAST83, NORTH83, GEO, PLUG, HOLE, CM, CAS, SCRN, WAT, PT, PTD, DISINFECTED from VW_GMAP_HTML_04")
rows = cursor.fetchall()

f = open ("rows_contaion_enter.txt","w")
f.write(str(len(rows)) + "\n")
for row in rows:
	line = "\t".join(map(toSting, row))
	if ("\r\n" in line):
		f.write(line)	
f.close()


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

cntr = 0
try:
	#with arcpy.da.InsertCursor(WellsReports, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")) as cur:
	with arcpy.da.InsertCursor(WellsReports, ("SHAPE@XY", "BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2")) as cur:
		for row in rows:
			bRow = wellsDict[row[0]]  # use BORE_HOLE_ID (row[0]) as unique key
			row = map(toSting, row)			
			#rowValue = [(0, 0), row[0], row[1], " ", row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			#rowValue = [(bRow[0], bRow[1]), row[0], row[1], bRow[10], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			#print rowValue
			rowValue = [(bRow[0], bRow[1]), row[0], row[1], bRow[10], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == len(rows)):
	print "WellsReport0 is created successfully!"
else:
	print "WellsReport0 is NOT created successfully!"


WellsReport1 = "WellsReport1"
#WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReport1
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReport1, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
arcpy.DefineProjection_management(arcpy.env.workspace + "\\"  + WellsReport1, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport1, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
fields = ["MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83"]
for field in fields:
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport1, field, "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
cntr = 0
try:
	with arcpy.da.InsertCursor(WellsReport1, ("SHAPE@XY", "BORE_HOLE_ID", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83")) as cur:
		for row in rows:
			row = map(toSting, row)			
			rowValue = [(0, 0), row[0], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == len(rows)):
	print "WellsReport1 is created successfully!"
else:
	print "WellsReport1 is NOT created successfully!"
	
WellsReport2 = "WellsReport2"
#WellsReportsLayer = arcpy.env.workspace + "\\"  + WellsReport2
arcpy.CreateFeatureclass_management(arcpy.env.workspace, WellsReport2, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
arcpy.DefineProjection_management(arcpy.env.workspace + "\\"  + WellsReport2, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "BORE_HOLE_ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")

arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "GEO", "TEXT", "", "", "3000", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "PLUG", "TEXT", "", "", "1000", "", "NULLABLE", "NON_REQUIRED", "")
fields = ["HOLE", "CM", "CAS", "SCRN", "WAT", "PT"]
for field in fields:
	arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, field, "TEXT", "", "", "300", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "PTD", "TEXT", "", "", "500", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(arcpy.env.workspace + "\\"  + WellsReport2, "DISINFECTED", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
cntr = 0
try:
	with arcpy.da.InsertCursor(WellsReport2, ("SHAPE@XY", "BORE_HOLE_ID", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED")) as cur:
		for row in rows:
			row = map(toSting, row)			
			rowValue = [(0, 0), row[0], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29]]
			cur.insertRow(rowValue)
			cntr = cntr + 1
except Exception as e:
	print e.message

if (cntr == len(rows)):
	print "WellsReport2 is created successfully!"
else:
	print "WellsReport2 is NOT created successfully!"

arcpy.MakeFeatureLayer_management (arcpy.env.workspace + "\\WellsReport0",  "WellsReportJoin")
arcpy.AddJoin_management("WellsReportJoin", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport1", "BORE_HOLE_ID")
arcpy.AddJoin_management("WellsReportJoin", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport2", "BORE_HOLE_ID")
arcpy.CopyFeatures_management("WellsReportJoin", arcpy.env.workspace + "\\WellsReports")
print "WellsReports is created successfully!"

#arcpy.JoinField_management(arcpy.env.workspace + "\\WellsReport0", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport1", "BORE_HOLE_ID", "")
#arcpy.FeatureClassToFeatureClass_conversion(arcpy.env.workspace + "\\WellsReport0", arcpy.env.workspace, "WellsReport3", "", "BORE_HOLE_ID \"BORE_HOLE_ID\" true false true 4 Long 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,BORE_HOLE_ID,-1,-1," + arcpy.env.workspace + "\\WellsReport0,BORE_HOLE_ID,-1,-1;WELL_ID \"WELL_ID\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,WELL_ID,-1,-1;BHK \"BHK\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,BHK,-1,-1;WELL_COMPLETED_DATE \"WELL_COMPLETED_DATE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,WELL_COMPLETED_DATE,-1,-1;RECEIVED_DATE \"RECEIVED_DATE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,RECEIVED_DATE,-1,-1;AUDIT_NO \"AUDIT_NO\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,AUDIT_NO,-1,-1;TAG \"TAG\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,TAG,-1,-1;CONTRACTOR \"CONTRACTOR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,CONTRACTOR,-1,-1;SWL \"SWL\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,SWL,-1,-1;FINAL_STATUS_DESCR \"FINAL_STATUS_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,FINAL_STATUS_DESCR,-1,-1;USE1 \"USE1\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,USE1,-1,-1;USE2 \"USE2\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,USE2,-1,-1;MOE_COUNTY_DESCR \"MOE_COUNTY_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,MOE_COUNTY_DESCR,-1,-1;MOE_MUNICIPALITY_DESCR \"MOE_MUNICIPALITY_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,MOE_MUNICIPALITY_DESCR,-1,-1;CON \"CON\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,CON,-1,-1;LOT \"LOT\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,LOT,-1,-1;STREET \"STREET\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,STREET,-1,-1;CITY \"CITY\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,CITY,-1,-1;UTMZONE \"UTMZONE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,UTMZONE,-1,-1;EAST83 \"EAST83\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,EAST83,-1,-1;NORTH83 \"NORTH83\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport0,NORTH83,-1,-1", "")
#arcpy.JoinField_management(arcpy.env.workspace + "\\WellsReport3", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport2", "BORE_HOLE_ID", "")
#arcpy.FeatureClassToFeatureClass_conversion(arcpy.env.workspace + "\\WellsReport3", arcpy.env.workspace, "WellsReports", "", "BORE_HOLE_ID \"BORE_HOLE_ID\" true false false 4 Long 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,BORE_HOLE_ID,-1,-1," + arcpy.env.workspace + "\\WellsReport3,BORE_HOLE_ID,-1,-1;WELL_ID \"WELL_ID\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,WELL_ID,-1,-1;BHK \"BHK\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,BHK,-1,-1;WELL_COMPLETED_DATE \"WELL_COMPLETED_DATE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,WELL_COMPLETED_DATE,-1,-1;RECEIVED_DATE \"RECEIVED_DATE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,RECEIVED_DATE,-1,-1;AUDIT_NO \"AUDIT_NO\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,AUDIT_NO,-1,-1;TAG \"TAG\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,TAG,-1,-1;CONTRACTOR \"CONTRACTOR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,CONTRACTOR,-1,-1;SWL \"SWL\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,SWL,-1,-1;FINAL_STATUS_DESCR \"FINAL_STATUS_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,FINAL_STATUS_DESCR,-1,-1;USE1 \"USE1\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,USE1,-1,-1;USE2 \"USE2\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,USE2,-1,-1;MOE_COUNTY_DESCR \"MOE_COUNTY_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,MOE_COUNTY_DESCR,-1,-1;MOE_MUNICIPALITY_DESCR \"MOE_MUNICIPALITY_DESCR\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,MOE_MUNICIPALITY_DESCR,-1,-1;CON \"CON\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,CON,-1,-1;LOT \"LOT\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,LOT,-1,-1;STREET \"STREET\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,STREET,-1,-1;CITY \"CITY\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,CITY,-1,-1;UTMZONE \"UTMZONE\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,UTMZONE,-1,-1;EAST83 \"EAST83\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,EAST83,-1,-1;NORTH83 \"NORTH83\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,NORTH83,-1,-1;GEO \"GEO\" true true false 3000 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,GEO,-1,-1;PLUG \"PLUG\" true true false 1000 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,PLUG,-1,-1;HOLE \"HOLE\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,HOLE,-1,-1;CM \"CM\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,CM,-1,-1;CAS \"CAS\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,CAS,-1,-1;SCRN \"SCRN\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,SCRN,-1,-1;WAT \"WAT\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,WAT,-1,-1;PT \"PT\" true true false 300 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,PT,-1,-1;PTD \"PTD\" true true false 500 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,PTD,-1,-1;DISINFECTED \"DISINFECTED\" true true false 255 Text 0 0 ,First,#," + arcpy.env.workspace + "\\WellsReport3,DISINFECTED,-1,-1", "")

# Remove useless layers
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport0" , "FeatureClass")
print "WellsReport0 is removed successfully!"
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport1" , "FeatureClass")
print "WellsReport1 is removed successfully!"
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport2" , "FeatureClass")
print "WellsReport2 is removed successfully!"
#arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport3" , "FeatureClass")

# Prepare the msd, mxd, and readme.txt
os.system("copy " + INPUT_PATH + "\\Wells.msd " + OUTPUT_PATH)
os.system("copy " + INPUT_PATH + "\\Wells.mxd " + OUTPUT_PATH)
f = open (INPUT_PATH + "\\readme_Wells.txt","r")
data = f.read()
f.close()
import time
dateString = time.strftime("%Y/%m/%d", time.localtime())
data = data.replace("[DATE]", dateString)
f = open (OUTPUT_PATH + "\\readme_Wells.txt","w")
f.write(data)
f.close()

# Compress the files together into a zip file
#from zipfile_infolist import print_info
import zipfile, os
target_dir = OUTPUT_PATH + '\\Wells.gdb'
zip = zipfile.ZipFile(OUTPUT_PATH + '\\Wells.zip', 'w', zipfile.ZIP_DEFLATED)
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
   for file in files:
      fn = os.path.join(base, file)
      zip.write(fn, "Wells.gdb\\" + fn[rootlen:])
zip.write(OUTPUT_PATH + '\\Wells.msd', "Wells.msd")
zip.write(OUTPUT_PATH + '\\Wells.mxd', "Wells.mxd")
zip.write(OUTPUT_PATH + '\\readme_Wells.txt', "readme_Wells.txt")
zip.close()

os.system("del " + OUTPUT_PATH + "\\Wells.msd")
os.system("del " + OUTPUT_PATH + "\\Wells.mxd")
os.system("del " + OUTPUT_PATH + "\\readme_Wells.txt")
os.system("rmdir " + OUTPUT_PATH + "\\Wells.gdb /s /q")
