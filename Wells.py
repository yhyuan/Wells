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
cursor.execute("select * from VW_GMAP_LL_04 where BORE_HOLE_ID = 1000055771")
text_file = open("VW_GMAP_LL_04.txt", "w")
#text_file.write("BORE_HOLE_ID\tWELL_ID\tLongitude\tLatitude\tBHK\tPREV_WELL_ID\tDPBR_M\tWELL_TYPE\tDEPTH_M\tYEAR_COMPLETED\n")
#text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY"]) + "\n")
text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "Longitude", "Latitude", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED"]) + "\n")
def toSting(item):
	if not item:
		return " "
	return str(item)
	
while True:
	row = cursor.fetchone()
	if not row:
		break
	text_file.write("\t".join(map(toSting, row[:10])) + "\n")
text_file.close()

cursor.execute("select * from VW_GMAP_HTML_04")
text_file = open("VW_GMAP_HTML_04.txt", "w")
text_file.write("\t".join(["BORE_HOLE_ID", "WELL_ID", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]) + "\n")  # , "X", "Y", "BHK", "PREV_WELL_ID", "DPBR_M", "WELL_TYPE", "DEPTH_M", "YEAR_COMPLETED"
	
while True:
	row = cursor.fetchone()
	if not row:
		break
	line = "\t".join(map(toSting, row))
	while "\r\n" in line:
		line = line.replace("\r\n", "")
	text_file.write(line + "\n")
text_file.close()
