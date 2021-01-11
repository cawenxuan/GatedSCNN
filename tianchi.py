import argparse
import json
import random
import shutil

from utils.datasets import create_folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label_file', type=str, default='data/annotations/train_annos.json', help='labels file path')
    opt = parser.parse_args()
    with open(opt.label_file, 'r') as load_f:
        train_annos = json.load(load_f)
    train_path, val_path = 'data/train', 'data/val'
    create_folder('{}/labels'.format(train_path))
    create_folder('{}/labels'.format(val_path))
    create_folder('{}/images'.format(val_path))
    train_image_names = [item['name'] for item in train_annos]
    # random select 388 images as val data
    val_image_names = random.sample(train_image_names, 388)
    for i in range(2):
        path = train_path if i == 0 else val_path
        image_names = train_image_names if i == 0 else val_image_names
        for item in train_annos:
            if item['name'] in image_names:
                file_name = '{}/labels/{}'.format(path, item['name'].replace('jpg', 'txt'))
                file = open(file_name, mode='a')
                tx, ty, bx, by = item['bbox']
                w, h = item['image_width'], item['image_height']
                cx, cy = (tx + bx) / 2, (ty + by) / 2
                bw, bh = bx - tx, by - ty
                file.write('{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(item['category'], cx / w, cy / h, bw / w, bh / h))
                file.close()
                if len(image_names) == 388:
                    shutil.copy('{}/images/{}'.format(train_path, item['name']),
                                '{}/images/{}'.format(val_path, item['name']))
