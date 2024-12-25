import os
import re

def get_files_with_extensions(directory, extensions):
    return [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in extensions)]

def delete_subtitle_files(directory):
    extensions = ['.cht.ass', '.tc.ass']
    subtitle_files = get_files_with_extensions(directory, extensions)
    for subtitle_file in subtitle_files:
        os.remove(os.path.join(directory, subtitle_file))
        print(f'Deleted: {subtitle_file}')

def extract_number_after_string(filename, given_string):
    pattern = re.escape(given_string) + r'(\d{2})'
    match = re.search(pattern, filename)
    return int(match.group(1)) if match else None

def rename_subtitle_files(directory, video_string, subtitle_string, offset=0):
    video_files = get_files_with_extensions(directory, ['.mkv'])
    subtitle_files = get_files_with_extensions(directory, ['.ass', '.srt'])

    video_files = [f for f in video_files if extract_number_after_string(f, video_string) is not None]
    subtitle_files = [f for f in subtitle_files if extract_number_after_string(f, subtitle_string) is not None]

    video_files.sort(key=lambda f: extract_number_after_string(f, video_string))
    subtitle_files.sort(key=lambda f: extract_number_after_string(f, subtitle_string))

    for subtitle_file in subtitle_files:
        subtitle_number = extract_number_after_string(subtitle_file, subtitle_string)
        print(f'Subtitle file: {subtitle_file}, extracted number: {subtitle_number}')
        if subtitle_number is None:
            continue

        matched = False
        for video_file in video_files:
            video_number = extract_number_after_string(video_file, video_string)
            if video_number is not None:
                video_number += offset
            print(f'Video file: {video_file}, extracted number: {video_number}')
            if video_number == subtitle_number:
                new_subtitle_name = os.path.splitext(video_file)[0] + os.path.splitext(subtitle_file)[1]
                os.rename(os.path.join(directory, subtitle_file), os.path.join(directory, new_subtitle_name))
                print(f'Renamed: {subtitle_file} to {new_subtitle_name}')
                matched = True
                break

        if not matched:
            print(f'No match found for: {subtitle_file}')

if __name__ == '__main__':
    directory = 'F:\\MP4\\_已看\\进击的巨人\\第三季'
    video_string = '[Moozzi2] Shingeki no Kyojin S3 - '
    subtitle_string = '[Snow-Raws] 進撃の巨人 Season 3 第'
    offset = 0  # 偏移量

    delete_subtitle_files(directory) #删除cht或tc结尾繁体字幕
    rename_subtitle_files(directory, video_string, subtitle_string, offset)