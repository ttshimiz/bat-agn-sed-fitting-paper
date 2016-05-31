# Standard module imports
import numpy as np
import scipy.stats as stats
import pandas as pd
import sys

# Useful directories
gh_dir = '/Users/ttshimiz/Github/'
sed_fit_dir = gh_dir + 'bat-agn-sed-fitting/'
casey_dir = sed_fit_dir + 'analysis/casey_bayes_results/'
data_dir = gh_dir + 'bat-data/'

sys.path.append(gh_dir+'asurv/')
sys.path.append(gh_dir+'linmix/')
sys.path.append(sed_fit_dir)
import asurv
import linmix
import models as bat_mod
from fitting import Filters
import pickle

# Setup the figures
execfile('../code/figure-setup.py')

####################################### FUNCTION FOR PLOTTING ############################
def plot_fit(waves, obs_flux, model, model_waves=np.arange(1, 1000),
             obs_err=None, plot_components=False, comp_colors=None,
             plot_mono_fluxes=False, filts=None,
             plot_fit_spread=False, nspread=1000,
             name=None, plot_params=False, upperlimit=False,
             fig=None, ax=None):

    red = sn.xkcd_rgb['pale red']
    blue = sn.xkcd_rgb['denim blue']
    lt_blue = sn.xkcd_rgb['pastel blue']
    
    if fig is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        if ax is None:
            ax = fig.add_subplot(111)
    
    zcorr = 1 + model.redshift
    #median_model = model(model_waves/zcorr) * zcorr

    #ax.loglog(model_waves, median_model, color=blue, label='Best Fit Model')

    if plot_fit_spread:
        dummy = model.copy()
        fixed = np.array([dummy.fixed[n] for n in dummy.param_names])
        param_rand = np.random.randint(low=0, high=len(model.chain_nb),
                                       size=nspread)
        rand_sed = np.zeros((nspread, len(model_waves)))

        for i in range(nspread):

            dummy.parameters[~fixed] = model.chain_nb[param_rand[i]]
            rand_sed[i, :] = dummy(model_waves/zcorr) * zcorr

        model_2_5, model_50, model_97_5 = np.percentile(rand_sed, [2.5, 50.0, 97.5], axis=0)
        ax.loglog(model_waves, model_50, color=blue, label='Best Fit Model')
        ax.fill_between(model_waves, model_2_5, model_97_5, color=lt_blue,
                        alpha=0.5, label='_nolabel')

    if plot_components:
        ncomps = model.n_components
        if comp_colors is None:
            comp_colors = sn.color_palette('colorblind',
                                                n_colors=ncomps+1)[1:]
        comps = model.eval_comps(model_waves/zcorr) * zcorr
        for i in range(ncomps):
            ax.loglog(model_waves, comps[i, :], ls='--',
                      label=model.comp_names[i], color=comp_colors[i])

    undetected = np.isnan(obs_flux)
    if plot_mono_fluxes:
        dummy2 = model.copy()
        filters = Filters()
        fwaves = filters.filter_waves
        filts = np.array(filts)[~undetected]
        mono_fluxes = np.array([filters.calc_mono_flux(f, fwaves[f],
                                dummy2(fwaves[f]/zcorr))*zcorr for f in filts])
        ax.plot(waves[~undetected], mono_fluxes, marker='s', ls='None',
                color=red, label='Model Fluxes')
        if sum(undetected) > 0:
            fluxes = np.hstack([mono_fluxes, obs_flux[~undetected],
                                obs_err[undetected]])
        else:
            fluxes = np.hstack([mono_fluxes, obs_flux])
    else:
        if sum(undetected) > 0:
            fluxes = np.hstack([obs_flux[~undetected],
                                obs_err[undetected]])
        else:
            fluxes = obs_flux

    if obs_err is None:
        ax.plot(waves[~undetected], obs_flux[~undetected], marker='o',
                ls='None', color='k', label='Observed Fluxes')
    else:
        ax.errorbar(waves[~undetected], obs_flux[~undetected],
                    yerr=obs_err[~undetected], marker='o', ls='None',
                    color='k', label='Observed Fluxes')
        if sum(undetected) > 0:
            #ax.quiver(waves[undetected], obs_err[undetected],
            #          np.zeros(sum(undetected)),
            #          -10*np.ones(sum(undetected)),
            #          width=0.01, color='r')
            ax.plot(waves[undetected], obs_err[undetected],
                    marker='o', mec=red, mfc='None', mew=1.5, ls='None')
    if plot_params:
        fs = mpl.rcParams['legend.fontsize']
        for i, n in enumerate(model.param_names):
            ln = tex_names[n]
            p = model.parameters[i]
            l = p - model.param_errs[i, 0]
            u = model.param_errs[i, 1] - p
            s = r'%s$ = %.2f^{+%.2f}_{-%.2f}$' % (ln, p, u, l)

            ax.text(0.97, 0.97-i*0.06, s, ha='right', va='top',
                    transform=ax.transAxes, fontsize=fs)

    if name is not None:
        ax.text(0.05, 0.95, name, fontsize=6, ha='left', va='top', transform=ax.transAxes)

    ax.set_xlim([10, 1000])
    ax.set_ylim([10**(-0.5)*min(fluxes), 10**(0.5)*max(fluxes)])
    #ax.legend(loc='upper left')
    ax.set_xlabel(r'$\lambda$ [$\mu$m]')
    ax.set_ylabel('Flux Density [Jy]')
    sn.despine()
    return fig

######################################### MAIN SCRIPT ####################################
# Upload the BAT fluxes for Herschel and WISE
herschel_data = pd.read_csv('/Users/ttshimiz/Github/bat-data/bat_herschel.csv', index_col=0,
                            na_values=0)
herschel_data = herschel_data.drop('Mrk3')
wise_data = pd.read_csv('/Users/ttshimiz/Github/bat-data/bat_wise.csv', index_col=0,
                        usecols=[0, 1, 2, 4, 5, 7, 8, 10, 11], na_values=0)
wise_data = wise_data.drop('Mrk3')
sed = herschel_data.join(wise_data[['W3', 'W3_err', 'W4', 'W4_err']])
names = sed.index.values

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

filt_use = np.array(['W3', 'W4', 'PACS70', 'PACS160', 'PSW', 'PMW', 'PLW'])
filt_err = np.array([s+'_err' for s in filt_use])
waves = np.array([12., 22., 70., 160., 250., 350., 500.])
ndetected = np.sum(np.isfinite(sed[filt_use].values), axis=1)

fig = plt.figure(figsize=(1.2*textwidth, 1.33*textwidth))
nseds_per_fig = 12
nfigs = np.int(np.ceil(np.float(len(names))/nseds_per_fig))

for i in range(nfigs):
    
    fig.clear()
    fig_names = names[i*nseds_per_fig:i*nseds_per_fig+nseds_per_fig]
    
    for j, n in enumerate(fig_names):
    
        subplot = j + 1
        ax = fig.add_subplot(4,3,subplot)
        
        pickle_file = ('/Users/ttshimiz/Github/bat-agn-sed-fitting/analysis/casey_bayes_results/beta_fixed_2_wturn_gaussianPrior/pickles/'
                       + n + '_casey_bayes_beta_fixed_2_wturn_gaussianPrior.pickle')
        f = open(pickle_file, 'rb')
        fit_results = pickle.load(f)
        model = fit_results['best_fit_model']
    
        src_sed = sed.loc[n][filt_use]
        src_err = sed.loc[n][filt_err]
        flux = np.array(src_sed, dtype=np.float)
        flux_err = np.array(src_err, dtype=np.float)
    
        fig_fit = plot_fit(waves, flux, model, obs_err=flux_err,
                           plot_components=True, plot_mono_fluxes=True,
                           filts=filt_use, plot_fit_spread=True,
                           name=n, plot_params=False, fig=fig, ax=ax)
                           
        if np.any(subplot == np.array([2,3,5,6,8,9,11,12])):
            ax.set_ylabel('')
        
        if (subplot < 10):
            ax.set_xlabel('')
        
    fig.subplots_adjust(wspace=0.3)
    fig.savefig(figsave_dir+'sedfig'+str(i+1)+'.pdf', bbox_inches='tight')
    
    
    

