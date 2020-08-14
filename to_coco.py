import json
import os
import argparse
import datetime
import sys
from typing import List

# image_type = 'body'  # body / face
license_num = 0  # number of licenses
human_keypoint17_names = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder", "right_shoulder",
                        "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee",
                        "right_knee", "left_ankle", "right_ankle"]
human_keypoint17_skeletons = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8],
                              [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]
human_keypoint12_names = ["left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist",
                          "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"]
human_keypoint12_skeletons = [[11, 9], [9, 7], [12, 10], [10, 8], [7, 8], [1, 7], [2, 8], [1, 2], [1, 3],
                              [2, 4], [3, 5], [4, 6]]
face_keypoint5_names = ['left_eye', 'right_eye', 'nose', 'mouth_left', 'mouth_right']
face_keypoint5_skeletons = [[1, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 5]]


def to_json(file_name, target_name):
    info = None
    licenses = None
    images: List[dict] = []
    annotations = []
    categories = []
    with open(file_name, 'r') as file:
        # info
        image_id = 0
        annotation_id = 0
        category_id = 0
        category_dict = {'body_17': 0, 'body_12': 0, 'face_5': 0}
        line = str(file.readline())
        anno = None
        while line:
            if line.startswith('# '):
                img = {"id": 0, "width": 0, "height": 0, "file_name": '', "license": None, "flickr_url": '',
                       "coco_url": '', "date_captured": None}
                image_id += 1
                line = line.replace('# ', '').split(' ')
                img['id'] = image_id
                img['file_name'] = line[0]
                img['width'] = round(float(line[1]), 0)
                img['height'] = round(float(line[2]), 0)
                images.append(img)
            elif line.startswith('body') or line.startswith('face'):
                cate = {'supercategory': 'person', 'id': 0, 'name': 'person',
                        'keypoints': [], 'skeleton': []}
                anno = {"keypoints": [], "num_keypoints": 0, "id": 0, "image_id": 0, "category_id": 0,
                        "segmentation": None, "area": 0.0, "bbox": [],
                        "iscrowd": 0}  # bbox = [x, y, width, height], iscrowd = 0 or 1
                # segmentation: rle if iscrowd == 1 or [polygon] if iscrowd == 0
                line = line.split(' ')
                category_str = '{}_{}'.format(line[0], line[1])
                anno["image_id"] = image_id
                annotation_id += 1
                anno["id"] = annotation_id
                anno["bbox"] = [float(line[i]) for i in range(2, 6)]
                if int(line[6]) > 1:
                    anno["iscrowd"] = 1
                else:
                    anno["iscrowd"] = 0
                if category_dict[category_str] == 0:
                    category_id += 1
                    category_dict[category_str] += category_id
                    cate['id'] = category_id
                    anno["category_id"] = category_id
                    if int(line[1]) == 17:
                        cate['keypoints'] = human_keypoint17_names
                        cate['skeleton'] = human_keypoint17_skeletons
                    elif int(line[1]) == 12:
                        cate['keypoints'] = human_keypoint12_names
                        cate['skeleton'] = human_keypoint12_skeletons
                    elif int(line[2]) == 5:
                        cate['keypoints'] = face_keypoint5_names
                        cate['skeleton'] = face_keypoint5_skeletons
                    categories.append(cate)
                else:
                    anno["category_id"] = category_dict[category_str]
            elif line.startswith('seg'):
                if anno["iscrowd"] == 0:  # polygon
                    line = line.split(' ')
                    anno["segmentation"] = [[]]
                    for i in range(1, len(line)):
                        if str(line[i]) == 'area':
                            anno['area'] = float(line[i+1])
                            break
                        anno["segmentation"][0].append(int(line[i]))
                else:  # RLE
                    line = line.split(' ')
                    anno["segmentation"] = {u'counts': [], u'size': [anno["bbox"][2], anno["bbox"][3]]}
                    anno['area'] = 0.0
                    for i in range(1, len(line)):
                        anno["segmentation"][u'counts'].append(int(line[i]))
                        if i % 2 == 0:
                            anno['area'] += int(line[i])
            else:
                line = line.split(' ')
                anno["keypoints"] = [float(line[i]) for i in range(len(line))]
                anno["num_keypoints"] = 0
                for i in range(len(line)):
                    if i % 3 == 0 and float(line[i]) > 0.5:
                        anno["num_keypoints"] += 1
                annotations.append(anno)
            line = str(file.readline())
    coco: dict = {'info': info, 'licenses': licenses, 'images': images, 'annotations': annotations,
                  'categories': categories}
    print(coco)
    with open(target_name, 'w') as target_file:
        target_file.write(json.dumps(coco, indent=4, separators=(',', ': ')))


def main(args):
    file_name = args.txt_name
    target_name = args.json_name
    # global image_type
    # image_type = args.image_type
    to_json(file_name, target_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_name', type=str, required=True, help='text file name')
    parser.add_argument('--json_name', type=str, required=True, help='json file name')
    # parser.add_argument('--image_type', type=str, default='body',
    #                     help='\"body\" for human body images, \"face\" for human face images')
    args = parser.parse_args()
    main(args)
