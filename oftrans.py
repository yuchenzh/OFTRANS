from pathlib import Path
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class OFTrans:
    def __init__(self, mech_file, low=300, high=3000, n_points=200):
        # own gas
        self.gas = ct.Solution(mech_file)
        self.TList = np.linspace(low, high, n_points)
        self.species = self.gas.species_names
        self.sutherland_params = {}
        
    def getMu4Species(self, species_name, T):
        self.gas.TPY = T, ct.one_atm, species_name + ":1.0"
        return self.gas.viscosity
    
    def getMuList4Species(self, species_name):
        muList = np.zeros_like(self.TList, dtype=np.float64)
        for i, T in enumerate(self.TList):
            muList[i] = self.getMu4Species(species_name, T)
        return muList

    def getSutherlandParams(self):
        for sp in self.species:
            self.sutherland_params[sp] = self.fit(sp)
    
    def fit(self, species_name):
        muList = np.zeros_like(self.TList, dtype=np.float64)
        muList = self.getMuList4Species(species_name)
        params, cov = curve_fit(self.sutherland, self.TList, muList, p0 = [1.512e-6, 120.] )
        return params[0], params[1]
    
    def sutherland(self, T, As, Ts):
        return As * T ** 1.5 / (T + Ts)
    
    def ofheader(self, version):
        header = (
            "/*--------------------------------*- C++ -*----------------------------------*\\\n"
            "| =========                 |\n"
            "| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n"
            "|  \\    /   O peration     | Website:  https://openfoam.org\n"
            "|   \\  /    A nd           | Version:  " + str(version)+"\n"
            "|    \\/     M anipulation  |\n"
            "\*---------------------------------------------------------------------------*/\n"
            "FoamFile\n"
            "{\n"
            "\tversion     2.0;\n"
            "\tformat      ascii;\n"
            "\tclass       dictionary;\n"
            "\tlocation    \"chemkin\";\n"
            "\tobject      transportProperties;\n"
            "}\n"
            "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
        )
        return header

    def writeEntry(self, name, As,Ts):
        entry = (
            "\"" + name + "\"\n"
            "{\n"
            "    transport\n"
            "    {\n"
            "        As   " + str(As) + ";\n"
            "        Ts   " + str(Ts) + ";\n"
            "    }\n"
            "}\n"
        )
        return entry
    
    def writeDefaultEntry(self):
        return self.writeEntry(".*", 1.512e-6, 120.)
    
    def __call__(self, version=7):
        # print(self.ofheader(7))
        # print(self.writeDefaultEntry())
        # for sp in self.species:
        #     As, Ts = self.sutherland_params[sp]
        #     print(self.writeEntry(sp, As, Ts))  
            
        # write to a file
        with open("./transportProperties", "w") as f:
            f.write(self.ofheader(version))
            f.write(self.writeDefaultEntry())
            for sp in self.species:
                As, Ts = self.sutherland_params[sp]
                f.write(self.writeEntry(sp, As, Ts))
    
        

        
        
