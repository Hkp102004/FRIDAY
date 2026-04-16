import shutil

source = r"C:\Users\Harsh\Downloads\cubas64_12.dll"
destination = r"C:\Users\Harsh\AppData\Local\Programs\Python\Python312\cubas64_12.dll"

shutil.copy(source, destination)

print("DLL copied successfully!")