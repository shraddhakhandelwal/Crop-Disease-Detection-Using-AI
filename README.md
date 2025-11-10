# Crop Disease Detection Using AI

An advanced AI-powered system for early detection of crop diseases, helping farmers optimize pesticide use and reduce crop losses.

## Key Features
- Early identification of plant diseases through leaf image analysis
- Data-driven insights for optimizing pesticide application
- User-friendly interface for real-time disease detection
- Comprehensive analysis reports for informed decision making

## Impact
- Helps farmers identify diseases early to prevent crop losses
- Optimizes pesticide use through precise disease detection
- Supports sustainable farming practices through data analysis
- Makes expert plant pathology knowledge more accessible

## Technical Details

### Machine Learning Components
- Transfer Learning with MobileNetV2 architecture for efficient training
- Data augmentation techniques for robust model performance
- Real-time image processing and analysis
- Confidence scoring for reliable disease detection

### Data Analysis Features
- Statistical analysis of disease patterns
- Visualization of detection confidence levels
- Historical tracking of disease occurrence
- Automated reporting and insights generation

### Technologies Used
- Python: Core implementation language
- TensorFlow/Keras: Deep learning framework
- OpenCV: Image processing
- Flask: Web interface
- Pandas/NumPy: Data analysis
- Matplotlib/Seaborn: Data visualization

Dataset
- This project uses a folder-per-class layout. Example structure:

  data/
    train/
      Healthy/
        img1.jpg
        img2.jpg
      Early_blight/
        img3.jpg
      Late_blight/
        img4.jpg

- If you want to use the PlantVillage dataset, download and extract it, then re-arrange into the above layout (or use a symlink).

Quick setup
1. Create a Python virtual environment and activate it.
2. Install dependencies:

   pip install -r requirements.txt

Docker (quick demo)
- Build the image and run the Flask demo locally:

  docker build -t crop-detect .
  docker run -p 5000:5000 -v %cd%:/app crop-detect

Note: The Docker image installs the packages in `requirements.txt` (including TensorFlow). The image can be large. If you only want to run the lightweight unit tests in CI, see `requirements-test.txt` and `.github/workflows/ci.yml`.

Runtime-only (smaller) Docker image
- If you only want the UI/runtime container without TensorFlow, use the smaller runtime image. It installs only Flask + Pillow and is intended for serving the UI. It will attempt to load `models/model.h5` if present, but without TensorFlow inference will fail unless you also install a compatible runtime or serve predictions remotely.

Build and run the smaller runtime image:

  docker build -f Dockerfile.runtime -t crop-detect-runtime .
  docker run -p 5000:5000 -v %cd%:/app crop-detect-runtime

Alternative: use official TensorFlow base image (faster TF setup)
- If `docker build -t crop-detect .` fails during TensorFlow pip install, try the prebuilt TensorFlow base image which avoids downloading and building TF wheels during the image build. A helper Dockerfile `Dockerfile.tf` is included.

Build using the TensorFlow base image:

  docker build -f Dockerfile.tf -t crop-detect-tfbase .
  docker run -d --name crop-detect-tfbase -p 5000:5000 crop-detect-tfbase

This approach uses the official `tensorflow/tensorflow:2.10.0` image and installs the remaining Python dependencies on top. It usually reduces failures and speeds up iteration.

Docker Compose helper
- You can use docker-compose to run either the regular image or the TF-base image. The compose file defines two services:
  - `web` (builds using `Dockerfile`, bound to host port 5001 to avoid accidental conflict)
  - `web_tfbase` (builds using `Dockerfile.tf`, bound to host port 5000)

Start the TF-base service with docker-compose:

  docker-compose up -d --build web_tfbase

Or on Windows use the included helper (PowerShell):

  .\run_tfbase.ps1

Then check logs with:

  docker-compose logs -f web_tfbase

Note: `web` in compose is kept for development if you want to use the original Dockerfile; it's exposed on port 5001 to avoid port conflicts when running `web_tfbase` on 5000.

Training
- Example (from project root):

  python src/train.py --data_dir data/train --epochs 10 --batch_size 32 --img_size 224 --model_out models/model.h5

This trains a MobileNetV2-based classifier and saves a model plus a `labels.json` mapping.

Predicting a single image

  python src/predict.py --model models/model.h5 --image examples/sample_leaf.jpg

Flask demo

  python src/app.py --model models/model.h5

Then open http://127.0.0.1:5000 and upload a leaf image.

Example Images
- Download example images for testing:

  python src/download_examples.py

This downloads sample images from the PlantVillage dataset into the `examples` folder, including:
- Healthy tomato leaf
- Early blight infected leaf
- Late blight infected leaf

Evaluation & Metrics
The training script automatically logs:
- Training/validation accuracy and loss
- Confusion matrix on validation set
- Per-class precision, recall, and F1 scores

View training metrics in real-time:
1. Start TensorBoard before training:
   ```
   tensorboard --logdir logs
   ```
2. Open http://localhost:6006 in your browser
3. Run training as usual

Common Issues & Troubleshooting

Docker:
1. If TensorFlow installation fails during Docker build:
   - Use `Dockerfile.tf` with the official TensorFlow base image
   - Run with `run_tfbase.ps1` or `docker-compose up web_tfbase`

2. If the web UI shows but prediction fails:
   - Check Docker logs: `docker-compose logs web_tfbase`
   - Ensure model file exists in models/model.h5
   - Try rebuilding with `docker-compose build web_tfbase`

Training:
1. Out of memory during training:
   - Reduce batch_size (e.g., --batch_size 16)
   - Use smaller image size (e.g., --img_size 160)

2. Poor accuracy:
   - Increase training epochs
   - Add more training data or augmentation
   - Try different learning rates (--lr flag)

Notes & next steps
- This project uses transfer learning (MobileNetV2) for accuracy and speed on small datasets
- Next improvements: 
  - Enhanced data augmentation (rotation, zoom, etc.)
  - Class balancing for uneven datasets
  - Learning rate scheduling
  - TPU/GPU optimization
  - TensorFlow Lite export for mobile
  - REST API deployment

Continuous integration
- A lightweight CI workflow is included at `.github/workflows/ci.yml`. It installs the minimal packages from `requirements-test.txt` and runs the unit tests with pytest. This keeps CI fast and avoids installing TensorFlow on CI for quick checks.

License
- Use this code as a starting point for research and prototyping. Cite datasets as needed.
