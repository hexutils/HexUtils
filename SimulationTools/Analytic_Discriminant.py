import numpy as np
import vector
import awkward as ak
import sympy
import numba as nb

@nb.vectorize([nb.float64(nb.complex128),nb.float32(nb.complex64)])
def abs2(x):
    return x.real**2 + x.imag**2

@nb.vectorize([nb.float64(nb.complex128),nb.float32(nb.complex64)])
def abs(x):
    return np.sqrt(x.real**2 + x.imag**2)

class Analytic_Discriminant(object):
    def __init__(
        self, 
        g1, g2, g4,
        mV, mX
        ):
        self.g = np.array((g1, g2, g4), dtype=np.float64)
        self.lep_1 = None
        self.lep_2 = None
        self.lep_3 = None
        self.lep_4 = None
        
        self.mV = mV
        self.mX = mX
    
    def set_couplings(
        self,
        g1, g2, g4
    ):
        self.g = np.array((g1, g2, g4))
    
    def input_vectors(
        self,
        m1, m2, costheta1, costheta2, phi
    ):
        self.m1 = np.array(m1)
        self.m2 = np.array(m2)
        self.theta1 = np.arccos(np.array(costheta1))
        self.theta2 = np.arccos(np.array(costheta2))
        self.phi = np.array(phi)
        
        temp_numerator = self.mX**2 - self.m1**2 - self.m2**2
        self.s = (temp_numerator)/2
        self.x = (temp_numerator/(2*self.m1*self.m2))**2 - 1
        self.VeV = 246.22 #GeV
        self.dGammaV = 2.4955 #for V=Z
        
        if len(m1) != len(m2) != len(costheta1) != len(costheta2) != len(phi):
            raise ValueError("All inputs must be the same length!")
        
        self.n = len(m1)
    
    def _gToA(
        self
    ):
        a1 = (self.mV/self.mX)**2*self.g[0]
        a1 += 2*self.s/(self.mX**2)*self.g[1]
        
        a2 = np.full(len(a1), -2*self.g[1], dtype=np.float64)
        a3 = np.full(len(a1), -2*self.g[2], dtype=np.float64)

        return a1, a2, a3
    
    @staticmethod
    @nb.njit(fastmath=True, cache=True)
    def _amplitudes(
        x,
        mX, m1, m2,
        a1, a2, a3,
        VeV, A
    ):
        temp_fac = m1*m2/(mX**2)
        sqrt_x = np.sqrt(x)
        multiplier = mX**2/VeV
        
        A[1] = -(a1*np.sqrt(1 + x) + a2*x*(temp_fac))
        
        A[0] = a1 + a3*temp_fac*sqrt_x*1j
        
        A[2] = a1 - A[0].imag*1j
        A *= multiplier
    
    @staticmethod
    @nb.njit(fastmath=True, cache=True)
    def _calculate_5d_space(
        APP, A00, AMM,
        theta1, theta2, phi
    ):
        Af1 = 0.14876764
        t1 = abs2(A00)*(2*np.sin(theta1)*np.sin(theta2))**2
        
        t2 = abs2(APP)
        t3 = abs2(AMM)
        
        nonzero_indices = (A00 != 0)
        t4 = np.zeros(len(A00))
        t4[nonzero_indices] = (
            4*abs(A00[nonzero_indices])*
            abs(APP[nonzero_indices])*
            np.cos(phi[nonzero_indices] + np.angle(APP[nonzero_indices]/A00[nonzero_indices]))
        )
        t5 = np.zeros(len(A00))
        t5[nonzero_indices] = (
            4*abs(A00[nonzero_indices])*
            abs(APP[nonzero_indices])*
            np.cos(phi[nonzero_indices] - np.angle(AMM[nonzero_indices]/A00[nonzero_indices]))
        )

        for i in (theta1, theta2):
            t2 *= (1 + 2*Af1*np.cos(i) + (np.cos(i))**2)
        
            t3 *= (1 - 2*Af1*np.cos(i) + (np.cos(i))**2)
        
            t4 *= (Af1 + np.cos(i))*np.sin(i)
        
            t5 *= (Af1 - np.cos(i))*np.sin(i)
        
        t6 = 2*abs(APP)*abs(AMM)*np.cos(2*phi + np.angle(APP/AMM))
        t6 *= (np.sin(theta1)*np.sin(theta2))**2
        
        return (t1+t2+t3+t4+t5+t6).astype(np.complex128)
    
    @staticmethod
    @nb.njit(fastmath=True, cache=True)
    def _propagator(
        m1, m2,
        mV, mX,
        dGammaV
    ):
        prop = np.sqrt(
            (1 - ((m1 + m2)/mX)**2)*(1 - ((m1 - m2)/mX)**2) + 0j
        )
        temp_fac = (mV*dGammaV)**2
        for mi in (m1 , m2):
            prop *= mi**3/((mi**2 - mV**2)**2 + temp_fac)
        return prop
    
    def discr(
        self
    ):
        a1, a2, a3 = self._gToA()
        A = np.zeros(
            (3, self.n), np.complex128 #rows are A++, A00, A--
        )
        self._amplitudes(
            self.x,
            self.mX, self.m1, self.m2,
            a1, a2, a3, self.VeV,
            A
        )
        # print(A)
        num = self._calculate_5d_space(
            *A.copy(),
            self.theta1, self.theta2, self.phi
        )
        prop = self._propagator(
            self.m1, self.m2,
            self.mV, self.mX,
            self.dGammaV
        )
        num *= prop
        return num.real
