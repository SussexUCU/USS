# Notes on investment returns 

Notes accompanying files in `data/assets_returns/nominal` folder above. 

Montly assets and investment returns are reported at end of month, the data give each month an integer where 31 December is month 1 of the next year and 31 March is month 4 of the same year.

## note 1

There is a problem in the reporting of investment returns in that: 
- Accounts 1996-2013 report investment returns from end of December to December. See p26 2013 report and accounts 'Investment performance shown below is on a calendar year rather than financial year basis.'

- Accounts 2014 and 2015 report investment returns for end of March to March and end of December to December. See page 28 in report and accounts 2014 and page 30 report and accounts 2015.

- Accounts 2016 onwards report investment returns March to March 

In all files the end of December to December is denoted by month 1 and the end of March to March is denoted by month 4.

File 'raw' has two entries for each year 2014 and 2015, one for month 1 and one for month 4. 

File 'derived2015' has only one entry for 2014 (month 1) and one entry for 2015 (month 4) where to account for the change over in reporting the following adjustment is made to the 2015 investment return. 

Using accounts 2015 which report
- December to December 15.1%
- March to March 17.9%

Calculate investment returns from December 2014 to March 2015 as follows: 

1. take monthly from both sets by raising to power 1/12. 
Dec-Dec monthly 1.3817%
Mar-Mar montly 1.1788%

2. average these monthly return from Dec-Dec and Mar-Mar
1.2803%

3. Raise to to the power of 15 to give 2015 investment return of 21.0240%


## note 2

The 1996 report and accounts is the earliest available document, but it is possible to get earlier information on assets and investment returns. 

The 1996 accounts reports page 14 'The 10 year return for the fund was 13.2% per annum, just ahead of the average fund and, again, well ahead of growth in average earnings of 6.5% and retail prices of 4.6% over the same period.'

The 1996 accounts reports page 14 an 18.4% return for 1996
  
Using the annualised figure of 13.2% and the 1996 figure of 18.4% the previous 9 years would average 12.6%
