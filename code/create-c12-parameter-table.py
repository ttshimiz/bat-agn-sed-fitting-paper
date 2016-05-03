import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
casey_dir = sed_fit_dir + 'analysis/casey_bayes_results/'
data_dir = gh_dir + 'bat-data/'

bat_c12 = pd.read_csv('../data/bat-agn-c12-params.csv', index_col=0)

bat_c12 = bat_c12.sort_index()

table_file = open('../tables/bat-agn-c12-parameters.txt', 'w')
for n in bat_c12.index.values:
    
    d = bat_c12.loc[n]
    d['alpha_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['alpha'], d['alpha_err_low'], d['alpha_err_high'])
    d['wturn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['wturn'], d['wturn_err_low'], d['wturn_err_high'])        

    if pd.isnull(d['tdust_flag']):
        d['tdust_tex'] = '...'
    else:
        d['tdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['tdust'], d['tdust_err_low'], d['tdust_err_high'])

    if d['mdust_flag'] == -1:
        d['mdust_tex'] = '$<{0:0.2f}$'.format(d['mdust'])
    else:
        d['mdust_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['mdust'], d['mdust_err_low'], d['mdust_err_high'])
        
    if d['lir_sf_flag'] == -1:
        d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_sf'])
    else:
        d['lir_sf_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_sf'], d['lir_sf_err_low'], d['lir_sf_err_high'])

    if d['lir_agn_flag'] == -1:
        d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_agn'])
    elif d['lir_agn_flag'] == 1:
        d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_agn'])
    else:
        d['lir_agn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_sf'], d['lir_sf_err_low'], d['lir_sf_err_high'])

    if d['agn_frac_flag'] == -1:
        d['agn_frac_tex'] = '$<{0:0.2f}$'.format(d['agn_frac'])
    elif d['agn_frac_flag'] == 1:
        d['agn_frac_tex'] = '$>{0:0.2f}$'.format(d['agn_frac'])
    else:
        d['agn_frac_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['agn_frac'], d['agn_frac_err_low'], d['agn_frac_err_high'])

    if d['lir_total_flag'] == -1:
        d['lir_total_tex'] = '$<{0:0.2f}$'.format(d['lir_total'])
    else:
        d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_low'], d['lir_total_err_high'])



    line = ('{0} & {1[mdust_tex]} & {1[tdust_tex]} & {1[alpha_tex]} &'
            '{1[wturn_tex]} & {1[lir_total_tex]} & {1[lir_sf_tex]} & {1[lir_agn_tex]} & {1[agn_frac_tex]} \\\\'.format(n, d))
            
    table_file.write(line+'\n')
    
table_file.close()