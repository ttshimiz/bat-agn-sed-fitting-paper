import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
decomp_dir = sed_fit_dir + 'analysis/decompir_results/sb+arp220/'
data_dir = gh_dir + 'bat-data/'

bat_decompir = pd.read_csv(decomp_dir+'final_fit_results_decompir_sb_and_arp220_v2.csv',
                           index_col=0)
bat_decompir_undetected = pd.read_csv(decomp_dir+'final_fit_results_decompir_sb_and_arp220_undetected.csv',
                                      index_col=0)
bat_decompir_uncertain = pd.read_csv(decomp_dir+'final_fit_results_decompir_sb_and_arp220_uncertainties_v3.csv',
                                     index_col=0)

bat_decompir = bat_decompir.join(bat_decompir_uncertain)

# Calculate the best-fit LIR_AGN and LIR_SF
bat_decompir['lir_sf'] = bat_decompir['lir_total'] + np.log10(1 - bat_decompir['agn_frac'])
bat_decompir['lir_agn'] = bat_decompir['lir_total'] + np.log10(bat_decompir['agn_frac'])

# Calculate the upper and lower errors for all of the parameters
params = ['lir_total', 'lir_sf', 'lir_agn', 'agn_frac']

for p in params:

    bat_decompir[p+'_err_up'] = bat_decompir[p+'_84'] - bat_decompir[p]
    bat_decompir[p+'_err_down'] = bat_decompir[p] - bat_decompir[p+'_16']

names_sorted = bat_decompir.index.sort_values()

decompir_params = pd.DataFrame(columns=['lir_total', 'lir_total_err_high', 'lir_total_err_low', 'lir_total_flag',
                                        'lir_sf', 'lir_sf_err_high', 'lir_sf_err_low', 'lir_sf_flag',
                                        'lir_agn', 'lir_agn_err_high', 'lir_agn_err_low', 'lir_agn_flag',
                                        'agn_frac', 'agn_frac_err_high', 'agn_frac_err_low', 'agn_frac_flag'],
                                        index = names_sorted)

for n in names_sorted:

    d = bat_decompir.loc[n]
    
    if (n != 'Mrk3'):

        if np.any(n == bat_decompir_undetected.index.values):
        
            decompir_params.loc[n, 'lir_total'] = d['lir_total_95']
            decompir_params.loc[n, 'lir_total_flag'] = -1
            decompir_params.loc[n, 'lir_sf'] = d['lir_sf_95']
            decompir_params.loc[n, 'lir_sf_flag'] = -1
            decompir_params.loc[n, 'lir_agn'] = d['lir_agn_05']
            decompir_params.loc[n, 'lir_agn_flag'] = 1
            decompir_params.loc[n, 'agn_frac'] = d['agn_frac_05']
            decompir_params.loc[n, 'agn_frac_flag'] = 1
            
        elif ((d['agn_frac'] < 0.1) | (d['agn_frac_16'] < 1e-10)):

            decompir_params.loc[n, 'lir_total'] = d['lir_total']
            decompir_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            decompir_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            decompir_params.loc[n, 'lir_total_flag'] = 0
        
            if (d['agn_frac_95'] > 0.1):
                
                decompir_params.loc[n, 'agn_frac'] = d['agn_frac_95']
                decompir_params.loc[n, 'agn_frac_flag'] = -1
                decompir_params.loc[n, 'lir_sf'] = d['lir_sf']
                decompir_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
                decompir_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
                decompir_params.loc[n, 'lir_sf_flag'] = 0
                decompir_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(d['agn_frac_95'])
                decompir_params.loc[n, 'lir_agn_flag'] = -1
            else:
            
                decompir_params.loc[n, 'agn_frac'] = 0.1
                decompir_params.loc[n, 'agn_frac_flag'] = -1
                decompir_params.loc[n, 'lir_sf'] = d['lir_sf']
                decompir_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
                decompir_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
                decompir_params.loc[n, 'lir_sf_flag'] = 0
                decompir_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(0.1)
                decompir_params.loc[n, 'lir_agn_flag'] = -1
        
        else:
        
            decompir_params.loc[n, 'lir_total'] = d['lir_total']
            decompir_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            decompir_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            decompir_params.loc[n, 'lir_total_flag'] = 0
            decompir_params.loc[n, 'lir_sf'] = d['lir_sf']
            decompir_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
            decompir_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
            decompir_params.loc[n, 'lir_sf_flag'] = 0
            decompir_params.loc[n, 'lir_agn'] = d['lir_agn']
            decompir_params.loc[n, 'lir_agn_err_low'] = d['lir_agn_err_down']
            decompir_params.loc[n, 'lir_agn_err_high'] = d['lir_agn_err_up']
            decompir_params.loc[n, 'lir_agn_flag'] = 0
            decompir_params.loc[n, 'agn_frac'] = d['agn_frac']
            decompir_params.loc[n, 'agn_frac_err_low'] = d['agn_frac_err_down']
            decompir_params.loc[n, 'agn_frac_err_high'] = d['agn_frac_err_up']
            decompir_params.loc[n, 'agn_frac_flag'] = 0
            

decompir_params.to_csv('../data/bat-agn-decompir-params.csv', index_label='Name')

            
        
            