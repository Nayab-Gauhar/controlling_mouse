# controlling_mouse

Control your mouse cursor using eye/iris tracking from a webcam.

## How it works

1. Detects your face and 68 facial landmarks using `dlib`.
2. Crops the left and right eye regions from the landmarks.
3. Processes each eye image (grayscale, blur, contrast, threshold) to isolate the iris.
4. Finds the iris center via contour detection.
5. Calibrates by asking you to look at the top-left, then bottom-right corner of the screen.
6. Maps your live gaze offset to screen coordinates and moves the cursor with `pyautogui`.

## Tech Stack

- Python
- dlib
- OpenCV (`opencv-python`)
- pyautogui
- numpy

## Requirements

- Python >= 3.12
- Webcam
- `shape_predictor_68_face_landmarks.dat` (included in `src/controlling_mouse/`)

## Installation

```bash
git clone https://github.com/Nayab-Gauhar/controlling_mouse.git
cd controlling_mouse
uv sync
```

## Usage

```bash
uv run src/controlling_mouse/main.py
```

- Look at the top-left corner of your screen when prompted, then the bottom-right corner.
- Cursor movement will follow your gaze after calibration.
- Press `q` to quit.
