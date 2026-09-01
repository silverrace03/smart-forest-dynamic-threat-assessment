# Reduced Project Specification

## Working title

**A Dataset-Driven Dynamic Threat Assessment Framework for Smart Forest
Monitoring and Ranger Emergency Response**

## Research problem

Existing forest-monitoring studies commonly classify an isolated event. They do
not consistently explain how heterogeneous, uncertain, spatially related events
should be combined into a response priority. The project therefore treats event
classification as an input and dynamic threat prioritization as the principal
research problem.

## Main contribution

An explainable Dynamic Threat Assessment Engine that combines:

- event severity;
- classifier confidence;
- virtual-zone importance;
- repetition and persistence;
- correlated events;
- time decay.

## Objectives

1. Prepare public datasets for acoustic threat, fire risk, and ranger falls.
2. Train and compare lightweight classification models for the three modules.
3. Convert unseen test samples into timestamped virtual IoT event messages.
4. Calculate a zone-level, explainable 0–100 Dynamic Threat Index.
5. Compare the proposed engine with fixed-threshold and static-score baselines.
6. Visualize current and historical threats in a software dashboard.

## Explicit exclusions

- physical IoT-node construction;
- measured LoRa range, battery lifetime, or hardware energy consumption;
- real forest deployment;
- medical diagnosis from wearable data;
- species-level wildlife recognition;
- claims of real-time field performance without field evidence.

## Minimum evaluation

- classifier precision, recall, F1-score, and confusion matrix;
- threat-category accuracy and critical-event recall;
- false critical-alert rate;
- DTI ablation study;
- raw-record versus compact-event data-size estimate;
- software inference and event-to-alert latency.

