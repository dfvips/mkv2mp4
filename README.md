# mkv2mp4
前言：由于 FFmpeg 本身并不直接支持在转换封装过程中复制并保留视频文件的标题和语言设置，给需要将 mkv 封装 mp4 并保持文件元数据完整性的用户带来了不便。
为了解决这一问题，开发了这个软件，它可以遍历当前文件夹的 mkv 文件，并生成完整的命令使 FFmpeg 在封装多语言和多字幕的 MKV 文件时，保留原始文件的标题和语言设置，并将其封装为 MP4 格式。

Preface:
Since FFmpeg does not natively support copying and preserving the title and language settings of video files during the remuxing process, it has posed an inconvenience for users who need to remux MKV files into MP4 while maintaining the integrity of file metadata.
To address this issue, this software has been developed. It scans the current folder for MKV files and generates complete commands that enable FFmpeg to preserve the original title and language settings when remuxing multilingual and multi-subtitle MKV files into MP4 format.

使用说明：使用前，请将 ffmpeg 设置环境变量，或者将 ffmpeg 放在 软件以及需要封装的 mkv 所在目录，然后双击软件即可轻松将多语言多字幕的 mkv 保留标题和语言设置封装为 mp4。

Instructions: Before using, please set the ffmpeg environment variable or place ffmpeg in the same directory as the software and the MKV file you need to process. Then, simply double-click the software to easily remux the MKV file with multiple languages and subtitles, keeping the title and language settings, into an MP4 format.
