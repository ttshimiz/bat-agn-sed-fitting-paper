import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
casey_dir = sed_fit_dir + 'analysis/casey_bayes_results/'

pgqso_casey = pd.read_csv(casey_dir+'pgqso_beta_fixed_2_wturn_gaussianPrior/final_fit_results_beta_fixed_2_wturn_gaussianPrior_pgqso.csv', index_col=0)

# Calculate the upper and lower errors for all of the parameters
params = ['mdust', 'tdust',
          'alpha', 'norm_pow', 'wturn',
          'lir_total', 'lir_agn', 'lir_sf', 'agn_frac']
          
for p in params:

    pgqso_casey[p+'_err_up'] = pgqso_casey[p+'_84'] - pgqso_casey[p]
    pgqso_casey[p+'_err_down'] = pgqso_casey[p] - pgqso_casey[p+'_16']
    

# Print out the table in LaTeX
table_file = open('../data/pgqso-c12-parameters.csv', 'w')

names_sorted = pgqso_casey.index.sort_values()
pg_undetected = np.array(['PG 0003+158', 'PG 0026+129', 'PG 1001+054', 'PG 1048-090',
                          'PG 1100+772', 'PG 1103-006', 'PG 1151+117', 'PG 1216+069', 
                          'PG 1259+593', 'PG 1352+183', 'PG 1425+267', 'PG 1617+175',
                          'PG 2251+113', 'PG 2304+042', 'PG 2308+098'])
                          
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

    d = pgqso_casey.loc[n]
    
    if np.any(n == pg_undetected):

        c12_params.loc[n, 'mdust'] = d['mdust']
        c12_params.loc[n, 'mdust_flag'] = -1
        c12_params.loc[n, 'lir_total'] = d['lir_total_95']
        c12_params.loc[n, 'lir_total_flag'] = -1
        
        if (d['agn_frac_05'] < 0.9):

            c12_params.loc[n, 'lir_sf'] = d['lir_sf_95']
            c12_params.loc[n, 'lir_sf_flag'] = -1
            c12_params.loc[n, 'lir_agn'] = d['lir_agn_05']
            c12_params.loc[n, 'lir_agn_flag'] = 1
            c12_params.loc[n, 'agn_frac'] = d['agn_frac_05']
            c12_params.loc[n, 'agn_frac_flag'] = 1

        else:

            c12_params.loc[n, 'lir_sf'] = d['lir_total_95'] + np.log10(0.1)
            c12_params.loc[n, 'lir_sf_flag'] = -1
            c12_params.loc[n, 'lir_agn'] = d['lir_total_95'] + np.log10(0.9)
            c12_params.loc[n, 'lir_agn_flag'] = 1
            c12_params.loc[n, 'agn_frac'] = 0.9
            c12_params.loc[n, 'agn_frac_flag'] = 1
    
    elif ((d['agn_frac_16'] < 0) | (d['agn_frac'] < 0.1)):
        
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
        
        if (d['agn_frac_95'] > 0.1):
            
            c12_params.loc[n, 'agn_frac'] = d['agn_frac_95']
            c12_params.loc[n, 'agn_frac_flag'] = -1
            c12_params.loc[n, 'lir_sf'] = d['lir_sf']
            c12_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
            c12_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
            c12_params.loc[n, 'lir_sf_flag'] = 0
                            
            if np.isfinite(d['lir_agn_95']):
                
                c12_params.loc[n, 'lir_agn'] = d['lir_agn_95']
                c12_params.loc[n, 'lir_agn_flag'] = -1

            else:
                
                c12_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(d['agn_frac_95'])
                c12_params.loc[n, 'lir_agn_flag'] = -1

        else:
            
            c12_params.loc[n, 'agn_frac'] = 0.1
            c12_params.loc[n, 'agn_frac_flag'] = -1
            c12_params.loc[n, 'lir_sf'] = d['lir_sf']
            c12_params.loc[n, 'lir_sf_err_low'] = d['lir_sf_err_down']
            c12_params.loc[n, 'lir_sf_err_high'] = d['lir_sf_err_up']
            c12_params.loc[n, 'lir_sf_flag'] = 0
            c12_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(0.1)
            c12_params.loc[n, 'lir_agn_flag'] = -1
            
    elif (d['agn_frac'] > 0.9):
        
        
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
        
        if (d['agn_frac_05'] < 0.9):
            c12_params.loc[n, 'lir_sf'] = d['lir_sf_95']
            c12_params.loc[n, 'lir_sf_flag'] = -1
            c12_params.loc[n, 'agn_frac'] = d['agn_frac_05']
            c12_params.loc[n, 'agn_frac_flag'] = 1
            c12_params.loc[n, 'lir_agn'] = d['lir_agn_05']
            c12_params.loc[n, 'lir_agn_flag'] = 1
        else:
            c12_params.loc[n, 'lir_sf'] = d['lir_total'] + np.log10(0.1)
            c12_params.loc[n, 'lir_sf_flag'] = -1
            c12_params.loc[n, 'agn_frac'] = 0.9
            c12_params.loc[n, 'agn_frac_flag'] = 1
            c12_params.loc[n, 'lir_agn'] = d['lir_total'] + np.log10(0.9)
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
        c12_params.loc[n, 'agn_frac_err_low'] = np.max([d['agn_frac_err_down'], 0.1])
        c12_params.loc[n, 'agn_frac_err_high'] = np.max([d['agn_frac_err_up'], 0.1])
        c12_params.loc[n, 'agn_frac_flag'] = 0


    
    c12_params.loc[n, 'alpha'] = d['alpha']
    c12_params.loc[n, 'alpha_err_low'] = d['alpha_err_down']
    c12_params.loc[n, 'alpha_err_high'] = d['alpha_err_up']
    c12_params.loc[n, 'alpha_flag'] = 0
    c12_params.loc[n, 'wturn'] = d['wturn']
    c12_params.loc[n, 'wturn_err_low'] = d['wturn_err_down']
    c12_params.loc[n, 'wturn_err_high'] = d['wturn_err_up']
    c12_params.loc[n, 'wturn_flag'] = 0
        
c12_params.to_csv('../data/pgqso-c12-params.csv', index_label='Name')