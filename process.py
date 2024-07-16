import jsonlines
from glob import glob
import json
import os
from pathlib import Path
import numpy as np
import librosa
import textgrid

tg = textgrid.TextGrid()

input_format = {
    "text": "",
    "ph_seq": "",
    "note_seq": "",
    "note_dur_seq": "",
    "is_slur_seq": "",
    "input_type": "phoneme"
}

def generate_json(json_filepath):
    with jsonlines.open(json_filepath, mode="w") as f:   # change the filepath or add loop to fit your file structure
        data = input_format
        data["text"] = f"{generate_lyrics(textgrid_filepath)}"
        data["ph_seq"] = f"{generate_phones(textgrid_filepath)}"
        data["note_seq"] = f"{generate_note(textgrid_filepath, wav_filepath)}"
        data["note_dur_seq"] = f"{generate_duration(textgrid_filepath, wav_filepath)}"
        # data["is_slur_seq"] = f""
        f.write(data)

def generate_lyrics(textgrid_filepath): #Textgrid_filepath
    tg.read(textgrid_filepath)
    words_tier = tg.getFirst('words')
    text_list = []
    for interval in words_tier.intervals:
        word = interval.mark
        text_list.append(word)
    result = ' '.join(text_list)
    return result

def generate_phones(textgrid_filepath): #Textgrid_filepath
    tg.read(textgrid_filepath)
    print(tg.tiers)
    phones_tier = tg.getFirst('phones')
    print(phones_tier)
    phones_list = []
    for interval in phones_tier.intervals:
        phone = interval.mark
        phones_list.append(phone)
    result = ' '.join(phones_list)
    return result

def get_word_info(textgrid_filepath, wav_filepath):
    tg.read(textgrid_filepath)
    audio_data, sample_rate = librosa.load(wav_filepath, sr=44100)
    f0, voiced_flag, voiced_idx = librosa.pyin(audio_data, fmin=100, fmax=1000, sr=sample_rate)
    word_durations = {}
    word_median_note = {}
    words_tier = tg.getFirst('phones')
    for interval in words_tier.intervals:
        word = interval.mark
        start_time = interval.minTime
        end_time = interval.maxTime
        duration = end_time - start_time

        word_f0 = f0[int(start_time * sample_rate // 512):int(end_time * sample_rate // 512)]
        median_f0 = np.nanmedian(word_f0)
        if len(word_f0) > 0:
            median_f0 = np.nanmedian(word_f0)
            median_note = librosa.hz_to_note(median_f0) if not np.isnan(median_f0) else "rest"
        else:
            median_f0 = float('nan')
            median_note = "rest"

        word_durations[word] = duration
        word_median_note[word] = median_note

    return {
        'word_durations': word_durations,
        'word_median_note': word_median_note
    }

def generate_note(textgrid_filepath, wav_filepath):
    word_info = get_word_info(textgrid_filepath, wav_filepath)
    word_median_note = word_info['word_median_note']

    note_list = list(word_median_note.values())
    result = ' '.join(note_list)
    return result

def generate_duration(textgrid_filepath, wav_filepath):
    word_info = get_word_info(textgrid_filepath, wav_filepath)
    word_durations = word_info['word_durations']

    duration_list = [f"{duration:.6f}" for duration in word_durations.values()]
    result = ' '.join(duration_list)
    return result

if __name__ == "__main__":
    textgrid_filepath = r"C:\Users\86188\Documents\MFA\align_output\被无声的时间__28.TextGrid" # change the filepath to yours
    wav_filepath = r"C:\Users\86188\Desktop\LRC_ms3_After\被无声的时间__28.wav"    # change the filepath to yours
    generate_json(json_filepath=r"C:\Users\86188\PycharmProjects\Generate_Cut\test.json")    # change the filepath to yours
