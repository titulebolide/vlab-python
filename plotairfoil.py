import matplotlib.pyplot as plt
import numpy as np
import vlab

D = []
L = []
A = []

xfoil = vlab.Xfoil()

for alpha in np.arange(-3,10,0.5):
    cd, cl = xfoil.cd_cl(vlab.naca4(0,0,12), alpha)
    print(cd, cl)
    if cd is not None and cl is not None:
        D.append(cd)
        L.append(cl)
        A.append(alpha)
D = np.array(D)
L = np.array(L)
A = np.array(A)


plt.subplot(1,2,1)
plt.scatter(D,L)
plt.grid()
plt.title('Polar')
plt.subplot(1,2,2)
plt.plot(A,L/D)
plt.grid()
plt.title('$C_L/C_D$ vs AoA')
plt.show()
