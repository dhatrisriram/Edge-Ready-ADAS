# Edge Ready ADAS: Real-Time Object Detection with Model Switching

This project implements a **real-time object detection system** for **Advanced Driver Assistance Systems (ADAS)** that dynamically switches between lightweight and heavyweight YOLO models based on system resource availability (CPU and RAM usage).

## 🚗 Project Objective

To optimize object detection performance on **edge devices** (like Jetson Nano, Raspberry Pi) by:
- Using a **lightweight model (YOLOv11S)** when resources are low
- Switching to a **heavyweight model (YOLOv7X)** when resources are available
- Monitoring system stats (CPU/RAM) in real-time using `psutil`

## 🧠 Key Features

- ✅ **Dynamic model switching logic** using `psutil`
- ✅ **Real-time object detection** (cars, pedestrians, traffic objects)
- ✅ **YOLOv7X and YOLOv11S models trained on BDD100K**
- ✅ **Resource monitoring dashboard**
- ✅ Optimized for edge deployment using TensorRT and ONNX Runtime (WIP)

## 📚 Project Requirements

To reproduce or test this project, make sure to have the following:

### 🔸 Dataset

- **[BDD100K](https://bdd-data.berkeley.edu/):**  
  A diverse driving dataset used for training the YOLO models.

  📥 Download Link: [https://bdd-data.berkeley.edu](https://bdd-data.berkeley.edu)

### 🔸 YOLO Model Repositories

We used official implementations of two YOLO models:

- 🔹 **YOLOv7 (for heavy model)**  
  GitHub: [https://github.com/WongKinYiu/yolov7](https://github.com/WongKinYiu/yolov7)  
  Used for accurate but resource-heavy inference.

- 🔹 **YOLOv11S (for lightweight model)**  
  GitHub: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)  
  Used when system resources (CPU/RAM) are constrained.

> Note: Ensure you clone the YOLOv7 repository and install the ultralytics package using pip install ultralytics before running inference.

### 🚀 How to Run

To start the adaptive ADAS system, run the master controller script.  
This script will automatically monitor your system resources and switch between the **Heavy (YOLOv7)** and **Light (YOLO11)** models.

```bash
python pesutil.py
```

## 🛠️ What Happens During Execution
### 🔍 Hardware Monitoring
The script uses psutil to check your real-time CPU and RAM usage.

### 🤖 Dynamic Selection
If resources are Low (High CPU/RAM), it triggers YOLO11S via yolov11/predict_11s.py.

If resources are Sufficient, it triggers YOLOv7X via yolov7/detect.py.

### 📁 Output
Results are saved in the runs/ directory.

Outputs are categorized based on the model used.

## 🎥 Results

For 11s:

![11s](runs/yolov11_output/210801775.jpg)

For 7x:

![7x](runs/yolov7_output/labels/210801775.jpg)

Overall model results:

![Sample Output](overall_model_result.png)
Detailed results are there under results of their respective model.

>⚠️ While we acknowledge that the current results are not fully satisfactory, they were achieved under significant hardware limitations, strict deadlines, and limited time for optimization. We are actively working on improving the model’s precision and recall, which will require further tuning and experimentation in future iterations.


## 📦 Model Files

Due to GitHub's file size limitations (100MB max per file on the free tier), we could not upload our trained YOLO models (`yolov7x_best.pt` and `yolov11s_best.pt`) to this repository.

## 🛠️ Technologies Used

- Python
- YOLOv7 and YOLOv11S (Ultralytics)
- OpenCV
- psutil
- PyTorch
- TensorRT (planned)
- ONNX Runtime (planned)

## 📈 Future Work

- Integrate GPU-based switching
- Add LiDAR + camera fusion (multimodal)
- Deploy to Jetson Nano / Raspberry Pi and benchmark FPS
- Add alert system (pedestrian crossing, etc.)

## 👨‍💻 Authors

- Dhatri P Sriram
- Aritra Ghosh Dastidar
- Disha Bharadwaj


