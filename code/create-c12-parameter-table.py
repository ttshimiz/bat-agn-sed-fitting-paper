import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
casey_dir = sed_fit_dir + 'analysis/casey_bayes_results/'
data_dir = gh_dir + 'bat-data/'

bat_casey = pd.read_csv(casey_dir+'beta_fixed_2_wturn_gaussianPrior/final_fit_results_beta_fixed_2_wturn_gaussianPrior_v3.csv', index_col=0)
bat_casey_undetected = pd.read_csv(casey_dir+'beta_fixed_2_wturn_gaussianPrior/final_fit_results_beta_fixed_2_wturn_gaussianPrior_undetected.csv', index_col=0)

# Join together the main and undetected tables
bat_casey_all = pd.concat([bat_casey, bat_casey_undetected])

# Calculate the upper and lower errors for all of the parameters
params = ['mdust', 'tdust',
          'alpha', 'norm_pow', 'wturn',
          'lir_total', 'lir_bb', 'lir_powlaw', 'agn_frac']
          
for p in params:

    bat_casey_all[p+'_err_up'] = np.round(bat_casey_all[p+'_84'] - bat_casey_all[p], 2)
    bat_casey_all[p+'_err_down'] = np.round(bat_casey_all[p] - bat_casey_all[p+'_16'], 2)
    

# Print out the table in LaTeX
table_file = open('../tables/bat-agn-c12-parameters.txt', 'w')

names_sorted = bat_casey_all.index.sort_values()

for n in names_sorted:

    d = bat_casey_all.loc[n]
    
    for p in params:
        if (pd.isnull(d[p]) | (n == 'Mrk3')):
            d[p+'_tex'] = '...'
        else:
            num = d[p]
            eup = d[p+'_err_up']
            edwn = d[p+'_err_down']

            if (pd.isnull(eup) & ((p == 'mdust') | (p == 'lir_total') | (p == 'lir_bb'))):
                d[p+'_tex'] = '$<{0:0.2f}$'.format(num)
            elif (pd.isnull(eup) & (p == 'agn_frac')):
                d[p+'_tex'] = '$>{0:0.2f}$'.format(num)
            elif ((p == 'agn_frac') & (d['agn_frac_2_5'] < 0)):
                num = d['agn_frac_95']
                d[p+'_tex'] = '$<{0:0.2f}$'.format(num)
            else:
    	        d[p+'_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(num, edwn, eup)
    	        
    line = ('{0} & {1[mdust_tex]} & {1[tdust_tex]} & {1[norm_pow_tex]} & {1[alpha_tex]} &'
            '{1[wturn_tex]} & {1[lir_total_tex]} & {1[lir_bb_tex]} & {1[lir_powlaw_tex]} & {1[agn_frac_tex]} \\\\'.format(n, d))
            
    table_file.write(line+'\n')
    
table_file.close()