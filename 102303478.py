import sys
import os
import yt_dlp
from moviepy.editor import AudioFileClip, concatenate_audioclips

def download_audio(singer, n):
    search_query = f"ytsearch{n}:{singer} songs"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song_%(id)s.%(ext)s',
        'quiet': True
    }

    downloaded_files = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=True)
        for entry in info['entries']:
            filename = ydl.prepare_filename(entry)
            downloaded_files.append(filename)

    return downloaded_files


def trim_audio(files, duration):
    clips = []
    for file in files:
        try:
            audio = AudioFileClip(file)
            if audio.duration > duration:
                audio = audio.subclip(0, duration)
            clips.append(audio)
        except:
            print("Skipping file:", file)
    return clips


def merge_audio(clips, output):
    final = concatenate_audioclips(clips)
    final.write_audiofile(output)


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 <file.py> <SingerName> <NumberOfVideos> <Duration> <OutputFile>")
        return

    singer = sys.argv[1]

    try:
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print("Invalid number or duration")
        return

    output = sys.argv[4]

    if n <= 10 or duration <= 20:
        print("Videos > 10 and Duration > 20 required")
        return

    print("Downloading audio...")
    files = download_audio(singer, n)

    print("Trimming...")
    clips = trim_audio(files, duration)

    print("Merging...")
    merge_audio(clips, output)

    print("Mashup created:", output)


if __name__ == "__main__":
    main()