# TİD Dataset Exploration (AUTSL & BosphorusSign22k)

Jira: SB-12

## Overview

Analysis of two public Turkish Sign Language (TİD) isolated-sign datasets: video format, resolution, frame rate, and annotation structure.

## Comparison

| Property | AUTSL | BosphorusSign22k |
|---|---|---|
| Source | Ankara University | Boğaziçi University |
| Signs (glosses) | 226 | 744 |
| Signers | 43 | 6 (native signers) |
| Videos / clips | 38,336 | 22,542 |
| Capture device | Kinect v2 | Kinect v2 |
| Modalities | RGB, depth, skeleton | RGB, depth, skeleton (+ pose estimates) |
| RGB resolution | 512x512 (clipped and resized) | 1920x1080 |
| Depth resolution | 512x512 | 512x424 |
| Frame rate | TODO (measure) | 30 fps |
| Skeleton | 25 joints, (x, y) | 25 joints, 3D |
| Video container / codec | TODO (measure) | TODO (measure) |
| Annotation format | TODO (inspect label files) | TODO (inspect label files) |
| Train/val/test split | 31 / 6 / 6 signers (signer-independent) | TODO |
| Access / license | TODO | TODO |

## AUTSL

### Video format
TODO: container, codec, file naming, folder structure (measured with `ffprobe`)

### Annotations
TODO: label file format, columns, class ID to sign name mapping

### Notes
- Recorded in indoor and outdoor environments with varied backgrounds.
- Two test sets (balanced and imbalanced).

## BosphorusSign22k

### Video format
TODO

### Annotations
TODO

### Notes
- Signs come from health, finance, and everyday-life domains.
- Higher resolution than AUTSL, fewer signers.

## Observations for SignBridge

TODO: short comparison and suitability notes (e.g. Kinect data vs. regular RGB camera input).

## Method

TODO: how the measurements were made (tools, sample files inspected).

## Sources

- Sincan & Keles, AUTSL: A Large Scale Multi-modal Turkish Sign Language Dataset and Baseline Methods, 2020. https://arxiv.org/abs/2008.00932
- BosphorusSign22k Sign Language Recognition Dataset, LREC 2020 workshop. https://arxiv.org/abs/2004.01283