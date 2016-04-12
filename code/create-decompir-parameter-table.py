import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
decomp_dir = sed_fit_dir + 'analysis/decompir_results/sb+arp220/'
data_dir = gh_dir + 'bat-data/'

bat_decompir = pd.read_csv(decomp_dir+'final_fit_results_decompir_sb_and_arp220_mle.csv',
                           index_col=0)
bat_decompir_uncertain = pd.read_csv(decomp_dir+'final_fit_results_decompir_sb_and_arp220_uncertainties_v2.csv',
                                     index_col=0)

bat_decompir = bat_decompir.join(bat_decompir_uncertain)

# Calculate the best-fit LIR_AGN and LIR_SF
bat_decompir['lir_sf'] = bat_decompir['lir_total'] + np.log10(1 - bat_decompir['agn_frac'])
bat_decompir['lir_agn'] = bat_decompir['lir_total'] + np.log10(bat_decompir['agn_frac'])

# Calculate the upper and lower errors for all of the parameters
params = ['lir_total', 'lir_sf', 'lir_agn', 'agn_frac']

for p in params:

    bat_decompir[p+'_err_up'] = np.round(bat_decompir[p+'_84'] - bat_decompir[p], 2)
    bat_decompir[p+'_err_down'] = np.round(bat_decompir[p] - bat_decompir[p+'_16'], 2)
    
# Print out the table in LaTeX
table_file = open('../tables/bat-agn-decompir-parameters.txt', 'w')

names_sorted = bat_decompir.index.sort_values()

for n in names_sorted:

    d = bat_decompir.loc[n]
    
    if (np.isfinite(d['lir_sf']) & (n != 'Mrk3')):
        if (d['agn_frac_2_5'] < 10**(-5)):
            if (d['agn_frac'] >= 0.01):
                d['agn_frac_tex'] = '$<{0:0.2f}$'.format(d['agn_frac_95'])
                d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_agn_95'])
            else:
                d['agn_frac_tex'] = '$<{0:0.2f}$'.format(0.01)
                d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_total'] - 2.)

        else:
            d['agn_frac_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['agn_frac'], d['agn_frac_err_down'], d['agn_frac_err_up'])
            d['lir_agn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_agn'], d['lir_agn_err_down'], d['lir_agn_err_up'])
        
        d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
        d['lir_sf_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_sf'], d['lir_sf_err_down'], d['lir_sf_err_up'])
    else:
        d['lir_total_tex'] = '...'
        d['lir_agn_tex'] = '...'
        d['lir_sf_tex'] = '...'
        d['agn_frac_tex'] = '...'
        d['host_name'] = '...'

    line = ('{0} & {1[host_name]} & {1[lir_total_tex]} & {1[lir_sf_tex]} & {1[lir_agn_tex]} &'
            '{1[agn_frac_tex]} \\\\'.format(n, d))

    table_file.write(line+'\n')
    
table_file.close()
    

