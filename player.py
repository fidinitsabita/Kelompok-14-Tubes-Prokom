import json
import sys
sys.path.append(r'D:\azzah\MusicCafeApp7\song_recommendations.json')
import vlc
import yt_dlp
import logging
import time
from utils import load_recommendations
from antrian import save_queue, update_queue_display

# Player-related functions
sys.path.append(r'D:\azzah\AppData\Roaming\Python\Python313\site-packages')
logging.basicConfig(filename="music_cafe_errors.log", level=logging.ERROR)
instance = vlc.Instance()
media_player = instance.media_player_new()

def get_youtube_stream_url(youtube_url):
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict['url']
    except Exception as e:
        error_message = f"Failed to fetch stream URL: {e}"
        logging.error(error_message)
        print(error_message)
        return None

def player_thread_function(queue, queue_listbox):
    while True:
        if not media_player.is_playing() and queue:
            next_song = queue.pop(0)
            save_queue(queue)
            try:
                stream_url = get_youtube_stream_url(next_song['song']['url'])
                if not stream_url:
                    raise ValueError("Stream URL is None")
                media = instance.media_new(stream_url)
                media_player.set_media(media)
                media_player.play()
                print(f"Playing: {next_song['song']['title']}")
            except Exception as e:
                error_message = f"Error playing song: {e}"
                logging.error(error_message)
                print(error_message)
            update_queue_display(queue_listbox, queue)
        time.sleep(1)