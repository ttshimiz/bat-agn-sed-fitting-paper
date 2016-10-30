# Script to check the upper limits for the 70 and 160 micron photometry

import numpy as np
import pandas as pd
import astropy.io.fits as fits
import astropy.coordinates as coord
import astropy.wcs as wcs
import photutils as pu
import astropy.units as u
import sys

sys.path.append('/Users/ttshimiz/Github/spire-catalog-photometry/')

import run_aperture_photometry as rap

# Upload the current Herschel photometry
bat_herschel = pd.read_csv('/Users/ttshimiz/Github/bat-data/bat_herschel.csv', index_col=0)
bat_info = pd.read_csv('/Users/ttshimiz/Github/bat-data/bat_info.csv', index_col=0)

#names = bat_herschel[bat_herschel['PACS160'] == 0].index
#names = ['2MASXJ20183871+4041003', '4U1344-60', 'AXJ1737.4-2907', '2MASXJ09023729-4813339', 'WKK4374']
names = ['WKK4374']
f = 'PACS160'
check_cirrus = pd.DataFrame(index=names, columns=['5-sig_ul_new', '5-sig_ul_old'])
for n in names:

    hdu_img = fits.open('/Users/ttshimiz/Dropbox/Herschel_Images/PACS/'+n+'_scanamorphos_pacs160_signal.fits')[0]
    hdu_err = fits.open('/Users/ttshimiz/Dropbox/Herschel_Images/PACS/'+n+'_scanamorphos_pacs160_error.fits')[0]
    #hdu_image = rap.prep_image(src_img, f)
    #hdu_err = rap.prep_image(err_img, f)
    im = hdu_img.data
    im_med, im_std = rap.estimate_bkg(im)
    thresh = im_med + 2.0*im_std
    segm_img = pu.detect_sources(im, thresh, npixels=5)
    props = pu.segment_properties(im-im_med, segm_img, wcs=wcs.WCS(hdu_img.header))
    ind_bat = rap.find_bat_source(coord_bat, props, 12.)
    
    ra_bat = bat_info.loc[n, 'RA_(J2000)']
    dec_bat = bat_info.loc[n, 'DEC_(J2000)']
    coord_bat = coord.SkyCoord(ra=ra_bat, dec=dec_bat, frame='fk5')
    
     
    #ap = pu.CircularAperture([88.368554, 70.88513], 7.71929)
    if ind_bat is None:
        ap, type = rap.create_spire_aperture(None, f, 'P', coord_bat=coord_bat, wcs=wcs.WCS(hdu_img.header))
    else:
        ap, type = rap.create_spire_aperture(props[ind_bat], f, 'P', extent=3.0, coord_bat=coord_bat, wcs=wcs.WCS(hdu_image.header))
    
    result, apertures = rap.spire_aperture_photometry(ap, hdu_img, hdu_err.data, 'point', f, pclass='P')
    
    print n, ':', result['total_err']*5
    
    check_cirrus.loc[n, '5-sig_ul_new'] = result['total_err']*5
    check_cirrus.loc[n, '5-sig_ul_old'] = bat_herschel.loc[n, 'PACS160_err']