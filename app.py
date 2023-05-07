import os
import datetime
import time
import yt_dlp
import ffmpeg
#import ffmpeg-python

# Define the path where videos will be downloaded
download_path = "C:\\PATH\\HERE" # This Path is for Windows OS. Update for your OS and path.

# Define the path to the file that stores the download history
history_file = os.path.join(download_path, "downloaded.txt")

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

    # Calculate the time 48 hours ago
    past_time = current_time - datetime.timedelta(hours=48)

    # Convert times to string format
    current_time_str = current_time.strftime("%B %d %Y")
    past_time_str = past_time.strftime("%B %d %Y")

    # Define the options for yt-dlp
    ydl_opts = {
        'ignoreerrors': True,
        'nopart': True,
        'download_archive': history_file,
        'dateafter': past_time_str,
        'datebefore': current_time_str,
        'writedescription': True,
        'writeinfojson': True,
        'writethumbnail': True,
        'playlistend': 3,
        'page': 1,
        'outtmpl': os.path.join(download_path, '%(uploader)s', '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }

    # Create a new yt-dlp object with the specified options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        # Get the metadata for the videos from the specified channel URL
        print(f"Checking for new videos uploaded in the past 48 hours...")
        metadata = ydl.extract_info('https://www.youtube.com/@CHANNELID/videos', download=True)

        # Wait for one hour before checking for new videos again
        print("Waiting for one hour before checking for new videos again...")
        time.sleep(3600)

        # Iterate over the metadata for each video
        for video in metadata['entries']:
            #ydl.process_ie_result(video, download=True)
            # Check if the video was uploaded within the last 48 hours
            if datetime.datetime.strptime(video['upload_date'], "%Y%m%d") >= past_time:
                # Check if the video has already been downloaded
                if video['id'] not in downloaded_ids:
                    # Download the video
                    video_date = datetime.datetime.strptime(video['upload_date'], "%Y%m%d").strftime("%Y-%m-%d")
                    output_filename = f"{video_date} {video['title']}.{video['ext']}"
                    output_path = os.path.join(download_path, video['uploader'], output_filename)
                    print(f"Downloading video '{video['title']}'...")
                    ydl_opts['outtmpl'] = output_path
                    ydl.process_ie_result(video, download=True)

                    # Merge the video and audio streams using ffmpeg
                    video_path = os.path.join(download_path, video['uploader'], f"{video_date} {video['title']}.mp4")
                    audio_path = os.path.join(download_path, video['uploader'], f"{video_date} {video['title']}.m4a")
                    output_path = os.path.join(download_path, video['uploader'],f"{video_date} {video['title']}.merged.mp4")

                    if not os.path.exists(os.path.dirname(output_path)):
                        os.makedirs(os.path.dirname(output_path))

                    # Open video and audio streams
                    video_stream = ffmpeg.input(video_path)
                    audio_stream = ffmpeg.input(audio_path)

                    # Merge streams and write output
                    merged_stream = ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output(output_path,codec="libx264",strict='experimental').run()

                    # Add the downloaded ID to the history file
                    downloaded_ids.add(video['id'])
                    with open(history_file, "a") as f:
                        f.write(f"{video['id']}\n")

                    # Delete the original video and audio files
                    #os.remove(video_path)
                    #os.remove(audio_path)
                    #already done after merge,
                else:
                    print(f"Video '{video['title']}' already downloaded, skipping...")
            else:
                print(f"Video '{video['title']}' was not uploaded within the last 48 hours, skipping...")

                # Print a summary of the downloaded videos
            print(f"\n{len(downloaded_ids)} videos downloaded in total.")

            if __name__ == "__main__":
                main()
