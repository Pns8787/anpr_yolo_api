from flask import Flask, request, jsonify, send_from_directory
import os, uuid
from detector import detect_plate_yolo
from ocr import extract_text
from utils import get_plate_coordinates

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to YOLO ANPR API"})

@app.route('/readnumberplate', methods=['POST'])
def read_plate():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image uploaded"}), 400

    file = request.files['image']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    try:
        plate_img, box = detect_plate_yolo(path)
        if plate_img is None:
            return jsonify({"status": "fail", "message": "Plate not detected"}), 200

        text = extract_text(plate_img)
        cx, cy = get_plate_coordinates(box)

        return jsonify({
            "status": "success",
            "data": {
                "message": "ANPR successful",
                "number_plate": text,
                "plate_Xcenter": int(cx),
                "plate_Ycenter": int(cy),
                "state": "Unknown",
                "view_image": f"/static/{filename}"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/static/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
