'''arcpy.MakeFeatureLayer_management (arcpy.env.workspace + "\\WellsReport0",  "WellsReportJoin")
print "Start adding joins!"
arcpy.AddJoin_management("WellsReportJoin", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport1", "BORE_HOLE_ID")
arcpy.AddJoin_management("WellsReportJoin", "BORE_HOLE_ID", arcpy.env.workspace + "\\WellsReport2", "BORE_HOLE_ID")
print "Start creating WellsReports!"
arcpy.CopyFeatures_management("WellsReportJoin", arcpy.env.workspace + "\\WellsReports")
print "WellsReports is created successfully!"
#arcpy.RemoveJoin_management("WellsReportJoin", "WellsReport1")
#arcpy.RemoveJoin_management("WellsReportJoin", "WellsReport2")

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

arcpy.DeleteField_management(arcpy.env.workspace + "\\WellsReports", "WellsReport1_OBJECTID;WellsReport1_BORE_HOLE_ID;WellsReport2_OBJECTID;WellsReport2_BORE_HOLE_ID")

layer = "Reports"
arcpy.MakeFeatureLayer_management(arcpy.env.workspace + "\\WellsReports", layer)
desc = arcpy.Describe(layer)
fieldInfo = desc.fieldInfo
fieldNameList = ["BORE_HOLE_ID", "WELL_ID", "BHK", "WELL_COMPLETED_DATE", "RECEIVED_DATE", "AUDIT_NO", "TAG", "CONTRACTOR", "SWL", "FINAL_STATUS_DESCR", "USE1", "USE2", "MOE_COUNTY_DESCR", "MOE_MUNICIPALITY_DESCR", "CON", "LOT", "STREET", "CITY", "UTMZONE", "EAST83", "NORTH83", "GEO", "PLUG", "HOLE", "CM", "CAS", "SCRN", "WAT", "PT", "PTD", "DISINFECTED"]
for index in range(2, fieldInfo.count):
	fieldInfo.setNewName(index, fieldNameList[index - 2])
	#print fieldInfo.getFieldName(index)
#time.sleep(60)
'''

import arcpy, time, os, zipfile
WellsPoints = "Wells"
OUTPUT_PATH = "output"
INPUT_PATH = "input"
arcpy.env.workspace = OUTPUT_PATH + "\\Wells.gdb"
start_time = time.time()

arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport0" , "FeatureClass")
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport1" , "FeatureClass")
arcpy.Delete_management( arcpy.env.workspace + "\\WellsReport2" , "FeatureClass")
arcpy.DeleteField_management(arcpy.env.workspace + "\\WellsReports", "OBJECTID_1;BORE_HOLE_ID_1;OBJECTID_12;BORE_HOLE_ID_12")

print "Change the projection Web Mercator"
arcpy.Project_management(arcpy.env.workspace + "\\WellsReports", arcpy.env.workspace + "\\WellsMore", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Project_management(arcpy.env.workspace + "\\" + WellsPoints, arcpy.env.workspace + "\\WellsBasic", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(arcpy.env.workspace + "\\WellsReports", "FeatureClass")
arcpy.Delete_management(arcpy.env.workspace + "\\" + WellsPoints, "FeatureClass")

# Process: Add Attribute Index
arcpy.AddIndex_management(arcpy.env.workspace + "\\WellsBasic", "BORE_HOLE_ID", "BORE_HOLE_ID_idx", "UNIQUE", "NON_ASCENDING")

# Process: Add Attribute Index (2)
arcpy.AddIndex_management(arcpy.env.workspace + "\\WellsBasic", "WELL_ID", "WELL_ID", "NON_UNIQUE", "NON_ASCENDING")

# Process: Add Attribute Index (3)
arcpy.AddIndex_management(arcpy.env.workspace + "\\WellsMore", "BORE_HOLE_ID", "BORE_HOLE_ID_IDX", "UNIQUE", "NON_ASCENDING")

# Process: Add Attribute Index (4)
arcpy.AddIndex_management(arcpy.env.workspace + "\\WellsMore", "WELL_ID", "WELL_ID_IDX", "NON_UNIQUE", "NON_ASCENDING")

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