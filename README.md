# dicom_tools

*关于dicom格式的CT文件的一些脚本*

    sort.py


将path目录下的dcm文件按照切片深度排序

    play.py [path]


播放path目录下的dcm文件动画（需经过sort排序）

    end_wise.py


播放path目录下的dcm文件动画（YZ方向切片，比较慢）

    save_image.py [path | file] --output [output]


将dcm文件保存为图片

    rename_path.py


将两个dcm序列目录按照成像时间排序为scan_1,scan_2