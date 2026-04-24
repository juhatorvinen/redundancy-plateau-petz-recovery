import numpy as np
from qutip import *

"""
Petz recovery utility functions
"""

def inverse_sqrt_matrix(A: Qobj, cutoff=1e-6) -> Qobj:
    """
    Compute the inverse square root of a positive semidefinite matrix A
    using eigendecomposition.

    Parameters
    ----------
        A : Qobj
            Matrix / qobj to consider inverting
    Returns
    -------
        inv : Qobj
            Return pseudo inverse of the original Qobj
    """

    """
    Convert A into a dense array, find eigenvalues and vectors,
    consider only hermitian part by calculating A * A.dag() / 2
    """
    eigvals, eigvecs = np.linalg.eigh((A + A.dag()).full() / 2.0)

    # Calculate an "adaptive" cutoff value for the pseudo inverse based on the maximum of eigenvalues
    epsilon = cutoff * np.max(eigvals)

    # Regularization ~ ensure all eigenvalues are atleast >= epsilon, prevents for example dividing by 0
    eigvals = np.maximum(eigvals, epsilon)

    # Find diag(eigenvalues)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(eigvals))

    # Construct A^-1/2 = eigenvec * diag(eigenvalues) * eigenvec.dag()
    A_inv_sqrt = eigvecs @ D_inv_sqrt @ eigvecs.conj().T

    # Return Qobj im the same diemensions as original operator
    return Qobj(A_inv_sqrt, dims=A.dims)

def petz_map_states(noise_map, reference, format=None) -> Qobj:
    """
    The state-specific "normal" version of the Petz map. Creates said map in specified format, either as
    a pre, and post-prodcut superoperator or as a list of kraus operators!

    Parameters
    ----------
        noise_map : Qobj
            Give the noisy channel/map you want to try recovering as a superoperator
        
        reference : Qobj
            The reference which the Petz definition relies on. Input as a Qobj, for example by Qobj(data), where data is some numpy array etc.

        format : str
            Default when none is specified is a superoperator, but you can opt for the kraus by specifying "kraus"

    Returns
    -------
        petz : Qobj
            Returns the state-specific Petz map corresponding to a noisy map and a reference!
    """

    # Convert superoperator into kraus operators for map
    map_as_kraus = to_kraus(noise_map)

    # Construct the three different maps the petz is comprised of
    square_of_ref = reference.sqrtm(sparse=False, tol=0)
    map_reference = sum([K * reference * K.dag() for K in map_as_kraus])
    map_inverse = inverse_sqrt_matrix(A=map_reference)

    # Now using qutips pre and post products, construct total map
    inverse = spre(map_inverse) * spost(map_inverse)
    adjoint_map = sum([spre(K.dag()) * spost(K) for K in map_as_kraus])
    roots = spre(square_of_ref) * spost(square_of_ref)

    # From outside in, form the total map as P = A * B * C = A*B(C*C)B*A
    petz_as_super = (roots * adjoint_map * inverse).tidyup(atol=1e-14)

    # Format specifying
    if format == "kraus":
        return to_kraus(petz_as_super)
    
    else:
        return petz_as_super
