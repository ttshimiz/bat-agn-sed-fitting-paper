import sys
sys.path.append('/Users/ttshimiz/Github/bat-agn-sed-fitting/')

import matplotlib
matplotlib.use('Agg')
import numpy as np
import plotting as bat_plot
import fitting as bat_fit
import models as bat_model
import pandas as pd
from astropy.modeling import fitting as apy_fit
import pickle
import matplotlib.pyplot as plt

# Upload the BAT fluxes for Herschel and WISE
herschel_data = pd.read_csv('../../bat-data/bat_herschel.csv', index_col=0,
                            na_values=0)
wise_data = pd.read_csv('../../bat-data/bat_wise.csv', index_col=0,
                        usecols=[0, 1, 2, 4, 5, 7, 8, 10, 11], na_values=0)

sed = herschel_data.join(wise_data[['W3', 'W3_err', 'W4', 'W4_err']])

# SPIRE fluxes that are seriously contaminated by a companion should be upper limits
psw_flag = herschel_data['PSW_flag']
pmw_flag = herschel_data['PMW_flag']
plw_flag = herschel_data['PLW_flag']

sed['PSW_err'][psw_flag == 'AD'] = sed['PSW'][psw_flag == 'AD']
sed['PSW'][psw_flag == 'AD'] = np.nan
sed['PMW_err'][pmw_flag == 'AD'] = sed['PMW'][pmw_flag == 'AD']
sed['PMW'][pmw_flag == 'AD'] = np.nan
sed['PLW_err'][plw_flag == 'AD'] = sed['PLW'][plw_flag == 'AD']
sed['PLW'][plw_flag == 'AD'] = np.nan

# Upload info on BAT AGN for redshift and luminosity distance
bat_info = pd.read_csv('../../bat-data/bat_info.csv', index_col=0)

filt_use = np.array(['PACS70', 'PACS160', 'PSW', 'PMW', 'PLW'])
filt_err = np.array([s+'_err' for s in filt_use])
waves = np.array([70., 160., 250., 350., 500.])

# Uncomment to fit sources with detections at all wavelengths
#sed_use = sed.dropna(how='any')

# Uncomment to fit sources with only N detected points.
# Change the integer on the right side of '==' to N.

sed_use = sed[np.sum(np.isfinite(sed[filt_use].values), axis=1) <= 1]
#sed_use = sed

names_use = sed_use.index
base_model = bat_model.Greybody(0.0, 15., 2.0)
base_model.tdust.fixed = True
base_model.beta.fixed = True

mdust_upper_limits = pd.Series(index = names_use)
tdust_test = np.array([40., 23., 15.])
mdust_test = np.arange(4.0, 10.0, 0.01)
upper_limits = pd.DataFrame(index = names_use, columns=['mdust40', 'mdust23', 'mdust15', 
                            'lbb40', 'lbb23', 'lbb15'])
for n in names_use:

    src_sed = sed_use.loc[n][filt_use]
    src_err = sed_use.loc[n][filt_err]
    
    flux = np.array(src_sed, dtype=np.float)
    flux_err = np.array(src_err, dtype=np.float)
        
    flux_detected = np.isfinite(flux)
    flux_use = flux[flux_detected]
    flux_err_use = flux_err[flux_detected]
    filt_detected = filt_use[flux_detected]
    waves_use = waves[flux_detected]
    
    src_z = bat_info.loc[n]['Redshift']
    src_lumD = bat_info.loc[n]['Dist_[Mpc]']

    model_test = base_model.copy()
    model_test.set_redshift(src_z)
    model_test.set_lumD(src_lumD)
    
    flux_test = flux
    flux_test[~flux_detected] = flux_err[~flux_detected]
    
    for t in tdust_test:
        
        model_test.tdust = t
        
        for m in mdust_test:
    
            model_test.mdust = m
            f_test  = np.zeros(len(waves))
        
            for i,w in enumerate(waves):
            
                f_test[i] = model_test(w)
            
            if np.any(f_test > flux_test):
                break
        if t == 40.:
            upper_limits.loc[n, 'mdust40'] = m
            upper_limits.loc[n, 'lbb40'] = np.log10(model_test.calc_luminosity())
        elif t == 23.:
            upper_limits.loc[n, 'mdust23'] = m
            upper_limits.loc[n, 'lbb23'] = np.log10(model_test.calc_luminosity())
        elif t == 15.:
            upper_limits.loc[n, 'mdust15'] = m
            upper_limits.loc[n, 'lbb15'] = np.log10(model_test.calc_luminosity())



