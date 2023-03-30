YouTube Video Downloader

This is a Python script that uses the yt_dlp library to download videos from a specified YouTube channel that were uploaded within the past 24 hours. The downloaded videos are saved to a specified directory and their metadata is saved to a file.

Requirements

    Python 3.6 or later
    yt_dlp library
    ffmpeg library
    Warning: On Windows OS, you need to add ffmpeg to system variables.
    I personally use scoop and its a great tool. you could simply run scoop install ffmpeg in cmd and it would be much quicker than doing it manually:
    
        Download FFmpeg from the official website (https://ffmpeg.org/download.html#build-windows) and extract the contents to a folder (e.g., C:\ffmpeg).
        Right-click on "This PC" (or "My Computer") and select "Properties".
        Click on "Advanced system settings" and then click on the "Environment Variables" button.
        In the "System variables" section, scroll down and find the "Path" variable and click on "Edit".
        Click on "New" and enter the path to the FFmpeg folder (e.g., C:\ffmpeg\bin) and click "OK".
        Click "OK" to close all windows and restart your command prompt.
        After following these steps, you should be able to call FFmpeg from the command prompt by simply typing "ffmpeg".
        
Usage

    Modify the download_path variable to specify the directory where downloaded videos should be saved.
    Modify the history_file variable to specify the file where download history should be saved.
    Run the script using python app.py in the command line.
    The script will check for new videos uploaded in the past 48 hours every hour and download any new videos it finds.

Note: You may need to modify the ydl_opts dictionary to specify different options for yt_dlp based on your needs.
Note2: ydl_opts = {'outtmpl':..} is steering where the output will be. I will update  the functionality to be fluid with the youtubers name and save to correct paths in the future
