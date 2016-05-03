import numpy as np
import pandas as pd
import scipy.stats as stats

results_dir = '/Users/ttshimiz/Github/bat-agn-sed-fitting/analysis/casey_bayes_results/beta_fixed2_wturn_gaussianPrior/'
results_file = results_dir'final_fit_results_beta_fixed_2_wturn_gaussianPrior_v4.csv'

bat_c12 = pd.read_csv(results_file, index_col=0)

lagn = 10**(bat_c12['lir_powlaw']) - 1./3.*10**(bat_c12['lir_bb'])
fagn = (10**(bat_c12['lir_powlaw']) - 1./3.*10**(bat_c12['lir_bb']))/10**(bat_c12['lir_total'])

sigma_lplaw = 10**(bat_c12['lir_powlaw'])*np.max(np.vstack([bat_c12['lir_powlaw']-bat_c12['lir_powlaw_16'], bat_c12['lir_powlaw_84']-bat_c12['lir_powlaw']]), axis=0)/0.434
sigma_lbb = 10**(bat_c12['lir_bb'])*np.max(np.vstack([bat_c12['lir_bb']-bat_c12['lir_bb_16'], bat_c12['lir_bb_84']-bat_c12['lir_bb']]), axis=0)/0.434
sigma_ltotal = 1n0**(bat_c12['lir_total'])*np.max(np.vstack([bat_c12['lir_total']-bat_c12['lir_total_16'], bat_c12['lir_total_84']-bat_c12['lir_total']]), axis=0)/0.434

sigma_correct = 0.1162655

sigma_corrlbb = 1/3.*10**bat_c12['lir_bb']*np.sqrt((sigma_correct*3)**2+(sigma_lbb/10**bat_c12['lir_bb'])**2)

rho_lpl_corrlbb = stats.pearsonr(10**bat_c12['lir_powlaw'], 1/3.*10**bat_c12['lir_bb'])[0]
cov_lpl_corrlbb = rho_lpl_corrlbb*sigma_lplaw*sigma_corrlbb

sigma_lagn = np.sqrt(sigma_lplaw**2 + sigma_corrlbb**2 - 2*cov_lpl_corrlbb)

rho_fagn = stats.pearsonr(lagn, 10**bat_c12['lir_total'])[0]
cov_fagn = rho_lagn*sigma_lagn*sigma_ltotal

sigma_fagn = fagn*np.sqrt((sigma_lagn/lagn)**2 + (sigma_ltotal/10**bat_c12['lir_total'])**2 -
                          2*cov_fagn/lagn/10**bat_c12['lir_total'])
