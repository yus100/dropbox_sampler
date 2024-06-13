import dropbox
import random
import csv
import io

# Access token
ACCESS_TOKEN = '1' #Get your own access token in Dropbox App Console

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Function to list all MP4 files in a folder recursively
def list_mp4_files(root_folder):
    mp4_files = []
    try:
        # List all files and folders recursively
        print(f"Accessing root folder: {root_folder}")
        response = dbx.files_list_folder(root_folder, recursive=True)
        while True:
            for entry in response.entries:
                if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.mp4'):
                    mp4_files.append(entry.path_lower)
            if not response.has_more:
                break
            response = dbx.files_list_folder_continue(response.cursor)
    except dropbox.exceptions.ApiError as err:
        print(f"Failed to list files: {err}")
    return mp4_files

def create_folder(path):
    dbx.files_create_folder_v2(path)
    print(f"Folder '{path}' created successfully")

def copy_file(from_path, to_path):
    dbx.files_copy_v2(from_path, to_path)

# Function to upload the CSV file to Dropbox
def upload_csv(file_names, csv_path):
    with io.StringIO() as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Video Name'])
        for name in file_names:
            writer.writerow([name])
        csvfile.seek(0)
        dbx.files_upload(csvfile.getvalue().encode('utf-8'), csv_path)
    print(f"CSV file created at '{csv_path}' in Dropbox")

# Main function to sample and copy 200 MP4 files and create a CSV
def sample_and_copy_videos(folder, sample_size, new_folder):
    
    mp4_files = list_mp4_files(folder)
    if len(mp4_files) < sample_size:
        print(f"Not enough MP4 files in the folder. Found {len(mp4_files)} files.")
        return
    
    sampled_files = random.sample(mp4_files, sample_size)
    
    # Create the new folder
    create_folder(new_folder)
    
    file_names = []
    for file_path in sampled_files:
        file_name = file_path.split('/')[-1]
        file_names.append(file_name)
        new_path = f"{new_folder}/{file_name}"
        copy_file(file_path, new_path)
    
    # Create the CSV file path within the new folder
    csv_path = f"{new_folder}/sampled_videos.csv"
    
    # Upload the CSV file to Dropbox
    upload_csv(file_names, csv_path)

# Example usage
if __name__ == "__main__":
    # Specify the folder in Dropbox
    dropbox_folder = '/TED video split'
    # Specify the new folder to copy the videos to and create the CSV file in
    new_dropbox_folder = '' # Change to your output folder
    sample_size = 200
    # Sample and copy 200 videos and create a CSV
    sample_and_copy_videos(dropbox_folder, sample_size, new_dropbox_folder)
