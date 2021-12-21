# USS
Starting to upload data on the Universities Superannuation Scheme. Hoping to add some calculations and graphs

## Overview

An attempt to put key USS data in one place. This is a work in progress


## Folder and file organisation

| Folder | Description  |
|:--|:--|
| `data/cashflows`|Raw data from USS. In nominal-basis and cpi-basis. Only 2017 and 2020 have been made availble. These are the projected future cashflows due to promised pensions measured at a valuation date. Cashflows are stated in the nominal-basis, even though they are approimately invarient in the cpi-basis. USS also give projected cpi-values at each valuation so it is straightforward to convert nominal-basis cashflows to cpi-basis cashflows. These data are the yearly projected pensions due from each valuation date. The data are given in two columns for each year. The first column is cashflows from pensions promised up to the valuation date. The second column is cashflows from pensions projected to be accrued in the coming year. The first column is used to calucate the Liabilities on a Technical Provisions (TP) basis, and hence any TP surplus or deficit. The second column is used to calculate the Future Service Costs. |   
| `data/cpi_gilts`|  Raw data from USS. These are the cpi prdictions from valuations held in 2020, 2018, November 2017, September 2017, 2014 and 2011. 2020 also has gilts projections. All projections are 1-year forward rates. These are used to convert discount-rates and cashflows from the nominal-basis to the cpi-basis.  |
| `data/discount_rates` | Raw data from USS. Given in a mix of cpi-basis, nominal-basis and gilts-basis. These are the prudent-assumptions used at each valuation to discount cpi-basis cashflows back to the valuation date to calculate the Liabiliites on a Technical Provisions basis, it is equivalent to calculating the Net Present Value of the future cost of pension provision.|  
| `data/assets_returns` | Raw data from USS. These are the annual reported investment returns on the Income Builder (DB) part of the USS fund. Given as annual percentage. Also the reported value of assets (GBP) in the Income Builder (DB) part of the fund.|  
| `fifth` |`fifth` | fifth blah|

## Data references

All data are from USS, but some of it is hard to find or confusing. Here is a list showing where the data have come from in each document. 

| data | year | location  |
|:--|:--|:--|
| `cashflows` |2017 | Cashflows 2017 tab 'Cash flows as at 31032017' |
|  |2020 | Casfhlows 2020 table 1 page 2 |
| `discount_rates` |2011 | Actuarial Valuation 2011 page 16|
| `cpi_gilts` |2008 | file Actuarial Valuation 2008 page 27 |
|  |2011 | Actuarial Valuation 2011 page 16 |
|  |2014 | Actuarial Valuation page 13 |
|  |2017 Sept | Technical Provisions Consultation 2017 September table 16 page 51|
|  |2017 Nov | Technical Provisions Consultation 2017 November table 7 page 11|
|  |2018| file `2018...` page 38 |
| `cpi_gilts/2019...` |`actuarial_valuations` | file `2019...` page X jg to calc. CPI 2019 |
|  |`cashflows` | file `2020...` table 1 page 2 |



