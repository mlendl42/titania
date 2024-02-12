from scipy.signal import medfilt
import numpy as np
import matplotlib.pyplot as plt
import os

def clip_outliers(x, y, yerr = None, clip=5, width=15, verbose=True, return_clipped_indices = False):

    """
    Remove outliers using a running median method. Points > clip*M.A.D are removed
    where M.A.D is the mean absolute deviation from the median in each window
    @tundeakins
    Parameters:
    ----------
    x: array_like;
        dependent variable.
        
    y: array_like; same shape as x
        Depedent variable. data on which to perform clipping
        
    yerr: array_like(x);
        errors on the dependent variable
        
    clip: float;
       cut off value above the median. Default is 5
    
    width: int;
        Number of points in window to use when computing the running median. Must be odd. Default is 15
        
    Returns:
    --------
    x_new, y_new, yerr_new: Each and array with the remaining points after clipping
    
    """
    dd = abs( medfilt(y-1, width)+1 - y)   #medfilt pads with zero, so filtering at edge is better if flux level is taken to zero(y-1)
    mad = dd.mean()
    ok= dd < clip * mad

    if verbose:
        print('\nRejected {} points more than {:0.1f} x MAD from the median'.format(sum(~ok),clip))
    
    if yerr is None:
        if return_clipped_indices:
            return x[ok], y[ok], ~ok
            
        return x[ok], y[ok]
    
    if return_clipped_indices:
        return x[ok], y[ok], yerr[ok], ~ok
    
    return x[ok], y[ok], yerr[ok]



def phase_fold(t, period, t0):
    """

    Phasefold data on the give period
    
    Parameters:
    ----------- 
    t: array_like;
        array of times
    period: float;
        period
    t0: float;
    	reference time
    
    Returns:
    --------
    phases: array_like;
        array of phases (not sorted)	
    """
    return ((t - t0 + 0.5*period)%period - 0.5*period )/period


def resolution_calculator(input_wavelength):
    
    '''
    This function calculate the resolution of your input spectrum 
    '''
    R_grid= (input_wavelength[1:-1]+input_wavelength[0:-2])/ (input_wavelength[1:-1]-input_wavelength[0:-2])/2
    
    return np.median(R_grid)

def convolving_spectrum(wave_new, HigherRes_wave, HigherRes_flux,):
    from astropy.convolution import convolve_fft
    from astropy.convolution import Gaussian1DKernel
    '''
    This function convolves a high-resoltion spectrum to any specified resolution using a Gaussian 1-d kernel. 
    
    '''
    
    # Measuring spectral Resolution
    R_LowerRes= resolution_calculator(wave_new)
    R_HigherRes= resolution_calculator(HigherRes_wave)
    
    sigma= R_HigherRes/ R_LowerRes
    
    gauss = Gaussian1DKernel(stddev=sigma)
    f_conv= convolve_fft(HigherRes_flux, gauss)
    
    LowerRes_flux= np.interp(wave_new, HigherRes_wave, f_conv)
    
    
    return wave_new, LowerRes_flux


def transit_SNR(D,sigma,T14,T23=None,n=1):
    """
    calculate the signal-to-noise ratio of a trapazoidal transit. according to kipping2023(https://arxiv.org/abs/2305.06790)
    @tundeakins

    Parameters
    ----------
    D : float
        transit depth in ppm
    sigma : float
        noise per unit of time in ppm
    T14 : float
        total transit duration
    T23 : float, optional
        duration of flat bottom transit , by default 0  
    n : int, optional
        number of transits, by default 1

    Returns:
    --------
    snr: float
        signal-to-noise ratio
    """
    noise = sigma/np.sqrt(n)
    if T23 == None:
        snr =  D/noise  *  np.sqrt( T14 )
    else:
        snr = D/noise  *  np.sqrt( (T14+2*T23)/3 )
    return snr