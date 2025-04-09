def get_plate_coordinates(box):
    if box is None:
        return 0, 0
    x1, y1, x2, y2 = box
    return (x1 + x2) / 2, (y1 + y2) / 2
