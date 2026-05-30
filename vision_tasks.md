# Vision Tasks in Computer Vision

## Overview

Computer vision is a field of artificial intelligence that allows computers to interpret and understand visual information such as images, videos, aerial images, and satellite imagery. Three basic computer vision tasks are commonly used to analyze images: **classification**, **detection**, and **segmentation**. Each task answers a different question about the image.

In the context of natural disasters, these tasks can help analyze satellite or drone images after floods, earthquakes, wildfires, storms, and landslides.

---

## 1. Image Classification

**Question it answers:** What is in this image?

Image classification assigns one label to the whole image. The model looks at the entire image and predicts the category that best describes it.

**General example:**  
A model looks at an image and classifies it as "dog", "cat", "car", or "building".

**Disaster-related examples:**

- Classifying a satellite image as "flooded" or "not flooded"
- Classifying a post-earthquake image as "no damage", "minor damage", "major damage", or "destroyed"
- Classifying the type of disaster as "wildfire", "flood", "earthquake", or "storm"

**Limitation:**  
Classification tells us the overall category of the image, but it does not show where the affected area or object is located.

---

## 2. Object Detection

**Question it answers:** What objects are in this image, and where are they?

Object detection identifies specific objects in an image and shows their locations using bounding boxes — rectangles drawn around each detected object.

**General example:**  
A model looks at a street image and detects cars, people, and traffic signs by drawing boxes around them.

**Disaster-related examples:**

- Detecting damaged buildings after an earthquake
- Detecting flooded roads or vehicles after a hurricane
- Detecting collapsed bridges or blocked roads
- Detecting rescue boats or emergency vehicles in disaster zones

**Limitation:**  
Bounding boxes give the approximate location of objects but may not describe the exact shape of irregular areas, such as flood regions or wildfire burn scars.

---

## 3. Image Segmentation

**Question it answers:** What is in this image, where is it, and what is its exact shape?

Image segmentation divides an image into meaningful regions by assigning a label to each pixel. It provides more detailed spatial information than classification or detection.

There are two common types:

- **Semantic segmentation:** labels all pixels by category, such as water, building, road, or vegetation.
- **Instance segmentation:** separates individual objects of the same category, such as building 1, building 2, and building 3.

**General example:**  
In a street scene, a model labels road pixels, sky pixels, car pixels, and person pixels separately.

**Disaster-related examples:**

- Marking the exact flooded area in a satellite image
- Mapping burned land after a wildfire
- Segmenting damaged buildings from undamaged buildings
- Identifying landslide regions from surrounding terrain

**Limitation:**  
Segmentation provides detailed information but is usually more complex and requires more detailed annotation and processing.

---

## Comparison Summary

| Task | Main Question | Output | Disaster Example |
|---|---|---|---|
| Classification | What is the overall image category? | One label for the whole image | Classify an image as flood or no flood |
| Object Detection | What objects are present and where? | Bounding boxes with labels | Detect damaged buildings after an earthquake |
| Segmentation | What exact areas belong to each class? | Pixel-level regions or masks | Mark the exact flooded area in a satellite image |

---

## Relevance to Disaster Analysis

In disaster-related remote sensing, classification, detection, and segmentation are useful for different levels of analysis. Classification can quickly identify the overall disaster type or damage level. Detection can locate affected objects such as damaged buildings, flooded roads, or blocked infrastructure. Segmentation can provide detailed spatial information by marking the exact affected regions, such as flooded areas, burned land, or damaged zones.

These tasks support disaster response by helping decision-makers understand what happened, where the damage is located, and how large the affected area is — enabling faster and more accurate emergency response using satellite, aerial, or drone imagery.

---

## Conclusion

Classification, detection, and segmentation are three core computer vision tasks. Classification provides an overall image-level label, detection identifies and locates objects, and segmentation gives detailed pixel-level information. In disaster analysis, these tasks can support faster damage assessment, affected-area mapping, and emergency response using satellite, aerial, or drone imagery.
