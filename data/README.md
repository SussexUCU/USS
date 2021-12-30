# Sources for data

Sources for data is mostly direct from USS documents. These sources detailed below, organised by data folder, then basis (nominal, CPI, or gilts) and then by year.


## `assets_returns`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 1987-2021 |see each .csv file in the `assets_returns` folder for page of relevant USS Annual Report and Account filed in [docs/reports_accounts/](https://github.com/SussexUCU/USS/tree/main/docs/reports_accounts 'report_accounts') |   
| `cpi`| 1987-2021 | cpi-basis values of assets and investment returns are derived from USS nominal-basis values using ONS historic CPI values|   


## `best_estimates`
| basis | year | source |
|:--|:--|:--| 
| `cpi`| 2017 November |page 18 of 2017 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |  
| `cpi`| 2018 | page 26 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "2017 valuation") |   
| `cpi`| 2020 | estimated from USS Document likely outcome of 2021 valuation - JG ask list if anyone can knows better source | 
| `cpi`| 2021 | estimated from USS Document likely outcome of 2021 valuation - JG ask list if anyone can knows source | 
| `nominal`| 2017, 2018, 2020, 2021 |derived from nominal using USS CPI projections for relevant year | 


## `cashflows`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 2017 | copied from tab 'Cash flows as at 31032017' in spreadsheet by Sam Marsh filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `nominal`| 2020 | copied from USS website and filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `cpi`| 2017, 2020 | cpi-basis values derived from nominal-basis values using USS CPI projections for relevant year (all CPI values in `data/cpi_gilts` folder and detailed below |   

## `cpi_gilts`

All the data on CPI and gilts projections from USS valuations are in the nominal-basis.
| year | source |
|:--|:--| 
| 2008 | see page 27 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2011 | see page 16 of 2011 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2014 | see page 13 of 2014 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2017 November | see page 13, table 22 in November 2017 Technical Provisions Consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2017 September | see page 51, table 16 in September 2017 Technical Provisions Consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2018 | see page 38 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2020 | blah Interim Actuarial Valuatoin 2019 page X |   

## `discount_rates`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 1987-2021 |see each .csv file in the `assets_returns` folder for page of relevant USS Annual Report and Account filed in [docs/reports_accounts/](https://github.com/SussexUCU/USS/tree/main/docs/reports_accounts 'report_accounts') |   
| `cpi`| 1987-2021 | cpi-basis values of assets and investment returns are derived from USS nominal-basis values using ONS historic CPI values|   

## `ons`
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 1987-2021 |see each .csv file in the `assets_returns` folder for page of relevant USS Annual Report and Account filed in [docs/reports_accounts/](https://github.com/SussexUCU/USS/tree/main/docs/reports_accounts 'report_accounts') |   
| `cpi`| 1987-2021 | cpi-basis values of assets and investment returns are derived from USS nominal-basis values using ONS historic CPI values|   

