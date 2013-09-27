# Compress the files together into a zip file
#from zipfile_infolist import print_info
import zipfile, os
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

os.system("del " + OUTPUT_PATH + "\\Wells.msd")
os.system("del " + OUTPUT_PATH + "\\Wells.mxd")
os.system("del " + OUTPUT_PATH + "\\readme_Wells.txt")
os.system("rmdir " + OUTPUT_PATH + "\\Wells.gdb /s /q")