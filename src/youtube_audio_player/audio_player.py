import datetime as dt
import logging
import subprocess
import shutil
import time
from pathlib import Path
from typing import Any, cast

import pygame
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
        pygame.mixer.init()

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
            duration = str(dt.timedelta(seconds=duration))
            info = {
                "title": video_info.get("title"),
                "duration": duration,
            }
            logger.info(info)
            return info

    def get_stream_info(self) -> str:
            ydl_opts: dict[str, Any] = {
               "quiet": True,
                "no_warnings": True,
                "cookiesfrombrowser": ("firefox",),
                "remote_components": "ejs:github",
                # Мы явно просим только аудио, чтобы получить ссылку на аудиопоток
                "format": "bestaudio/best",
            }
            with yt_dlp.YoutubeDL(cast("Any", ydl_opts)) as dlp:
                info = dlp.extract_info(self.url, download=False)
                player_url = info.get("url") or " "
                logger.info(player_url)
                return player_url
