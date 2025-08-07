from ultralytics import YOLO
import rasterio
import torch
import numpy as np
import os
import csv
import matplotlib.pyplot as plt


model = YOLO("/home/luarzou/Downloads/roofmaterial/yolo/runs/train4_trainings_ergebnisse_valDatensatz/weights/best.pt")

# #Train the model on the COCO8 dataset for 100 epochs
# train_results = model.train(
#     data="/home/luarzou/Downloads/roofmaterial/yolo/roofmaterial.yaml",  # Path to dataset configuration file
#     epochs=100,  # Number of training epochs
#     imgsz=500,  # Image size for training
#     device="cuda",  # Device to run on (e.g., 'cpu', 0, [0,1,2,3])
# )

# #Evaluate the model's performance on the validation set
metrics = model.val(data="/home/luarzou/Downloads/roofmaterial/yolo/roofmaterial_force_test.yaml", device="cuda", save_json=True, plots=True, save_conf=True)



# The following code performs the prediction of roofing materials on the given inference dataset, 
# converts the detection bounding boxes from the local image coordinate system into a global coordinate reference system (EPSG:25832).
# The georeferenced detections are then written as WKT format and exported into a .txt file for each image.

directory = r"./inference_dataset"

# Iterate over files in directory
for name in os.listdir(directory):
    file = directory + name
    name_wo_ex = os.path.splitext(name)[0]


    #get crs und bbox coords from airborne image
    dat = rasterio.open(file)

    # Perform object detection on an image
    results = model(file, iou=0.9, conf=0.06, device='cuda:0', save_txt=True, save=True)
    # results[0].show()  # Display results

    geo_left=dat.bounds.left
    geo_bottom=dat.bounds.bottom
    geo_right=dat.bounds.right
    geo_top=dat.bounds.top


    yolo_boxes = results[0].boxes.xyxy.tolist()
    cls = results[0].boxes.cls.tolist()

    counter = 0
    for cls_val in cls:
        yolo_boxes[counter].insert(0,cls_val)
        counter = counter + 1

    x_res = 0.2
    y_res = 0.2

    img_width = 500 
    img_height = 500

    output_file = "./results/inference_bboxes_wkt" + name_wo_ex + ".txt"
    with open(output_file, 'w') as f:
        for box in yolo_boxes:
            cls, x_min_px, y_min_px, x_max_px, y_max_px = box

            # Convert pixel to real-world coords
            x_min = geo_left + x_min_px * x_res
            x_max = geo_left + x_max_px * x_res
            y_max = geo_top - y_min_px * y_res  # top - y_px
            y_min = geo_top - y_max_px * y_res

            # Create WKT POLYGON string
            polygon_wkt = (
                f"POLYGON(({x_min:.6f} {y_min:.6f}, "
                f"{x_max:.6f} {y_min:.6f}, "
                f"{x_max:.6f} {y_max:.6f}, "
                f"{x_min:.6f} {y_max:.6f}, "
                f"{x_min:.6f} {y_min:.6f}))"
            )

            # Write to file with class
            f.write(f"{int(cls)}; {polygon_wkt}\n")

