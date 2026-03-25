# 🌊 Hamburg Digital Twin: HEC-RAS Automation API

This project aims to transform the **HEC-RAS** hydrodynamic modeling software from a traditional desktop application into a fully automated **backend engine** for the Hamburg Digital Twin. It allows for dynamic scenario generation based on external parameters (e.g., sea-level rise, dyke heightening) without manual GUI interaction.

## 🚀 Key Features

- **Dynamic Scenario Generation (`create_scenario.py`):** Clones a reference HEC-RAS unsteady flow plan (`.uXX`), parses the Fortran-based text file, and mathematically updates the **Stage Hydrograph** boundary conditions based on specified parameters (e.g., +1.2m) without breaking HEC-RAS's strict 8-character width formatting.
  
- **Headless Execution (`run_model.py`):** Executes existing or newly generated HEC-RAS plans directly via the **HEC-RAS Native CLI (Command Line Interface)** in the background. It bypasses Windows Registry issues and COM interface limitations, ensuring the most reliable and fastest computation.

## 📂 Project Structure

```text
RAS_Automation_Project/
├── scripts/
│   ├── digital_twin/
│   │   ├── create_scenario.py   # Injects parameters into the flow file
│   │   └── run_model.py         # Triggers the headless HEC-RAS engine
│   └── playground/              # R&D and testing scripts
├── results/                     # Generated charts and analysis outputs
└── README.md                    # Project documentation
```

## 💻 Usage

**1. Generate a New Scenario:**
Injects external parameters (like sea-level rise) into the model.
```powershell
python scripts/digital_twin/create_scenario.py
```

**2. Run the Engine in the Background:**
Computes the specified plan without opening the HEC-RAS UI.
```powershell
python scripts/digital_twin/run_model.py
```

## 🔮 Future Roadmap (Next Steps)
- [ ] Merge the scenario generator and execution engine into a single `pipeline.py` script for seamless end-to-end automation.
- [ ] Implement Geometry (`.gXX`) parsing to manipulate Dyke/Levee heights dynamically.
- [ ] Integrate **FastAPI** to turn this system into a REST API, triggerable via HTTP requests from external platforms (e.g., React, Unity).

