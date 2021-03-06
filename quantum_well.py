# Tutorial 2.3.2. Spatially dependent values through functions
# ============================================================
#
# Physics background
# ------------------
#  transmission through a quantum well
#
# Kwant features highlighted
# --------------------------
#  - Functions as values in Builder

import kwant

# For plotting
from matplotlib import pyplot


def make_system(a=1, t=1.0, W=10, L=30, L_well=10):
    # Start with an empty tight-binding system and a single square lattice.
    # `a` is the lattice constant (by default set to 1 for simplicity.
    lat = kwant.lattice.square(a)

    syst = kwant.Builder()

    #### Define the scattering region. ####
    # Potential profile
    def potential(site, pot):
        (x, y) = site.pos
        if (L - L_well) / 2 < x < (L + L_well) / 2:
            return pot
        else:
            return 0

    def onsite(site, pot):
        return 4 * t + potential(site, pot)

    syst[(lat(x, y) for x in range(L) for y in range(W))] = onsite
    syst[lat.neighbors()] = -t

    #### Define and attach the leads. ####
    lead = kwant.Builder(kwant.TranslationalSymmetry((-a, 0)))
    lead[(lat(0, j) for j in range(W))] = 4 * t
    lead[lat.neighbors()] = -t
    syst.attach_lead(lead)
    syst.attach_lead(lead.reversed())

    return syst


def plot_conductance(syst, energy, welldepths):

    # Compute conductance
    data = []
    for welldepth in welldepths:
        smatrix = kwant.smatrix(syst, energy, params=dict(pot=-welldepth))
        data.append(smatrix.transmission(1, 0))

    pyplot.figure()
    pyplot.plot(welldepths, data)
    pyplot.xlabel("well depth [t]")
    pyplot.ylabel("conductance [e^2/h]")
    pyplot.show()


def main():
    syst = make_system()

    # Check that the system looks as intended.
    kwant.plot(syst)

    # Finalize the system.
    syst = syst.finalized()

    # We should see conductance steps.
    plot_conductance(syst, energy=0.2,
                     welldepths=[0.01 * i for i in range(100)])


# Call the main function if the script gets executed (as opposed to imported).
# See <http://docs.python.org/library/__main__.html>.
if __name__ == '__main__':
    main()
