import os
from pydub import AudioSegment
from pypinyin import pinyin, lazy_pinyin, Style
import glob

output_dir = r"C:\Users\86188\Desktop\LRC_ms3_After"

audio_files = glob.glob("C:/Users/86188/Desktop/LRC_ms3_Before/*/*.wav")


for audio_file in audio_files:
    # print(audio_files)
    sound = AudioSegment.from_wav(audio_file)
    the_file = os.path.basename(audio_file)
    (the_file_name, the_file_format) = os.path.splitext(the_file)

    audio_file_directory = os.path.dirname(audio_file)

    lrc_file_path = os.path.join(audio_file_directory, the_file_name + ".lrc")
    f = open(lrc_file_path,"r", encoding = "utf-8")
    a = f.readlines()

    l = a[0]
    t = l[2:10]
    m = t[:2]
    s = t[3:5]
    ms = t[6:]
    # print(m)
    # print(s)
    # print(ms)
    m = int(m)
    s = int(s)
    ms = int(ms)
    t = m * 60 * 1000 + s * 1000 + ms

    last = t
    # crop_audio = sound[:t]
    os.makedirs(output_dir, exist_ok=True)
    file_count = 0
    lastLRC = ""
    a = a[1:]

    for l in a:
        t = l[1:10]
        # print(t)
        LRC= l[11:]
        # print(type(LRC))
        txt_file_name = f"{lastLRC.strip()}__{file_count}.txt"


        lyrics_file = open(os.path.join(output_dir, txt_file_name), "w", encoding="utf-8")
        # pinyin_lyrics = ' '.join([''.join(item) for item in lazy_pinyin(lastLRC.strip())])
        pinyin_lyrics = ' '.join([''.join(item) for item in pinyin(lastLRC.strip(), style=Style.TONE3)])
        lyrics_file.write(pinyin_lyrics)
        # lyrics_file.write(lastLRC.strip())
        lyrics_file.close()

        lastLRC = LRC

        m = t[:2]
        s = t[3:5]
        ms = t[6:]
        m = int(m)
        s = int(s)
        ms = int(ms)

        t = m*60*1000+s*1000+ms

        # save_name = "crop_" + str(t) + file_name
        # save_name = f"crop_{str(t)}_{os.path.basename(txt_file_name.replace('__*', ''))}"
        # print(save_name)
        # save_name = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(txt_file_name))[0]}.wav")

        wav_file_name = f"{os.path.splitext(txt_file_name)[0]}.wav"
        save_path = os.path.join(output_dir, wav_file_name)
        sound[last:t].export(save_path, format="wav", tags={'album': os.path.basename(output_dir)})

        last = t
        file_count += 1





