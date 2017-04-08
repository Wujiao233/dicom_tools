import dicom
import os
import sys


def get_path_filelist(path,filter=None):
    files = os.listdir(path)
    file_list = []
    for f in files:
        if (os.path.isfile(path + '/' + f)):
            if filter is None:
            # 添加文件
                file_list.append(f)
            else:
                if filter in f:
                    file_list.append(f)

    return file_list

while True:
    path = input('Path:')
    filter_name = '.dcm'

    if os.path.isdir(path):
        file_list = get_path_filelist(path,filter_name)
        # print(file_list)
        deep_and_filename = {}
        for f in file_list:
            dicom_tmp = dicom.read_file(path + '/' + f)
            deep_and_filename.setdefault(float(dicom_tmp.SliceLocation),f);

        deep_list = list(deep_and_filename.keys())
        deep_list.sort(reverse=True)

        counter = 0
        for deep in deep_list:
            old_name = deep_and_filename[deep]
            os.renames(path + '/' + old_name, path + '/' + str(counter) + '.dcm')
            counter += 1

        print(deep_list)
