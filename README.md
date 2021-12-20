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

## Data sources

| data | docs folder | location  |
|:--|:--|:--|
| `cashflows.../2017...` |`cashflows` | file `2017...` tab 'Cash flows as at 31032017' |
| `cashflows.../2020...` |`cashflows` | file `2020...` table 1 page 2 |
| `cpi_gilts.../2008...` |`actuarial_valuation` | file `...2008` page 27 |
| `cpi_gilts.../2011...` |cpi_gilts | file `...2011` page 16 |
| `cpi_gilts.../2014...` |cpi_gilts | file `...2014` page 13 |
| `cpi_gilts.../2017_Sept...` |cpi_gilts | file `2017_Sept...` table 16 page 51|
| `cpi_gilts.../2017_Nov...` |cpi_gilts | file `2017_Nov...` table 7 page 11|



