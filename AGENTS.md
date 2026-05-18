# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

A Flask-based object detection model evaluation platform. Supports YOLOv5/YOLOv8 models for object detection evaluation with metrics like mAP, IoU, Precision, Recall. Features include dataset management, multi-model comparison, and visualization.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Access at http://localhost:5000
```

## Architecture

### Entry Point
- **app.py**: Application factory pattern, route registration

### Configuration
- **config.py**: Environment-specific config (development/production/testing)
- **models/model_config.yaml**: Model definitions (YOLOv5/YOLOv8 variants)

### Blueprints (Route Layer)
- **blueprints/dataset.py**: Dataset upload and management API
- **blueprints/model.py**: Model listing and loading API
- **blueprints/evaluate.py**: Evaluation and comparison API
- **blueprints/results.py**: History and results API

### Services (Business Logic)
- **services/dataset_service.py**: Dataset CRUD operations
- **services/detection_service.py**: Model inference and evaluation
- **services/metrics_service.py**: mAP, IoU, Precision, Recall calculations
- **services/comparison_service.py**: Multi-model comparison

### Models (Data Layer)
- **models/model_manager.py**: Dynamic model loading from config
- **models/yolo_detector.py**: YOLO model wrapper (Ultralytics)
- **models/base_detector.py**: Abstract detector interface
- **models/dataset.py**: Dataset model (SQLite)
- **models/eval_history.py**: Evaluation history (SQLite)

### Templates
- **templates/index.html**: Homepage
- **templates/datasets.html**: Dataset management page
- **templates/evaluation.html**: Evaluation page
- **templates/comparison.html**: Model comparison page
- **templates/results.html**: Results history page

## Supported Models

Configured in `models/model_config.yaml`:
- YOLOv5: n, s, m, l, x variants
- YOLOv8: n, s, m, l, x variants

Models are auto-downloaded on first use via Ultralytics.

## Key Configuration

- Upload path: `static/uploads/`
- Max file size: 100MB
- Supported image formats: jpg, jpeg, png, bmp, webp
- Default conf_threshold: 0.25
- Default iou_threshold: 0.45

## API Endpoints

```
GET  /api/datasets/              # List datasets
POST /api/datasets/upload        # Create dataset and upload images
GET  /api/datasets/<id>          # Get dataset info
DELETE /api/datasets/<id>        # Delete dataset
GET  /api/datasets/<id>/images   # Get image list for dataset
GET  /api/datasets/all-images    # Get all uploaded images

GET  /api/models/list            # List available models
GET  /api/models/<id>/info       # Get model info

POST /evaluate/api/run           # Run single model evaluation
POST /evaluate/api/compare       # Compare multiple models

GET  /results/api/history        # Get evaluation history
GET  /results/api/<id>           # Get result details
```

## Dataset Format

This platform is for model performance evaluation, not training. Simply upload images without annotation files:

```
static/uploads/
├── <dataset_id>/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.png
```

## Extending Models

Add new models to `models/model_config.yaml`:
```yaml
models:
  yolo11n:
    name: "YOLO11 Nano"
    type: "yolo"
    version: "v11"
    size: "n"
    weights: "yolo11n.pt"
    description: "Latest YOLO model"
    input_size: 640
    params: "2.6M"
```
