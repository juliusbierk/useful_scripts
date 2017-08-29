import numpy as np
from scipy.misc import factorial
import scipy.linalg

def diones(N, offset):
	return np.diag(np.ones(N-abs(offset)),offset)

def make_operators(s):
	ds = s[1] - s[0]
	N = len(s)

	A = np.eye(N)

	A1 = (diones(N, 1) - diones(N, -1))/(2*ds)
	A1[0,0] = -1/ds; A1[0,1] = 1/ds
	A1[-1,-2] = -1/ds; A1[-1,-1] = 1/ds

	A2 = (1*diones(N, 1) + 1*diones(N, -1) - 2*diones(N, 0))/ds**2
	A2[0,:4] = np.array([2,-5,4,-1])/ds**2
	A2[-1,-4:] = np.array([2,-5,4,-1])[::-1]/ds**2

	A3 = (-0.5*diones(N, -2) + diones(N, -1) - diones(N, 1) + 0.5*diones(N, 2))/ds**3
	A3[(0,1,-2,-1),:] = 0
	A3[0,:5] = np.array([-5/2.,9,-12,7,-3/2.])/ds**3
	A3[1,1:6] = np.array([-5/2.,9,-12,7,-3/2.])/ds**3
	A3[-1,-5:] = -np.array([-5/2.,9,-12,7,-3/2.])[::-1]/ds**3
	A3[-2,-6:-1] = -np.array([-5/2.,9,-12,7,-3/2.])[::-1]/ds**3

	A4 = (diones(N, -2) - 4*diones(N, -1) + 6*diones(N, 0) - 4*diones(N, 1) + diones(N, 2))/ds**4
	A4[(0,1,-1,-2),:] = 0
	A4[0,:6] = np.array([3,-14,26,-24,11,-2])/ds**4
	A4[1,1:7] = np.array([3,-14,26,-24,11,-2])/ds**4
	A4[-1,-6:] = np.array([3,-14,26,-24,11,-2])[::-1]/ds**4
	A4[-2,-7:-1] = np.array([3,-14,26,-24,11,-2])[::-1]/ds**4

	Int = np.ones(N)*ds # trapz rule
	Int[0] /= 2.0
	Int[-1] /= 2.0

	return A, A1, A2, A3, A4, Int


def finite_diff_coeffs(stencil, deriv):
	A = np.array([stencil**n for n in range(len(stencil))])
	b = np.zeros(len(stencil))
	b[deriv] = factorial(deriv)

	return scipy.linalg.solve(A, b)

def make_operator(x, order, deriv):
	W = np.zeros((len(x), len(x)))
	
	i0 = 0
	i1 = order + 1
	for i in range(len(x)):
		coeffs = finite_diff_coeffs(x[i0:i1] - x[i], deriv)
		W[i, i0:i1] = coeffs

		if (i0+i1)//2 == i and i1+1 <= len(x):
			i0 += 1
			i1 += 1
	return W

def make_operators2(s, order=4):
	N = len(s)
	A = np.eye(N)
	A1 = make_operator(s, order, 1)
	A2 = make_operator(s, order, 2)
	A3 = make_operator(s, order, 3)
	A4 = make_operator(s, order, 4)
	ds = s[1] - s[0]
	Int = np.ones(N)*ds # trapz rule
	Int[0] /= 2.0
	Int[-1] /= 2.0

	return A, A1, A2, A3, A4, Int

if __name__ == '__main__':
	import numpy as np 
	import matplotlib.pyplot as plt
	s = np.linspace(0, 60, 100)
	A, A1, A2, A3, A4, Int = make_operators(s)
	A_2, A1_2, A2_2, A3_2, A4_2, Int = make_operators2(s, order=5)

	plt.plot(A4[0,:])
	plt.plot(A4_2[0,:])

	plt.show()
