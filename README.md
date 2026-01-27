# HEC-RAS Automation with Python (ras-commander)

This repository contains a Python-based automation toolkit for **HEC-RAS 6.x** using the `ras-commander` library. It is designed to streamline the process of extracting simulation results, analyzing hydraulic data, and visualizing model outcomes directly from HDF5 files.

## 🚀 Features
- **Project Initialization:** Seamless connection to HEC-RAS project files (`.prj`).
- **Automated Data Extraction:** Accessing plan details, simulation durations, and volume errors via `results_df`.
- **Result Visualization:** Generating automated plots for Volume Balance (Starting vs. Ending Volume) using `matplotlib`.
- **HDF5 Integration:** Reading direct computation messages and plan information from RAS HDF files.

## 📁 Project Structure
- `scripts/`: Python automation scripts (initialization, data extraction, and plotting).
- `results/`: Automated visual outputs and data summaries.
- `data/`: (Local only) HEC-RAS project and geometry files.
- `venv/`: Virtual environment for dependency management.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ergunumut/RAS_automation](https://github.com/ergunumut/RAS_automation)
   cd RAS_automation
Set up the virtual environment:



python -m venv venv
.\venv\Scripts\activate
Install dependencies:



pip install ras-commander matplotlib pandas
📊 Sample Output
The current workflow includes a volume comparison analysis for the "WADI-Curve" plan. It tracks the net volume change in the system to ensure mass balance consistency.

⚠️ Requirements
HEC-RAS 6.6 (or compatible 6.x version)

Python 3.10+ (Developed and tested with 3.13)

ras-commander 0.88.6+

📝 License
This project is for educational and engineering research purposes.