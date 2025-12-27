import sys
from ultralytics import YOLO
from pathlib import Path

def main():
    # Use arguments if provided by pesutil.py, otherwise use defaults
    weights = sys.argv[1] if len(sys.argv) > 1 else "yolo11s.pt"
    source = sys.argv[2] if len(sys.argv) > 2 else "210801775.jpg"
    
    # Load model
    model = YOLO(weights)
    
    # Run inference
    # Note: project and name are set so they don't conflict with YOLOv7
    results = model.predict(
        source=source, 
        save=True, 
        project="runs", 
        name="yolov11_output",
        exist_ok=True
    )
    
    print(f"YOLOv11 inference complete on {source}")

if __name__ == "__main__":
    main()