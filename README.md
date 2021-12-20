# USS
Data on the Universities Superannuation Scheme

With some calculations and graphs

## Overview

We are attempting to put all USS data in one place.

This is a work in progress


## Folder and file organisation

| Folder | Description  |
|:--|:--|
| `data/cashflows`|Raw data from USS. The projected future cashflows due to promised pensions for valuations in 2017 and 2020. Cashflows are stated in the nominal-basis, although they are approimately invarient in the cpi-basis. USS also give projected cpi-values at each valuation so it is straightforward to convert nominal-basis cashflows to cpi-basis cashflows. These data are the yearly projected pensions due on each valuation date. The data are given in two columns for each year. The first column is cashflows from pensions promised up to the valuation date. The second column is cashflows from pensions projected to be accrued in the coming year. The first column is used to calucate the Liabilities on a Technical Provisions (TP) basis, and hence any TP surplus or deficit. The second column is used to calculate the Future Service Costs. |   
| `data/cpi_gilts`|  Raw data from USS. These are the cpi projections from valuations in 2020, 2018, November 2017, September 2017, 2014 and 2011. 2020 also has gilts projections. All projections are 1-year forward rates. These are used to convert discount-rates and cashflows from the nominal-basis to the cpi-basis.  |
| `data/discount_rates` | Raw data from USS. These are the prudent-assumptions used at each valuation to discount cpi-basis cashflows back to the valuation date to calculate the Liabiliites on a Technical Provisions basis, it is equivalent to calculate the Net Present Value of the future cost of pension provision.|  
| `data/refs` | List of document and page number for each data set. |
| `fifth` |`fifth` | fifth blah|

## Data references

| Data | Source  |
|:--|:--|
| `cashflows`|2020: docs/cashflows_2017_2020/2017_valuation_cashflows_Sam_Marsh_valuation_modeller_AUG_18_dummy_data.xlsx (https://user-images.githubusercontent.com/67890269/146770261-6b719d31-ec32-4a6a-a88b-bb4502a1c220.png)
 // 2017 https://github.com/SussexUCU/USS/blob/main/docs/cashflows_2017_2020/2017_valuation_cashflows_Sam_Marsh_valuation_modeller_AUG_18_dummy_data.xlsx |   
| `data/cpi_gilts`|  Raw data from USS. These are the cpi projections from valuations in 2020, 2018, November 2017, September 2017, 2014 and 2011. 2020 also has gilts projections. All projections are 1-year forward rates. These are used to convert discount-rates and cashflows from the nominal-basis to the cpi-basis.  |
| `data/discount_rates` | Raw data from USS. These are the prudent-assumptions used at each valuation to discount cpi-basis cashflows back to the valuation date to calculate the Liabiliites on a Technical Provisions basis, it is equivalent to calculate the Net Present Value of the future cost of pension provision.|  
| `data/refs` | List of document and page number for each data set. |
| `fifth` |`fifth` | fifth blah|
