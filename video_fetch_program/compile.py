import pprint
from pydub import AudioSegment
import os
import json

total_chunks = 4

total_text=''
total_segments=[]
id=0
os.makedirs("compiled_files", exist_ok=True)
for i in range(total_chunks):
    with open(f"65_JavaScript Exercise 11 - Calculate the Factorial_chunk_{i}.json", "r") as f:
        dict = json.load(f)

        total_text += dict["text"]
        for segment in dict["segments"]:
            total_segments.append({
                "id": id,
                "seek": segment["seek"],
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })
            id+=1
with open("compiled_files/65_Exercise11.json", 'w') as f:
    data = {
        "text": total_text,
        "segments": total_segments,
    }
    json.dump(data, f, ensure_ascii=False, indent=4)
