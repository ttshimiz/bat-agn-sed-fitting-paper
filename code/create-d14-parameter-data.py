import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
dale_dir = sed_fit_dir + 'analysis/dale14_results/'
data_dir = gh_dir + 'bat-data/'

bat_dale = pd.read_csv(dale_dir+'final_fit_results_dale14_v2.csv',
                       index_col=0)
bat_dale_undetected = pd.read_csv(dale_dir+'final_fit_results_dale14_undetected.csv',
                                  index_col=0)
bat_dale_uncertain = pd.read_csv(dale_dir+'final_fit_results_dale14_uncertainties_v2.csv',
                                 index_col=0)

bat_dale = bat_dale.join(bat_dale_uncertain)

# Calculate the best-fit LIR_AGN and LIR_SF
bat_dale['lir_sf'] = bat_dale['lir_total'] + np.log10(1 - bat_dale['agn_frac_total'])
bat_dale['lir_agn'] = bat_dale['lir_total'] + np.log10(bat_dale['agn_frac_total'])

# Calculate the upper and lower errors for all of the parameters
params = ['lir_total', 'lir_sf', 'lir_agn', 'agn_frac_total']

for p in params:
    for n in bat_dale.index:
        bat_dale.loc[n, p+'_err_up'] = bat_dale.loc[n, p+'_84'] - bat_dale.loc[n, p]
        bat_dale.loc[n, p+'_err_down'] =bat_dale.loc[n, p] - bat_dale.loc[n, p+'_16']

names_sorted = bat_dale.index.sort_values()

d14_params = pd.DataFrame(columns=['lir_total', 'lir_total_err_high', 'lir_total_err_low', 'lir_total_flag',
                                        'lir_sf', 'lir_sf_err_high', 'lir_sf_err_low', 'lir_sf_flag',
                                        'lir_agn', 'lir_agn_err_high', 'lir_agn_err_low', 'lir_agn_flag',
                                        'agn_frac', 'agn_frac_err_high', 'agn_frac_err_low', 'agn_frac_flag'],
                                        index = names_sorted)

for n in names_sorted:

    d = bat_dale.loc[n]
    
    if (n != 'Mrk3'):

        if np.any(n == bat_dale_undetected.index.values):
        
            d14_params.loc[n, 'lir_total'] = d['lir_total_95']
            d14_params.loc[n, 'lir_total_flag'] = -1
            d14_params.loc[n, 'lir_sf'] = d['lir_sf_95']
            d14_params.loc[n, 'lir_sf_flag'] = -1
            d14_params.loc[n, 'lir_agn'] = d['lir_agn_05']
            d14_params.loc[n, 'lir_agn_flag'] = 1
            d14_params.loc[n, 'agn_frac'] = d['agn_frac_total_05']
            d14_params.loc[n, 'agn_frac_flag'] = 1
            
        elif ((d['agn_frac_total'] < 0.1)):

            d14_params.loc[n, 'lir_total'] = d['lir_total']
            d14_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            d14_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            d14_params.loc[n, 'lir_total_flag'] = 0
        
            if (d['agn_frac_total_95'] > 0.1):
                
                d14_params.loc[n, 'agn_frac'] = d['agn_frac_total_95']
                d14_params.loc[n, 'agn_frac_flag'] = -1
                d14_params.loc[n, 'lir_sf'] = d['lir_sf']
                d14_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
                d14_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
                d14_params.loc[n, 'lir_sf_flag'] = 0
                d14_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(d['agn_frac_total_95'])
                d14_params.loc[n, 'lir_agn_flag'] = -1
            else:
            
                d14_params.loc[n, 'agn_frac'] = 0.1
                d14_params.loc[n, 'agn_frac_flag'] = -1
                d14_params.loc[n, 'lir_sf'] = d['lir_sf']
                d14_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
                d14_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
                d14_params.loc[n, 'lir_sf_flag'] = 0
                d14_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(0.1)
                d14_params.loc[n, 'lir_agn_flag'] = -1
        
        else:
        
            d14_params.loc[n, 'lir_total'] = d['lir_total']
            d14_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            d14_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            d14_params.loc[n, 'lir_total_flag'] = 0
            d14_params.loc[n, 'lir_sf'] = d['lir_sf']
            d14_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
            d14_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
            d14_params.loc[n, 'lir_sf_flag'] = 0
            d14_params.loc[n, 'lir_agn'] = d['lir_agn']
            d14_params.loc[n, 'lir_agn_err_low'] = d['lir_agn_err_down']
            d14_params.loc[n, 'lir_agn_err_high'] = d['lir_agn_err_up']
            d14_params.loc[n, 'lir_agn_flag'] = 0
            d14_params.loc[n, 'agn_frac'] = d['agn_frac_total']
            d14_params.loc[n, 'agn_frac_err_low'] = d['agn_frac_total_err_down']
            d14_params.loc[n, 'agn_frac_err_high'] = d['agn_frac_total_err_up']
            d14_params.loc[n, 'agn_frac_flag'] = 0
            

d14_params.to_csv('../data/bat-agn-d14-params.csv', index_label='Name')

            
        
            