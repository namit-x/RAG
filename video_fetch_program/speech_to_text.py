import whisper
import os
from tqdm import tqdm
from time import strftime
from pydub import AudioSegment
import json

folder = "audios1"
model = whisper.load_model("large-v2")

os.makedirs("transcribed_files", exist_ok=True)

# Get all files with sizes and sort smallest first (original)
files_with_size = [(f, os.path.getsize(os.path.join(folder, f)))
                   for f in os.listdir(folder)]
files_sorted = [f for f in sorted(files_with_size, key=lambda x: x[1])]

print(f"Found {len(files_sorted)} files to transcribe.\n")

for file, size in files_sorted:
    start_time = strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{start_time}] Starting: {file}")

    try:
        audio_path = os.path.join(folder, file)
        filename = file.rsplit(".", 1)[0]

        # Load full audio
        audio = AudioSegment.from_file(audio_path)
        duration_sec = len(audio) / 1000
        print(f"lenght of the audio file is: {duration_sec}")
        chunk_length = 60 * 1000  # 4 mins per chunk
        chunks = range(0, len(audio), chunk_length)

        text_result = ""
        with tqdm(total=duration_sec, desc=f"Transcribing {file}", unit="sec") as pbar:
            for i, start_ms in enumerate(chunks):
                end_ms = min(start_ms + chunk_length, len(audio))
                chunk = audio[start_ms:end_ms]
                chunk_path = f"{filename}_chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                # Transcribe this chunk
                result = model.transcribe(
                    chunk_path, language="hi", task="translate")
                pbar.update((end_ms - start_ms) / 1000)

                chunk_folder = filename + "_chunks"
                os.makedirs(chunk_folder, exist_ok=True)
                output_path = f"transcribed_files/{chunk_folder}/{filename}_chunk_{i}.json"
                os.remove(chunk_path)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        end_time = strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{end_time}] Completed: {file}\n")

    except Exception as e:
        print(f"Error processing {file}: {e}\n")
