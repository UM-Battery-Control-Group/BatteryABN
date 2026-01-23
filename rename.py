import os

directory = "/data"

for root, dirs, files in os.walk(directory):
    for filename in files:
        if "GM_JULY_2022" in filename:
            new_filename = filename.replace("GM_JULY_2022", "GMJuly_2022")
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_filename)
            os.rename(old_path, new_path) 
            print(f"Renamed: {old_path} -> {new_path}")
