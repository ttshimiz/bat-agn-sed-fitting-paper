import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
casey_dir = sed_fit_dir + 'analysis/casey_bayes_results/'
data_dir = gh_dir + 'bat-data/'

bat_casey = pd.read_csv(casey_dir+'beta_fixed_2_wturn_gaussianPrior/final_fit_results_beta_fixed_2_wturn_gaussianPrior_v4.csv', index_col=0)
bat_casey_undetected = pd.read_csv(casey_dir+'beta_fixed_2_wturn_gaussianPrior/final_fit_results_beta_fixed_2_wturn_gaussianPrior_undetected.csv', index_col=0)

# Join together the main and undetected tables
bat_casey_all = pd.concat([bat_casey, bat_casey_undetected])

# Calculate the upper and lower errors for all of the parameters
params = ['mdust', 'tdust',
          'alpha', 'norm_pow', 'wturn',
          'lir_total', 'lir_agn', 'lir_sf', 'agn_frac']
          
for p in params:

    bat_casey_all[p+'_err_up'] = bat_casey_all[p+'_84'] - bat_casey_all[p]
    bat_casey_all[p+'_err_down'] = bat_casey_all[p] - bat_casey_all[p+'_16']
    

# Print out the table in LaTeX
table_file = open('../data/bat-agn-c12-parameters.csv', 'w')

names_sorted = bat_casey_all.index.sort_values()

c12_params = pd.DataFrame(columns=['mdust', 'mdust_err_high', 'mdust_err_low', 'mdust_flag',
                                   'tdust', 'tdust_err_high', 'tdust_err_low', 'tdust_flag',
                                   'alpha', 'alpha_err_high', 'alpha_err_low', 'alpha_flag',
                                   'wturn', 'wturn_err_high', 'wturn_err_low', 'wturn_flag',
                                   'lir_total', 'lir_total_err_high', 'lir_total_err_low', 'lir_total_flag',
                                   'lir_sf', 'lir_sf_err_high', 'lir_sf_err_low', 'lir_sf_flag',
                                   'lir_agn', 'lir_agn_err_high', 'lir_agn_err_low', 'lir_agn_flag',
                                   'agn_frac', 'agn_frac_high', 'agn_frac_low', 'agn_frac_flag'],
                          index = names_sorted)

for n in names_sorted:

    d = bat_casey_all.loc[n]
    
    
    if (n != 'Mrk3'):
        if np.any(n == bat_casey_undetected.index.values):

            c12_params.loc[n, 'mdust'] = d['mdust']
            c12_params.loc[n, 'mdust_flag'] = -1
            c12_params.loc[n, 'lir_total'] = d['lir_total_95']
            c12_params.loc[n, 'lir_total_flag'] = -1
            
            if (d['agn_frac_05'] < 0.95):

                c12_params.loc[n, 'lir_sf'] = d['lir_sf_95']
                c12_params.loc[n, 'lir_sf_flag'] = -1
                c12_params.loc[n, 'lir_agn'] = d['lir_agn_05']
                c12_params.loc[n, 'lir_agn_flag'] = 1
                c12_params.loc[n, 'agn_frac'] = d['agn_frac_05']
                c12_params.loc[n, 'agn_frac_flag'] = 1

            else:

                c12_params.loc[n, 'lir_sf'] = d['lir_total_95'] + np.log10(0.05)
                c12_params.loc[n, 'lir_sf_flag'] = -1
                c12_params.loc[n, 'lir_agn'] = d['lir_total_95'] + np.log10(0.95)
                c12_params.loc[n, 'lir_agn_flag'] = 1
                c12_params.loc[n, 'agn_frac'] = 0.95
                c12_params.loc[n, 'agn_frac_flag'] = 1
        
        elif ((d['agn_frac_16'] < 0) | (d['agn_frac'] < 0.05)):
            
            c12_params.loc[n, 'mdust'] = d['mdust']
            c12_params.loc[n, 'mdust_err_low'] = d['mdust_err_down']
            c12_params.loc[n, 'mdust_err_high'] = d['mdust_err_up']
            c12_params.loc[n, 'mdust_flag'] = 0
            c12_params.loc[n, 'lir_total'] = d['lir_total']
            c12_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            c12_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            c12_params.loc[n, 'lir_total_flag'] = 0
            c12_params.loc[n, 'tdust'] = d['tdust']
            c12_params.loc[n, 'tdust_err_low'] = d['tdust_err_down']
            c12_params.loc[n, 'tdust_err_high'] = d['tdust_err_up']
            c12_params.loc[n, 'tdust_flag'] = 0
            
            if (d['agn_frac_95'] > 0.05):
                
                c12_params.loc[n, 'agn_frac'] = d['agn_frac_95']
                c12_params.loc[n, 'agn_frac_flag'] = -1
                c12_params.loc[n, 'lir_sf'] = d['lir_sf_05']
                c12_params.loc[n, 'lir_sf_flag'] = 1
                                
                if np.isfinite(d['lir_agn_95']):
                    
                    c12_params.loc[n, 'lir_agn'] = d['lir_agn_95']
                    c12_params.loc[n, 'lir_agn_flag'] = -1

                else:
                    
                    c12_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(d['agn_frac_95'])
                    c12_params.loc[n, 'lir_agn_flag'] = -1

            else:
                
                c12_params.loc[n, 'agn_frac'] = 0.05
                c12_params.loc[n, 'agn_frac_flag'] = -1
                c12_params.loc[n, 'lir_sf'] = d['lir_total'] + np.log10(0.95)
                c12_params.loc[n, 'lir_sf_flag'] = 1
                c12_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(0.05)
                c12_params.loc[n, 'lir_agn_flag'] = -1
                
        elif (d['agn_frac'] > 0.95):

            c12_params.loc[n, 'mdust'] = d['mdust']
            c12_params.loc[n, 'mdust_err_low'] = d['mdust_err_down']
            c12_params.loc[n, 'mdust_err_high'] = d['mdust_err_up']
            c12_params.loc[n, 'mdust_flag'] = 0
            c12_params.loc[n, 'lir_total'] = d['lir_total']
            c12_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            c12_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            c12_params.loc[n, 'lir_total_flag'] = 0
            c12_params.loc[n, 'tdust'] = d['tdust']
            c12_params.loc[n, 'tdust_err_low'] = d['tdust_err_down']
            c12_params.loc[n, 'tdust_err_high'] = d['tdust_err_up']
            c12_params.loc[n, 'tdust_flag'] = 0
            c12_params.loc[n, 'lir_sf'] = d['lir_sf_95']
            c12_params.loc[n, 'lir_sf_flag'] = -1
            c12_params.loc[n, 'agn_frac'] = d['agn_frac_05']
            c12_params.loc[n, 'agn_frac_flag'] = 1
            c12_params.loc[n, 'lir_agn'] = d['lir_agn_05']
            c12_params.loc[n, 'lir_agn_flag'] = 1
            
        else:

            c12_params.loc[n, 'mdust'] = d['mdust']
            c12_params.loc[n, 'mdust_err_low'] = d['mdust_err_down']
            c12_params.loc[n, 'mdust_err_high'] = d['mdust_err_up']
            c12_params.loc[n, 'mdust_flag'] = 0
            c12_params.loc[n, 'lir_total'] = d['lir_total']
            c12_params.loc[n, 'lir_total_err_low'] = d['lir_total_err_down']
            c12_params.loc[n, 'lir_total_err_high'] = d['lir_total_err_up']
            c12_params.loc[n, 'lir_total_flag'] = 0
            c12_params.loc[n, 'tdust'] = d['tdust']
            c12_params.loc[n, 'tdust_err_low'] = d['tdust_err_down']
            c12_params.loc[n, 'tdust_err_high'] = d['tdust_err_up']
            c12_params.loc[n, 'tdust_flag'] = 0
            c12_params.loc[n, 'lir_sf'] = d['lir_sf']
            c12_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
            c12_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
            c12_params.loc[n, 'lir_sf_flag'] = 0
            c12_params.loc[n, 'lir_agn'] = d['lir_agn']
            c12_params.loc[n, 'lir_agn_err_low'] = d['lir_agn_err_down']
            c12_params.loc[n, 'lir_agn_err_high'] = d['lir_agn_err_up']
            c12_params.loc[n, 'lir_agn_flag'] = 0
            c12_params.loc[n, 'agn_frac'] = d['agn_frac']
            c12_params.loc[n, 'agn_frac_err_low'] = d['agn_frac_err_down']
            c12_params.loc[n, 'agn_frac_err_high'] = d['agn_frac_err_up']
            c12_params.loc[n, 'agn_frac_flag'] = 0


        
        c12_params.loc[n, 'alpha'] = d['alpha']
        c12_params.loc[n, 'alpha_err_low'] = d['alpha_err_down']
        c12_params.loc[n, 'alpha_err_high'] = d['alpha_err_up']
        c12_params.loc[n, 'alpha_flag'] = 0
        c12_params.loc[n, 'wturn'] = d['wturn']
        c12_params.loc[n, 'wturn_err_low'] = d['wturn_err_down']
        c12_params.loc[n, 'wturn_err_high'] = d['wturn_err_up']
        c12_params.loc[n, 'wturn_flag'] = 0
        
c12_params.to_csv('../data/bat-agn-c12-params.csv', index_label='Name')