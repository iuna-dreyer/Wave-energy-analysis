# Wave Energy Analysis

## Overview

This project implements a compact workflow for analysing offshore wave conditions using operational wave data from the Copernicus Marine Service.

The workflow covers:
- extraction and processing of multi-dimensional wave datasets
- analysis of spatial and temporal variability in wave conditions
- estimation of wave energy potential from standard wave parameters
- implementation of a simplified dynamic model of a generic wave energy converter

The focus is on building a reproducible, Python-based pipeline for handling real ocean wave datasets and deriving engineering-relevant insights for wave energy applications.


## Objectives

The main objectives of this project are:

- Process and structure operational ocean wave data (significant wave height, mean wave period, and wave direction)
- Analyse spatial and temporal variability of wave conditions in the Portuguese offshore region
- Identify and characterise energetic events within the dataset
- Estimate wave energy potential using standard deep-water wave energy formulations
- Develop a simplified dynamic model representing the response of a generic wave energy converter
- Link real wave conditions to the dynamic model to evaluate system response under realistic forcing
- Produce clear visualisations to support interpretation of wave climate and energy variability


## Data Source

Provider: 
Copernicus Marine Service 
https://marine.copernicus.eu/ accessed 2026-05-08

Product: 
Global Ocean Waves Analysis and Forecast
GLOBAL_ANALYSISFORECAST_WAV_001_027

Dataset:
3-hourly cmems_mod_glo_wav_anfc_0.083deg_PT3H-i

Variables:
Sea surface wave from direction VMDR [°]
Sea surface wave mean period from variance spectral density second frequency moment VTM02 [s]
Sea surface wave significant height VHM0 [m]

Area:
(Coast of Portugal)
N 44
S 36
W -13
E -8

Date Range:
From 01/01/2026 00:00
To   01/04/2026 00:00

Original filename:
cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_1778234914435.nc

## Methods

1. **Data Acquisition**
    - Loading operational wave data from NetCDF files provided by the Copernicus Marine Services using `xarray`.

2. **Exploratory Analysis**
    - Analysing units and dimensions.
    - Assessing spatial and temporal variability of wave conditions.
    - Computing summary statistics, distributions, and time series.
    - Creating and exporting overview plots and text file.

3. **Data Selection**
    - Selecting a representative offshore point for time-series-based and energy analysis.

4. **Wave Energy Estimation**
    - Computing wave power using standard deep-water wave energy relations based on significant wave height and wave period of a basic sinusoid wave.

5. **Dynamic Modelling**
    - Using a simplified single-degree-of-freedom mass-spring-damper system  to represent a generic wave energy converter.
    - Taking wave height time series as external forcing input.

6. **Visualisation**
    - Inputting to the model the time-series on the selected point.
    - Plotting the results in order to allow for interptretation.


## Tools

The project is implemented in Python using the following libraries:

- `xarray` — NetCDF data handling and multi-dimensional array processing
- `numpy` — numerical computations
- `math` — mathematical functions
- `pandas` — time-series structuring and analysis
- `matplotlib` — data visualisation
- `scipy` — numerical integration for dynamic modelling
- `cartopy` — production of maps and geospatial data analysis


## Assumptions

The following assumptions are made throughout the analysis:

- Wave data from the Copernicus Marine Service is treated as a physically consistent representation of ocean wave conditions over the selected region and period.
- Significant wave height (Hs) and mean wave period (T) are sufficient to characterise wave energy content for the purposes of this study.
- Deep-water wave energy approximations are valid for the offshore region considered.
- Wave direction is treated as secondary information and is not explicitly included in the energy estimation model.
- The wave energy converter is represented as a simplified linear single-degree-of-freedom system.
- The forcing applied to the dynamic model is assumed to scale proportionally with significant wave height.
- Effects such as device control systems, nonlinear hydrodynamics, and mooring dynamics are neglected.


## Results

To be completed


## Author
Iuna Dreyer

