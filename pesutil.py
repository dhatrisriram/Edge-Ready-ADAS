import sys
import psutil
import subprocess
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────

MODEL_HEAVY   = Path("weights/yolov7x.pt")
MODEL_LIGHT   = Path("weights/yolo11s.pt")

PREDICT_SCRIPT = Path("yolov11/predict_11s.py")
DETECT_SCRIPT   = Path("yolov7/detect.py")

IMAGE_SOURCE    = Path("210801775.jpg")
OUTPUT_DIR      = Path("runs")

CPU_THRESHOLD   = 40
RAM_THRESHOLD   = 60

# ── FUNCTIONS ─────────────────────────────────────────────────────────────

def get_system_load():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return cpu, ram

def select_model():
    cpu, ram = get_system_load()
    print(f"[INFO] CPU: {cpu:.1f}% | RAM: {ram:.1f}%")
    if cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD:
        print("[INFO] High load = using LIGHT model (YOLOv11).")
        return "yolov11", PREDICT_SCRIPT, MODEL_LIGHT
    else:
        print("[INFO] Sufficient resources = using HEAVY model (YOLOv7).")
        return "yolov7", DETECT_SCRIPT, MODEL_HEAVY

def run_inference(script_path: Path, model_path: Path, mode: str):
    print(f"[INFO] Running {script_path.name} with {model_path.name}")

    if mode == "yolov11":
        # We pass the weights and image path as arguments to the script
        cmd = [
            sys.executable, str(script_path),
            str(model_path),  # sys.argv[1]
            str(IMAGE_SOURCE) # sys.argv[2]
        ]
    else:
        
        cmd = [
            sys.executable, str(script_path),
            "--weights", str(model_path),
            "--source", str(IMAGE_SOURCE),
            "--conf-thres", "0.25",
            "--project", str(OUTPUT_DIR),
            "--name", "yolov7_output",
            "--exist-ok"
        ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[INFO] ✅ Done. Results saved in: {OUTPUT_DIR / (mode + '_output')}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ❌ Inference failed: {e}")

def run():
    mode, script, model = select_model()
    run_inference(script, model, mode)

if __name__ == "__main__":
    run()
