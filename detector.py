import cv2
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.augmentations import letterbox

model = DetectMultiBackend('plate.pt', device='cpu')
stride, names, pt = model.stride, model.names, model.pt

def detect_plate_yolo(image_path):
    img0 = cv2.imread(image_path)
    img = letterbox(img0, new_shape=640, stride=stride)[0]
    img = img.transpose((2, 0, 1))[::-1]  # BGR to RGB
    img = torch.from_numpy(img).float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    with torch.no_grad():
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)[0]

    if pred is None or len(pred) == 0:
        return None, None

    box = pred[0][:4].cpu().numpy()
    x1, y1, x2, y2 = map(int, box)
    plate = img0[y1:y2, x1:x2]
    return plate, (x1, y1, x2, y2)
