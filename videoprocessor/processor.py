import argparse
import json
import os
import subprocess
from datetime import datetime as dt
from typing import List

from data_types import Stream, VideoInfo


def check_float(val: str) -> bool:
    """Checks if a string is a valid float.

    Args:
        val (str): String to be checked.

    Returns:
        bool: True if the string is a valid float, False otherwise.
    """
    try:
        _ = float(val)
        return True
    except ValueError:
        return False


class VideoProcessor:
    """Class to process video files using FFmpeg.

    Attributes:
        video_path (str): Path to the video file.
        info (dict): Information about the video file extracted using ffprobe.
    """

    def __init__(self, video_path: str):
        """Initializes VideoProcessor with a specific video file.

        Args:
            video_path (str): Path to the video file to be processed.
        """
        super().__init__()
        self.video_path = video_path
        self.info: VideoInfo = self.get_video_info()

    def get_video_info(self):
        """Extracts video information using ffprobe.

        Returns:
            dict: Parsed JSON output from ffprobe containing video information.
        """
        cmd = f'ffprobe -v quiet -print_format json -show_streams "{self.video_path}"'
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

        if result.stderr:
            print("Error:", result.stderr)

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Failed to decode JSON. Output was:")
            print(result.stdout)
            return VideoInfo(streams=[])

    def get_video_codec(self):
        """Retrieves the video codec of the video file.

        Returns:
            str: The video codec name, or 'copy' if not found.
        """
        video_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        return video_stream.get("codec_name", "copy") if video_stream else "copy"

    def get_audio_codec(self):
        """Retrieves the audio codec of the video file.

        Returns:
            str: The audio codec name, or 'copy' if not found.
        """
        audio_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "audio"
            ),
            None,
        )
        return audio_stream["codec_name"] if audio_stream else "copy"

    def get_video_bitrate(self):
        """Retrieves the bitrate of the video stream.

        Returns:
            str: Bitrate of the video, or '500k' as a default value.
        """
        video_stream: Stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "video"
            )
        )
        return video_stream.get("bit_rate", "500k")

    def get_audio_bitrate(self):
        """Retrieves the bitrate of the audio stream.

        Returns:
            str: Bitrate of the audio, or None if not found.
        """
        audio_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "audio"
            ),
            None,
        )
        return audio_stream.get("bit_rate") if audio_stream else None

    def get_video_dimensions(self):
        """Retrieves the dimensions (width and height) of the video.

        Returns:
            tuple: Width and height of the video, or (None, None) if not found.
        """
        video_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        if video_stream:
            return video_stream.get("width"), video_stream.get("height")
        return None, None

    def get_audio_sample_rate(self):
        """Retrieves the sample rate of the audio stream.

        Returns:
            str: Sample rate of the audio, or None if not found.
        """
        audio_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "audio"
            ),
            None,
        )
        return audio_stream.get("sample_rate") if audio_stream else None

    def get_frame_rate(self):
        """Retrieves the frame rate of the video.

        Returns:
            float: Frame rate of the video, or None if not calculable.
        """
        video_stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        if video_stream and video_stream.get("r_frame_rate"):
            num, den = map(int, video_stream["r_frame_rate"].split("/"))
            return num / den if den != 0 else None
        return None

    def get_duration(self):
        """Retrieves the duration of the video.

        Returns:
            float: Duration of the video in seconds, or None if not found.
        """
        video_stream: Stream = next(
            (
                stream
                for stream in self.info["streams"]
                if stream["codec_type"] == "video"
            )
        )
        if not video_stream:
            return None
        if video_stream.get("duration") and check_float(str(video_stream["duration"])):
            duration = video_stream.get("duration")
            if duration:
                return float(duration)
            else:
                return None

    def burn_subtitles(self, subs_path: str, output_path: str) -> int:
        """Burns subtitles into the video.

        Args:
            subs_path (str): Path to the subtitle file.
            output_path (str): Path for the output video file with subtitles.
        """
        video_codec = self.get_video_codec()
        bitrate = self.get_video_bitrate()

        ffmpeg_cmd = f"ffmpeg -i {self.video_path} -c:v {video_codec} -b:v {bitrate} -vf subtitles={subs_path} -c:a copy {output_path}"
        result = subprocess.run(ffmpeg_cmd, shell=True)
        return result.returncode

    @staticmethod
    def concatenate_videos(input_videos: List[str], output_path: str) -> int:
        """Concatenates multiple videos into a single video file.

        Args:
            input_videos (List[str]): A list of paths to the input video files.
            output_path (str): Path for the output concatenated video file.
        """
        # with NamedTemporaryFile(mode="w+", delete=True) as temp_file:
        temp_filename = f"temp_{int(dt.timestamp(dt.now()))}.txt"
        result = None
        with open(temp_filename, "w+") as temp_file:
            for video in input_videos:
                _ = temp_file.write(f"file '{video}'\n")
            temp_file.flush()

            ffmpeg_cmd = (
                f"ffmpeg -f concat -safe 0 -i {temp_file.name} -c copy {output_path}"
            )
            result = subprocess.run(ffmpeg_cmd, shell=True)
        os.remove(temp_filename)
        return result.returncode

    @staticmethod
    def main():
        """Main method to run VideoProcessor as a command-line tool."""
        parser = argparse.ArgumentParser(
            description="Burn subtitles into a video file."
        )
        _ = parser.add_argument("video_path", help="Path to the input video file")
        _ = parser.add_argument("subs_path", help="Path to the subtitle file")
        _ = parser.add_argument("output_path", help="Path for the output video file")

        args = parser.parse_args()

        processor = VideoProcessor(args.video_path)
        _ = processor.burn_subtitles(args.subs_path, args.output_path)
        print(f"Subtitles burned successfully to {args.output_path}")


if __name__ == "__main__":
    VideoProcessor.main()
