# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Repository Overview

A personal collection of standalone scripts, notebooks, and reference tools for data science, machine learning, cloud engineering, geospatial analysis, and telematics. There is no package structure, test suite, or CI/CD pipeline — each file is an independent utility or demo.

**Primary languages:** Python, R, SQL
**Secondary languages:** Shell (bash), VBA, Sublime Text snippets

## Repository Structure

```
my_tools/
├── *.py                          # Python scripts and utilities
├── *.R / *.Rmd                   # R scripts and R Markdown EDA files
├── *.sql                         # SQL query utilities
├── *.ipynb                       # Jupyter notebooks
├── *.sh                          # Shell scripts
├── *.vb                          # VBA macros for Excel
├── env_dev*.yml                  # Conda environment files
├── vsc-extensions.txt            # VS Code extension list
├── solar_panel_detection_INCOMPLETE/   # Incomplete subproject with training data
│   └── data/train/*.tif          # GeoTIFF training images
├── sublimetext_snippet/          # Sublime Text code snippets
└── README.md                     # Repository overview
```

## Script Categories

### Data Processing & DataFrames
| File | Description |
|------|-------------|
| `polars_usage.py` | Polars DataFrame reference — lazy evaluation, window functions, filtering, joins |
| `datatable_usage.py` | datatable.Frame operations with typed helper functions (`to_vals`, `rename_cols`, etc.) |
| `pandas_sql_data_mining.py` | Pandas + SQL Server via pyodbc/SQLAlchemy; DataFrame manipulation patterns |
| `combine_all_csv.py` | Merge multiple CSV files into one |
| `json_load_transfer.py` | JSON load/transform utilities |
| `guess_probability_distribution.py` | Fit statistical distributions to data |

### AWS / Cloud
| File | Description |
|------|-------------|
| `s3_buckets_creation_deletion.py` | S3 bucket creation/deletion via `boto` |
| `s3_file_search_and_download.py` | S3 file search and download |
| `file_pattern_match_on_s3.py` | Glob-style pattern matching on S3 keys |
| `compareListOnS3.py` | Compare local vs S3 file lists |
| `extract_aws_filelist.py` | Enumerate AWS file listings |
| `get_list_of_folders_ons3.py` | List S3 folder structure |
| `exec_spark.py` | PySpark job execution helper |

### Machine Learning & Modeling
| File | Description |
|------|-------------|
| `automated_data_imputation_by_h2o_gbm.R` | H2O GBM-based data imputation |
| `tree_glm_models_for_poisson_regression_demo.R` | Tree + GLM Poisson regression demo |
| `tree_models_for_insurance_pricing_model_demo.R` | Insurance pricing with tree models |
| `Hybrid_GBM_BoostrapRRF.R` | Hybrid GBM + Bootstrap RRF model |
| `survival_analysis_cox_regression_byGBM.R` | Cox regression via GBM |
| `find_interaction_by_gbm.R` | Detect variable interactions via GBM |
| `sample_keras_for_image_classfication.py` | Keras CNN image classification |
| `sample_zillow_kaggle_challenge_code.py` | Zillow Kaggle competition code |
| `AutoEncoder_for_AdsDataset.ipynb` | Autoencoder for anomaly detection |
| `Introduction_to_Stacking_in_Python(with_plotly).ipynb` | Model stacking example |
| `quantile_regression_by_xgboost_gbm.ipynb` | Quantile regression with XGBoost |
| `Simple_GBM_Interaction_Geo_Spatial_Prediction_R.ipynb` | GBM geospatial prediction in R |
| `Multivariate Time Series Forecasting with LSTMs in PyTorch.ipynb` | LSTM time-series forecasting |

### Geospatial
| File | Description |
|------|-------------|
| `pggis2shp.py` | Export PostGIS layers to Shapefile |
| `transform_and_upload_ShapeFile.py` | Reproject and upload Shapefiles |
| `alignPtShpWithPolyShp_Fun.R` | Align point shapefile to polygon shapefile |
| `python_batch_google_geocoding.py` | Batch geocoding via Google Maps API |
| `generate_noearth_xyz.py` | Generate non-earth XYZ point clouds |
| `zonal_stats.py` | Raster zonal statistics |
| `geopandas_sample_usage.ipynb` | GeoPandas operations reference |
| `geo_find_nearest_road_by_GPS_point.ipynb` | Nearest road lookup by GPS coordinate |

### Image Processing
| File | Description |
|------|-------------|
| `image_find_books.py` | Detect books in images |
| `image_shadow_removal_1.py` | Shadow removal method 1 |
| `image_shadow_removal_2.py` | Shadow removal method 2 |
| `image_svd_transform.py` | SVD-based image compression/transform |
| `image_watershed_segmentation2.py` | Watershed image segmentation |
| `image_watershed_segmentationSample.py` | Watershed segmentation sample |
| `las_into_building_non_building.py` | LiDAR point cloud building classification |
| `solar_panel_detection_INCOMPLETE/` | Incomplete solar panel detection (GeoTIFF training images present) |

### Telematics / GPS
| File | Description |
|------|-------------|
| `simple_telematics_data_extraction_ver1.py` | Telematics feature extraction v1 |
| `simple_telematics_data_extraction_ver2.py` | Telematics feature extraction v2 (class-based, multiprocessing) |
| `accelerometer_process_telematics.ipynb` | Accelerometer data processing |
| `sample_trip_accelerometer_data_merge.ipynb` | Trip + accelerometer data merging |
| `test_cython_on_gps_telematics_data.ipynb` | Cython optimization for GPS processing |
| `kalman_filter_demo_on_GPS.ipynb` | Kalman filter for GPS smoothing |
| `Design_Kalman_Filter.ipynb` | Kalman filter design reference |

### R Statistical Tools
| File | Description |
|------|-------------|
| `basic_spline_features.R` | Basic spline feature generation |
| `B-spline and its decomposition.R` | B-spline construction and decomposition |
| `spline_creation_and_predict.R` | Spline model creation and prediction |
| `stepAIC_Fun.R` | Stepwise AIC model selection function |
| `Variable_Clustering_Dentrogram.R` | Variable clustering dendrogram |
| `relativity_bar_lines_plot.R` | Relativity bar + line plots |
| `power_test_simulation_in_parallel.R` | Parallel power test simulation |
| `R_and_Database.R` | R database connectivity (ODBC/DBI) |
| `R_fst_feather_file_and_data_dictionary_creation.R` | fst/feather file I/O + data dictionaries |
| `loadJson_fun.R` | JSON loading utility for R |
| `random_name_generator.R` | Random name generation in R |
| `whichPythonVersion.R` | Call Python from R and detect version |

### SQL Utilities
| File | Description |
|------|-------------|
| `dates_and_schedules.sql` | Date arithmetic and scheduling queries |
| `lat_long_distance_function_SQL.sql` | Haversine distance function in SQL |
| `select_top3_field_values.sql` | Top-N per group SQL patterns |
| `weather_imputation.sql` | Weather data gap-filling in SQL |

### EDA Notebooks / Reports
| File | Description |
|------|-------------|
| `EDA_The Most Dangerous Places to Work in the USA.rmd` | Workplace safety EDA in R Markdown |
| `EDA_Univariate_Analysis.Rmd` | Univariate analysis template |
| `kaggle_zillow_EDA_v01–v04.Rmd` | Zillow Kaggle EDA (R versions) |
| `kaggle_zillow_EDA_v03.ipynb` | Zillow Kaggle EDA (Python version) |

### Utility / Productivity Scripts
| File | Description |
|------|-------------|
| `decorators.py` | Reusable decorators: `suppress_errors`, `memorize_simple`, `memorize` (class), `logs` |
| `email_notification.py` | Send email notifications from Python |
| `ftp_download.py` | FTP file download utility |
| `exeBashFile_in_parallel.py` | Execute bash scripts in parallel via multiprocessing |
| `photo_video_file_management_and_backup.py` | Photo/video deduplication and backup |
| `workspace_save_restore.py` | Save/restore Python workspace variables |
| `python_save_workspace_content.py` | Minimal workspace content saver |
| `matplotlib_plots.py` | Common matplotlib plot patterns |
| `random_name_generator.py` | Random name generation in Python |
| `Lottery_NY4Life.py` | NY Lottery number analysis |

### Shell / Infrastructure
| File | Description |
|------|-------------|
| `docker_basic_operation.sh` | Docker build/run/stop command reference |
| `change_py26_to_py27_in_HortonworksHDP.sh` | Python version migration on HDP cluster |
| `sample_use_esri_plugin_on_hive.sh` | ESRI plugin usage on Hive |

### Excel / VBA
| File | Description |
|------|-------------|
| `Fuzzy_Words_Comparison_Excel.vb` | Fuzzy string matching macro for Excel |
| `timeseries_plot_compar_Excel.vb` | Time-series comparison chart macro |

## Environment Setup

### Python (Conda)
Three conda environment YAML files are included for reproducibility:

```bash
# Python 3.6 environment
conda env create --file=env_dev36_20210516.yml

# Python 3.8 environment (May 2021)
conda env create --file=env_dev38_20210516.yml

# Python 3.8 environment (Sept 2021, most complete)
conda env create --file=env_dev38_20210901.yml

# Export current environment
conda env export > myenv.yml
```

Key packages available across environments: numpy, pandas, scikit-learn, scipy, matplotlib, xgboost, h2o, polars, datatable, boto/boto3, geopandas, shapely, pyodbc, sqlalchemy, keras/tensorflow, pytorch, pyspark, scrapy, pyinstaller, cython, Jupyter.

### R
No explicit package management file. R packages are installed inline within each `.R` script. Common packages used: `data.table`, `ggplot2`, `dplyr`, `caret`, `h2o`, `xgboost`, `survival`, `splines`, `sp`, `rgdal`.

### VS Code Extensions
The file `vsc-extensions.txt` lists all VS Code extensions. To restore them:
1. Install the **VSC Extension Export & Import** extension
2. Run `VSC Import` from the Command Palette, pointing to `vsc-extensions.txt`

## Code Conventions

### Python
- Scripts use `# -*- coding: utf-8 -*-` and `#!/usr/bin/env python` headers
- Author noted as `@author: pm` in docstrings
- Helper functions use Google-style or NumPy-style docstrings
- Type hints used in newer files (e.g., `datatable_usage.py`)
- AWS credentials are loaded from external JSON files (e.g., `s3_key.json`) — never hardcoded
- Multiprocessing used for CPU-bound parallelism (`multiprocessing` module)
- Polars preferred over pandas for performance; use `.lazy()` + `.collect()` patterns

### R
- Scripts are self-contained with library imports at the top
- Functions follow `camelCase` or `snake_case` naming
- R Markdown files (`.Rmd`) contain narrative + code for EDA reports

### SQL
- Written for SQL Server / T-SQL dialect (some Hive SQL in shell scripts)
- Custom scalar functions defined for reuse (e.g., distance calculations)

## Key Patterns to Know

### Polars Best Practices (from `polars_usage.py`)
```python
# Prefer lazy evaluation
df.lazy().select([...]).collect()

# Use .over() for window functions instead of merge
pl.col("A").sum().over("group_col")

# Avoid .to_numpy() for performance; work with pl.Series directly
```

### Datatable Helper Functions (from `datatable_usage.py`)
```python
from datatable_usage import to_vals, rename_cols
# to_vals(dt_table, "col") -> np.ndarray
# rename_cols(dt_table, {"old": "new"})
```

### Decorators (from `decorators.py`)
```python
from decorators import suppress_erros, memorize_simple, memorize, logs

@memorize()              # memoize with verbose output
@suppress_erros          # silently swallow exceptions
@logs("path/to/log.txt") # log errors to file
```

### AWS S3 Credentials
S3 scripts expect a `s3_key.json` file (not committed to git) with connection details. Pattern:
```python
import json
s3_key_info = json.load(open("s3_key.json", "r"))
```

## Development Workflow

This repo is a flat script collection — there is no build system, test runner, or linting configuration. When adding or modifying scripts:

1. Keep scripts self-contained and independently runnable
2. Add a module-level docstring explaining purpose and usage
3. Load credentials from external files, never hardcode them
4. For new Python utilities, follow the existing pattern of short focused scripts
5. For notebooks, keep outputs cleared before committing where possible

## Git Workflow

```bash
# The main branch is 'master'
git checkout master
git pull origin master

# Feature branches follow the pattern:
# claude/<description>-<id>
git checkout -b claude/my-feature-XYZ
git push -u origin claude/my-feature-XYZ
```

## Notable Files to Reference

- `decorators.py` — utility decorators usable across all Python scripts
- `polars_usage.py` — comprehensive Polars API reference with comments
- `datatable_usage.py` — datatable operations with well-typed helper functions
- `pandas_sql_data_mining.py` — SQL Server + Pandas integration patterns
- `env_dev38_20210901.yml` — most complete conda environment specification
