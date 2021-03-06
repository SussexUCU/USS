# Sources for data

Data in folders above are mostly copied direct from USS documents or derived in a straight-forward way from data in USS documents. In a few cases they are estimated from a wider range of USS parameters. 
The location of sources for each data file are detailed in the tables below. 
The tables are organised by data folder, then basis (nominal, CPI, or gilts) and then by year.


## `assets_returns`
These are the yearly USS reported assets and investment returns in the DB or income builder part of the pension fund. All given in the year they are reported meaning they are in the nominal-basis. 
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 1987-2021 |copied direct from Annual Report and Accounts. See each .csv file in [data/assets_returns](https://github.com/SussexUCU/USS/tree/main/data/assets_returns 'assets_returns') data folder above for page of relevant USS Annual Report and Account filed in [docs/reports_accounts](https://github.com/SussexUCU/USS/tree/main/docs/reports_accounts 'report_accounts') |   
| `cpi`| 1987-2021 | derived using script in [code](https://github.com/SussexUCU/USS/tree/main/code 'code') to get cpi-basis values by month of reporting of assets and investment returns from USS nominal-basis values using ONS historic CPI values filed in [data/ons](https://github.com/SussexUCU/USS/tree/main/data/ons "ons")|   


## `best_estimates`
These are the USS 'best-estimates' of projected returns on assets for the DB or income builder part of the pension fund. They can be given in cpi-basis, nominal-basis or gilts-basis. Unable to find best-estimates earlier than 2017.
| basis | year | source |
|:--|:--|:--| 
| `cpi`| 2011 | estimated from prudent discount rate, method and calculation in [best estimates](https://github.com/SussexUCU/USS/tree/main/data/best_estimates 'best estimates'  |  
| `cpi`| 2014 | estimated from prudent discount rate, method and calculation in (JG to do - see 2014 note on best estimates and outperforance)[best estimates](https://github.com/SussexUCU/USS/tree/main/data/best_estimates 'best estimates'  |  
| `cpi`| 2017 November | copied direct from page 18 of 2017 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |  
| `cpi`| 2018 | copied direct from page 26 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| `cpi`| 2020 | estimated from gilts-basis value on page 12 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs") | 
| `cpi`| 2021 | estimated from gilts-basis value on page 12 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs")   | 
| `nominal`| 2017, 2018 |derived nominal-basis values using cpi-basis values and USS CPI projections for relevant year filed in [data/cpi_gilts](https://github.com/SussexUCU/USS/tree/main/data/cpi_gilts 'cpi_gilts') | 
| `nominal`| 2014, 2015, 2020, 2021 |these can be readily derived as nominal-basis values using cpi-basis values and USS CPI projections for relevant year filed in [data/cpi_gilts](https://github.com/SussexUCU/USS/tree/main/data/cpi_gilts 'cpi_gilts') - we haven't done this yet.| 

## `break_even_discount_rates`
These are calculated or estimated values of discount rates that would have produced a deficit of zero for each valuation. These are calculated from cashflows for 2017 and 2020. Since USS do not provide cashflows for 2011 or 2014 we estimate these break even discount rates. Methods detailed in 
| basis | year | source |
|:--|:--|:--| 
| `cpi`| 2011 | derived from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even") |  
| `cpi`| 2014 | derived from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even") |  
| `cpi`| 2017 November | calculated from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even") |  
| `cpi`| 2018 | derived from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even") |   
| `cpi`| 2020 | calculated from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even") | 
| `cpi`| 2021 | derived from USS data as per calculation method shown in README file of [data/break_even_discount_rates](https://github.com/SussexUCU/USS/tree/main/data/break_even_discount_rates "break even")  | 
| `nominal`| 2011, 2014, 2017, 2018, 2020, 2021 |these can be readily derived as nominal-basis values using cpi-basis values and USS CPI projections for relevant year filed in [data/cpi_gilts](https://github.com/SussexUCU/USS/tree/main/data/cpi_gilts 'cpi_gilts') - we haven't done this yet. | 



## `cashflows`
These are the projected amounts that USS expects to pay as a result of the DB or income builder pension promises built up prior to the valuation date. They are quoted as yearly amounts and are usually quoted in the nominal-basis, which is strange as they should be invarient in the cpi-basis as they are pegged to cpi (that is pensions should grow roughly in line with cpi). Unable to find any cashflows except for 2017 and 2020. However, both these cashflows give data for first: pensions promised up to the valuation date (these are strongly protected and are used to calculate the USS quoted 'deficit') and second: pensions predicted to be promised as a result of payment that will be made by USS members one year into the future (these are not strongly protected and are used to calculate the future service costs). Because these extra one-year ahead cashflows are given it is possible to estimate 2018 and 2021 casfhlows. 
| basis | year | source |
|:--|:--|:--| 
| `nominal`| 2017 | copied direct from tab 'Cash flows as at 31032017' in spreadsheet by Sam Marsh filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `nominal`| 2020 | copied direct from page 2, table 1 of USS website .pdf of 2020 cashflows and filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   
| `cpi`| 2017, 2020 | derived cpi-basis values from nominal-basis values using USS CPI projections for relevant year (all CPI values in [data/cpi_gilts](https://github.com/SussexUCU/USS/tree/main/data/cpi_gilts 'cpi_gilts') folder and detailed below |   

## `cpi_gilts`
At each valuation USS state their predictions for how CPI will grown in the future. They also state their predictions for returns on government gilts. These seem to be generally inline with Bank of England predictions on the valuation date. All the data on CPI and gilts projections from USS valuations are in the nominal-basis.
| year | source |
|:--|:--| 
| 2008 | copied direct from page 27 of 2018 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2011 | copied direct from page 16 of 2011 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2014 | copied direct from page 13 of 2014 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| 2017 November | copied direct from page 13, table 22 of November 2017 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2017 September | copied direct from page 51, table 16 of September 2017 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| 2018 | copied direct from page 38 of 2018 consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |   
| 2020 | copied direct from page 4, table 2 of USS website .pdf of 2020 cashflows and filed in [docs/cashflows](https://github.com/SussexUCU/USS/tree/main/docs/cashflows 'cashflows') |   

## `discount_rates`

These are rates that future cashflows should be discounted at (on a prudent basis) to calculate the USS quoted 'deficit'. These discount rates are usually an annualised value at a quoted confidence level (between around 65% to 90%) of the projected asset distribution, these asset projections also give the USS 'best-estimates' quoted above. USS generally quote discount rates in multiple documents and the data can be quoted in three ways (i) yearly discount rates in data tables or (ii) formulae for deriving yearly discount rates (iii) single equivalent discount rates (SEDR) over a 50 year period that represent some average of the yearly discount rates. These three methods can have differences in third or higher significant figures. Where possible data are taken from the actual valuations. 

| basis | year | source |
|:--|:--|:--| 
| `nominal`| 2011 |copied direct from page 16, table A.2 of 2011 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations")|   
| `cpi`| 2011 | derived from page 16 of 2011 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations")|   
| `nominal`| 2014 | copied direct from page 13, table A.2 of 2014 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations")|   
| `cpi`| 2014 | derived from page 13, table A.2 of 2014 valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations")|   
| `nominal`| 2017 November |copied direct from page 11, table 7 of 2017 November consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| `cpi`| 2017 November | derived from page 11, table 7 of 2017 November consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| `nominal`| 2017 September | copied direct from page 51, table 16 of 2017 September consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |   
| `cpi`| 2017 September | derived from page 51, table 16 of 2017 September consultation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations")|   
| `nominal`| 2018 |copied direct from page 23 of 2018 valuation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |   
| `cpi`| 2018 | derived from page 23 of 2018 valuation in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |  
| `nominal`| 2019 |derived from page 3 of 2019 interim valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations") |   
| `cpi`| 2019 | copied direct from page 3 of 2019 interim valuation in [docs/actuarial_valuations](https://github.com/SussexUCU/USS/tree/main/docs/actuarial_valuations "valuations")|
| `nominal`| 2020 with UUK cuts |estimated from gilts-basis value on page 13 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs") |   
| `cpi`| 2020 maintaining benefits | estimated from gilts-basis value on page 13 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs") |
| `nominal`| USS proposed 2021 with UUK cuts |estimated from gilts-basis value on page 13 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs") |   
| `cpi`| USS proposed 2021 maintaining benefits | estimated from gilts-basis value on page 13 of the USS document 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs")|



## `ons`

Raw data from [Office for National Statistics](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23  "ONS") (ONS), CPI, is given here with date of download and link to ONS page. Also derived CPI data to account for the way USS historically reported assets (march-march) and investment returns (dec-dec up to 2014 then march-march from 2015). 
| basis | year | source |
|:--|:--|:--| 
| `nominal`| update when MH completes ONS work |[Office for National Statistics](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23  "ONS") |   

## `prudence`

These are the percentage confidence levels between USS annualised 'best-estimates' on returns and the prudently adjusted discount rate used to calculate the Technical Provisions Liabilities. 
| year | source |
|:--|:--|
| 2018-2021| page 9 'Lens 1c: CL allowing for investment outperformance in the recovery planusing USS' FBB return model (Recovery plan 15/18 years for 2020 and 10 years for 2021)' of 'The likely outcome of a 2021 valuation' in [docs/2020_extra_docs](https://github.com/SussexUCU/USS/tree/main/docs/2020_extra_docs  "2020_extra_docs") |
| 2014-2017| page 6 'The 67th percentile confidence level (2014: 65th)' of the TP consultation 2017 in [docs/tp_consultations_related](https://github.com/SussexUCU/USS/tree/main/docs/tp_consultations_related "consultations") |
| 2011| assumed to be inline with 2014 value |
