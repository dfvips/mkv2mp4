import subprocess
import re
import os
from colorama import Fore, Style

def extract_metadata(file_path):
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 获取所有字幕和音轨流信息（包含流的顺序、语言和标题）
    streams = re.findall(r'Stream #(\d+):(\d+)\((\w+)\): (Audio|Subtitle):.*\n\s+Metadata:\n\s+title\s+:\s+([^\n]+)', result.stderr)
    
    # 提取音轨和字幕流的顺序、语言和标题
    metadata = {
        'audio': [],
        'subtitle': []
    }
    for stream_index, track_index, lang, track_type, title in streams:
        if track_type.lower() == 'audio':
            metadata['audio'].append({
                'stream_index': stream_index,
                'track_index': track_index,
                'language': lang,
                'title': title
            })
        elif track_type.lower() == 'subtitle':
            metadata['subtitle'].append({
                'stream_index': stream_index,
                'track_index': track_index,
                'language': lang,
                'title': title
            })
    
    return metadata

def extract_video_codec(file_path):
    """Extract the video codec type (e.g., HEVC, H.264) from the video file."""
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    # 查找视频流编码信息
    match = re.search(r'Video: (.*?),', result.stderr)
    if match:
        return match.group(1)
    return None

def generate_ffmpeg_commands(directory, bat_file_path):
    ffmpeg_command = ''
    for file_name in os.listdir(directory):
        if file_name.endswith('.mkv'):
            file_path = os.path.join(directory, file_name)
            
            # 提取视频编码格式
            video_codec = extract_video_codec(file_path)
            
            # 判断是否是 HEVC 编码
            video_codec_flag = ''
            if video_codec and 'hevc' in video_codec.lower():
                video_codec_flag = ' -tag:v hvc1'
            
            # 提取音轨和字幕流的 metadata
            metadata = extract_metadata(file_path)
            
            # 生成 ffmpeg 命令
            ffmpeg_command += f'ffmpeg -i "{file_path}" -map 0 -map_chapters -1 -c:v copy -c:a copy -c:s mov_text{video_codec_flag}'
            
            # 添加音轨的 metadata 配置
            for i, data in enumerate(metadata['audio']):
                track_index = data['track_index']
                lang = data['language']
                title = data['title']
                ffmpeg_command += f' -metadata:s:a:{i} title="{title}" -metadata:s:a:{i} language={lang}'
            
            # 添加字幕流的 metadata 配置
            for i, data in enumerate(metadata['subtitle']):
                track_index = data['track_index']
                lang = data['language']
                title = data['title']
                ffmpeg_command += f' -metadata:s:s:{i} title="{title}" -metadata:s:s:{i} language={lang}'
            
            # 输出命令到 .bat 文件
            output_file = file_name.replace('.mkv', '.mp4')  # 修改输出文件名的后缀
            ffmpeg_command += f' -y "{output_file}"\n'
    
    if ffmpeg_command != '':   
        ffmpeg_command = 'chcp 65001\n' + ffmpeg_command
        with open(bat_file_path, 'w', encoding='utf-8') as bat_file:
            bat_file.write(ffmpeg_command)

        # 启动新的命令窗口执行 .bat 文件并保持原窗口打开
        subprocess.run(['cmd', '/K', 'start', bat_file_path])

print('MKV2MP4 By Dreamfly')
print(Fore.LIGHTBLUE_EX + 'Version: 2024.12.27 00:20' + Style.RESET_ALL)

# 示例：将所有 .mkv 文件的 ffmpeg 命令写入 "process_videos.bat"
generate_ffmpeg_commands('.', 'mkv2mp4.bat')
