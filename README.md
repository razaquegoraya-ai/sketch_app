# Photo to Sketch Converter

<img width="1440" alt="Screenshot 2025-03-01 at 6 48 27 PM" src="https://github.com/user-attachments/assets/a825e8b7-cdad-47bb-959c-71ff9e4ef9fa" />


A Flask web application that converts photos into artistic line sketches using computer vision techniques.

## Features

- Upload photos through a web interface
- Convert photos to clean line sketches
- Advanced edge detection and noise reduction
- Real-time sketch generation
- Clean and modern UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sketch_app.git
cd sketch_app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`
3. Click "Choose File" to select an image
4. Click "Convert to Sketch" to generate the line sketch
5. The converted sketch will appear next to the original image

## Technical Details

The sketch conversion process uses several computer vision techniques:
- Bilateral filtering for noise reduction while preserving edges
- Adaptive thresholding for detail preservation
- Canny edge detection for line extraction
- Morphological operations for line refinement

## Project Structure

```
sketch_app/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html     # Main page template
├── static/            # Static files
│   ├── css/          # Stylesheets
│   └── sketches/     # Generated sketches
└── uploads/          # Temporary storage for uploads
```

## Requirements

- Python 3.6+
- OpenCV (cv2)
- Flask
- NumPy

## License

MIT License # sketch_app
