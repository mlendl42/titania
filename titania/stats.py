import numpy as np

def template_for_funcs(t, n=None):
    """
    description of what the function does: Function creates an array of equally spaced points in time

    Specify in parameters the input arguments (and the expected data type), and in returns, what the output of the function.

    write also the author of the function
    @tundeakins
    
    Parameters:
    -----------
    t : array;
        time stamps of the observation. 
    n: int;
        number of equally-spaced points to create.

    Returns:
    --------
    output: array-like;
        an smooth array of time 
    Example:
    --------
    >>> t = np.sort(np.random.randn(100)*100)     #randomly generated times
    >>> t_smooth = template_for_funcs(t, 1000)
    """
    return np.linspace(min(arg1),max(arg1), arg2)


def BF_from_BIC(del_BIC):
    """
    estimate bayes factor from delta BIC @tundeakins

    Parameters
    ----------
    del_BIC : float
        bayesian information criterion
    
    Returns:
    --------
    BF : float;
        the Bayes Factor
    """
    return np.exp(-del_BIC/2)

def bic(log_like, n, k):

    """
    Compute the bayesian information criteria @tundeakins
    
    Parameters:
    -----------
    
    log_like: array-like;
        The maximized value of the likelihood function of the model M.
    n: array-like;
        Number of data points in the observation.
    k: array-like;
        Number of parameters estimated by the model
        
    Returns:
    --------
    BIC: array-like input;
        The value of the Bayesian information Criterion. Model with lowest bic is preferred
        
    """
    import numpy as np
    return -2. * log_like + k * np.log(n)
    
def red_chisquare(data, model, error, npar):
    """
    Calculate the reduced chisquare, x2_red, given by sum(((data-model)/error)**2) / (len(data)-npar)
    if x2_red ~ 1, the model fits the data well.
    if x2_red << 1, the errors are overestimated, or the model is overfitting the data.
    if x2_red >> 1, the errors are underestimated, or the model is underfitting the data.
    @tundeakins

    Parameters:
    -----------
    data : array;
        the observed data.
    model : array-like data;
        calculated model to explain the data.
    error : array-like data;
        error on the observed data points.
    npar : int;
        number of fitted parameters in the model.
        
    Returns:
    --------
    x2_red : float;
        the reduced chisquare 
    """
    
    return np.sum(((data-model)/error)**2) / (len(data)-npar)
    
    
def aic(log_like, n, k):
    """
    The Aikake information criterion.
    A model comparison tool based of infomormation theory. It assumes that N is large i.e.,
    that the model is approaching the Central Limit Theorem. @tundeakins
    
    Parameters:
    -----------
    log_like: array-like;
        The maximized value of the likelihood function of the model M.
    n: array-like;
        Number of data points in the observation.
    k: array-like;
        Number of parameters estimated by the model
        
    Returns:
    --------
    AIC: array-like input;
        The value of the Akaike Information Criterion. Model with lowest aic is preferred
    """

    val = -2. * log_like + 2 * k
    val += 2 * k * (k + 1) / float(n - k - 1)

    if not np.isfinite(val):
        val = 0
        warnings.warn('AIC was NAN. Recording zero, but you should examine your fit.')

    return val
    
def r_squared(obs, calc):
    """
    Calculate the R2_score commonly referred to as coefficient of determination. It measure how close the regression line is to the  observed values. Best possible value is 1.0
    @tundeakins
    
	Parameters:
    ----------
    obs : array-like;
            array of observed values
    calc : array-like;
            array of calculated values e.g from model
    Return:
    --------
    r2 : float;
            r2_score value
    """      
  
    return 1 - (np.sum(np.square(obs-calc)) / np.sum(np.square(obs-np.mean(obs))) )