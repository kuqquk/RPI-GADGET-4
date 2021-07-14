'''
Reading data from a hdf5 file using h5py

h5py installed in anaconda, LOAD ANACONDA MODULE FIRST:
module load anaconda3/2020.11
'''

import h5py


snapPath = './g2-collision/outputs'
snapshot = f'{snapPath}/snapshot_000.hdf5'      # the snapshot at t=0, the same as ICfile

with h5py.File(snapshot, 'r') as f:      # open snapshot in 'read-only' mode
    ''' Let's see the structrue of a snapshot file: '''

    print(list(f.keys()))      # just like listing a python dict
    '''
    ['Config',          # same as Config.sh
     'Header',          # stores Boxsize, number of particles, time of snapshot ...
     'Parameters',      # same as param.txt
     'PartType0',       # gas particles
     'PartType1',       # dark mater (DM) particles
     'PartType2',       # stellar particles which are in the galaxy disk   (axisymmetric component of a disk galaxy)
     'PartType3',       # stellar particles which are in the galaxy bulge  (spherical component of a disk galaxy)
     'PartType4']       # stars born from gas particles (star formation is enabled in this simulation)
    '''


    ''' Header '''
    h = f['Header']
    print(list(h.attrs))    # ['Header'] is a data group with some attributes
    '''
    ['BoxSize',
     'Git_commit',
     'Git_date',
     'MassTable',
     'NumFilesPerSnapshot',
     'NumPart_ThisFile',
     'NumPart_Total',
     'Redshift',
     'Time']
     '''
    print(h.attrs['time'])     # time (in code unit) of this snapshot
    print(h.attrs['NumPart_Total'])    # total number of each type of particles [npart0, npart1, ..., npart5]
    print(h.attrs['MassTable'])     # mass-per-particle of each type of particles


    ''' 
    Gas
    gas particles are SPH particles, GADGET4 computes them differently 
    than other self-gravitational particles
    '''
    gas = f['PartType0']    # ['PartType0'] is a data group with some data set
    list(gas.keys())
    ''' 
    # names ('key') of data sets
    ['Coordinates',     # Cartesian coordinates
     'Density',
     'ElectronAbundance',
     'InternalEnergy',
     'Masses',
     'Metallicity',
     'ParticleIDs',
     'SmoothingLength',
     'StarFormationRate',
     'Velocities']      # Cartesian velocity
    '''
    posGas = gas['Coordinates'][:]    # use [:] to list positions, and pos.shape = (npart1, 3)
    pidGas = gas['ParticleIDs'][:]    # particle ID is the unique for each particle



    ''' Dark matter halo '''
    halo = f['PartType1']     
    print(list(halo.keys()))
    '''
    ['Coordinates', 'ParticleIDs', 'Velocities']    # names ('key') of data sets
    '''
    posHalo = halo['Coordinates'][:]    # use [:] to list positions, and pos.shape = (npart1, 3)
    pidHalo = halo['Coordinates'][:]    # particle ID is the unique for each particle


    ''' GADGET-4 treats disk and buldge particles same as DM particles '''
    disk = f['PartType2']
    buldge = f['PartType3']


    ''' 
    Stars
    These star particles come from the gas particles: npart0 + npart4 = constant
    npart4(t=0) = 0
    '''
    star = f['PartType4']
    print(list(star.keys()))
    '''
    ['Coordinates',
     'Masses',
     'Metallicity',
     'ParticleIDs',
     'StellarFormationTime',
     'Velocities']
    '''


    ''' 
    Code unit
    The unit in the snapshot is in (~gigayears), kiloparsec, and 10^10 SolarMass
    '''
    params = f['Parameters']
    print(list(params.attrs))      # ['Config', 'Header', 'Parameters'] are data groups with attributes
    '''
    [...,
     'UnitLength_in_cm',
     'UnitMass_in_g',
     'UnitVelocity_in_cm_per_s']    # You can also find this in param.txt.
    '''
    UnitLength = params.attrs['UnitLength_in_cm']   # 3.085678e21 cm = 1 kpc
    UnitMass = params.attrs['UnitMass_in_cm']       # 1.989e43 g = 10^10 solar mass
    UnitVelocity = params.attrs['UnitVelocity_in_cm_per_s']     # 100000.0 cm/s = 1 km/s

    # derived unit and G
    UnitTime = UnitLength / UnitVelocity    # 3.08568*10^16 s = 0.978462 Gyr
    GravityConstant_in_CGS = 6.67408e-8
    GravityConstantInternal = GravityConstant_in_CGS * (UnitLength**-3) * (UnitMass) * (UnitTime**2)    # 43007.5 [kpc^3 (10^10 M_solar)^-1 (0.98 Gyr)^-2]

    '''
    So if you find a PartType4 particle 
    at Coordinates=[7, 0.0, 0.0], with Velocities=[0.0, 1.4, 0.0], StellarFormationTime=6.6
    It means 
        coordinates = [7, 0.0, 0.0] kpc, 
        Velocities = [0.0, 1.4, 0.0] km/s,
        StellarFormationTime = 6.6 * 0.978462 Gyr = 6.52 Gyr    # we can take UnitTime ~ 1 Gyr
    '''

'''
More infomation of HDF5 file check:
https://portal.hdfgroup.org/display/HDF5/Introduction+to+HDF5 
'''
