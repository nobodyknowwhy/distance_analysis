import os

count_jpg = 0
count_json = 0
for root_name, dir_list, file_list in os.walk(r"D:\hqxkj\PycharmProjects\01code\data_processing\1744597038608265217\2025"):
    for file_name in file_list:
        if file_name.endswith('.jpg'):
            count_jpg += 1
        else:
            count_json += 1

print(count_jpg, count_json)