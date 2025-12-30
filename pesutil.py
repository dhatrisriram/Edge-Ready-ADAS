import sys
import psutil
import subprocess
import time
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────
MODEL_HEAVY   = Path("weights/yolov7x.pt")
MODEL_LIGHT   = Path("weights/yolo11s.pt")

PREDICT_SCRIPT = Path("yolov11/predict_11s.py")
DETECT_SCRIPT   = Path("yolov7/detect.py")

IMAGE_SOURCE    = Path("210801775.jpg")
OUTPUT_DIR      = Path("runs")

# Thresholds
CPU_THRESHOLD   = 40
RAM_THRESHOLD   = 60

# Hysteresis Settings 
STABILITY_REQUIRED = 5  # Seconds: Time resources must stay in a state before switching
CHECK_INTERVAL     = 1  # Seconds: How often to poll system resources

# ── ADAPTIVE CONTROLLER ───────────────────────────────────────────────────

class AdaptiveADASController:
    def __init__(self):
        self.current_mode = None
        self.stability_counter = 0
        self.target_mode = None
        self.active_process = None

    def get_system_load(self):
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        return cpu, ram

    def determine_required_mode(self):
        cpu, ram = self.get_system_load()
        if cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD:
            return "yolov11"
        return "yolov7"

    def execute_inference(self, mode):
        """Starts the inference process and cleans up the previous one."""
        # Prevent redundant switching
        if self.current_mode == mode:
            return

        print(f"\n[SYSTEM] Resource state stable. Switching to: {mode.upper()}")
        
        # Kill the previous process to free up RAM/CPU immediately
        if self.active_process and self.active_process.poll() is None:
            print(f"[INFO] Terminating previous {self.current_mode} process...")
            self.active_process.terminate()
            self.active_process.wait()

        # Build command based on project-specific CLI arguments
        if mode == "yolov11":
            script, model = PREDICT_SCRIPT, MODEL_LIGHT
            cmd = [sys.executable, str(script), str(model), str(IMAGE_SOURCE)]
        else:
            script, model = DETECT_SCRIPT, MODEL_HEAVY
            cmd = [
                sys.executable, str(script),
                "--weights", str(model),
                "--source", str(IMAGE_SOURCE),
                "--project", str(OUTPUT_DIR),
                "--name", "yolov7_output",
                "--exist-ok"
            ]

        # Use Popen instead of run() to allow the controller to remain active
        self.active_process = subprocess.Popen(cmd)
        self.current_mode = mode

    def monitor_and_run(self):
        print("--- Edge-Ready ADAS: Adaptive Monitoring Active ---")
        try:
            while True:
                new_target = self.determine_required_mode()

                # HYSTERESIS LOGIC:
                # If the system detects a need to change, start a countdown.
                # This prevents 'jitter' from momentary CPU spikes.
                if new_target != self.current_mode:
                    if new_target == self.target_mode:
                        self.stability_counter += 1
                    else:
                        self.target_mode = new_target
                        self.stability_counter = 1
                else:
                    # Resources are back to matching the current running model
                    self.stability_counter = 0

                # Switch only after meeting the stability threshold
                if self.stability_counter >= STABILITY_REQUIRED:
                    self.execute_inference(self.target_mode)
                    self.stability_counter = 0

                # UI Feedback
                cpu, ram = self.get_system_load()
                print(f"[MONITOR] CPU: {cpu}% | RAM: {ram}% | Stability: {self.stability_counter}/{STABILITY_REQUIRED}s", end='\r')
                
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n[INFO] Manual Stop. Cleaning up processes...")
            if self.active_process:
                self.active_process.terminate()

if __name__ == "__main__":
    controller = AdaptiveADASController()
    controller.monitor_and_run()
