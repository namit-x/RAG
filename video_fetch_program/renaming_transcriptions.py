import pprint
import os

folder = 'transcriptions_testing'

transcription_folders = os.listdir(folder)

for folder_name in transcription_folders:
    files = os.listdir(f"{folder}/{folder_name}")
    for i, file in enumerate(files):
        chunk_no = file.rsplit("chunk_")[1][:-5]
        file_base_name = file.rsplit('_chunk_')[0]

        new_file = chunk_no + "_" + file_base_name + ".json"

        os.rename(f"{folder}/{folder_name}/{file}",
                  f"{folder}/{folder_name}/{new_file}")
