import os
import pprint
import json

transcriptions = "transcriptions"
folders = os.listdir(transcriptions)

# for folder_name in folders:
#     combined_text=""
#     folder = sorted(os.listdir(f'{transcriptions}/{folder_name}'))
#     for i in range(len(folder)):
#         with open(f"{transcriptions}/{folder_name}/{folder[i]}", 'r') as f:
#             chunk = json.load(f)
#             # pprint.pprint(chunk)
#             # for item in chunk:
#                 # print(item)
#             print(f"combining text from {folder[i]}")
#             combined_text = combined_text+chunk["text"]
#     print(combined_text)

all_files=[]
for folder_name in folders:
    folder = os.listdir(f"{transcriptions}/{folder_name}")
    # print(folder)
    for file in folder:
        if "points" in file:
            continue
        all_files.append(file)

nums = []
for i, file_name in enumerate(all_files):
    num = int(''.join(filter(str.isdigit, file_name)))
    if num>900000:
        print(file_name)
    nums.append(num)

file_nums = set(list(nums))

# pprint.pprint(file_nums)