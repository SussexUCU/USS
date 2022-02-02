# Calculations of break even discount rates

These are the annualised rates of return of assets that would mean the scheme was fully (100%) funded. That is no deficit and no surplus as per USS definition of TP deficit and surplus. 

The values are in the .csv files linked above. 

Update February 2022

Attempt to calculate breakeven discount rates from the latest asset data. 

[Oct2021 estimation of breakeven discount rate](https://docs.google.com/spreadsheets/d/1Ym-QQj-l7lQt-eB734xuIABlSj2U7SLdfKU3Tjns-vY/edit#gid=157077178 "Oct2021") October 2021 estimation of breakeven discount rate


The calculations are in the Excel files linked above, which are copies of the google sheets linked below. 

[2021 calculation of breakeven discount rate](https://docs.google.com/spreadsheets/d/1hZUzScgtPOYlRoO7J7Yh8vpqjIsuqporQZomzBa3iRE/edit?usp=sharing "2021")

[2020 calculation of breakeven discount rate](https://docs.google.com/spreadsheets/d/1fKTwYUSWamdtAaUD65phWHKObs0Y3LKz25dugHrc0uM/edit?usp=sharing "2020")

[2018 calculation of breakeven discount rate](https://docs.google.com/spreadsheets/d/1HO5uHGFvljiC0xaLOi0VlLLDguH2N9dxh4ay9H762yM/edit?usp=sharing "2018")

[2017 calculation of breakeven discount rate](https://docs.google.com/spreadsheets/d/1F1BMRor-MNPVJrTX5SvwxUEHSkik16YlLEQhj3FNGwM/edit?usp=sharing "2017")

[2014 calculation of estimation of breakeven discount rate](https://docs.google.com/spreadsheets/d/14MY_lWTzAlc4yrZqex7VwGi1X1QzpzvsIPR5hIRJ7QM/edit?usp=sharing "2014")

[2011 calculation of estimation of breakeven discount rate](https://docs.google.com/spreadsheets/d/10I2StPVmcJx51Zt6iZ5sjch3sbhd98U1BHgc0Hz4Pig/edit?usp=sharing "2011")



The calculation method is roughly as follows.

## Method for calculating 2017 and 2020

Use cashflows for 2017 and 2020 (both provided by USS) and the USS provided discount rates to calculate the TP Liabilites and check they agree within 1% of the USS calculated TP Liabilities. Then use the same calculation to find the discount rate percentage that produces the smallest surplus possible. 

## Method for deriving 2018 and 2021

Use the cashflows for 2017 and 2020 (both provided by USS) but add the 1-year projected cashflows which are also given (USS use these to calculate the Future Service Costs). However there is a problem in that the first year of cashflows includes DB pension paymenst plus lumpsumps and disability/death in service. So some unknown fraction of the first year of payments will have been paid during 2017 and 2020 respectively. To estimate this fraction we find the proportion of y1 cashflows that reproduce the USS calcluated TP Liabiliites within 1%. Then use this same calculation to find a discount rate percentage that produces the smallest surplus possible. 

## Method for estimating 2011 and 2014

USS does not supply cashflows for 2011 or 2014, but if we assume the same profile of the cashflows as for 2017 then we can apply a factor to each term of cashflows to reproduce the TP Liabiliites quoted by USS. Once we have this factor we then use this same calculation to find a discount rate percentage that produces the smallest surplus possible. 
