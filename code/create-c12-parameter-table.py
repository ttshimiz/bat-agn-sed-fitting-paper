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
table_file = open('../tables/bat-agn-c12-parameters.txt', 'w')

names_sorted = bat_casey_all.index.sort_values()

for n in names_sorted:

    d = bat_casey_all.loc[n]
    
    
    if (n != 'Mrk3'):
        if np.any(n == bat_casey_undetected.index.values):
 
            d['lir_total_tex'] = '$<{0:0.2f}$'.format(d['lir_total_95'])
            d['mdust_tex'] = '$<{0:0.2f}$'.format(d['mdust'])
            d['tdust_tex'] = '...'
            
            if (d['agn_frac_05'] < 0.95):

                d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_sf_95'])
                d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_agn_05'])
                d['agn_frac_tex'] = '$>{0:0.2f}$'.format(d['agn_frac_05'])

            else:

                d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_total_95'] + np.log10(0.05))
                d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_total_95'] + np.log10(0.95))
                d['agn_frac_tex'] = '$>{0:0.2f}$'.format(0.95)
        
        elif ((d['agn_frac_16'] < 0) | (d['agn_frac'] < 0.05)):

            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
            d['mdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['mdust'], d['mdust_err_down'], d['mdust_err_up'])
            d['tdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['tdust'], d['tdust_err_down'], d['tdust_err_up'])
            
            if (d['agn_frac_95'] > 0.05):
                
                d['agn_frac_tex'] = '$<{0:0.2f}$'.format(d['agn_frac_95'])
                d['lir_sf_tex'] = '$>{0:0.2f}$'.format(d['lir_sf_05'])
                
                if np.isfinite(d['lir_agn_95']):

                    d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_agn_95'])

                else:

                    d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_total'] + np.log10(d['agn_frac_95']))
            else:

                d['agn_frac_tex'] = '$<{0:0.2f}$'.format(0.05)
                d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_total'] + np.log10(0.05))
                d['lir_sf_tex'] = '$>{0:0.2f}$'.format(d['lir_total'] + np.log10(0.95))
                
        elif (d['agn_frac'] > 0.95):

            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
            d['mdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['mdust'], d['mdust_err_down'], d['mdust_err_up'])
            d['tdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['tdust'], d['tdust_err_down'], d['tdust_err_up'])
            d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_sf_95'])
            d['agn_frac_tex'] = '$>{0:0.2f}$'.format(d['agn_frac_05'])
            d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_agn_05'])

        else:

            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
            d['mdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['mdust'], d['mdust_err_down'], d['mdust_err_up'])
            d['tdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['tdust'], d['tdust_err_down'], d['tdust_err_up'])
            d['lir_sf_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_sf'], d['lir_sf_err_down'], d['lir_sf_err_up'])
            d['lir_agn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_agn'], d['lir_agn_err_down'], d['lir_agn_err_up'])
            d['agn_frac_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['agn_frac'], d['agn_frac_err_down'], d['agn_frac_err_up'])    
        
        d['alpha_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['alpha'], d['alpha_err_down'], d['alpha_err_up'])	        
        d['wturn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['wturn'], d['wturn_err_down'], d['wturn_err_up'])
        d['norm_pow_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['norm_pow'], d['norm_pow_err_down'], d['norm_pow_err_up']) 
        
    else:
        d['mdust_tex'] = '...'
        d['tdust_tex'] = '...'
        d['alpha_tex'] = '...'
        d['wturn_tex'] = '...'
        d['lir_total_tex'] = '...'
        d['lir_sf_tex'] = '...'
        d['lir_agn_tex'] = '...'
        d['agn_frac_tex'] = '...'
            
    line = ('{0} & {1[mdust_tex]} & {1[tdust_tex]} & {1[alpha_tex]} &'
            '{1[wturn_tex]} & {1[lir_total_tex]} & {1[lir_sf_tex]} & {1[lir_agn_tex]} & {1[agn_frac_tex]} \\\\'.format(n, d))
            
    table_file.write(line+'\n')
    
table_file.close()