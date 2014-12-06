import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../')
import gillespy

class Tyson2StateOscillator(gillespy.Model):
    """
    Here, as a test case, we run a simple two-state oscillator (Novak & Tyson 
    2008) as an example of a stochastic reaction system.
    """
    def __init__(self, parameter_values=None, omega=150):
        """
        """
        gillespy.Model.__init__(self, name="tyson-2-state", volume=omega)
        # =============================================
        # Define model species, initial values, parameters, and volume
        # =============================================    
        
        
        # Parameter values  have been converted to be in population, rather than
        # concentration units. For example, a concentration unit of 0.5mol/(L*s)
        # is multiplied by a volume unit (omega), to get a population/s rate
        # constant. As this scaling depends on omega values for non-mass action
	# terms, we have left omega as 
        P = gillespy.Parameter(name='P', expression=2.0)
        kt = gillespy.Parameter(name='kt', expression=20.0)
        kd = gillespy.Parameter(name='kd', expression=1.0)
        a0 = gillespy.Parameter(name='a0', expression=0.005)
        a1 = gillespy.Parameter(name='a1', expression=0.05)
        a2 = gillespy.Parameter(name='a2', expression=0.1)
        kdx = gillespy.Parameter(name='kdx', expression=1.0)
        self.add_parameter([P, kt, kd, a0, a1, a2, kdx])
        
        # Species
        # Initial values of each species (concentration converted to pop.)
        species_names = ['X','Y']
        X = gillespy.Species(name='X', initial_value=int(0.65609071*omega))
        Y = gillespy.Species(name='Y', initial_value=int(0.85088331*omega))
        self.add_species([X, Y])
        
        # =============================================  
        # Define the reactions within the model
        # =============================================  
        
        # creation of X:
        rxn1 = gillespy.Reaction(name = 'X production',
                        reactants = {},
                        products = {X:1},
                        propensity_function = '150*1/(1+(Y*Y/((150*150))))')
        
        # degradadation of X:
        rxn2 = gillespy.Reaction(name = 'X degradation',
                    reactants = {X:1},
                    products = {},
                    rate = kdx)
        
        # creation of Y:
        rxn3 = gillespy.Reaction(name = 'Y production',
                    reactants = {X:1},
                    products = {X:1, Y:1},
                    rate = kt)
        
        # degradation of Y:
        rxn4 = gillespy.Reaction(name = 'Y degradation',
                    reactants = {Y:1},
                    products = {},
                    rate = kd)
            
        # nonlinear Y term:
        rxn5 = gillespy.Reaction(name = 'Y nonlin',
                    reactants = {Y:1},
                    products = {},
                    propensity_function = 'Y/(a0 + a1*(Y/150)+a2*Y*Y/(150*150))')
        
        self.add_reaction([rxn1,rxn2,rxn3,rxn4,rxn5])



if __name__ == '__main__':

    tyson_model = Tyson2StateOscillator()

    # =============================================
    # Simulate the mode and return the trajectories 
    # =============================================  
    # To set up the model, first create an empty model object. Then, add
    # species and parameters as was set up above.
    tyson_trajectories = gillespy.StochKitSolver.simulate(tyson_model)
    
    # =============================================  
    # plot just the first trajectory, 0, in both time and phase space:
    # =============================================  
    from matplotlib import gridspec
    
    plt.figure(figsize=(3.5*2,2.62))
    gs = gridspec.GridSpec(1,2)
    
    
    ax0 = plt.subplot(gs[0,0])
    ax0.plot(tyson_trajectories[0][:,0], tyson_trajectories[0][:,1], 
             label='X')
    ax0.plot(tyson_trajectories[0][:,0], tyson_trajectories[0][:,2], 
             label='Y')
    ax0.legend()
    ax0.set_xlabel('Time')
    ax0.set_ylabel('Species Count')
    ax0.set_title('Time Series Oscillation')
    
    ax1 = plt.subplot(gs[0,1])
    ax1.plot(tyson_trajectories[1][:,1], tyson_trajectories[0][:,2], 'k')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Phase-Space Plot')
    
    plt.tight_layout()
    plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
