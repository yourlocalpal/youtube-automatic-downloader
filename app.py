import os
import datetime
import time
import yt_dlp

# Define the path where videos will be downloaded
download_path = "G:\\plex\\Twitch" #this is a windows path. replace it for your OS and dir path

# Define the path to the file that stores the download history
history_file = f"{download_path}\\downloaded.txt"

# Create an empty set to store the IDs of downloaded videos
downloaded_ids = set()

# If the history file exists, read the IDs of downloaded videos from it
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        for line in f:
            if "ID" in line:
                downloaded_ids.add(line.split(":")[1].strip())

while True:
    # Get the current date and time
    current_time = datetime.datetime.now()

    # Calculate the time 24 hours ago
    past_time = current_time - datetime.timedelta(hours=24)

    # Convert times to string format
    current_time_str = current_time.strftime("%Y%m%d%H%M%S")
    past_time_str = past_time.strftime("%Y%m%d%H%M%S")

    # Define the output template for downloaded videos
    output_template = f"{download_path}\\%(uploader)s\\%(title)s.%(ext)s"

    # Define the options for yt-dlp
    ydl_opts = {
        'ignoreerrors': True,
        'nopart': True,
        'download_archive': history_file,
        'outtmpl': output_template,
        'dateafter': past_time_str,
        'datebefore': current_time_str,
        'writedescription': True,
        'writeinfojson': True,
        'writethumbnail': True,
        'playlistend': 5,
        'page': 1
    }

    # Create a new yt-dlp object with the specified options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get the metadata for the videos from the specified channel URL
        print(f"Checking for new videos uploaded in the past 24 hours...")
        metadata = ydl.extract_info('https://www.youtube.com/channel/UCQeRaTukNYft1_6AZPACnog/videos', download=False)

        # Iterate over the metadata for each video
        for video in metadata['entries']:
            # Check if the video was uploaded within the last 24 hours
            if datetime.datetime.strptime(video['upload_date'], "%Y%m%d") >= past_time:
                # Check if the video has already been downloaded
                if video['id'] not in downloaded_ids:
                    # Download the video
                    print(f"Downloading video '{video['title']}'...")
                    ydl.download(['https://www.youtube.com/watch?v=' + video['id']])

                    # Add the video's ID to the set of downloaded IDs
                    downloaded_ids.add(video['id'])

    # Write the set of downloaded IDs to the history file
    with open(history_file, "w") as f:
        for id in downloaded_ids:
            f.write(f"ID: {id}\n")

    # Wait for one hour before checking for new videos again
    print("Waiting for one hour before checking for new videos again...")
    time.sleep(3600)
