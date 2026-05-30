# DisasterM3 Paper Summary

## Problem Statement

Disasters like earthquakes, floods, wildfires, and explosions cause massive damage every year. One of the biggest challenges in disaster response is understanding what happened, where, and how bad the damage is. Satellites can capture images of affected areas quickly, but someone still has to analyze those images. This takes time, and time is critical in disasters.

AI models that can look at images and answer questions in natural language — called Vision-Language Models or VLMs — seem like a good solution. The problem is that these models were mostly trained on everyday images. When you show them a satellite image of a collapsed building after an earthquake and ask "how many buildings were destroyed?", they often give wrong answers. The paper says this happens for a few reasons. First, there is almost no disaster-specific training data for these models. Second, satellite images taken after disasters sometimes use a different sensor called SAR, which looks very different from a regular photo. Third, counting damaged objects in aerial images is genuinely difficult, even for humans.

So the gap is clear — we have powerful AI models, but they were not built with disaster scenarios in mind, and they show it when tested.

---

## Solution

The authors built a dataset called DisasterM3 to fix this. The name comes from its three main features: multi-hazard, multi-sensor, and multi-task.

It covers 36 real disaster events — things like the Beirut explosion, the Turkey earthquake, Hurricane Harvey, and the Maui fires. These events come from 5 continents and fall into 10 disaster categories. The dataset has 26,988 satellite image pairs, each showing the same location before and after the disaster. It also has around 123,000 question-answer pairs that cover 9 different tasks.

The multi-sensor part is important. During bad weather, regular optical cameras on satellites are blocked by clouds. SAR sensors can see through clouds, so they are used for post-disaster images in some cases. DisasterM3 includes both types, which makes the benchmark harder and more realistic.

The 9 tasks go from simple to complex. Some ask the model to identify what type of disaster happened or which structures were affected. Others ask it to count damaged buildings, estimate how much of a road is flooded, or segment specific objects in the image. The hardest tasks ask the model to generate a full disaster description or write recovery advice — which is much closer to what real disaster analysts actually do.

---

## Experiments

The authors tested 14 different VLMs on this benchmark. The models included open-source ones like LLaVA, InternVL3, Kimi-VL, and Qwen2.5-VL, commercial ones like GPT-4o and GPT-4.1, and remote sensing models like GeoChat, TeoChat, and EarthDial. For segmentation tasks, they also tested LISA, PSALM, HyperSeg, and GeoPixel.

The results were not great for most models. Even the strongest ones struggled with disaster-specific tasks, especially counting and SAR-based questions. Remote sensing models did not do much better than general models, which was surprising. It showed that being trained on satellite images in general is not the same as understanding disaster damage specifically.

Then the authors fine-tuned four models — Qwen2.5-VL, InternVL3, LISA, and PSALM — using the DisasterM3 training data. After fine-tuning, the results improved a lot. QA accuracy went up by as much as 10.4% and referring segmentation improved by up to 40.8%. This made it clear that disaster-specific data actually helps, and that the main problem was not the models themselves but the lack of relevant training data.

---

## My Take

Before reading this paper, I thought disaster image analysis was mostly about classifying whether something is damaged or not. Reading it changed that view. The paper shows it is a much broader problem — comparing before and after images, counting things, identifying spatial relationships, and writing reports. That is a lot to ask from a model.

What I find interesting is that even GPT-4o, one of the strongest commercial models available, still struggled on several tasks. That says something about how hard this problem actually is. The DisasterM3 dataset seems like a useful starting point for building AI tools that can genuinely support disaster response teams.

For the internship project, this paper sets the foundation. The framework being built needs to evaluate models on tasks exactly like these, across multiple datasets and in a way that makes it easy to compare results.
