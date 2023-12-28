
# VideoProcessor

![GitHub release (with filter)](https://img.shields.io/github/v/release/djstompzone/videoprocessor) [![Python package](https://github.com/DJStompZone/VideoProcessor/actions/workflows/python-package.yml/badge.svg)](https://github.com/DJStompZone/VideoProcessor/actions/workflows/python-package.yml) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/djstompzone/videoprocessor) ![GitHub License](https://img.shields.io/github/license/djstompzone/VideoProcessor) 



## Introduction
`VideoProcessor` is a Python class designed to facilitate video processing tasks using FFmpeg. This class currently provides methods for extracting video and audio information, burning subtitles into videos, and concatenating multiple videos into a single file.

## Installation
To use the `VideoProcessor` class, you need to have FFmpeg installed on your system. You can download FFmpeg from [here](https://ffmpeg.org/download.html).

## Class Methods
- `get_video_info()`: Extracts video information using ffprobe.
- `get_video_codec()`: Retrieves the video codec.
- `get_audio_codec()`: Retrieves the audio codec.
- `get_video_bitrate()`: Retrieves the bitrate of the video stream.
- `get_audio_bitrate()`: Retrieves the bitrate of the audio stream.
- `get_video_dimensions()`: Retrieves the dimensions of the video.
- `get_audio_sample_rate()`: Retrieves the sample rate of the audio.
- `get_frame_rate()`: Retrieves the frame rate of the video.
- `get_duration()`: Retrieves the duration of the video.
- `burn_subtitles(subs_path, output_path)`: Burns subtitles into the video.
- `concatenate_videos(input_videos, output_path)`: Concatenates multiple videos into a single file.

## Static Methods
- `main()`: Main method to run VideoProcessor as a command-line tool.

## Example Usage
```python
from video_processor import VideoProcessor

# Initialize the processor with a video file
processor = VideoProcessor('example_video.mp4')

# Extract video information
codec = processor.get_video_codec()
bitrate = processor.get_video_bitrate()

# Hardcode subtitles into the video
processor.burn_subtitles('subtitles.srt', 'output_with_subs.mp4')

# Concatenate videos
processor.concatenate_videos(['video1.mp4', 'video2.mp4'], 'concatenated_video.mp4')
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
If you'd like to help improve this project, feel free to submit a [pull request](https://github.com/DJStompZone/VideoProcessor/pulls). 
If you've found a problem and just want to let us know, you can also [submit a new issue](https://github.com/DJStompZone/VideoProcessor/issues/new/choose)

## Contact
Want to get in touch with the authors? Come say hi on our [Discord server](https://djstomp.net)
