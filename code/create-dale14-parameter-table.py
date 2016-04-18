import pandas as pd
import numpy as np

# Directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
dale_dir = sed_fit_dir + 'analysis/dale14_results/'
data_dir = gh_dir + 'bat-data/'

bat_dale = pd.read_csv(dale_dir+'final_fit_results_dale14.csv',
                       index_col=0)
bat_dale_undetected = pd.read_csv(dale_dir+'final_fit_results_dale14_undetected.csv',
                                  index_col=0)
bat_dale_uncertain = pd.read_csv(dale_dir+'final_fit_results_dale14_uncertainties.csv',
                                 index_col=0)

bat_dale = bat_dale.join(bat_dale_uncertain)

# Calculate the best-fit LIR_AGN and LIR_SF
bat_dale['lir_sf'] = bat_dale['lir_total'] + np.log10(1 - bat_dale['agn_frac_total'])
bat_dale['lir_agn'] = bat_dale['lir_total'] + np.log10(bat_dale['agn_frac_total'])

# Calculate the upper and lower errors for all of the parameters
params = ['lir_total', 'lir_sf', 'lir_agn', 'agn_frac_total']

for p in params:
    for n in bat_dale.index:
        bat_dale.loc[n, p+'_err_up'] = np.max([bat_dale.loc[n, p+'_84'] - bat_dale.loc[n, p], 0.01])
        bat_dale.loc[n, p+'_err_down'] = np.max([bat_dale.loc[n, p] - bat_dale.loc[n, p+'_16'], 0.01])
    
# Print out the table in LaTeX
table_file = open('../tables/bat-agn-dale14-parameters.txt', 'w')

names_sorted = bat_dale.index.sort_values()

for n in names_sorted:

    d = bat_dale.loc[n]
    
    if (n != 'Mrk3'):

        if np.any(n == bat_dale_undetected.index.values):

            d['lir_total_tex'] = '$<{0:0.2f}$'.format(d['lir_total_95'])

            if (d['agn_frac_total_05'] != 1.0):

                d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_sf_95'])
                d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_agn_05'])
                d['agn_frac_total_tex'] = '$>{0:0.2f}$'.format(d['agn_frac_total_05'])

            else:

                d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_total_95'] + np.log10(0.05))
                d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_total_95'] + np.log10(0.95))
                d['agn_frac_total_tex'] = '$>{0:0.2f}$'.format(0.95)

        elif ((d['agn_frac_total'] == 0) | (d['agn_frac_total_err_down'] == d['agn_frac_total'])):

            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])

            if (d['agn_frac_total_95'] >= 0.05):
                d['agn_frac_total_tex'] = '$<{0:0.2f}$'.format(d['agn_frac_total_95'])
                d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_agn_95'])
                d['lir_sf_tex'] = '$>{0:0.2f}$'.format(d['lir_sf_05'])
            else:
                d['agn_frac_total_tex'] = '$<{0:0.2f}$'.format(0.05)
                d['lir_agn_tex'] = '$<{0:0.2f}$'.format(d['lir_total'] + np.log10(0.05))
                d['lir_sf_tex'] = '$>{0:0.2f}$'.format(d['lir_total'] + np.log10(0.95))
                
        elif (d['agn_frac_total'] == 1.0):

            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
            d['lir_sf_tex'] = '$<{0:0.2f}$'.format(d['lir_sf_95'])
            d['agn_frac_total_tex'] = '$>{0:0.2f}$'.format(d['agn_frac_total_05'])
            d['lir_agn_tex'] = '$>{0:0.2f}$'.format(d['lir_agn_05'])

        else:

            d['agn_frac_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['agn_frac_total'], d['agn_frac_total_err_down'], d['agn_frac_total_err_up'])
            d['lir_agn_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_agn'], d['lir_agn_err_down'], d['lir_agn_err_up'])
            d['lir_total_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_total'], d['lir_total_err_down'], d['lir_total_err_up'])
            d['lir_sf_tex'] = '${0:0.2f}_{{-{1:0.2f}}}^{{+{2:0.2f}}}$'.format(d['lir_sf'], d['lir_sf_err_down'], d['lir_sf_err_up'])
        
        d['agn_frac_mir_tex'] = '${0:0.2f}$'.format(d['agn_frac_mir'])
        d['alpha_tex'] = '${0:0.4f}$'.format(d['alpha'])

    else:

        d['lir_total_tex'] = '...'
        d['lir_agn_tex'] = '...'
        d['lir_sf_tex'] = '...'
        d['agn_frac_total_tex'] = '...'
        d['agn_frac_mir_tex'] = '...'
        d['alpha_tex'] = '...'

    line = ('{0} & {1[alpha_tex]} & {1[agn_frac_mir_tex]} & {1[lir_total_tex]} & {1[lir_sf_tex]} & {1[lir_agn_tex]} &'
            '{1[agn_frac_total_tex]} \\\\'.format(n, d))

    table_file.write(line+'\n')
    
table_file.close()
    

