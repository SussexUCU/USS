# USS
Data on the Universities Superannuation Scheme

With some calculations and graphs

## Overview

We are attempting to put all USS data in one place.

This is a work in progress


| Folder | sub-folder | Description  |
|:--|:--|:--|
| `data`   | `cashflows`   |raw data from USS. These are used to calculate liabilities. The only data available from USS are 2017 and 2020 valuations cashflows. Cashflows are invarient in the cpi-basis, although USS state cashflows in the nominal-basis. However USS also give projected cpi-values at each valuation so it is straightforward to convert nominal-basis cashflows to cpi-basis cashflows. These data are the yearly projected pensions due on each valuation date. The data are given in two columns for each year. The first column is cashflows from pensions promised up to the valuation date. The second column is cashflows from pensions projected to be accrued in the coming year. The first column is used to calucate the Laibilities on a Technical Provisions (TP) bases, and hence any TP surplus or deficit. The second column is used to calculate the Future Service Costs.   |   
| `data`  |`cpi_gilts`  |  raw data from USS. These are the CPI projections from valuations 2020, 2018, 2017 November, 2017 September, 2014 and 2011. Not all have gilts projections. All projections are 1-year forward rates. These are used to convert discount-rates and cashflows from the nominal-basis to the CPI-basis.  |
| `data`  |`discount_rates`  | raw data from USS. |  
| `fourth` |`fourth` | fourth blah |
| `fifth` |`fifth` | fifth blah|

