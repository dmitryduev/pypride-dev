# from numba import jit
# import time
import numpy as np
import os
from jplephem.spk import SPK


def lagint(npo, xi, yi, xo):
    """
     Lagrange interpolation
    :param npo: number of points to use = order + 1
    :param xi: input x's
    :param yi: input y's
    :param xo: interpolation point(s)
    :return:
    """
    l = len(xo) if hasattr(xo, '__len__') else 1
    m = len(xi)

    # np - number of points = order + 1
    # order of the interpolant must be <= m
    if npo > m:
        npo = m

    wl = int(np.floor(npo / 2))
    wr = int(np.ceil(npo / 2))

    y = np.empty(l)
    dy = np.empty(l)

    for k in range(l):
        xok = xo[k] if hasattr(xo, '__len__') else xo
        # nearest nod in the grid right to xo, number of elements left to xo:
        nl = int(np.searchsorted(xi, xok))
        # number of elements right to xo
        nr = m - nl
        # cut npo points around xo
        if wl > nl:
            xin = xi[0: npo]
            yin = yi[0: npo]
        elif wr > nr:
            xin = xi[m - npo:]
            yin = yi[m - npo:]
        else:
            xin = xi[nl - wl: nl + wr]
            yin = yi[nl - wl: nl + wr]
        # print(xin, yin)
        # Perform the Lagrange interpolation with the Aitken method. y: interpolated value. dy: error estimated.
        for i in range(1, npo + 1):
            for j in range(1, npo - i + 1):
                xi1 = xin[j - 1]
                xi2 = xin[j + i - 1]
                fi1 = yin[j - 1]
                fi2 = yin[j]
                # print(i, j, '\t', xi1, xi2, fi1, fi2)
                yin[j - 1] = (xok - xi1) / (xi2 - xi1) * fi2 + (xok - xi2) / (xi1 - xi2) * fi1

        y[k] = yin[0]
        dy[k] = (abs(y[k] - fi1) + abs(y[k] - fi2)) / 2.

    return y, dy


def lagintd(npo, xi, yi, xo):
    """
     Lagrange interpolation with differentiation
    :param npo: number of points to use = order + 1
    :param xi: input x's
    :param yi: input y's
    :param xo: interpolation point(s)
    :return:
    """
    l = len(xo) if hasattr(xo, '__len__') else 1
    m = len(xi)

    # np - number of points = order + 1
    # order of the interpolant must be <= m
    if npo > m:
        npo = m

    wl = int(np.floor(npo / 2))
    wr = int(np.ceil(npo / 2))

    y = np.empty(l)
    dy = np.empty(l)

    q = np.empty((npo, npo))
    dq = np.empty((npo, npo))

    for k in range(l):
        xok = xo[k] if hasattr(xo, '__len__') else xo
        # nearest nod in the grid right to xo, number of elements left to xo:
        nl = int(np.searchsorted(xi, xok))
        # number of elements right to xo
        nr = m - nl
        # cut npo points around xo
        if wl > nl:
            xin = xi[0: npo]
            yin = yi[0: npo]
        elif wr > nr:
            xin = xi[m - npo:]
            yin = yi[m - npo:]
        else:
            xin = xi[nl - wl: nl + wr]
            yin = yi[nl - wl: nl + wr]
        # print(xin, yin)

        # Perform the Lagrange interpolation with differentiation with the Aitken method.

        q[:, 0] = yin

        for i in range(1, npo):
            for j in range(1, i + 1):
                xi1 = xin[i - j]
                xi2 = xin[i]
                fi1 = q[i, j - 1]
                fi2 = q[i - 1, j - 1]
                q[i, j] = ((xok - xi1) * fi1 - (xok - xi2) * fi2) / (xi2 - xi1)

        for j in range(1, npo):
            dq[j, 1] = (q[j, 0] - q[j - 1, 0]) / (xin[j] - xin[j - 1])

        for i in range(2, npo):
            for j in range(2, i + 1):
                xi1 = xin[i - j]
                xi2 = xin[i]
                fi1 = dq[i, j - 1]
                fi2 = dq[i - 1, j - 1]
                dq[i, j] = ((xok - xi1) * fi1 - (xok - xi2) * fi2) / (xi2 - xi1)
                fi1 = q[i, j - 1]
                fi2 = q[i - 1, j - 1]
                dq[i, j] = dq[i, j] + (fi1 - fi2) / (xi2 - xi1)

        y[k] = q[-1, -1]
        dy[k] = dq[-1, -1]

    return y, dy


homedir = os.environ['HOME']

cache_dir = os.path.join(homedir, '.pypride')
cats_dir = os.path.join(cache_dir, 'cats')
eph_dir = os.path.join(cache_dir, 'jpl_eph')

kernels = {'de403': SPK.open(os.path.join(eph_dir, 'de403.bsp')),
           'de405': SPK.open(os.path.join(eph_dir, 'de405.bsp')),
           'de421': SPK.open(os.path.join(eph_dir, 'de421.bsp')),
           'de430': SPK.open(os.path.join(eph_dir, 'de430.bsp'))}


def pleph(jd, ntarg: int, ncent: int = 12, namfil: str = 'de430'):
    """
        Mimic the old fortran subroutine:

    !     THIS SUBROUTINE READS THE JPL PLANETARY EPHEMERIS
    !     AND GIVES THE POSITION AND VELOCITY OF THE POINT 'NTARG'
    !     WITH RESPECT TO 'NCENT'.
    !     NTARG = INTEGER NUMBER OF 'TARGET' POINT.
    !
    !     NCENT = INTEGER NUMBER OF CENTER POINT.
    !
    !            THE NUMBERING CONVENTION FOR 'NTARG' AND 'NCENT' IS:
    !
    !                1 = MERCURY           8 = NEPTUNE
    !                2 = VENUS             9 = PLUTO
    !                3 = EARTH            10 = MOON
    !                4 = MARS             11 = SUN
    !                5 = JUPITER          12 = SOLAR-SYSTEM BARYCENTER
    !                6 = SATURN
    !                7 = URANUS
    :param jd:
    :param ntarg:
    :param ncent:
    :param namfil:
    :return:
    """
    kernel = kernels[namfil]

    if ncent == 12:  # SSB
        if ntarg == 3:  # earth
            p1, v1 = kernel[0, 3].compute_and_differentiate(jd)
            p2, v2 = kernel[3, 399].compute_and_differentiate(jd)
            p = p1 + p2
            v = v1 + v2
        elif ntarg == 10:  # moon
            p1, v1 = kernel[0, 3].compute_and_differentiate(jd)
            p2, v2 = kernel[3, 301].compute_and_differentiate(jd)
            p = p1 + p2
            v = v1 + v2
        elif ntarg == 11:  # sun
            p, v = kernel[0, 10].compute_and_differentiate(jd)
        else:
            p, v = kernel[0, ntarg].compute_and_differentiate(jd)
    else:
        if ntarg == 12:  # SSB
            p1, v1 = 0.0, 0.0
        elif ntarg == 3:  # earth
            p1, v1 = kernel[0, 3].compute_and_differentiate(jd)
            p11, v11 = kernel[3, 399].compute_and_differentiate(jd)
            p1 += p11
            v1 += v11
        elif ntarg == 10:  # moon
            p1, v1 = kernel[0, 3].compute_and_differentiate(jd)
            p11, v11 = kernel[3, 301].compute_and_differentiate(jd)
            p1 += p11
            v1 += v11
        elif ntarg == 11:  # sun
            p1, v1 = kernel[0, 10].compute_and_differentiate(jd)
        else:
            p1, v1 = kernel[0, ntarg].compute_and_differentiate(jd)

        if ncent == 3:  # earth
            p2, v2 = kernel[0, 3].compute_and_differentiate(jd)
            p22, v22 = kernel[3, 399].compute_and_differentiate(jd)
            p2 += p22
            v2 += v22
        elif ncent == 10:  # moon
            p2, v2 = kernel[0, 3].compute_and_differentiate(jd)
            p22, v22 = kernel[3, 301].compute_and_differentiate(jd)
            p2 += p22
            v2 += v22
        elif ncent == 11:  # sun
            p2, v2 = kernel[0, 10].compute_and_differentiate(jd)
        else:
            p2, v2 = kernel[0, ncent].compute_and_differentiate(jd)

        p = p1 - p2
        v = v1 - v2

    return p, v / 86400
