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

# Now define the data for the USS personas 
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
r = (pension_df['new_pension_20yr_pa']/pension_df['new_pension_pa'])**(1/n_years)
pension_df['new_pension_total_geomet'] = pension_df['new_pension_pa']*(r**n_years - 1)/(r-1)


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

# Total and mean loss

print("Total and mean losses")

for df in df_by_cpi_list:
    total_loss_pounds, mean_loss_pounds, mean_loss_percent = total_and_mean_losses(df)
    
    print("Total loss GBP: {:.3} b".format(total_loss_pounds/1e9), 
          "Mean loss GBP: {:.1f} k".format(mean_loss_pounds/1e3), 
          "Mean loss %: {:.3f}".format(mean_loss_percent) )

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
title_txt = "According to USS modeller, lump sum and DC taken as annuity, CPI {}%"

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
    ax.get_figure().savefig(f'uuk_cuts_salary_stack_cpi{cpi:}.pdf')
    # ax.annotate("A", (0.5,0.5), xycoords='axes fraction')


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
    ax.get_figure().savefig(f'uuk_cuts_age_stack_cpi{cpi:}.pdf')


#%%
# Pounds losses, stacked by salary

xlabel_gbp_txt = "Loss in retirement, age 66-86 [GBP, today's money']"
ylabel_txt = "Number of active USS members"
suptitle_txt = "Loss in future USS pension value due to UUK cuts 2022"
title_txt = "According to USS modeller, lump sum and DC taken as annuity, CPI {}%"

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
    ax.get_figure().savefig(f'uuk_cuts_gbp_salary_stack_cpi{cpi:}.pdf')


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
    ax.get_figure().savefig(f'uuk_cuts_gbp_age_stack_cpi{cpi:}.pdf')#%%

#%%
# Now for side-by-side for those under 40k

cols_40k = [(253,217,102),
        (237,125,50),
        (112,48,160)
        ]

newcmp_40k = colormap_from_rgb_list(cols_40k)

suptitle_txt_40k = "Loss in future USS pension value due to UUK cuts 2022 \n Staff with salary under " +chr(163)+ "{}k"
title_txt_40k = "According to USS modeller, lump sum and DC taken as annuity"

salary_thresh = 40000

pension_df_under40k = pension_df[pension_df['salary'] < salary_thresh].copy()

pension_df_under40k['binned_by_pc_loss'] = pd.cut(pension_df_under40k['loss_percent'], 
                                               bins=pc_bin_edges, right=False, labels=pc_bin_labels)
pension_df_under40k['inflation'] *= 100
pension_df_under40k['inflation'] = pension_df_under40k['inflation'].round(1)

pension_df_under40k_binned = bin_and_remove_zeros(pension_df_under40k.copy())

pension_df_under40k_binned_grouped = pension_df_under40k_binned.groupby(['binned_by_pc_loss','inflation']).sum().unstack()
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
ax_40k.get_figure().savefig('uuk_cuts_under_{}k_all_cpi.pdf'.format(salary_thresh//1000))

#%%

print("Loss in retirement for those earning under 40k")
for cpi in [2.5, 2.8, 3.0]:
    df = pension_df_under40k[pension_df_under40k['inflation'] == cpi]
    a, b, c = total_and_mean_losses(df)
    print("Total loss GBP: {:.3} b".format(a/1e9), 
          "Mean loss GBP: {:.1f} k".format(b/1e3), 
          "Mean loss %: {:.3f}".format(c) )

#%%

# And the saving of data files

for df_by_cpi, non_zero_nos_df in zip(df_by_cpi_list, non_zero_nos_df_list):

    df_by_cpi.to_csv(f'uss_pension_pc_loss_cpi{cpi:}.csv', index=False)
    non_zero_nos_df.to_csv(f'uss_binned_pc_loss_age_salary_cpi{cpi:}.csv', index=False)

