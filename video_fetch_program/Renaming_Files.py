import os

folder = "audios"
print("renamed:\n")
for file in os.listdir(folder):
    vid_num = file.split("#")[1].split(".")[0]
    ext=file[-4:]
    new_file= file.split(" ｜ ")[0]
    new_name = vid_num+"_"+new_file+ext
    new_path = os.path.join(folder, new_name)
    old_path = os.path.join(folder, file)
    os.rename(old_path, new_path)
