from .audio_player import YouTubeAudioPlayer


def main() -> None:
    player = YouTubeAudioPlayer("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    player.play_video()
