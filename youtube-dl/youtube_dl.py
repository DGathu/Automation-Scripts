import yt_dlp
import time
from tqdm import tqdm

def get_video_info(ydl, url):
    """
    Fetches and displays basic information about the YouTube video.
    :param ydl: YoutubeDL object
    :param url: URL of the YouTube video
    """
    with ydl:
        result = ydl.extract_info(url, download=False)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
    
    print(f"Title: {video['title']}")
    print(f"Length: {video['duration']} seconds")
    print(f"Views: {video['view_count']}")
    print(f"Author: {video['uploader']}")

def select_quality(ydl, url):
    """
    Prompts the user to select the desired quality for the video download.
    :param ydl: YoutubeDL object
    :param url: URL of the YouTube video
    :return: Quality string
    """
    with ydl:
        result = ydl.extract_info(url, download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
    
    formats = video['formats']
    print("\nAvailable qualities:")
    for i, format in enumerate(formats):
        if 'height' in format and 'fps' in format:
            print(f"{i + 1}. {format['height']}p - {format['fps']}fps - {format['ext']}")
        elif 'acodec' in format and 'vcodec' in format:
            print(f"{i + 1}. {format['acodec']} - {format['vcodec']} - {format['ext']}")
    
    while True:
        try:
            choice = int(input("Select the quality (1-{}): ".format(len(formats))))
            if 1 <= choice <= len(formats):
                return formats[choice - 1]['format_id']
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def download_video(url, quality):
    """
    Downloads the selected video stream and displays progress information.
    :param url: URL of the YouTube video
    :param quality: Quality string
    """
    ydl_opts = {
        'format': quality,
        'progress_hooks': [lambda d: progress_hook(d)],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    """
    Progress hook to display download progress.
    :param d: Download status dictionary
    """
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d['downloaded_bytes']
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)
        
        pbar.total = total_bytes
        pbar.update(downloaded_bytes - pbar.n)
        pbar.set_description(f"Downloading {d['_percent_str']} at {d['_speed_str']}")
        pbar.set_postfix(eta=f"{eta}s")

def main():
    """
    Main function to handle user interaction and download process.
    """
    print("Welcome to the YouTube Downloader!")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    while True:
        url = input("\nEnter the YouTube video link (or 'exit' to quit): ")
        if url.lower() == 'exit':
            break
        
        try:
            get_video_info(ydl, url)
            quality = select_quality(ydl, url)
            global pbar
            pbar = tqdm(total=0, unit='B', unit_scale=True, desc="Downloading")
            download_video(url, quality)
            pbar.close()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()