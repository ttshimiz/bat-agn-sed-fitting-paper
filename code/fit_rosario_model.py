# Fit the Rosario+12 model to our BAT AGN data

import numpy as np
import emcee
from astropy.modeling import Fittable1DModel, Parameter
from scipy.special import erf

def log_like(dummy, x, xerr, y, yerr, flag, nsig):
    
    detected = (flag == 1)
    y_model = dummy(x)
    alpha = dummy.parameters[2]
    beta = dummy.parameters[1]
    sigsqr = dummy.parameters[3]
    sig_total_detected = (alpha/(1+(10**((x[detected]-beta)*alpha)))*xerr[detected])**2 + yerr[detected]**2 + sigsqr
    sig_total_undetected = (alpha/(1+(10**((x[~detected]-beta)*alpha)))*xerr[~detected])**2 + (y[~detected]/nsig[~detected])**2 + sigsqr
    llike_detected = -0.5*(np.sum((y[detected]-y_model[detected])**2/sig_total_detected +
                                   np.log(2*np.pi*sig_total_detected)))
    llike_undetected = np.log(0.5*(1+erf((y[~detected]-y_model[~detected])/(sig_total_undetected*np.sqrt(2)))))
    
    llike_undetected[np.isinf(llike_undetected)] = -743.0
        
    return llike_detected + np.sum(llike_undetected)
    

def log_prior(params, model, fixed):

    pnames = np.array(model.param_names)
    bounds = np.array([model.bounds[n] for n in model.param_names])
    bounds = bounds[~fixed]
    lp = np.array(map(uniform_prior, params, bounds))

    return sum(lp)
    

def log_post(params, x, xerr, y, yerr, flag, nsig, model, fixed):

    lprior = log_prior(params, model, fixed)
    if not np.isfinite(lprior):
        return -np.inf
    else:
        dummy = model.copy()
        dummy.parameters[~fixed] = params
        llike = log_like(dummy, x, xerr, y, yerr, flag, nsig)
        if not np.isfinite(llike):
            return -np.inf
        else:
            return lprior + llike

def uniform_prior(x, bounds):

    if bounds[0] is None:
        bounds[0] = -np.inf
    if bounds[1] is None:
        bounds[1] = np.inf

    if (x >= bounds[0]) & (x <= bounds[1]):
        return 0
    else:
        return -np.inf
        
 
class RosarioModel(Fittable1DModel):
    
    sfr0 = Parameter(default=0.0, bounds=(-2.0, 2.0))
    lx0 = Parameter(default=43.5, bounds=(41.0, 46.0))
    alpha = Parameter(default=0.8, bounds=(0.0, 4.0))
    sigsqr = Parameter(default=0.1, bounds=(0.0, None))
    
    def __init__(self, sfr0, lx0, alpha):
        self.chain = None
        self.chain_nb = None
        self.param_errs = None
        super(RosarioModel, self).__init__(sfr0, lx0, alpha)
        
    
    def evaluate(self, x, sfr0, lx0, alpha, sigsqr):
    
         return np.log10(10**(sfr0) + 10**(sfr0)*(10**x/10**lx0)**alpha)


def fit_model(lx, lx_err, sfr, sfr_err, flags, nsig, model,
              nwalkers=50, nsteps=1000, nburn=200, threads=8):


    fixed = np.array([model.fixed[n] for n in model.param_names])
    ndims = np.sum(~fixed)
    init = model.parameters[~fixed]
    init_walkers = [init + 1e-4*np.random.randn(ndims)
                    for k in range(nwalkers)]
                    
    mcmc = emcee.EnsembleSampler(nwalkers, ndims, log_post,
                                 args=(lx, lx_err, sfr, sfr_err, flags, nsig, model, fixed),
                                 threads=threads)
    
    mcmc.run_mcmc(init_walkers, nsteps)
    model.chain = mcmc.chain[:, :, :].reshape(-1, ndims)
    model.chain_nb = mcmc.chain[:, nburn:, :].reshape(-1, ndims)
    
    if threads > 1:
        mcmc.pool.close()
    
    model.parameters[~fixed] = np.median(model.chain_nb, axis=0)
    model.param_errs = np.zeros((len(model.parameters), 6))
    model.param_errs[~fixed] = np.percentile(model.chain_nb, q=[2.5, 5., 16, 84, 95., 97.5], axis=0).T
    
    return model
    
    

    
    
