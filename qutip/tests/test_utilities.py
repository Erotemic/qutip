import numpy as np
from numpy.testing import assert_, run_module_suite

from qutip import convert_unit, clebsch


def test_unit_conversions():
    "utilities: energy unit conversions"

    T = np.random.rand() * 100.0

    diff = convert_unit(convert_unit(T, orig="mK", to="GHz"),
                        orig="GHz", to="mK") - T
    assert_(abs(diff) < 1e-6)
    diff = convert_unit(convert_unit(T, orig="mK", to="meV"),
                        orig="meV", to="mK") - T
    assert_(abs(diff) < 1e-6)

    diff = convert_unit(convert_unit(convert_unit(T, orig="mK", to="GHz"),
                                     orig="GHz", to="meV"),
                        orig="meV", to="mK") - T
    assert_(abs(diff) < 1e-6)

    w = np.random.rand() * 100.0

    diff = convert_unit(convert_unit(w, orig="GHz", to="meV"),
                        orig="meV", to="GHz") - w
    assert_(abs(diff) < 1e-6)

    diff = convert_unit(convert_unit(w, orig="GHz", to="mK"),
                        orig="mK", to="GHz") - w
    assert_(abs(diff) < 1e-6)

    diff = convert_unit(convert_unit(convert_unit(w, orig="GHz", to="mK"),
                                     orig="mK", to="meV"),
                        orig="meV", to="GHz") - w
    assert_(abs(diff) < 1e-6)

def test_unit_clebsch():
    "utilities: Clebsch–Gordan coefficients "
    N = 15
    for _ in range(100):
        "sum_m1 sum_m2 C(j1,j2,j3,m1,m2,m3)*C(j1,j2,j3',m1,m2,m3') ="
        "delta j3,j3' delta m3,m3'"
        j1 = np.random.randint(0, N+1)
        j2 = np.random.randint(0, N+1)
        j3 = np.random.randint(abs(j1-j2), j1+j2+1)
        j3p = np.random.randint(abs(j1-j2), j1+j2+1)
        m3 = np.random.randint(-j3, j3+1)
        m3p = np.random.randint(-j3p, j3p+1)
        if np.random.rand() < 0.25:
            j1 += 0.5
            j3 += 0.5
            j3p += 0.5
            m3 += np.random.choice([-0.5, 0.5])
            m3p += np.random.choice([-0.5, 0.5])
        if np.random.rand() < 0.25:
            j2 += 0.5
            j3 += 0.5
            j3p += 0.5
            m3 += np.random.choice([-0.5, 0.5])
            m3p += np.random.choice([-0.5, 0.5])
        sum_match = -1
        sum_differ = -int(j3 == j3p and m3 == m3p)
        for m1 in np.arange(-j1,j1+1):
            for m2 in np.arange(-j2,j2+1):
                c1 = clebsch(j1, j2, j3, m1, m2, m3)
                c2 = clebsch(j1, j2, j3p, m1, m2, m3p)
                sum_match += c1**2
                sum_differ += c1*c2
        assert_(abs(sum_match) < 1e-6)
        assert_(abs(sum_differ) < 1e-6)

    for _ in range(100):
        "sum_j3 sum_m3 C(j1,j2,j3,m1,m2,m3)*C(j1,j2,j3,m1',m2',m3) ="
        "delta m1,m1' delta m2,m2'"
        j1 = np.random.randint(0,N+1)
        j2 = np.random.randint(0,N+1)
        m1 = np.random.randint(-j1,j1+1)
        m1p = np.random.randint(-j1,j1+1)
        m2 = np.random.randint(-j2,j2+1)
        m2p = np.random.randint(-j2,j2+1)
        if np.random.rand() < 0.25:
            j1 += 0.5
            m1 += np.random.choice([-0.5, 0.5])
            m1p += np.random.choice([-0.5, 0.5])
        if np.random.rand() < 0.25:
            j2 += 0.5
            m2 += np.random.choice([-0.5, 0.5])
            m2p += np.random.choice([-0.5, 0.5])
        sum_match = -1
        sum_differ = -int(m1 == m1p and m2 == m2p)
        for j3 in np.arange(abs(j1-j2),j1+j2+1):
            for m3 in np.arange(-j3,j3+1):
                c1 = clebsch(j1, j2, j3, m1, m2, m3)
                c2 = clebsch(j1, j2, j3, m1p, m2p, m3)
                sum_match += c1**2
                sum_differ += c1*c2
        assert_(abs(sum_match) < 1e-6)
        assert_(abs(sum_differ) < 1e-6)


if __name__ == "__main__":
    run_module_suite()
