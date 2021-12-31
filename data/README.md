# Sources for data

Sources for data are direct from USS documents. 
The location of these sources are detailed in the tables below. 
The tables are organised by data folder, then basis (nominal, CPI, or gilts) and then by year.


## `assets_returns`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 1987-2021 |direct from Annual Report and Accounts. See each .csv file in the `assets_returns` data folder above for page of relevant USS Annual Report and Account filed in [docs/reports_accounts/](https://github.com/SussexUCU/USS/tree/main/docs/reports_accounts 'report_accounts') |   
| `cpi`| 1987-2021 | derived cpi-basis values of assets and investment returns from USS nominal-basis values using ONS historic CPI values|   


## `best_estimates`
| basis | year | source |
|:--|:--|:--| 
| `cpi`| 2017 November |direct from page 18 of 2017 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |  
| `cpi`| 2018 | direct from page 26 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "2017 valuation") |   
| `cpi`| 2020 | estimated from USS Document likely outcome of 2021 valuation - JG ask list if anyone can knows better source | 
| `cpi`| 2021 | estimated from USS Document likely outcome of 2021 valuation - JG ask list if anyone can knows source | 
| `nominal`| 2017, 2018, 2020, 2021 |derived nominal-basis values using cpi-basis values and USS CPI projections for relevant year | 


## `cashflows`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 2017 | direct from tab 'Cash flows as at 31032017' in spreadsheet by Sam Marsh filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `nominal`| 2020 | direct from page 2, table 1 of USS website .pdf of 2020 cashflows and filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `cpi`| 2017, 2020 | derived cpi-basis values from nominal-basis values using USS CPI projections for relevant year (all CPI values in `data/cpi_gilts` folder and detailed below |   

## `cpi_gilts`

All the data on CPI and gilts projections from USS valuations are in the nominal-basis.
| year | source |
|:--|:--| 
| 2008 | direct from page 27 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2011 | direct from page 16 of 2011 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2014 | direct from page 13 of 2014 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2017 November | direct from page 13, table 22 of November 2017 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2017 September | direct from page 51, table 16 of September 2017 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2018 | direct from page 38 of 2018 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |   
| 2020 | direct from page 4, table 2 of USS website .pdf of 2020 cashflows and filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   

## `discount_rates`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| blah |blah |   
| `cpi`| blah | blah|   

## `ons`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| blah |blah |   
| `cpi`| blah | blah|   

