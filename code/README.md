## USS pensions code updates

To update Sam Marsh prudent projections graph: 

- update CPI by updating `ons_cpi_annual_series.csv` and `ons_cpi_index_series.csv` direct from ONS site: see Folder [ons]([https://github.com/SussexUCU/USS/tree/b1ce885eb2e5e1285a72187809d959660faf5bbf/data/ons](https://github.com/SussexUCU/USS/tree/main/data/ons)
- update assets values by updating `1992_todate_raw_assets_nominal.csv` by adding row from USS data: see Folder nominal in folder [assets_returns](https://github.com/SussexUCU/USS/tree/b1ce885eb2e5e1285a72187809d959660faf5bbf/data/assets_returns).
- update discount rates by adding new file `<YEAR>_DISCOUNT_RATE_maintain_benefits_cpi_basis.csv` all stored in Folder [discount rates](https://github.com/SussexUCU/USS/tree/b1ce885eb2e5e1285a72187809d959660faf5bbf/data/discount_rates/cpi)
- Note: have not added instructions for 1. Best_est or 2. Break_even yet as 1. USS best-est data inconsistent, and 2. have not got data/calculated break-evens
- Run code as below
  
## USS pensions code
- `uss_pensions.py` - a python module for reading in data and defining useful functions for operating on it.
- `plot_assets.ipynb` - a Jupyter Notebook which shows how the module is used to calculate CPI-adjusted USS asset values and plot them in a clone of [Sam Marsh's famous graph from USSBriefs 106](https://medium.com/ussbriefs/how-extreme-prudence-and-misguided-risk-management-sent-the-uss-into-crisis-baf78c35d9e1).
- `plot_heatmap_hist.py` - python/pandas script for plotting histograms of pensions cuts from UUK heat map and USS modeller data
