import os
from geomdl import BSpline, knotvector
import numpy as np

def clean_files():
    for fname in ('xf_input.txt', 'xf_output.txt', 'xf_airfoil.txt', ':00.bl'):
        if os.path.exists(fname):
            os.remove(fname)

def cd_cl(airfoil, alpha):
    clean_files()

    af_x, af_y = airfoil
    with open('xf_airfoil.txt', 'w') as f:
        f.write('NACA Airfoil')
        for i in range(len(af_x)):
            f.write(f'\n{af_x[i]}  {af_y[i]}')

    with open('xf_input.txt','w') as f:
        f.write(f"""
load xf_airfoil.txt
PANE
OPER
VISC 3e6
PACC
xf_output.txt

a {alpha}
!
!

QUIT
""")
    os.system('xfoil < xf_input.txt > /dev/null')

    def parse_data(s):
        def remove_multiple_space(s):
            return s.replace('  ', ' ')
        for _ in range(4):
            s = remove_multiple_space(s)
        if s.startswith(' '):
            s = s[1:]
        res = []
        for i in s.split(' '):
            try:
                res.append(float(i))
            except ValueError:
                res.append(None)
        return res

    with open('xf_output.txt', 'r') as f:
        alpha, cl, cd, cdp, cm, _,_,_,_ = parse_data(f.readlines()[-1])

    clean_files()

    return cd, cl


from math import cos, sin, tan
from math import atan
from math import pi
from math import pow
from math import sqrt

def linspace(start,stop,np):
    return [start+(stop-start)*i/(np-1) for i in range(np)]

def naca4(m, p, t, n=400, finite_TE = False, half_cosine_spacing = False):
    """
    Returns 2*n+1 points in [0 1] for the given 4 digit NACA number string
    """

    m = m/100.0
    p = p/10.0
    t = t/100.0

    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843

    if finite_TE:
        a4 = -0.1015 # For finite thick TE
    else:
        a4 = -0.1036 # For zero thick TE

    if half_cosine_spacing:
        beta = linspace(0.0,pi,n+1)
        x = [(0.5*(1.0-cos(xx))) for xx in beta]  # Half cosine based spacing
    else:
        x = linspace(0.0,1.0,n+1)

    yt = [5*t*(a0*sqrt(xx)+a1*xx+a2*pow(xx,2)+a3*pow(xx,3)+a4*pow(xx,4)) for xx in x]

    xc1 = [xx for xx in x if xx <= p]
    xc2 = [xx for xx in x if xx > p]

    if p == 0:
        xu = x
        yu = yt

        xl = x
        yl = [-xx for xx in yt]

        xc = xc1 + xc2
        zc = [0]*len(xc)
    else:
        yc1 = [m/pow(p,2)*xx*(2*p-xx) for xx in xc1]
        yc2 = [m/pow(1-p,2)*(1-2*p+xx)*(1-xx) for xx in xc2]
        zc = yc1 + yc2

        dyc1_dx = [m/pow(p,2)*(2*p-2*xx) for xx in xc1]
        dyc2_dx = [m/pow(1-p,2)*(2*p-2*xx) for xx in xc2]
        dyc_dx = dyc1_dx + dyc2_dx

        theta = [atan(xx) for xx in dyc_dx]

        xu = [xx - yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yu = [xx + yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

        xl = [xx + yy * sin(zz) for xx,yy,zz in zip(x,yt,theta)]
        yl = [xx - yy * cos(zz) for xx,yy,zz in zip(zc,yt,theta)]

    X = xu[::-1] + xl[1:]
    Z = yu[::-1] + yl[1:]

    return X,Z

def nurbs(suc,pre,n=400):
    assert len(suc)==len(pre)
    xs = np.linspace(0,1,len(suc)+2).tolist()
    pts = np.array([
        xs[::-1] + xs[1:],
        [0] + suc[::-1] + [0] + pre + [0]
    ]).transpose().tolist()
    crv=BSpline.Curve()
    crv.degree=2
    crv.ctrlpts=pts
    crv.knotvector = knotvector.generate(crv.degree, crv.ctrlpts_size)
    airfoil = np.array([
        crv.evaluate_single(t) for t in np.linspace(0,1,n)
    ])
    return airfoil[:,0],airfoil[:,1]
