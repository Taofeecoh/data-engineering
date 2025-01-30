import requests
import os
import shutil
from zipfile import ZipFile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]



def main():
    # make new duirectory
    path = "./downloads"
    try:
        os.mkdir(path)
        print("directory created!")
    except FileExistsError:
        """for dir in os.listdir(path):
            os.remove(os.path.join(path, dir)) # Remove all files in the directory
        os.rmdir(path) # Remove the empty directory"""
        # Excluding the above code block now because PermissionError is now solved for the code line below.

        shutil.rmtree(path)
        os.mkdir(path)
        print("directory recreated!")


     # Iterate through links
    bad_request = []  # Handle error in request
    for link in download_uris:
        file_name = link.split("/")[-1]  # Retrive filename from url

        # Send requests to website
        r = requests.get(link) 
        if r.status_code != 200:  # Set condition to investigate bad request
            bad_request.append(link)
        elif r.status_code == 200:
            # Save files in newly created folder
            with open(os.path.join(path, file_name), "wb") as wf:   # Create file name
                wf.write(r.content)   # Write binary : write zip file from contents into created file above
                with ZipFile(os.path.join(path, file_name)) as rf:  # Open zipfile and read content to be extracted
                    rf.extractall(path)
        
        # Clean directory; remove files and directory that are not csv
        for file in os.listdir(path): # List files/dir in the download directory
            file = os.path.join(path, file)
            if os.path.isfile(file) and not file.endswith(".csv"): # Check if item in folder is file and not csv, then remove
                os.remove(file)
            elif os.path.isdir(file):  #Check if it is a directory and remove
                shutil.rmtree(file)
    
    return bad_request

if __name__ == "__main__":
    main()

# print("end of request")
