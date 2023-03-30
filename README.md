YouTube Video Downloader

This is a Python script that uses the yt_dlp library to download videos from a specified YouTube channel that were uploaded within the past 24 hours. The downloaded videos are saved to a specified directory and their metadata is saved to a file.

Requirements

    Python 3.6 or later
    yt_dlp library

Usage

    Install the yt_dlp library by running pip install yt_dlp in the command line.
    Modify the download_path variable to specify the directory where downloaded videos should be saved.
    Modify the history_file variable to specify the file where download history should be saved.
    Run the script using python app.py in the command line.
    The script will check for new videos uploaded in the past 48 hours every hour and download any new videos it finds.

Note: You may need to modify the ydl_opts dictionary to specify different options for yt_dlp based on your needs.

