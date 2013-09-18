# Install pyodbc from https://code.google.com/p/pyodbc/
# Pick pyodbc-3.0.6.win32-py2.5.exe since ArcGIS 9.3 only 
# support python 2.5
# Create a ODBC User DSN with Wells as the name. 
LL_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "X": 2, "Y": 3, "BHK": 4, "PREV_WELL_ID": 5, "DPBR_M": 6, "WELL_TYPE": 7, "DEPTH_M": 8, "YEAR_COMPLETED": 9, "WELL_COMPLETED_DATE": 10, "RECEIVED_DATE": 11, "AUDIT_NO": 12, "TAG": 13, "CONTRACTOR": 14, "SWL": 15, "FINAL_STATUS_DESCR": 16, "USE1": 17, "USE2": 18, "MOE_COUNTY_DESCR": 19, "MOE_MUNICIPALITY_DESCR": 20, "CON": 21, "LOT": 22, "STREET": 23, "CITY": 24}
HT_FieldsDict = {"BORE_HOLE_ID": 0, "WELL_ID": 1, "WELL_COMPLETED_DATE": 2, "RECEIVED_DATE": 3, "AUDIT_NO": 4, "TAG": 5, "CONTRACTOR": 6, "SWL": 7, "FINAL_STATUS_DESCR": 8, "USE1": 9, "USE2": 10, "MOE_COUNTY_DESCR": 11, "MOE_MUNICIPALITY_DESCR": 12, "CON": 13, "LOT": 14, "STREET": 15, "CITY": 16, "UTMZONE": 17, "EAST83": 18, "NORTH83": 19, "GEO": 20, "PLUG": 21, "HOLE": 22, "CM": 23, "CAS": 24, "SCRN": 25, "WAT": 26, "PT": 27, "PTD": 28, "DISINFECTED": 29}


import sys
reload(sys)
sys.setdefaultencoding("latin-1")

import pyodbc
cnxn = pyodbc.connect('DSN=Wells')
cursor = cnxn.cursor()
cursor.execute("select * from VW_GMAP_LL_04")
text_file = open("VW_GMAP_LL_04.txt", "w")
#text_file.write("BORE_HOLE_ID\tWELL_ID\tLongitude\tLatitude\tBHK\tPREV_WELL_ID\tDPBR_M\tWELL_TYPE\tDEPTH_M\tYEAR_COMPLETED\n")
#text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY"]) + "\n")
text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED"]) + "\n")
def toSting(item):
	if not item:
		return " "
	return str(item)
wellsDict = {};
while True:
	row = cursor.fetchone()
	if not row:
		break
	wellsDict[row[0]] = row[1:10]
	text_file.write("\t".join(map(toSting, row[:10])) + "\n")
text_file.close()

lengthLargerthan255Dict = {}  # {28: 0, 20: 0, 21: 0}
cursor.execute("select * from VW_GMAP_HTML_04")
text_file = open("VW_GMAP_HTML_04.txt", "w")
#text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]) + "\n")  # , "X", "Y", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED"
text_file.write("\t".join(["WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED", "BORE_HOLE_ID", "WELL_ID", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]) + "\n")  # , "X", "Y", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED"	
print "\t".join(["WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED", "BORE_HOLE_ID", "WELL_ID", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"])
while True:
	row = cursor.fetchone()
	if not row:
		break
	#if (not (not row[27])):
	#	items = row[27].strip().split(";");
	#	if len(items[12]) != 0:
	#		print str(row[1]) + ", " + row[27]
	rowstr = map(toSting, row)
	isLargerthan255Character = False
	for i in range(len(rowstr)):
		if(len(rowstr[i]) > 255):
			isLargerthan255Character = True #print rowstr[0] + "\t" + str(i)
			if not (i in lengthLargerthan255Dict):
				lengthLargerthan255Dict[i] = 0
	line = "\t".join(rowstr)
	while "\r\n" in line:
		line = line.replace("\r\n", "")
	line = "\t".join(map(toSting, wellsDict[row[0]])) + "\t" + line
	if isLargerthan255Character:
		print rowstr[0] + "\t" + rowstr[20] + "\t" + rowstr[21] + "\t" + rowstr[28]
	text_file.write(line + "\n")
text_file.close()
#print lengthLargerthan255Dict
# Since ArcGIS can not open the text file with text field which is longer than 255 characters, the following steps are required. 
# 1. Create a table in Oracle with following SQL: CREATE TABLE wells_data ( BORE_HOLE_ID int, GEO varchar2(4000), PLUG varchar2(4000), PTD varchar2(4000));
# 2. Use SQL loader to load the advisory.txt to Oracle. sqlldr username/password@sde control=1.ctl, log=1.log, bad=1.bad
