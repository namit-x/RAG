import whisper
import os

folder = "audios"
model = whisper.load_model("large")

count = 0
os.makedirs("transcribed_text", exist_ok=True)

# Get all files with their sizes
files_with_size = [(f, os.path.getsize(os.path.join(folder, f))) for f in os.listdir(folder)]

# Sort by size descending (largest first)
files_sorted = [f for f, size in sorted(files_with_size, key=lambda x: x[1], reverse=True)]

for file in files_sorted:
    result = model.transcribe(f"audios/{file}",
                          language="hi",
                          task="translate")
    filename = file[:-4]
    with open(f"transcribed_text/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])