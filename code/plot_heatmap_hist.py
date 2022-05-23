#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 17:29:51 2022

Code to plot histograms of pension cuts post 2022, using UUK Heatmap data and 
USS modeller data (read in from CSV files)

USS_HeatMap_2020_CSV_adapted.csv
uss_scraper_output_heatmap.csv
uss_scraper_output_heatmap_65.5.csv

available on sussexucu_github

Outputs:
- PDF files with histograms
- .csv files with computed cuts
- .csv file with summary statistics
    
@author: hindmars
"""


import numpy as np
import matplotlib as mpl
# import matplotlib.pyplot as plt
import pandas as pd

#%%
# Load UUK heatmap data

heatmap_fname = '../data/heatmap_membership2020/USS_HeatMap_2020_CSV_adapted.csv'
heatmap_df = (pd.read_csv(heatmap_fname)).fillna(0)

# Unpick columned column/row label
heatmap_df.rename(columns={'Midpoint age / salary':'age'}, inplace=True)
heatmap_df = heatmap_df.set_index('age')

#%%
# Load scraped pensions data. First has age 67.5, which is confusing, and should be replaced.

pension_fname = '../data/heatmap_membership2020/uss_scraper_output_heatmap.csv'
pension_655_fname = '../data/heatmap_membership2020/uss_scraper_output_heatmap_65.5.csv'

pension_df = pd.read_csv(pension_fname)
pension_df = pension_df.drop(pension_df[pension_df['dob'] == 1954].index)

# Do replacement with 65.5 data
pension_655_df = pd.read_csv(pension_655_fname)
pension_df = pd.concat([pension_df, pension_655_df])

pension_df["age"] = 2021.5 - pension_df["dob"]
# print(pension_df[['dob', 'age', 'new_pension_pa', 'new_pension_20yr_pa']])

print("Pension data loaded") 

# Now define the data for the USS personas Aria, Bryn and Chloe
personas_list = [["Aria", 37, 30000],  ["Bryn", 43, 50000],  ["Chloe", 51, 70000]]

salary_bins = [32500, 52500, 72500]
age_bins = [37.5, 42.5, 52.5]

personas_df = pd.DataFrame(personas_list, columns=["name", "age", "salary"]).set_index("name")

personas_df['salary_bin'] = salary_bins
personas_df['age_bin'] = age_bins

#%%
# Now find percentage cut to total received between ages 66 and 86. 
# Check differences between linear change and geometric change.

n_years = 20

print("Peforming linear and geometric sums for total pension")

pension_df['old_pension_total'] = pension_df['old_pension_pa']*n_years
pension_df['new_pension_total_linear'] = (pension_df['new_pension_pa'] 
                                          + pension_df['new_pension_20yr_pa'])*n_years/2
r = (pension_df['new_pension_20yr_pa']/pension_df['new_pension_pa'])**(1/(n_years-1))
pension_df['new_pension_total_geomet'] = pension_df['new_pension_pa']*(1 - r**n_years )/(1-r)


geom_lin_diff = pension_df['new_pension_total_geomet'] - pension_df['new_pension_total_linear']
rel_diff = geom_lin_diff/pension_df['new_pension_total_linear']

print("Maximum relative difference (new pensions)", max(rel_diff))

#%%

print("Calculating percentage loss under new pension")

pension_df['loss_percent'] = 100*(pension_df['old_pension_total'] - \
    pension_df['new_pension_total_linear'])/pension_df['old_pension_total']

# print(pension_df['loss_percent'])

print("Minimem loss %", min(pension_df['loss_percent']))
print("Maximem loss %", max(pension_df['loss_percent']))

print("Calculating pounds loss under new pension")

pension_df['loss_pounds'] = (pension_df['old_pension_total'] - \
    pension_df['new_pension_total_linear'])

print("Minimem loss GBP", min(pension_df['loss_pounds']))
print("Maximem loss GBP", max(pension_df['loss_pounds']))

#%%
# Now put heatmap numbers into scraper data
# There must be a more pandas-like way to do this

pension_df['number'] = 0

for i, rowdata in pension_df.iterrows():
    age = rowdata['age']
    salary = rowdata['salary'].astype(int)
    number = heatmap_df.loc[str(age), str(salary)]
    getit = np.logical_and(pension_df['age']==age, pension_df['salary']==salary)
    pension_df.loc[getit,'number'] = int(number)
    
# print(pension_df[['age', 'salary', 'number']])
#%%
# Binning the data
print("Binning the data")
gbp_bin_edges = np.linspace(0, 350000, 8)
gbp_bin_labels = [ '{:}-{:}k'.format(int(l)//1000,int(r)//1000) 
                  for l, r in zip(gbp_bin_edges[:-1], gbp_bin_edges[1:])]

pc_bin_edges = np.linspace(0,50,11)
pc_bin_labels = [ '{:}-{:}%'.format(int(l),int(r)) 
                 for l, r in zip(pc_bin_edges[:-1], pc_bin_edges[1:])]

salary_bin_edges = np.append(np.linspace(0,80000,5,dtype=int), np.inf)
salary_bin_labels = [ '{:}-{:}k'.format((int(l)//1000),(int(r)//1000)) 
                     for l, r in zip(salary_bin_edges[:-2], salary_bin_edges[1:-1])]
salary_bin_labels.append('80k+')
  
age_bin_edges = np.linspace(20,70,6,dtype=int)
age_bin_labels = [ '{:}-{:}'.format(int(l),int(r)) 
                  for l, r in zip(age_bin_edges[:-1], age_bin_edges[1:])]
# age_bin_labels.append('65+')

pension_df_cpi25 = pension_df[pension_df['inflation']==0.025].copy()
pension_df_cpi28 = pension_df[pension_df['inflation']==0.028].copy()
pension_df_cpi30 = pension_df[pension_df['inflation']==0.030].copy()

df_by_cpi_list = [pension_df_cpi25, pension_df_cpi28, pension_df_cpi30]
cpi_list = [25,28,30]

def bin_and_remove_zeros(df_by):
    df_by["binned_by_pc_loss"] = pd.cut(df_by['loss_percent'], 
                                        bins=pc_bin_edges, right=False, labels=pc_bin_labels)
    df_by["binned_by_pounds_loss"] = pd.cut(df_by['loss_pounds'], 
                                        bins=gbp_bin_edges, right=False, labels=gbp_bin_labels)
    df_by["binned_by_salary"] = pd.cut(df_by['salary'], 
                                       bins=salary_bin_edges, right=False, labels=salary_bin_labels)
    df_by["binned_by_age"] = pd.cut(df_by['age'], 
                                               bins=age_bin_edges, right=False, labels=age_bin_labels)
    nos_by_pcloss_salary = df_by.groupby([df_by["binned_by_pc_loss"], 
                                          df_by["binned_by_pounds_loss"], 
                                          df_by["binned_by_salary"], 
                                          df_by["binned_by_age"], 
                                          df_by["inflation"]])['number'].sum().reset_index()

    return nos_by_pcloss_salary[nos_by_pcloss_salary['number'] > 0]

non_zero_nos_df_list = []

for df_by_cpi, cpi in zip(df_by_cpi_list, cpi_list):
    non_zero_nos_df = bin_and_remove_zeros(df_by_cpi)
    non_zero_nos_df_list.append(non_zero_nos_df)

non_zero_nos_29_43_df_list = []
for df, cpi in zip(df_by_cpi_list, cpi_list):
    df_29_42 = df[np.logical_and(df["salary"] > 33309, df["salary"] < 50296)]
    non_zero_nos_df = bin_and_remove_zeros(df_29_42)
    non_zero_nos_29_43_df_list.append(non_zero_nos_df)

#%%
# Now for salaries under 40k
salary_thresh = 40000

pension_df_under40k = pension_df[pension_df['salary'] < salary_thresh].copy()

pension_df_under40k['binned_by_pc_loss'] = pd.cut(pension_df_under40k['loss_percent'], 
                                               bins=pc_bin_edges, right=False, labels=pc_bin_labels)
pension_df_under40k['inflation'] *= 100
pension_df_under40k['inflation'] = pension_df_under40k['inflation'].round(1)

pension_df_under40k_binned = bin_and_remove_zeros(pension_df_under40k.copy())

pension_df_under40k_binned_grouped = pension_df_under40k_binned.groupby(['binned_by_pc_loss','inflation']).sum().unstack()
#%%

# Calculate pension losses for poersonas

personas_df['loss_percent'] = 0
personas_df['loss_pounds'] = 0

for idx in personas_df.index:
    s_bin = personas_df.loc[idx, 'salary_bin']
    a_bin = personas_df.loc[idx, 'age_bin']
    foo = pension_df[np.logical_and(pension_df['salary'] == s_bin, 
                                          pension_df['age'] == a_bin)][['loss_percent', 'loss_pounds', 'inflation']]
    print(idx, foo)

#%%

def total_and_mean_losses(df):
    total_pensioners = df["number"].sum()
    losses_pounds = df["number"] * df["loss_pounds"]
    losses_percent_wt = df["number"] * df["loss_percent"]/total_pensioners
    total_loss_pounds = losses_pounds.sum()
    # losses_pounds_wt = losses_pounds/total_pensioners
    mean_loss_pounds = total_loss_pounds/total_pensioners
    mean_loss_percent = losses_percent_wt.sum()
    return total_loss_pounds, mean_loss_pounds, mean_loss_percent

def quartile_losses(df, key):
    df_sorted = df.sort_values(key)
    df_sorted["cum_number"] = df_sorted["number"].cumsum()
    q_list = np.array([0.25,0.5,0.75])
    loss_quartiles = np.zeros((len(q_list),))
    num_quartiles = df_sorted["cum_number"].max() * q_list
    for n, q in enumerate(q_list):
        idx = np.abs(num_quartiles[n] - df_sorted["cum_number"]).argmin()
        loss_quartiles[n] = df_sorted[key].iloc[idx]

    return loss_quartiles

# Assemble various quantities into a DataFrame

losses_df = pd.DataFrame( [c/10 for c in cpi_list ], columns=["CPI"])

# Total and mean loss

print("Total and mean losses")

total_mean_losses = []
for cpi, df in zip(cpi_list, df_by_cpi_list):
    total_loss_pounds, mean_loss_pounds, mean_loss_percent = total_and_mean_losses(df)
    total_mean_losses.append([total_loss_pounds, mean_loss_pounds, mean_loss_percent])
    
    print("CPI {:.1f}%  Total loss GBP: {:.3}b".format(cpi/10, total_loss_pounds/1e9), 
          "CPI {:.1f}%  Mean loss GBP: {:.1f}k".format(cpi/10, mean_loss_pounds/1e3), 
          "CPI {:.1f}%  Mean loss %: {:.3f}".format(cpi/10, mean_loss_percent) )

tml_df = pd.DataFrame(total_mean_losses, 
                      columns=["Total loss GBP", "Mean loss GBP", "Mean loss %"])

losses_df = losses_df.join(tml_df)

#%%
print("Quartile losses (percent)")

loss_percent_quartiles_list = []
np.set_printoptions(precision=0)
for cpi, df in zip(cpi_list, df_by_cpi_list):
    loss_percent_quartiles = quartile_losses(df, "loss_percent")
    loss_percent_quartiles_list.append(loss_percent_quartiles)
    print("CPI {:.1f}%  Quartile losses %:   ".format(cpi/10), loss_percent_quartiles) 

lpcq_df = pd.DataFrame(loss_percent_quartiles_list, 
                       columns=["% loss Q1", "% loss Q2", "% loss Q3"])

losses_df = losses_df.join(lpcq_df)

#%%
print("Quartile losses (pounds)")

loss_pounds_quartiles_list = []
np.set_printoptions(precision=1)
for cpi, df in zip(cpi_list, df_by_cpi_list):
    loss_pounds_quartiles = quartile_losses(df, "loss_pounds")
    loss_pounds_quartiles_list.append(loss_pounds_quartiles)
    print("CPI {:.1f}%  Quartile losses GBP:   ".format(cpi/10), loss_pounds_quartiles) 

lgbpq_df = pd.DataFrame(loss_pounds_quartiles_list, 
                        columns=["GBP loss Q1", "GBP loss Q2", "GBP loss Q3"])

losses_df = losses_df.join(lgbpq_df)

#%%
# Lecturer A and B pay scale 2021
# 43, 50296
# 42, 48835
# 41, 47419
# 40, 46042
# 39, 44706
# 38, 43434
# 37, 42149
# 36, 40927
# 35, 39739
# 34, 38587
# 33, 37467
# 32, 36382
# 31, 35326
# 30, 34304
# 29, 33309

# Total and mean losses for grades 29-42

print("Grades (29-43) Total and mean losses")

total_mean_losses_29_43 = []
for cpi, df in zip(cpi_list, df_by_cpi_list):
    lect_df = df[np.logical_and(df["salary"] > 33309, df["salary"] < 50296)]
    total_loss_pounds, mean_loss_pounds, mean_loss_percent = total_and_mean_losses(lect_df)
    total_mean_losses_29_43.append([total_loss_pounds, mean_loss_pounds, mean_loss_percent])
    print("CPI {:.1f}%  Total loss GBP: {:.3}b".format(cpi/10, total_loss_pounds/1e9), 
          "Mean loss GBP: {:.1f}k".format(mean_loss_pounds/1e3), 
          "Mean loss %: {:.3f}".format(mean_loss_percent),
           "Total number (29-43): {:}".format(lect_df["number"].sum()))

tml_29_43_df = pd.DataFrame(total_mean_losses, 
                      columns=["Total loss grades 29-43 GBP", "Mean loss grades 29-43 GBP", "Mean loss grades 29-43 %"])

losses_df = losses_df.join(tml_29_43_df)
#%%
print("Grades (29-43) quartile losses")

loss_percent_quartiles_29_43_list = []

for cpi, df in zip(cpi_list, df_by_cpi_list):
    lect_df = df[np.logical_and(df["salary"] > 33309, df["salary"] < 50296)]
    loss_percent_quartiles = quartile_losses(lect_df, "loss_percent")
    loss_percent_quartiles_29_43_list.append(loss_percent_quartiles)
    # print("Quartile losses kGBP:", loss_pounds_quartiles/1e3)
    print("CPI {:.1f}%  Grades (29-43) Quartile losses %:   ".format(cpi/10), loss_percent_quartiles) 


lpcq_29_43_df = pd.DataFrame(loss_percent_quartiles_29_43_list, 
                       columns=["Grades (29-43) % loss Q1", "Grades (29-43) % loss Q2", "Grades (29-43) % loss Q3"])

losses_df = losses_df.join(lpcq_29_43_df)

#%%
print("Grades (29-43) Quartile losses (pounds)")

loss_pounds_quartiles_29_43_list = []

np.set_printoptions(precision=0)
for cpi, df in zip(cpi_list, df_by_cpi_list):
    lect_df = df[np.logical_and(df["salary"] > 33309, df["salary"] < 50296)]
    loss_pounds_quartiles = quartile_losses(lect_df, "loss_pounds")
    loss_pounds_quartiles_29_43_list.append(loss_pounds_quartiles)
    # print("Quartile losses kGBP:", loss_pounds_quartiles/1e3)
    print("CPI {:.1f}%  Grades (29-43) Quartile losses GBP:   ".format(cpi/10), loss_pounds_quartiles) 

lgbpq_29_43_df = pd.DataFrame(loss_percent_quartiles_29_43_list, 
                       columns=["Grades (29-43) GBP loss Q1", "Grades (29-43) GBP loss Q2", "Grades (29-43) GBP loss Q3"])

losses_df = losses_df.join(lgbpq_29_43_df)

#%%
# Total and mean losses for grades under 40s

print("Age under 40: Total and mean losses")

total_mean_losses_age_under_40 = []
for cpi, df in zip(cpi_list, df_by_cpi_list):
    young_df = df[df["age"] < 40]
    total_loss_pounds, mean_loss_pounds, mean_loss_percent = total_and_mean_losses(young_df)
    total_mean_losses_age_under_40.append([total_loss_pounds, mean_loss_pounds, mean_loss_percent])
    print("CPI {:.1f}%  Total loss GBP: {:.3}b".format(cpi/10, total_loss_pounds/1e9), 
          "Mean loss GBP: {:.1f}k".format(mean_loss_pounds/1e3), 
          "Mean loss %: {:.3f}".format(mean_loss_percent),
           "Total number age < 40: {:}".format(young_df["number"].sum()))

tml_age_under_40_df = pd.DataFrame(total_mean_losses_age_under_40, 
                      columns=["Total loss Age < 40 GBP", "Mean loss Age < 40 GBP", "Mean loss Age < 40 %"])

losses_df = losses_df.join(tml_age_under_40_df)
#%%
print("Age < 40 quartile losses")

loss_percent_quartiles_age_under_40_list = []

for cpi, df in zip(cpi_list, df_by_cpi_list):
    young_df = df[df["age"] < 40]
    loss_percent_quartiles = quartile_losses(young_df, "loss_percent")
    loss_percent_quartiles_age_under_40_list.append(loss_percent_quartiles)
    # print("Quartile losses kGBP:", loss_pounds_quartiles/1e3)
    print("CPI {:.1f}%  Age < 40 Quartile losses %:   ".format(cpi/10), loss_percent_quartiles) 


lpcq_age_under_40_df = pd.DataFrame(loss_percent_quartiles_age_under_40_list, 
                       columns=["Age < 40 % loss Q1", "Age < 40 % loss Q2", "Age < 40 % loss Q3"])

losses_df = losses_df.join(lpcq_age_under_40_df)

#%%
print("Age < 40 Quartile losses (pounds)")

loss_pounds_quartiles_age_under_40_list = []

np.set_printoptions(precision=0)
for cpi, df in zip(cpi_list, df_by_cpi_list):
    young_df = df[df["age"] < 40]
    loss_pounds_quartiles = quartile_losses(young_df, "loss_pounds")
    loss_pounds_quartiles_age_under_40_list.append(loss_pounds_quartiles)
    # print("Quartile losses kGBP:", loss_pounds_quartiles/1e3)
    print("CPI {:.1f}%  Age < 40 Quartile losses GBP:   ".format(cpi/10), loss_pounds_quartiles) 

lgbpq_age_under_40_df = pd.DataFrame(loss_percent_quartiles_age_under_40_list, 
                       columns=["Age < 40 GBP loss Q1", "Age < 40 GBP loss Q2", "Age < 40 GBP loss Q3"])

losses_df = losses_df.join(lgbpq_age_under_40_df)

#%%
print("Lecturer age 37 on 40k losses (pounds)")

np.set_printoptions(precision=0)
loss_pounds_37_40k_list = []
loss_percent_37_40k_list = []
losses_37_40k = []
for cpi, df in zip(cpi_list, df_by_cpi_list):
    lect_37_40k_df = df[np.logical_and(df["salary"] >= 37500, df["salary"] <= 47500)]
    lect_37_40k_df = lect_37_40k_df[np.logical_and(lect_37_40k_df["age"] > 37,lect_37_40k_df["age"]<43)]
    weight = lect_37_40k_df["number"]/(lect_37_40k_df["number"].sum())
    loss_pounds_37_40k = (lect_37_40k_df["loss_pounds"] * weight).sum()
    # loss_pounds_37_40k_list.append(loss_pounds_37_40k)
    loss_percent_37_40k = (lect_37_40k_df["loss_percent"] * weight).sum()
    # loss_percent_37_40k_list.append(loss_percent_37_40k)
    losses_37_40k.append([loss_percent_37_40k, loss_pounds_37_40k])
    print("CPI {:.1f}%  Lecturer age 37 on 40k losses GBP: {:.0f}".format(cpi/10,loss_pounds_37_40k) 
        + "   losses %: {:.0f}".format(loss_percent_37_40k) ) 

l_37_40k_df = pd.DataFrame(losses_37_40k, 
                       columns=["Age 37, 40k % loss", "Age 37, 40k GBP loss"])

losses_df = losses_df.join(l_37_40k_df)

#%%

print("Loss in retirement for those earning under 40k")

total_mean_loss_under_40k_list = []
for cpi in cpi_list:
    df = pension_df_under40k[pension_df_under40k['inflation'] == cpi/10]
    a, b, c = total_and_mean_losses(df)
    total_mean_loss_under_40k_list.append([a, b, c])
    print("Total loss GBP: {:.3} b".format(a/1e9), 
          "Mean loss GBP: {:.1f} k".format(b/1e3), 
          "Mean loss %: {:.3f}".format(c) )

tml_under_40k_df = pd.DataFrame(total_mean_losses, 
                      columns=["Total loss grades < 40k bGBP", "Mean loss < 40k GBP", "Mean loss < 40k %"])

losses_df = losses_df.join(tml_under_40k_df)


#%%

print("Earning under 40k quartile losses percent")

loss_percent_quartiles_under40k_list = []
for cpi in cpi_list:
    df = pension_df_under40k[pension_df_under40k['inflation'] == cpi/10]
    loss_percent_quartiles = quartile_losses(df, "loss_percent")
    loss_percent_quartiles_under40k_list.append(loss_percent_quartiles)
    print("CPI {:.1f}%  Under 40k Quartile losses GBP:   ".format(cpi/10), loss_percent_quartiles) 

lpcq_under_40k_df = pd.DataFrame(loss_percent_quartiles_under40k_list, 
                       columns=["Under 40k % loss Q1", "Under 40k % loss Q2", "Under 40k % loss Q3"])

losses_df = losses_df.join(lpcq_under_40k_df)


#%%

print("Earning under 40k quartile losses GBP")

loss_pounds_quartiles_under40k_list = []
for cpi in cpi_list:
    df = pension_df_under40k[pension_df_under40k['inflation'] == cpi/10]
    loss_pounds_quartiles = quartile_losses(df, "loss_pounds")
    loss_pounds_quartiles_under40k_list.append(loss_pounds_quartiles)
    print("CPI {:.1f}%  Under 40k Quartile losses GBP:   ".format(cpi/10), loss_pounds_quartiles) 

lgbpq_under_40k_df = pd.DataFrame(loss_pounds_quartiles_under40k_list, 
                       columns=["Under 40k GBP loss Q1", "Under 40k GBP loss Q2", "Under 40k GBP loss Q3"])

losses_df = losses_df.join(lgbpq_under_40k_df)


#%%
#Now for the plotting 

def colormap_from_rgb_list(cols, A=1.0):
    rgba_cols = []
    for col in cols:
        x = [c/256 for c in col]
        x += [A]
        rgba_cols.append(x)
    
    return mpl.colors.ListedColormap(rgba_cols)

cols = [(1,176,240),
        (1,176,80),
        (255,192,1),
        (192,0,1),
        (0,32,97)
        ]

newcmp = colormap_from_rgb_list(cols)

#%%
# Percentage losses, stacked by salary

xlabel_txt = "Percentage loss in retirement, age 66-86"
ylabel_txt = "Number of active USS members"
suptitle_txt = "Loss in future USS pension value due to UUK cuts 2022"
title_txt = "According to USS modeller, DC taken as annuity, CPI {}%"

for non_zero_nos_df, cpi in zip(non_zero_nos_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pc_loss','binned_by_salary']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True,  
                        xlabel=xlabel_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Salary ("+chr(163)+")", loc="upper left")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger', x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'salary_stack_cpi{cpi:}.pdf')


#%%
# Percentage losses stacked by age

for non_zero_nos_df, cpi in zip(non_zero_nos_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pc_loss','binned_by_age']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True, 
                        xlabel=xlabel_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Age now (yr)", loc="upper left")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger',  x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'age_stack_cpi{cpi:}.pdf')


#%%
# Pounds losses, stacked by salary

xlabel_gbp_txt = "Loss in retirement, age 66-86 [GBP, today's money']"
ylabel_txt = "Number of active USS members"
suptitle_txt = "Loss in future USS pension value due to UUK cuts 2022"
title_txt = "According to USS modeller, DC taken as annuity, CPI {}%"

for non_zero_nos_df, cpi in zip(non_zero_nos_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pounds_loss','binned_by_salary']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True,  
                        xlabel=xlabel_gbp_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Salary ("+chr(163)+")", loc="upper right")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger', x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'gbp_salary_stack_cpi{cpi:}.pdf')


#%%
# Pounds losses stacked by age

for non_zero_nos_df, cpi in zip(non_zero_nos_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pounds_loss','binned_by_age']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True, 
                        xlabel=xlabel_gbp_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Age now (yr)", loc="upper right")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger',  x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'gbp_age_stack_cpi{cpi:}.pdf')#%%

#%%
# Percentage losses, stacked by salary grades 29-43

xlabel_txt = "Percentage loss in retirement, age 66-86"
ylabel_txt = "Number of active USS members"
suptitle_txt = "Loss in future USS pension value due to UUK cuts 2022, gds. 29-43"
title_txt = "According to USS modeller, DC taken as annuity, CPI {}%"

for non_zero_nos_df, cpi in zip(non_zero_nos_29_43_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pc_loss','binned_by_salary']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True,  
                        xlabel=xlabel_txt, ylabel=ylabel_txt, 
                        ylim=(0,40000), colormap=newcmp)
    ax.legend(title=r"Salary ("+chr(163)+")", loc="upper left")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger', x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'salary_stack_29_43_cpi{cpi:}.pdf')
    # ax.annotate("A", (0.5,0.5), xycoords='axes fraction')


#%%
# Percentage losses stacked by age grades 29-43

for non_zero_nos_df, cpi in zip(non_zero_nos_29_43_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pc_loss','binned_by_age']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True, 
                        xlabel=xlabel_txt, ylabel=ylabel_txt, 
                        ylim=(0,40000), colormap=newcmp)
    ax.legend(title=r"Age now (yr)", loc="upper left")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger',  x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'age_stack_29_43_cpi{cpi:}.pdf')


#%%
# Pounds losses, stacked by salary, grades 29-43

xlabel_gbp_txt = "Loss in retirement, age 66-86 [GBP, today's money']"
ylabel_txt = "Number of active USS members"
suptitle_txt = "Loss in future USS pension value due to UUK cuts 2022, grades 29-43"
title_txt = "According to USS modeller, DC taken as annuity, CPI {}%"

for non_zero_nos_df, cpi in zip(non_zero_nos_29_43_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pounds_loss','binned_by_salary']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True,  
                        xlabel=xlabel_gbp_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Salary ("+chr(163)+")", loc="upper right")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger', x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'gbp_salary_stack_29_43_cpi{cpi:}.pdf')


#%%
# Pounds losses stacked by age, grades 29-43

for non_zero_nos_df, cpi in zip(non_zero_nos_29_43_df_list, cpi_list):
    grouped_df = non_zero_nos_df.groupby(['binned_by_pounds_loss','binned_by_age']).sum().unstack()
    ax = grouped_df.plot.bar(y='number', stacked=True, 
                        xlabel=xlabel_gbp_txt, ylabel=ylabel_txt, 
                        ylim=(0,80000), colormap=newcmp)
    ax.legend(title=r"Age now (yr)", loc="upper right")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(which='major', axis='y')
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    ax.grid(which='minor', axis='y', alpha=0.25)
    ax.get_figure().suptitle(suptitle_txt, fontsize='larger',  x=0.55, y=0.93)
    ax.set_title(title_txt.format(cpi/10), fontsize='smaller', x=0.49)
    ax.get_figure().tight_layout()
    ax.get_figure().savefig(f'gbp_age_stack_29_43_cpi{cpi:}.pdf')#%%
#%%
# Now for side-by-side for those under 40k

cols_40k = [(253,217,102),
        (237,125,50),
        (112,48,160)
        ]

newcmp_40k = colormap_from_rgb_list(cols_40k)

suptitle_txt_40k = "Loss in future USS pension value due to UUK cuts 2022 \n Staff with salary under " +chr(163)+ "{}k"
title_txt_40k = "According to USS modeller, DC taken as annuity"

ax_40k = pension_df_under40k_binned_grouped.plot.bar(y='number', 
                    xlabel=xlabel_txt, ylabel=ylabel_txt, 
                    ylim=(0,25000), colormap=newcmp_40k)
ax_40k.legend(title=r"CPI (%)", loc="upper left")
ax_40k.tick_params(axis='x', labelrotation=45)
ax_40k.grid(which='major', axis='y')
ax_40k.minorticks_on()
ax_40k.xaxis.set_tick_params(which='minor', bottom=False)
ax_40k.grid(which='minor', axis='y', alpha=0.25)
ax_40k.get_figure().suptitle(suptitle_txt_40k.format(salary_thresh//1000), fontsize='larger',  x=0.55, y=0.93)
ax_40k.set_title(title_txt_40k, fontsize='smaller', x=0.49)
ax_40k.get_figure().tight_layout()
ax_40k.get_figure().savefig('{}k_all_cpi.pdf'.format(salary_thresh//1000))


#%%

# And the saving of data files

for cpi, df_by_cpi, non_zero_nos_df in zip(cpi_list, df_by_cpi_list, non_zero_nos_df_list):

    df_by_cpi.to_csv(f'heatmap_modeller_alldata_cpi{cpi:}.csv', index=False)
    non_zero_nos_df.to_csv(f'heatmap_modeller_binnedlosses_cpi{cpi:}.csv', index=False)


losses_df.to_csv("heatmap_modeller_losses_cpi_25_28_30_digest.csv", index=False)
