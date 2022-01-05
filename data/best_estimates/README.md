# Calculations of breakeven rates

Here are links to google sheets for calculations of breakeven discount rates for 2017, 2018, 2020, and 2021. Results are then quoted in the .csv files linked above. 
(JG: I will eventually upload these as Excel files to this folder, but only once the calcs have had final check.)

[2021 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/1hZUzScgtPOYlRoO7J7Yh8vpqjIsuqporQZomzBa3iRE/edit?usp=sharing "2021")

[2020 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/1fKTwYUSWamdtAaUD65phWHKObs0Y3LKz25dugHrc0uM/edit?usp=sharing "2020")

[2018 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/1HO5uHGFvljiC0xaLOi0VlLLDguH2N9dxh4ay9H762yM/edit?usp=sharing "2018")

[2017 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/1F1BMRor-MNPVJrTX5SvwxUEHSkik16YlLEQhj3FNGwM/edit?usp=sharing "2017")

[2014 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/14MY_lWTzAlc4yrZqex7VwGi1X1QzpzvsIPR5hIRJ7QM/edit?usp=sharing "2014")

[2011 breakeven discount rate calculation](https://docs.google.com/spreadsheets/d/10I2StPVmcJx51Zt6iZ5sjch3sbhd98U1BHgc0Hz4Pig/edit?usp=sharing "2011")


The calculation method is roughly as follows and agrees with the Excel IRR function.

## Method for calculating 2017 and 2020

Use cashflows for 2017 and 2020 (both provided by USS) and the USS provided discount rates to calculate the TP Liabilites and check they agree within 1% of the USS calculated TP Liabilities. Then use the same calculation to find the discount rate percentage that produces the smallest surplus possible. 

## Method for deriving 2018 and 2021

Use the cashflows for 2017 and 2020 (both provided by USS) but add the 1-year projected cashflows which are also given (USS use these to calculate the Future Service Costs). However there is a problem in that the first year of cashflows includes DB pension paymenst plus lumpsumps and disability/death in service. So some unknown fraction of the first year of payments will have been paid during 2017 and 2020 respectively. To estimate this fraction we find the proportion of y1 cashflows that reproduce the USS calcluated TP Liabiliites within 1%. Then use this same calculation to find a discount rate percentage that produces the smallest surplus possible. 

## Method for estimating 2011 and 2014

USS does not supply cashflows for 2011 or 2014, but if we assume the same profile of the cashflows as for 2017 then we can apply a factor to each term of cashflows to reproduce the TP Liabiliites quoted by USS. Once we have this factor we then use this same calculation to find a discount rate percentage that produces the smallest surplus possible. 
