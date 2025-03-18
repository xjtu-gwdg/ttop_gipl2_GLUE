# ttop_gipl2_GLUE

## Overview
This project analyzes the parameter uncertainties of the TTOP and GIPL2 models. The study employs the Latin Hypercube Sampling (LHS) method to explore multi-dimensional parameter space, ensuring a uniform and representative parameter distribution. The Generalized Likelihood Uncertainty Estimation (GLUE) framework is used to quantify uncertainty, with the mean bias as the likelihood function.

## Installation
```bash
pip install -r requirements.txt
```

## Run

   ```bash
   python scripts/TTOP model parameters.py
   python scripts/GIPL2 model parameters.py
   ```

## Model Parameters
### TTOP Model
The TTOP model includes three parameters:
- **nf**: The ratio between ground surface temperatures and air temperatures during freezing days.
- **nt**: The ratio between ground surface temperatures and air temperatures during thawing days.
- **rk**: The ratio of soil thermal conductivity in frozen and thawed states.

### GIPL2 Model
The GIPL2 model includes seven parameters:
- **VWC**: he volumetric water content (fraction of 1).
- **a**: The coefficient a of the unfrozen water curve.
- **b**: The coefficient b of the unfrozen water curve.
- **TVHC**: Thawed volumetric heat capacities (J/(m³·K)).
- **FVHC**: Frozen volumetric heat capacities (J/(m³·K)).
- **THC**: Thawed heat conductivities (W/(m·K)).
- **FHC**: Thawed heat conductivities (W/(m·K)).

## Methodology
- **LHS Method**: In this study, the parameter space is sampled using the Latin Hypercube Sampling (LHS) method to generate 10,000 parameter sets. For demonstration purposes, the GIPL2 model example is limited to 100 samples to expedite the testing process.
- **GLUE Framework**: The Generalized Likelihood Uncertainty Estimation (GLUE) framework is applied, using the mean bias as the likelihood function.
- **Observational Data**: The example code utilizes observation data from Borehole No. 66 to compare model outputs for quick computation. The TTOP model runs for the year 2010, aligning with the observation period of Borehole No. 66, while the GIPL2 model runs for the period 1960–2010.

## File Structure
- **data/**
  - `GIPL_GLUE/`: Contains the source code of the GIPL2 model.
  - `tas.csv` and `pr.csv`: Air temperature and precipitation data for Borehole No. 66 from 1960-2010.
- **temp/**
  - Temporary directory for GIPL2 model runtime files.
- **scripts/**
  - `1. TTOP model parameters.py`
  - `2. GIPL2 model parameters.py`
  - `utils/`: Contains function packages used in the scripts.

## Notes
- The example code is optimized for efficiency and quick demonstration.
- In a full-scale analysis, all borehole data should be used instead of just Borehole No. 66.


