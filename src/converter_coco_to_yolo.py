from ultralytics.data import converter

converter.convert_coco(
    labels_dir="/home/luarzou/Downloads/roofmaterial/dataset/annotations/yolo/annotations/",
    save_dir="/home/luarzou/Downloads/roofmaterial/dataset/annotations/yolo/",
    use_segments=False,
    use_keypoints=False,
    cls91to80=False,
    lvis=False,
)