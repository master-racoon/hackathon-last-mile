#!/bin/bash

# Train ML Model Script
# This script builds and runs the ML training service

set -e

echo "=========================================="
echo "ML Model Training"
echo "=========================================="
echo ""

# Check if data file exists
if [ ! -f "./data/south_africa_all_with_weather_clean.csv" ]; then
    echo "ERROR: Training data not found!"
    echo "Please place your CSV file at: ./data/south_africa_all_with_weather_clean.csv"
    echo ""
    echo "See ./data/README.md for more information about the required data format."
    exit 1
fi

echo "✓ Training data found"
echo ""
echo "Building ML training service..."
docker-compose build ml-training

echo ""
echo "Starting training..."
echo "=========================================="
docker-compose --profile train up ml-training

echo ""
echo "=========================================="
echo "Training completed!"
echo ""
echo "Model files saved to:"
echo "  - ./models/catboost_model.json"
echo "  - ./models/model_metadata.json"
echo "=========================================="
