from flask import Flask, render_template, request, redirect, url_for, flash
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Configure upload and output folders
UPLOAD_FOLDER = 'static/uploads/'
SKETCH_FOLDER = 'static/sketches/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SKETCH_FOLDER'] = SKETCH_FOLDER

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SKETCH_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_sketch(image_path, output_path):
    try:
        # Get the absolute path to the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Read and preprocess the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to read the image file.")

        # Resize image if too large
        max_size = 1024
        height, width = image.shape[:2]
        if max(height, width) > max_size:
            scale = max_size / float(max(height, width))
            image = cv2.resize(image, None, fx=scale, fy=scale)
            height, width = image.shape[:2]

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply strong bilateral filter for noise reduction while preserving edges
        blurred = cv2.bilateralFilter(gray, d=15, sigmaColor=45, sigmaSpace=45)

        # Apply additional bilateral filter with different parameters
        blurred = cv2.bilateralFilter(blurred, d=9, sigmaColor=25, sigmaSpace=25)

        # Edge detection with different thresholds
        edges1 = cv2.Canny(blurred, threshold1=20, threshold2=40)

        # Dilate edges to connect them
        kernel = np.ones((2,2), np.uint8)
        edges1 = cv2.dilate(edges1, kernel, iterations=1)

        # Get fine details using adaptive threshold
        adaptive = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=9,
            C=3
        )

        # Clean up adaptive result
        kernel = np.ones((2,2), np.uint8)
        adaptive = cv2.morphologyEx(adaptive, cv2.MORPH_OPEN, kernel)

        # Combine edges with adaptive result
        sketch = cv2.addWeighted(edges1, 0.7, adaptive, 0.3, 0)

        # Remove noise and connect lines
        kernel = np.ones((3,3), np.uint8)
        sketch = cv2.morphologyEx(sketch, cv2.MORPH_CLOSE, kernel)

        # Remove small dots
        kernel = np.ones((2,2), np.uint8)
        sketch = cv2.morphologyEx(sketch, cv2.MORPH_OPEN, kernel)

        # Final threshold to clean up
        _, sketch = cv2.threshold(sketch, 40, 255, cv2.THRESH_BINARY)

        # Invert to get black lines on white background
        sketch = cv2.bitwise_not(sketch)

        # Thin lines slightly
        kernel = np.ones((2,2), np.uint8)
        sketch = cv2.erode(sketch, kernel, iterations=1)

        # Final smoothing
        sketch = cv2.medianBlur(sketch, 3)

        # Save the sketch with maximum quality
        cv2.imwrite(output_path, sketch, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        return True
    except Exception as e:
        print(f"Error during sketch conversion: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded!', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Invalid file type! Allowed types: PNG, JPG, JPEG.', 'error')
            return redirect(request.url)

        # Save the uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)

        # Generate the sketch
        sketch_filename = f"sketch_{file.filename}"
        sketch_path = os.path.join(app.config['SKETCH_FOLDER'], sketch_filename)
        success = convert_to_sketch(upload_path, sketch_path)

        if success:
            # Render the result page
            return render_template('index.html',uploaded_image=upload_path,sketch_image=sketch_path)
        else:
            flash('Error processing the image. Please try again.', 'error')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)