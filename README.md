# dicom_tools

*关于dicom格式的CT文件的一些脚本*
将path目录下的dcm文件按照切片深度排序

    sort.py


播放path目录下的dcm文件动画（需经过sort排序）

    play.py [path]


播放path目录下的dcm文件动画（YZ方向切片，比较慢）

    end_wise.py


将dcm文件保存为图片

    save_image.py [path | file] --output [output]


将两个dcm序列目录按照成像时间排序为scan_1,scan_2

    rename_path.py


将dcm序列根据数据切割成为肿瘤所在位置的多层切片

    crop_in_3d.py [option] # 详见--help
    
包含get_segmented_lungs函数，将CT层图中肺部部分分割并返回

    cut_lung.py 
    
将CT序列层叠，切割分离，并建立3d视图（很慢）

*[参考资料](https://www.kaggle.com/arnavkj95/data-science-bowl-2017/candidate-generation-and-luna16-preprocessing "Kaggle")*

    plot_3d.py

