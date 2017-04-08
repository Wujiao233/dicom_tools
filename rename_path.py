import dicom
import os
import sys


def get_path_dictlist(path):
    files = os.listdir(path)
    dict_list = []
    for f in files:
        if os.path.isdir(path + '/' + f):
            dict_list.append(f)

    return dict_list


while True:
    path = input("Path:")
    dict_list = get_path_dictlist(path)

    dcm_1 = dicom.read_file(path + '/' + dict_list[0] + '/0.dcm').InstanceCreationTime
    dcm_2 = dicom.read_file(path + '/' + dict_list[1] + '/0.dcm').InstanceCreationTime

    if int(dcm_1) < int(dcm_2):
        os.rename(path + '/' + dict_list[0], path + '/scan_1')
        os.rename(path + '/' + dict_list[1], path + '/scan_2')
    else:
        os.rename(path + '/' + dict_list[1], path + '/scan_1')
        os.rename(path + '/' + dict_list[0], path + '/scan_2')
