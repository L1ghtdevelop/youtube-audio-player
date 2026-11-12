import datetime as dt
import logging
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, cast

import yt_dlp

logger = logging.getLogger(__name__)

def clear_log_file() -> None:
    with Path.open(Path("player.log"), "w") as file:
        file.write("")

class YouTubeAudioPlayer:
    def __init__(self, url: str) -> None:
        logging.basicConfig(filename="player.log", level=logging.INFO)

        self.url = url

        clear_log_file()

    def get_video_info(self) -> dict:
        ydl_opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "cookiesfrombrowser": ("firefox",),
            "remote_components": "ejs:github",
        }
        with yt_dlp.YoutubeDL(cast("Any", ydl_opts)) as dlp:
            video_info = dlp.extract_info(self.url, download=False)
            duration = video_info.get("duration") or 1
            duration_secs = video_info.get("duration") or 1
            duration = str(dt.timedelta(seconds=duration))
            info = {
                "title": video_info.get("title"),
                "duration": duration,
                "duration_seconds": duration_secs,
            }
            logger.info(info)
            return info

    def get_stream_url(self) -> str:
            ydl_opts: dict[str, Any] = {
               "quiet": True,
                "no_warnings": True,
                "cookiesfrombrowser": ("firefox",),
                "remote_components": "ejs:github",
                "format": "bestaudio/best",
            }
            with yt_dlp.YoutubeDL(cast("Any", ydl_opts)) as dlp:
                info = dlp.extract_info(self.url, download=False)
                player_url = info.get("url") or " "
                logger.info(player_url)
                return player_url

    def play_video(self) -> None:
        mpv_path : str = shutil.which("mpv") or "mpv"
        stream_url = self.get_stream_url()
        info = self.get_video_info()
        len_short_title = 25
        title = str(info["title"])
        format_title = title[:22] + "..." if len(title) > len_short_title else title
        total_seconds = info["duration_seconds"]
        start_time = time.time()

        with subprocess.Popen( # noqa: S603
            [mpv_path, "--no-video", stream_url],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        ) as process:
            print("\033[2J\033[H", end="")
            print(f"> {format_title}", flush=True)
            while process.poll() is None:
                elapsed = int(time.time() - start_time)
                elapsed = min(elapsed, total_seconds)
                print(f"\033[2;1H\033[K{elapsed}/{total_seconds}", end="", flush=True)
                time.sleep(1)
