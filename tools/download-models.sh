#!/usr/bin/env bash

urls=(
#   "https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5" \
#   "https://raw.githubusercontent.com/khinthetnwektn/ObjectsDetectionTesting1/eeaf85c9658f13de9a0d32e9e54418395023213f/models/yolo-tiny.h5" \
  "https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5"
)

rm models/*.h5*
for f in $urls;
do
    wget $f -P models
done
