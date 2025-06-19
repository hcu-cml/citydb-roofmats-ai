import os
import cv2
import json
import numpy as np
from PIL import Image

# Define color to category_id mapping (example RGB values)
COLOR_TO_CATEGORY = {
    (127, 203, 86): 0,  # concrete
    (93, 187, 238): 1,      # metal
    (17, 224, 120): 2,    # glass
    (236, 113, 228): 3,      # roof_tiles
    (209, 190, 116): 4         # tar_paper
}

CATEGORIES = [
    {"id": 0, "name": "concrete"},
    {"id": 1, "name": "metal"},
    {"id": 2, "name": "glass"},
    {"id": 3, "name": "roof_tiles"},
    {"id": 4, "name": "tar_paper"}
]

def create_coco_annotations(image_dir, mask_dir, output_json):
    images = []
    annotations = []
    annotation_id = 1

    for image_name in os.listdir(image_dir):
        # print(image_name)
        # if not image_name.endswith(".jpg"):
        #     continue

        output_removed = image_name.split('_')[1]
        # print(output_removed)
        image_id = int(output_removed.split('.')[0])
        # print(image_id)

        image_path = os.path.join(image_dir, image_name)
        mask_path = os.path.join(mask_dir, image_name)

        image = cv2.imread(image_path)
        height, width, _ = image.shape

        images.append({
            "id": image_id,
            "file_name": image_name,
            "height": height,
            "width": width
        })

        # Load RGB mask
        mask = np.array(Image.open(mask_path).convert('RGB'))

        # Get unique RGB colors
        # unique_colors = np.unique(mask.reshape(-1, mask.shape[2]), axis=0)
        # print("Unique RGB values in mask:", unique_colors)

        unique_colors = np.unique(mask.reshape(-1, 3), axis=0)
        for color in unique_colors:
            color_tuple = tuple(color)
            if color_tuple not in COLOR_TO_CATEGORY:
                continue  # skip unknown colors

            category_id = COLOR_TO_CATEGORY[color_tuple]
            binary_mask = np.all(mask == color, axis=-1).astype(np.uint8)

            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 10:
                    continue  # skip tiny regions

                x, y, w, h = cv2.boundingRect(contour)
                segmentation = contour.flatten().tolist()

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "bbox": [x, y, w, h],
                    "area": w * h,
                    "segmentation": [segmentation],
                    "iscrowd": 0
                }
                annotations.append(annotation)
                annotation_id += 1

    coco_format_json = {
        "images": images,
        "annotations": annotations,
        "categories": CATEGORIES
    }

    with open(output_json, "w") as f:
        json.dump(coco_format_json, f, indent=4)

#Run the program for train, test, val
create_coco_annotations('./dataset/train/images/', 
                        './dataset/train/gt/', 
                        './train.json')

create_coco_annotations('./dataset/test/images/', 
                        './dataset/test/gt/', 
                        './test.json')

create_coco_annotations('./dataset/val/images/', 
                        './dataset/val/gt/', 
                        './val.json')

