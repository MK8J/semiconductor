import numpy as np
from pylab import *
import sys
import os
import scipy.constants as Const
import ConfigParser

# TODO:
# Need to make bandgap class, that includes that impact of BNG

sys.path.append(
    os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir)))

from semiconductor.helper.helper import HelperFunctions




class IntrinsicBandGap(HelperFunctions):
    '''
    The intrinsic bandgap as a function of temperature
        it changes as a result of:
             different effective carrier mass (band strucutre)
    '''         

    model_file = 'bandgap.models'

    def __init__(self, matterial='Si', model_author=None):
        self.Models = ConfigParser.ConfigParser()
        self.matterial = matterial

        constants_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            matterial,
            self.model_file)

        self.Models.read(constants_file)

        self.change_model(model_author)


    # def E0(self, temp=False, E0=False):
    #     """
    #     just a function that provide E0 based on the E0 provided
    #     If no E0 is provided it defults to the self.E0 value
    #     """

    #     if not E0:
    #         E0 = self.E0
    #     else:
    #         self.E0 = E0

    #     self.E = getattr(self, 'E0_' + E0)()
    #     return self.E

    # def E0_Thurmond(self, temp=False):
    #     """
    #     Doesn't work, gives too high numbers
    #     Taken from Couderc2014
    #     Think its a mistake in the thta paper
    #     """

    #     if not np.all(temp):
    #         temp = self.Temp

    #     E0 = 1.17

    #     alpha = 4.73e-4
    #     beta = 636.

    #     E = E0 - alpha * temp**2 / (temp + beta)
    # print self.E0_Passler(temp)/1.602e-19,E
    #     return E * Const.e

    def update_Eg(self, temp=None):

        if temp is None:
            temp = self.temp
        self.Eg = getattr(self, self.model)(self.vals, temp)

        return self.Eg

    def Eg_Passler(self, vals, temp):
        """
        taken from Couderc2014
        depent on temperature
        """

        gamma = (1. - 3. * vals['delta']**2) / \
            (np.exp(vals['theta'] / temp) - 1)
        xi = 2. * temp / vals['theta']

        # Values for each sum component
        No2 = np.pi**2. * xi**2. / (3. * (1 + vals['delta']**2))
        No3 = (3. * vals['delta']**2 - 1) / 4. * xi**3
        No4 = 8. / 3. * xi**4.
        No5 = xi**6.

        E = vals['e0'] - vals['alpha'] * vals['theta'] * \
            (gamma + 3. * vals['delta']**2 / 2 *
             ((1. + No2 + No3 + No4 + No5)**(1. / 6.) - 1))
        return E * Const.e


class BandGapNarrowing(HelperFunctions):
    '''
    Bang gap narrowing accounts for a reduction in bandgap that 
    occurs as a result from no thermal effects. These include:
        doping. It is dopant dependent
        excess carrier density (non thermal distribution)
    Note: I currently believed that the impact of dopants 
        is much larger than the impact of the carrier distribution
    '''     


    model_file = 'bandgapnarrowing.models'
    def __init__(self, matterial='Si', model_author=None):
        self.Models = ConfigParser.ConfigParser()
        self.matterial = matterial

        constants_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            matterial,
            self.model_file)

        self.Models.read(constants_file)

        self.change_model(model_author) 

    def update_BGN(self, doping, min_car_den = None):

        # if temp is None:
        #     temp = self.temp
        self.BGN = getattr(self, self.model)(self.vals, doping)

        return self.BGN

    def apparent_BNG(self, vals, doping):
        '''
        It states that the 'apparent BGN' 
        where N is the net dopant concentration. 
        '''
        DEg = np.zeros(doping.shape)

        index = doping > vals['n_onset']
        DEg[index] = (vals['de_slope'] * np.log(doping[index] / vals['n_onset']))

        return DEg


if __name__ == "__main__":
    # a = IntrinsicCarrierDensity()
    # a._PlotAll()
    # plt.show()
    a = BandGapNarrowing('Si')
    # deltan = np.logspace(12, 17)
    # print a.Radiative.ni, a.Auger.ni
    doping = np.logspace(12,20,100)
    a.plot_all_models('update_BGN', doping=doping)
    # print plt.plot(doping, a.update_BGN(doping))
    plt.semilogx()
    plt.show()