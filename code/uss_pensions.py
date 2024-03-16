#!/usr/bin/env python
# coding: utf-8

"""A module for loading and transforming USS pensions data from the SussexUCU USS GitHub site.

It loads data from the ../data directory, of three kinds

- Asset values and returns
- Discount rates from valuations since 2011
- ONS data on CPI index and annual rate.
"""


import os
import numpy as np
import scipy.stats as sta
import csv

# ### General helper functions

def prod_by_sum_of_logs(y, x):
    """Perform a cumulative product of a set of annual growth factors recorded at arbitrary interbals. """
    res = np.ones_like(x)
    dy = np.diff(y, prepend=y[0]-1)
    res = np.exp(np.cumsum(np.log(x) * dy))
    return res

def log_interp(z, x, y):
    """Log interpolator - useful for asset values, or other quantities which grow exponentially."""
    logy = np.log10(y)
    return np.power(10.0, np.interp(z, x, logy, left=np.nan, right=np.nan))

def growth_function(y, a, A0):
    """An exponential function for fits to asset growth. Returns A0*np.exp(a*(y-BASE_YEAR)),"""
    return A0*np.exp(a*(y-BASE_YEAR))

def get_annualised_growth_rate(data, years=30):
    return sta.gmean(1 + data[0:years,1]) - 1

def dec_year_to_y_m(y):
    """Converts a year as a decimnal to a pair of integers year, month"""
    year = int(y)
    month =int( np.round((y - year)*12) + 1)
    return [year, month]

def write_csv(fn, field, array):
    """Write an array of decimal year, data value to a csv file fn. """
    fields = ['Year', 'Month', field]
    with open(fn, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(fields) 

        for arow in array:
            row = dec_year_to_y_m(arow[0]) +  [arow[1]]
            csvwriter.writerow(row) 
    
    print("Array of " + field + " written to file " + fn)
    return

# Relative paths for data
path_base = '../data/'
path_assets = path_base + 'assets_returns/'
path_cpi = path_base + 'cpi_gilts/'
path_discount = path_base + 'discount_rates/'
path_ons = path_base + 'ons/'
path_best_est = path_base + 'best_estimates/'

# Default base year for CPI adjustment.Fraction 1/4 means Apeil 1st.
BASE_YEAR = 2023.25

to_approx_index_day = 1/24
decimal_year_by_month = {
                'JAN' : 0/12 + to_approx_index_day,
                'FEB' : 1/12 + to_approx_index_day,
                'MAR' : 2/12 + to_approx_index_day,
                'APR' : 3/12 + to_approx_index_day,
                'MAY' : 4/12 + to_approx_index_day,
                'JUN' : 5/12 + to_approx_index_day,
                'JUL' : 6/12 + to_approx_index_day,
                'AUG' : 7/12 + to_approx_index_day,
                'SEP' : 8/12 + to_approx_index_day,
                'OCT' : 9/12 + to_approx_index_day, 
                'NOV' : 10/12 + to_approx_index_day,
                'DEC' : 11/12 + to_approx_index_day
                }

decimal_year_by_quarter = {'Q1' : 0/4,
                           'Q2' : 1/4,
                           'Q3' : 2/4,
                           'Q4' : 3/4
                           }

# Historic CPI annual rates and index, from ONS.

def get_ons_data(path_ons, filename, freq="monthly"):
    """
    Loads csv file containing ONS data from path_ons/filename, and returns 
    shape (N,2) array of Year and Value at freq given by annually, quarterly, or monthly.
    """
    
    ons_raw = np.genfromtxt(path_ons + filename, delimiter=',', dtype=str, skip_header=8)
    ons_raw = np.char.strip(ons_raw,'"')
    
    ons = []
    
    if freq == "monthly":
        for entry, cpi in ons_raw:
            data = entry.split()
            if len(data) > 1:
                if data[1] in decimal_year_by_month:
                    epoch = float(data[0]) + decimal_year_by_month[data[1]]
                    ons.append([epoch, float(cpi)])
    elif freq == "quarterly":
        for entry, cpi in ons_raw:
            data = entry.split()
            if len(data) > 1:
                if data[1] in decimal_year_by_quarter:
                    epoch = float(data[0]) + decimal_year_by_month[data[1]]
                    ons.append([epoch, float(cpi)])
    elif freq == "annually":
        for entry, cpi in ons_raw:
            data = entry.split()
            if len(data) == 1:
                epoch = float(data[0]) 
                ons.append([epoch, float(cpi)])
    else:
        raise ValueError("Frequency must be 'monthly', quarterly', 'annually'")
    
    return np.array(ons)


print("ONS data loading:")
cpi_annual_monthly_ons = get_ons_data(path_ons, 'ons_cpi_annual_series.csv')
cpi_annual_monthly_ons[:,1] *= 0.01
print("Annual CPI change, monthly, as array             cpi_annual_monthly_ons, last entry {}".format(cpi_annual_monthly_ons[-1,:]))
cpi_annual_annually_ons = get_ons_data(path_ons, 'ons_cpi_annual_series.csv', "annually")
cpi_annual_annually_ons[:,1] *= 0.01
print("Annual CPI change, annually, as array            cpi_annual_annually_ons")
cpi_annual_jan_jan_ons = cpi_annual_monthly_ons[0::12,:]
print("Annual CPI change, annually Jan-Jan, as array    cpi_annual_jan_jan_ons")


cpi_index_monthly_ons = get_ons_data(path_ons, 'ons_cpi_index_series.csv')
cpi_index_monthly_ons[:,1] *= 0.01
print("Annual CPI index (2015=1.00), monthly, as array  cpi_index_monthly_ons, last entry {}".format(cpi_index_monthly_ons[-1,:]))
print()

# ### CPI helper functions

def cum_cpi_ons(base_yr=BASE_YEAR, cpi_ons=cpi_annual_jan_jan_ons):
    """
    Calculates cumulative CPI index from ONS data, relative to a base year, 
    which defaults to the value specified above in BASE_YEAR. Default is to use 
    Jan-Jan data, which seems to agree with ONS CPI index.
    
    Returns an array of two columns, year and value.
    """
    base_yr_ind = np.where(cpi_ons[:, 0] == base_yr)[0][0]
    cum_cpi = cpi_ons.copy()
    cum_cpi[base_yr_ind,1] = 1.0
    cum_cpi[base_yr_ind+1:, 1] = np.cumprod(1 + cpi_ons[base_yr_ind:-1, 1])
    cum_cpi[base_yr_ind-1::-1, 1] = np.cumprod(1/(1 + cpi_ons[base_yr_ind:0:-1, 1]))

    return cum_cpi


def get_cpi_ons(y, cpi_ons=cpi_annual_monthly_ons):
    """
    Returns ONS annual CPI in year y, by linear interpolation.
    y can be single number, array, or range.
    
    Returns values with the same shape as y. 
    Years outside the ONS data return a nan.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    cpi_arr = np.ones((len_y, 2))
    cpi_arr[:,0] = y
    cpi_arr[:,1] = np.interp(y, cpi_ons[:,0], cpi_ons[:,1], left=np.nan, right=np.nan)
    return cpi_arr


def get_cum_cpi_ons(y, base_year=BASE_YEAR):
    """
    Gets ONS cumulative CPI in year y relative to base_year. Fractions of year by geometric interpolation,. 
    y can be single number, array, or range.
    
    Returns two columns, [years, value], with the same years as y. 
    Years outside the ONS data return a nan.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    cum_cpi_arr = np.ones((len_y, 2))
    cum_cpi_arr[:,0] = y
    cum_cpi_ons_arr = cum_cpi_ons(base_year)
    cum_cpi_arr[:,1] = log_interp(y, cum_cpi_ons_arr[:, 0], cum_cpi_ons_arr[:, 1])
    return cum_cpi_arr

def get_cpi_index_ons(y, base_year=BASE_YEAR):
    """
    Gets ONS CPI index in year y relative to base_year. Fractions of year by geometric interpolation,
    between monthly ONS data.
    y can be single number, array, or range.
    
    Returns two columns, [years, value], with the same years as y. 
    Years outside the ONS data return a nan.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    cpi_index_arr = np.ones((len_y, 2))
    cpi_index_arr[:,0] = y
    cpi_index_base_year = log_interp(base_year, cpi_index_monthly_ons[:, 0], cpi_index_monthly_ons[:, 1])
    cpi_index_arr[:,1] = log_interp(y, cpi_index_monthly_ons[:, 0], cpi_index_monthly_ons[:, 1])/cpi_index_base_year
    return cpi_index_arr

def get_cpi_adjusted(a, base_year=BASE_YEAR):
    """Returns CPI-adjusted version of array, relative to base_year."""
    a_adj = a.copy()
    cpi_index = get_cpi_index_ons(a[:,0], base_year)
    a_adj[:,1] /= cpi_index[:,1]
    return a_adj

# Historic USS assets and investment growth

def get_uss_assets_data(path_assets, filename):
    """Loads USS assets data."""
    data_in = np.genfromtxt(path_assets + filename, delimiter=',', usecols=(0,1,2), skip_header=1, dtype=float)
    in_shape = data_in.shape 
    data = np.zeros((in_shape[0], 2))
    # Second column is month, turn into decimal year
    data[:,0] = data_in[:,0] + (data_in[:,1]-1)/12
    data[:,1] = data_in[:,2]
    return data

print("USS historic assets and investment growth data loading:")
# assets_nom = np.genfromtxt(path_assets + 'nominal/1992_2021_raw_assets_nominal.csv', delimiter=',', usecols=(0,1,2), skip_header=1, dtype=float)
assets_nom = get_uss_assets_data(path_assets, 'nominal/1992_todate_raw_assets_nominal.csv')
print("Assets (nominal, B GBP) from annual report       assets_nom")
# inv_ret_nom = np.genfromtxt(path_assets + 'nominal/1987_2021_raw_investment_returns_nominal.csv', delimiter=',', usecols=(0,1,2), skip_header=1, dtype=float)
inv_ret_nom = get_uss_assets_data(path_assets, 'nominal/1987_todate_raw_investment_returns_nominal.csv')
print("Investment returns (nominal basis)               inv_ret_nom")


# ## Assets and investment return helper functions
def get_inv_ret_nom(y, base_yr=BASE_YEAR, inv_ret_arr=inv_ret_nom):
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    inv_ret = np.ones((len_y,2))
    inv_ret[:,0] = y
    inv_ret[:,1] = log_interp(y, inv_ret_arr[:, 0], ( 1 + inv_ret_arr[:, 1]) ) - 1
    return inv_ret


def cum_inv_ret_nom(inv_ret=inv_ret_nom):
    """
    Calculate cumulative investment returns, from  
    nominal investment returns.
    
    Returns an array of two columns, year and value.
    """

    cum_inv_ret = inv_ret.copy()
    cum_inv_ret[:,1] = prod_by_sum_of_logs(inv_ret[:,0], 1 + inv_ret[:,1])

    return cum_inv_ret 


def get_cum_inv_ret_nom(y, base_yr=BASE_YEAR):
    """
    Get cumulatuve investment returns for any set of years y, with linear interpolation 
    for fractional years.
    
    Returns two columns, [years, value], with the same years as y. 
    Years outside the ONS CPI data return a nan.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    cum_inv_ret = np.ones((len_y,2))
    cum_inv_ret[:,0] = y
    cum_inv_ret_arr = cum_inv_ret_nom()
    cum_inv_ret_base_year = log_interp(base_yr, cum_inv_ret_arr[:, 0], cum_inv_ret_arr[:, 1])
    cum_inv_ret[:,1] = log_interp(y, cum_inv_ret_arr[:, 0], 
                     cum_inv_ret_arr[:, 1]) * get_assets_nom_reported(base_yr)[0,1]/cum_inv_ret_base_year
    
    return cum_inv_ret 


def get_assets_nom_reported(y, base_year=BASE_YEAR):
    """
    Get value of assets (nominal) reported in USS annual statements for set of years y, 
    log interpolating. 
    
    Returns a two-column array of years y and values.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    assets = np.ones((len_y, 2))
    assets[:,0] = y
    assets[:,1] = log_interp(y, assets_nom[:, 0], assets_nom[:, 1])
    return assets


def get_assets_cpi_reported(y, base_year=BASE_YEAR):
    """
    Get value of assets reported in USS annual statements for set of years y.
    
    Returns a two-column array of years y and values.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    assets_cpi_all = assets_nom.copy()
    assets_cpi_all[:,1] = assets_nom[:,1]/ (get_cpi_index_ons(assets_nom[:,0], base_year)[:,1])
    assets_cpi = np.ones((len_y, 2))
    assets_cpi[:,0] = y
    assets_cpi[:,1] = log_interp(y, assets_cpi_all[:, 0], assets_cpi_all[:, 1])
    return assets_cpi



print("Estimating USS assets from investment returns, normalised to nominal assets in year {}:".format(BASE_YEAR))
# print("assets_cpi_inv_ret_2020 = get_assets_cpi_inv_ret(assets_nom[:,0])")
# assets_cpi_inv_ret_2020 = get_assets_cpi_inv_ret(assets_nom[:,0])
cum_inv_ret_nom = get_cum_inv_ret_nom(inv_ret_nom[:,0])
print("Stored in array:                                ", "cum_inv_ret_nom")

def assets_nominal_to_cpi(base_year=BASE_YEAR):
    print("Converting reported assets and estimated assets to CPI basis, base year {}:".format(base_year))
    assets_reported_cpi = get_cpi_adjusted(assets_nom, base_year)
    assets_inv_ret_cpi = get_cpi_adjusted(cum_inv_ret_nom, base_year)
    print("Reported assets CPI stored in array:           ", "assets_reported_cpi")
    print("Estimated assets CPI stored in array:           ", "assets_inv_ret_cpi")
    print("*** Note 1: assets are estimated using investment returns, \
            with reported assets at {} as the basis".format(base_year))
    print("*** Note 2: they are estimated at end March by geometric interpolation of end Dec values.")
    print()
    return assets_reported_cpi, assets_inv_ret_cpi

# Future discount rates, assume column 0 is year, column 1 is term, column 2 is discount rate
# Should really compute from term to be derived more directly from data
# Should really load from original data in nominal, and compute from USS projected CPI

valuation_list = ['2011', '2014', 
                  '2017a', '2017b', 
                  '2018', '2019', 
                  '2020a', '2020b', 
                  '2021a', '2021b', 
                  '2022a', '2022b', '2022c', '2022d', '2022e', '2022f',
                  '2023']

disc_prud_filename_list = [
        '2011_DISCOUNT_RATE_cpi_basis.csv',
        '2014_DISCOUNT_RATE_cpi_basis.csv',
        '2017_September_DISCOUNT_RATE_cpi_basis.csv',
        '2017_November_DISCOUNT_RATE_cpi_basis.csv',
        '2018_DISCOUNT_RATE_cpi_basis.csv', 
        '2019_DISCOUNT_RATE_interim_cpi_basis.csv',
        '2020_DISCOUNT_RATE_maintain_benefits_cpi_basis.csv',
        '2020_DISCOUNT_RATE_UUK_cuts_cpi_basis.csv',
        '2021_DISCOUNT_RATE_USS_est_maintain_benefits_cpi_basis.csv',
        '2021_DISCOUNT_RATE_USS_est_UUK_cuts_cpi_basis.csv',
        '2022_DISCOUNT_RATE_maintain_benefits_cpi_basis.csv',
        '2022_DISCOUNT_RATE_USS_est_UUK_cuts_cpi_basis.csv',
        '2022_JUNE_DISCOUNT_RATE_maintain_benefits_cpi_basis.csv',
        '2022_JUNE_DISCOUNT_RATE_USS_est_UUK_cuts_cpi_basis.csv', 
        '2022_SEPT_DISCOUNT_RATE_maintain_benefits_cpi_basis.csv',
        '2022_SEPT_DISCOUNT_RATE_USS_est_UUK_cuts_cpi_basis.csv',
        '2023_DISCOUNT_RATE_restore_benefits_cpi_basis.csv'
        ]

best_est_list = ['2017', '2018', '2020', '2020 FMP', '2021', '2021 FMP', 
                 '2022 FMP', '2022 JUN FMP', '2022 SEP FMP']

disc_best_filename_list = [
        '2017_November_BEST_EST_cpi_basis.csv',
        '2018_BEST_EST_cpi.csv', 
        '2020_BEST_EST_cpi.csv',
        '2020_FMP_FBB_30yr_pre_ret_best_est_CPI.csv',
        '2021_BEST_EST_cpi.csv',
        '2021_FMP_FBB_30yr_pre_ret_best_est_CPI.csv',
        '2022_FMP_FBB_30yr_pre_ret_best_est_CPI.csv',
        '2022_JUNE_FMP_FBB_30yr_pre_ret_best_est_CPI.csv',
        '2022_SEPT_FMP_FBB_30yr_pre_ret_best_est_CPI.csv'
    ]

disc_prud_filename_dict = dict(zip(valuation_list, disc_prud_filename_list))
disc_best_filename_dict = dict(zip(best_est_list, disc_best_filename_list))

def get_disc_data(path, disc_filename_dict=disc_prud_filename_dict, cols=(0,2), basis='cpi'):
    sep = ""
    if basis[-1] != os.sep:
        sep = os.sep
    disc_rate_dict = {}
    for val in disc_filename_dict:
        filename = path + basis + sep + disc_filename_dict[val]
        try:
            disc_rate_array = np.genfromtxt(filename, delimiter=',', usecols=cols, skip_header=1)
            disc_rate_dict[val] = disc_rate_array
        except:
            pass
    return disc_rate_dict
    
print("USS discount rates data loading:")
disc_prud_cpi_dict = get_disc_data(path_discount, disc_prud_filename_dict)
print("Prudent discount rates as dictionary             disc_prud_cpi_dict")
disc_best_cpi_dict = get_disc_data(path_best_est, disc_best_filename_dict)
print("Best estimate discount rates as dictionary       disc_best_cpi_dict")
print()


# ## Discount rate helper functions

def cum_disc_uss_cpi(valuation, disc_dict=disc_prud_cpi_dict):
    """
    Calculates cumulative discounts forward from a given valuation date, 
    using USS data. Data is input using a dictionary, with year as key, 
    and 2-column arrays (year, value) as values. Default is prudent discount 
    rate data. 
    Allowed values for valuation are in 'valuation_list' variable.
        
    Returns an array of two columns, year and value.
    """
    disc = disc_dict[valuation]
    cum_disc = disc.copy()
    cum_disc[:, 1] = np.cumprod(1/(1 + disc[:, 1]))
    return cum_disc

def get_cum_disc_uss_cpi(y, valuation, disc_dict=disc_prud_cpi_dict):
    """
    Get USS cumulative discounts in year y, by geometric interpolation, relative to year of valuation.
    y can be single number, array, or range.
    
    Returns two columns, [years, value], with the same years as y. 
    Years outside the ONS data return a nan.
    """
    if hasattr(y, '__iter__'):
        len_y = len(y)
    else:
        len_y = 1
    cum_disc = np.ones((len_y,2))
    cum_disc[:,0] = y
    disc_arr = cum_disc_uss_cpi(valuation, disc_dict)
    cum_disc[:,1] = log_interp(y, disc_arr[:, 0], disc_arr[:, 1])

    return cum_disc


# Finally do the conversion of assets from nominal to CPI basis
assets_reported_cpi, assets_inv_ret_cpi = assets_nominal_to_cpi()