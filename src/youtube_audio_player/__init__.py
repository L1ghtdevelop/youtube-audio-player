import argparse

from .audio_player import YouTubeAudioPlayer


def main() -> None:
    parser = argparse.ArgumentParser(description="Audio player from youtube CLI client")
    parser.add_argument("url_video", help="Url video to play")
    args = parser.parse_args()
    player = YouTubeAudioPlayer(args.url_video)
    player.play_video()
