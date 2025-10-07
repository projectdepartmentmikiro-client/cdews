C-DEWS: Community Dengue Early Warning System

C-DEWS (Community Dengue Early Warning System) is a next-generation dengue vector surveillance platform developed by the Business Intelligence Research and Development Center (BIRD-C), Isabela State University. It combines IoT, computer vision, and data analytics to monitor mosquito egg densities (OL index) and provide early alerts to communities and health agencies about dengue risk.

Table of Contents

Overview

Background & Motivation

Key Components

Features & Functionalities

System Architecture

Data Processing & Analytics

Deployment & Field Trials

How to Use / Integration

Project Status & Roadmap

Team, Partners & Acknowledgments

References

1. Overview

C-DEWS builds upon the idea of Ovicidal-Larvicidal (OL) traps that collect mosquito eggs in a controlled medium. In C-DEWS, each trap is enhanced with a camera + connectivity so that images are captured, uploaded, analyzed automatically, and the egg count index is computed in real time. The system also supports metadata (device location, station info) and stores results in a database for visualization, alerts, and further analytics.

2. Background & Motivation

Dengue is a persistent public health challenge in the Philippines and many tropical countries.

Conventional surveillance relies heavily on manual counting, periodic inspections, and delayed reporting.

C-DEWS seeks to make surveillance continuous, automated, scalable, and community-driven.

The IoT-based OL trap concept for dengue surveillance is registered in the Philippine Health Research Registry under “IoT-Based OL Trap and Community Dengue Early Warning System (C-DEWS)”. 
Philippine Health Research Registry

C-DEWS has been showcased under DOST’s HeaRTnovation program as a funding beneficiary. 
PCHRD
+1

A peer-reviewed paper, “Design and implementation of an IoT-OL trap for community-based dengue early warning system,” describes the architecture, hardware, and performance (with > 99.5 % detection accuracy in lab setting). 
INNSpub
+1

3. Key Components
Component	Description
OL Trap with Camera	Physical trap to attract and collect mosquito eggs; includes a mini-camera to photograph the egg surface at regular intervals.
Connectivity Module	Sends images or metadata to a central server (via WiFi, 4G, or LoRa).
Image Processing / Vision Model	Runs detection (using CNN / Roboflow) to count Aedes mosquito eggs from images.
Backend & Database	Stores captured data, metadata, results; supports queries, logging, analytics.
Frontend / Dashboard (optional)	Visualization of OL index trends, alerts, map views.
Analytics & Alert Engine	Correlates egg index, location, weather, and dengue case data to generate early warnings.
4. Features & Functionalities

Automatic Egg Counting: Each trap image is uploaded and analyzed to count eggs in near real time.

Metadata Support: Device identifiers, station name, barangay, purok, latitude & longitude are stored.

Image Outputs: Original image, annotated image (egg bounding boxes), black & white or thresholded versions.

Logging: Results saved in CSV and SQLite (or other database) with timestamp, device, location, egg count.

Historical Table / Record View: A table view of all captured data, accessible for review.

Clear / Reset Function: Option to clear stored images and database entries.

Scalable Architecture: Suitable for deployment across multiple barangays, integrated with central health systems.

5. System Architecture

Trap Device: Captures images periodically or on demand.

Local Module: Optionally preprocess (resize, compress) before upload.

Server Endpoint (e.g., Flask + ngrok / cloud server): Accepts image + metadata → saves file → runs detection → logs results → returns JSON with counts and image URLs.

Database & File Storage: SQLite (or heavier DB) + filesystem store of image files.

Viewer / Dashboard / Analytics Module: Visualize trends, set thresholds, send alerts.

6. Data Processing & Analytics

Detection Model: Based on Roboflow / CNN, trained to detect class name “albopictus” eggs.

Image Transformations:

Original

Annotated (bounding boxes)

Grayscale / thresholded (black & white)

Index Computation: Eggs counted per trap → OL index (per area) → alerts.

Storage: Results stored in both SQLite & CSV.

Visualization: Table view, graphs over time, maps.

7. Deployment & Field Trials

A field test was conducted in Cauayan City, Isabela to deploy traps across barangays. 
PCHRD
+2
INNSpub
+2

The prototype traps were connected via antennas to mitigate signal issues. 
PCHRD

Data from the traps was successfully transmitted and integrated into the backend, enabling real-time index computation. 
PCHRD

The current Technology Readiness Level (TRL) is estimated around TRL 5. 
PCHRD

8. How to Use / Integration

Provide the trap device with camera + connectivity.

Send POST requests to the server’s /predict endpoint with:

Form fields: device_id, station_name, barangay, purok, latitude, longitude

File field: file (the image)

Receive JSON response containing egg count and image URLs.

View table or dashboard by accessing /table on server (if supported).

Clear data using /clear_uploads route (if included).

Example JSON response format:

{
  "timestamp": "2025-10-08 15:00:23",
  "device_id": "Trap001",
  "egg_count": 42,
  "image_url": "...",
  "bw_image_url": "...",
  "annotated_image_url": "..."
}

9. Project Status & Roadmap

Status: Prototype deployed, field trials ongoing, detection accuracy promising.

Next Steps / Roadmap:

Improve detection model robustness under varying lighting, dirt, debris.

Integrate meteorological data (rainfall, humidity, temperature) to build predictive models.

Merge dengue case data from local health offices to validate correlation.

Develop a full web dashboard for public and health officials.

Scale deployment to multiple municipalities and integrate with government health systems.

Seek additional funding and collaboration for expansion.

10. Team, Partners & Acknowledgments

Implementing Institution: Isabela State University (ISU), BIRD-C
Primary Funding / Supporting Agencies:

DOST / PCHRD (Philippine Council for Health Research and Development) 
PCHRD
+1

Japan’s National Institute of Information and Communications Technology (cooperating) 
Philippine Health Research Registry

Local Government Unit, Cauayan City (installation support) 
Philippine Health Research Registry

Lead Researchers / Team:

Betchie E. Aguinaldo (IT / systems) 
Philippine Health Research Registry
+1

Arnel C. Fajardo (AI / image processing) 
Philippine Health Research Registry
+1

Additional team members in software, field work roles 
Philippine Health Research Registry

Acknowledgments:
Thanks to the DOST PCHRD program for funding, local LGU support in Cauayan City, and community partners for trial sites.

11. References & Further Reading

IoT-Based OL Trap and Community Dengue Early Warning System (Registry) 
Philippine Health Research Registry

DOST / PCHRD project description of C-DEWS 
PCHRD

“Design and implementation of an IoT-OL trap for community-based dengue early warning system” (2025) 
INNSpub
+1

Dengue Early Warning Systems as Outbreak Prediction Tools (systematic review) 
pubmed.ncbi.nlm.nih.gov
