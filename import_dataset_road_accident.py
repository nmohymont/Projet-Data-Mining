import kagglehub
import os
import shutil

# 1. Get the absolute path of the directory where this script is saved
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Define the target directory "CSV" in the same folder
target_dir = os.path.join(current_dir, "DATA/RAW")

# 3. Download the dataset to the default Kaggle cache
# We do NOT pass 'path=' here to avoid the URL error
cache_path = kagglehub.dataset_download("xavierberge/road-accident-dataset")

# 4. Create the CSV folder if it doesn't exist
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 5. Move/Copy files from the cache to your local CSV folder
# This bypasses the library's path bug entirely
for filename in os.listdir(cache_path):
    source_file = os.path.join(cache_path, filename)
    destination_file = os.path.join(target_dir, filename)
    
    # We copy the file to your folder
    if os.path.isfile(source_file):
        shutil.copy(source_file, destination_file)
        print(f"Successfully copied: {filename}")

print("-" * 30)
print(f"All files are now located in: {target_dir}")