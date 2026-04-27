import numpy as np
from qutip import rand_ket, Qobj, basis, tensor, ket2dm, qload, sigmax, sigmay, sigmaz, qeye, rand_unitary

"""
File for quick utilities accessed in main simulations.
"""

def generate_complex_array(n: int, type: str, low_lim: float, hgh_lim: float, seed=None,  matrix=False, dim1=None, dim2=None, order=None) -> np.ndarray:
    """
    Create an array of n random complex numbers with real and imaginary parts 
    distributed between low_lim and hgh_lim based on type of distribution.

    Parameters:
        n : int 
            number of divisions for distribution

        type : str 
            distribution type - "uniform", "normal", "gamma"

        seed : int 
            seed input for numpy random seed

        low_lim : float 
            lower limit for distribution

        hgh_lim : float 
            cap for distribution

        matrix : Bool 
            Default False. Whether you want the array to be in a ndarray format
            of dimensions (dim1, dim2), used for the bath to environment coefficients.

        order : str 
            Type of order you want the array to be in.
            Default is None, corresponding to a disordered, random array of numbers
            drawn according to the other parameters. "ordered" for an array of length
            n with each entry being "low_lim + i*hgh_lim". Note that something inbetween,
            a semi-ordered array may be created by setting low_lim and hgh_lim very close
            and just running the normal array creation.

    Returns
    -------
    array : np.ndarray
        Returns a numpy array according to specifications.

    """

    #if seed was given, set it
    rng = np.random.default_rng()

    if seed is not None:
        rng = np.random.default_rng(seed=seed)

    #if a strictly ordered array was desired, produce it immidiately
    if order == "ordered":

        if not matrix:
            return np.array([low_lim + 1j * hgh_lim] * n)
        else:
            return np.full(shape=(dim1, dim2), fill_value=(low_lim + 1j * hgh_lim))
    
    else:

        if type == "uniform":

            #Create real and imaginary parts of each entry in the array
            if not matrix:

                real_parts = rng.uniform(low_lim, hgh_lim, n)
                imag_parts = rng.uniform(low_lim, hgh_lim, n)

                #sum to create complex array, C = a + ib, where i == j in python
                #and return array
                return (real_parts + 1j * imag_parts)
            
            else:

                #create matrix with same format as above
                real_parts = rng.uniform(low_lim, hgh_lim, (dim1, dim2))
                imag_parts = rng.uniform(low_lim, hgh_lim, (dim1, dim2))

                return (real_parts + 1j * imag_parts)
        
        elif type == "normal":

            if not matrix:
            
                #same principle, but centered at average of given interval
                #with a default width of 1 centered at average of given interval

                real_parts = rng.normal((hgh_lim + low_lim) / 2, 1, n)
                imag_parts = rng.normal((hgh_lim + low_lim) / 2, 1, n)

                return (real_parts + 1j * imag_parts)
            
            else:

                #create matrix with same principle
                real_parts = rng.normal((hgh_lim + low_lim) / 2, 1, (dim1, dim2))
                imag_parts = rng.normal((hgh_lim + low_lim) / 2, 1, (dim1, dim2))

                return (real_parts + 1j * imag_parts)
        
        elif type == "gamma":

            if not matrix:

                #again, same principle but a gamma distr. with a scale of one
                #and the "peak" at average of given interval

                shape = (hgh_lim + low_lim) / 2

                real_parts = rng.gamma(shape, scale=1.0, size=n)
                imag_parts = rng.gamma(shape, scale=1.0, size=n)

                return (real_parts + 1j * imag_parts)
            
            else:

                #create matrix with same principle
                shape = (hgh_lim + low_lim) / 2

                real_parts = rng.gamma(shape, scale=1.0, size=(dim1, dim2))
                imag_parts = rng.gamma(shape, scale=1.0, size=(dim1, dim2))

                return (real_parts + 1j * imag_parts)
            

        
        else:
            raise ValueError("type parameter needed....")

def generate_real_array(n, type: str, low_lim: float, hgh_lim: float, seed=None, matrix=False, dim1=None, dim2=None, order=None) -> np.ndarray:
    """
    Create an array of n random real numbers distributed between
    low_lim and hgh_lim according to given distribution type.

    Parameters
    ----------
        n : int 
            number of divisions for distribution
        type : str 
            distribution type - "uniform", "normal", "gamma"
        seed : int
            seed input for numpy random seed
        low_lim : float
            lower limit for distribution
        hgh_lim : float 
            cap for distribution

        matrix : Bool
            Whether you want the array to be in a ndarray format
            of dimensions (N,M), used for the bath to environment coefficients.

        order : str
            Type of order you want the array to be in.
            Default is None, corresponding to a disordered, random array of numbers
            drawn according to the other parameters. "ordered" for an array of length
            n with each entry being "low_lim". Note that something inbetween,
            a semi-ordered array may be created by setting low_lim and hgh_lim very close
            and just running the normal array creation.
        
    Returns
    -------
    array : np.ndarray
        Returns a numpy array according to specifications.

        """

    rng = np.random.default_rng()


    #if seed was given, set it
    if seed is not None:
        rng = np.random.default_rng(seed=seed)

    if order == "ordered":

        if not matrix:
            return np.full(shape=n, fill_value=low_lim)
        else:
            return np.full(shape=(dim1, dim2), fill_value=hgh_lim)


    else:
        if type == "uniform":

            if not matrix:

                #Create real parts of each entry in the array
                return rng.uniform(low_lim, hgh_lim, n)
            
            else:
                return rng.uniform(low_lim, hgh_lim, size=(dim1, dim2))
        
        elif type == "normal":
            
            if not matrix:
                #same principle, but centered at average of given interval
                #with a default width of 1 centered at average of given interval
                return rng.normal((hgh_lim + low_lim) / 2, 1, n)
            else:
                return rng.normal((hgh_lim + low_lim) / 2, 1, (dim1, dim2))
        
        elif type == "gamma":

            shape = (hgh_lim + low_lim) / 2

            if not matrix:
                #again, same principle but a gamma distr. with a scale of one
                #and the "peak" at average of given interval
                return rng.gamma(shape, scale=1.0, size = n)
            else:
                return rng.gamma(shape, scale=1.0, size = (dim1, dim2))
        else:
            raise ValueError("type parameter needed....")

def generate_state_from_coords(coordinates) -> Qobj:

    """
    Generate any qubit density matrix expanded in terms of the identity operator
    and Bloch vector + Pauli operators. 

    Parameters
    ----------
    coordinates : tuple or array-like
        Organize the spherical coordinates on the Bloch sphere such that
        we have (r, theta, phi) or [r, theta, phi] etc.
    
    Returns
    -------
    dm : Qobj
        Returns the Qobj that corresponds to 1/2 * (identity + r * (sigma_x, sigma_y, sigma_z))
    """

    # extract coordinates
    r = coordinates[0]
    theta = coordinates[1]
    phi = coordinates[2]

    # create a qubit state by using the identity + pauli matrices representation in polar cordinates
    dm = 1 / 2 * (qeye(2) + r*np.sin(theta)*np.cos(phi)*sigmax() + r*np.sin(theta)*np.sin(phi)*sigmay() + r*np.cos(theta)*sigmaz())
    return dm

def gue_hermitian(N: int, rng) -> Qobj:
    """
    Construct Hermitian matrices according to the GUE(N) ensamble, i.e.
    the ensamble of Gaussian unitary enxamble of N x N hermitian matrices.

    Parameters
    ----------
    N : int
        Dimension(s) of square matrix
    rng : Generator instance -like
        Give random number generator, e.g. np.random.default_rng()
        which is created outside of the function.
    
    Returns
    -------
    H : Qobj
        N x N hermitian matrix in QuantumObject form

    """

    """
    First, we draw N number of real-valued Gaussian numbers
    with mean 0, variance 1 as per the "standard" normal
    distribution. These numbers are then placed on the diagonal
    of a square matrix, and the variance is scaled to be in accordance
    with 2/N.
    """
    H = np.diag(rng.standard_normal(N)).astype(complex) * np.sqrt(2/N)

    """
    After building diagonal entries, the off-diagonal elements
    are built such that H_ij = x + i*y, H_ji = H_ij^dagger, and
    x,y are pulled again from standard normal distributions with
    variance scaled to be 1/(2N).
    """
    for i in range(N):
        for j in range(i+1, N):

            # prepare complex entries
            x, y = rng.standard_normal(2) / np.sqrt(2*N)

            # set all off-diagonal elements
            H[i, j] = x + 1j*y
            H[j, i] = x - 1j*y

    # return final
    return Qobj(H)

def xi_unitaries(r, g_l, t, xi_obs, gamma_obs):
    """
    Generate the time evolution operator governing
    the evolution of the states of the environment Xi.

    Parameters
    ----------
    r : int
        Indexing parameter from the definition to access correct terms from 
        the system's observable
    g_l : float
        Coupling strength between the system and the l:th qubit
    t : float
        The time step to which one considers evoulution to
    xi_obs : Qobj
        The environment qubit's observable in the coupling
    gamma_obs : Qobj
        The system's observable in the coupling

    Returns
    -------
    U : Qobj
        The unitary time evolution operator for the l:th qubit in the environment

    """

    # find correct diagonal term of system's observable
    omega_r = gamma_obs.full()[r,r]

    # create term operator to exponate and unitary
    exp = -1j * omega_r * t * g_l * xi_obs
    U = exp.expm()

    # return unitary
    return U

def decoherence_gamma(N, coeff, g_k, t, t_0=0):

    """
    A quick and simple function for creating the product sum functions on the off-diagonal
    terms caused by the CPTP decoherence map!

    Parameters
    ----------
    N : int
        Number of qubits in the environment and number of terms in the product sum
    coeff : array-like
        Array-like object containing the population terms of the states in the enviroment.
    g_k : array-like
        Array of coupling constants. Should be of length N.
    t : float
        A time value to calculate the product sum to. Probably pulled from an array.
    t_0 : float
        Starting time. Defaults to zero for ease of use but can be defined separately for other use.

    Returns
    -------
    gamma : float
        Value of the prodcut sum, which is just a number.
    """

    # init value of function
    gamma = 1

    # product series with N terms, picking corresponding values from arrays
    for i in range(N):

        # coefficients of the state of the environment
        alpha = coeff[i][0]
        beta = coeff[i][1]

        #coupling constant
        g = g_k[i]

        # create term and calculate product in to the term
        term = (alpha * np.exp(-2j * g * (t-t_0)) + beta * np.exp(2j * g * (t-t_0)))
        gamma *= term

    return gamma

