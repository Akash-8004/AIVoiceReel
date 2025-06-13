import shutil
import os

folders_to_delete = ['__pycache__', '.vs', '.dist', 'dist', 'build']

for folder in folders_to_delete:
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
            print(f"Deleted: {folder}")
        except Exception as e:
            print(f"Error deleting {folder}: {e}")
    else:
        print(f"Not found: {folder}")
