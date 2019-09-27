#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 21:44:16 2019

@author: ubuntu
"""
from dataset.voc_dataset import VOCDataset

class WIDERFaceDataset(VOCDataset):
    """wider face数据集，来自港中文大学
    训练集图片总数：12880，跟voc07+12的数据量差不多
    原始下载数据集不能直接使用，需要采用转换成voc格式的xml标注文件，参考：
    https://github.com/open-mmlab/mmdetection/tree/master/configs/wider_face
    https://github.com/sovrasov/wider-face-pascal-voc-annotations
    """
    CLASSES = ('face', )

    def __init__(self,                  
                 root_path=None,
                 ann_file=None,
                 subset_path=None,
                 img_transform=None,
                 label_transform=None,
                 bbox_transform=None,
                 aug_transform=None,
                 data_type=None):
        super().__init__(
                root_path, 
                ann_file, 
                subset_path,
                img_transform, 
                label_transform, 
                bbox_transform,
                aug_transform,
                data_type)
    
    def load_annotation_inds(self, ann_file):
        """从多个标注文件读取标注列表
        """
        img_anns = []
        for i, af in enumerate(ann_file): 
            with open(af) as f:
                img_ids = f.readlines()
            for j in range(len(img_ids)):
                img_ids[j] = img_ids[j][:-1]  # 去除最后的\n字符
            # 基于图片id打开annotation文件，获取img/xml文件名
            for img_id in img_ids:
                folder = img_id.split('_')[0] + '--' + img_id.split('_')[1]  #需要额外生成文件夹名称
                img_file = self.subset_path[i] + 'images/{}/{}.jpg'.format(folder, img_id)
                xml_file = self.subset_path[i] + 'Annotations/{}.xml'.format(img_id)
                
                img_anns.append(dict(img_id=img_id, img_file=img_file, xml_file=xml_file))
        return img_anns
    
    
if __name__ == '__main__':
    data_root_path = '/home/ubuntu/MyDatasets/WIDERFace/'
    params = dict(
                    root_path = data_root_path,
                    ann_file = [data_root_path + 'train.txt'],
                    subset_path = [data_root_path + 'WIDER_train/'],
                    data_type='train')
    
    dset = WIDERFaceDataset(**params)
    data = dset[0]
    print(len(dset))