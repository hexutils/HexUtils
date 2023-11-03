import numpy as np
import vector
import useful_helpers as help
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplhep as hep
import functools

class angle_calculator(object):
    def __init__(self, pt, eta, phi, m, id, needStack=False,
                 name_override={}, range_override={}):
        """a calculator for the 4 lepton angles given a set of 4 lepton 4-vectors

        Parameters
        ----------
        pt : Iterable
            A list of pT for each event
        eta : Iterable
            A list of eta for each event
        phi : Iterable
            A list of phi for each event
        m : Iterable
            A list of m for each event
        id : Iterable
            A list of ids for each event
        needStack : bool, optional
            _description_, by default False
        name_override : dict, optional
            _description_, by default {}
        range_override : dict, optional
            _description_, by default {}

        Raises
        ------
        KeyError
            _description_
        KeyError
            _description_
        """
        
        pt, eta, phi, m, id = list(map(np.array, [pt, eta, phi, m, id]))

        if needStack:
            pt = np.stack(pt, axis=0)
            eta = np.stack(eta, axis=0)
            phi = np.stack(phi, axis=0)
            m = np.stack(m, axis=0)
            id = np.stack(id, axis=0)
            
        self.lep_1 = vector.array(
            {
                "pt":pt[:,0],
                "phi":phi[:,0],
                "eta":eta[:,0],
                "M":m[:,0]
            }
        )
        self.lep_1_id = id[:,0]
        
        self.lep_2 = vector.array(
            {
                "pt":pt[:,1],
                "phi":phi[:,1],
                "eta":eta[:,1],
                "M":m[:,1]
            }
        )
        self.lep_2_id = id[:,1]
        
        self.lep_3 = vector.array(
            {
                "pt":pt[:,2],
                "phi":phi[:,2],
                "eta":eta[:,2],
                "M":m[:,2]
            }
        )
        self.lep_3_id = id[:,2]
        
        self.lep_4 = vector.array(
            {
                "pt":pt[:,3],
                "phi":phi[:,3],
                "eta":eta[:,3],
                "M":m[:,3]
            }
        )
        self.lep_4_id = id[:,3]
        
        
        Z1_sort_mask = (
            (self.lep_2_id!=-9000)
            &
            (
                (#for OS pairs, lep1 is the particle.
                    (self.lep_1_id*self.lep_2_id<0)
                    & 
                    (self.lep_1_id<0) 
                )
                |
                ( #for SS pairs, a random deterministic convention is used.
                    (
                        (self.lep_1_id*self.lep_2_id>0)
                        |
                        (
                            (self.lep_1_id==0) 
                            & 
                            (self.lep_2_id==0)
                        )
                    )
                    &
                    (self.lep_1.phi <= self.lep_2.phi)
                )
            )
        )
        np.where(Z1_sort_mask, self.lep_2, self.lep_1) #swap leptons if the mask is true
        self.Z1 = self.lep_1 + self.lep_2
        
        
        Z2_sort_mask = (
            (self.lep_4_id!=-9000)
            &
            (
                (#for OS pairs, lep1 is the particle.
                    (self.lep_3_id*self.lep_4_id<0)
                    & 
                    (self.lep_3_id<0) 
                )
                |
                ( #for SS pairs, a random deterministic convention is used.
                    (
                        (self.lep_3_id*self.lep_4_id>0)
                        |
                        (
                            (self.lep_3_id==0) 
                            & 
                            (self.lep_4_id==0)
                        )
                    )
                    &
                    (self.lep_3.phi <= self.lep_4.phi)
                )
            )
        )
        np.where(Z2_sort_mask, self.lep_4, self.lep_3) #swap leptons if the mask is true
        self.Z2 = self.lep_3 + self.lep_4
        
        self.X = self.Z1 + self.Z2
        
        
        self.quantities = {
            "costhetastar":r'$\cos \theta^*$',
            "costheta1":r'$\cos \theta_1$',
            "costheta2":r'$\cos \theta_2$',
            "phi":r'$\phi$',
            "phi1":r'$\phi_1$',
            "pt":r'$p_T(X)$',
            "px":r'$p_x(X)$',
            "py":r'$p_y(X)$',
            "pz":r'$p_z(X)$',
        }
        
        self.ranges = {
            "costhetastar":(-1,1),
            "costheta1":(-1,1),
            "costheta2":(-1,1),
            "phi":(-np.pi, np.pi),
            "phi1":(-np.pi, np.pi),
            "pt":None,
            "px":None,
            "py":None,
            "pz":None,
        }
        
        for i in name_override.keys():
            if i not in self.quantities.keys():
                errortext = i + " not a quantity!"
                errortext += "\nQuantities are the following:\n"
                errortext += "\n".join(list(self.quantities.keys()))
                errortext = help.print_msg_box(errortext, title="ERROR")
                raise KeyError("\n" + errortext)
            self.quantities[i] = name_override[i]
        
        for i in range_override.keys():
            if i not in self.quantities.keys():
                errortext = i + " not a quantity!"
                errortext += "\nQuantities are the following:\n"
                errortext += "\n".join(list(self.quantities.keys()))
                errortext = help.print_msg_box(errortext, title="ERROR")
                raise KeyError("\n" + errortext)
            self.ranges[i] = range_override[i]
        
        plt.cla()
    
    @classmethod
    def from_xyz_leptons(cls, 
                         x1, y1, z1, e1, id1,
                         x2, y2, z2, e2, id2,
                         x3, y3, z3, e3, id3,
                         x4, y4, z4, e4, id4,
                         name_override={}, range_override={}):
        lepton1 = vector.array(
            {
                "px":x1,
                "py":y1,
                "pz":z1,
                "E":e1
            }
        )

        lepton2 = vector.array(
            {
                "px":x2,
                "py":y2,
                "pz":z2,
                "E":e2
            }
        )
        
        lepton3 = vector.array(
            {
                "px":x3,
                "py":y3,
                "pz":z3,
                "E":e3
            }
        )
        
        lepton4 = vector.array(
            {
                "px":x4,
                "py":y4,
                "pz":z4,
                "E":e4
            }
        )
        
        pt_array = np.stack(
            [
                lepton1.pt,
                lepton2.pt,
                lepton3.pt,
                lepton4.pt
            ], axis=1
        )
        
        phi_array = np.stack(
            [
                lepton1.phi,
                lepton2.phi,
                lepton3.phi,
                lepton4.phi
            ], axis=1
        )
        
        eta_array = np.stack(
            [
                lepton1.eta,
                lepton2.eta,
                lepton3.eta,
                lepton4.eta
            ], axis=1
        )
        
        m_array = np.stack(
            [
                lepton1.M,
                lepton2.M,
                lepton3.M,
                lepton4.M
            ], axis=1
        )
        
        
        id_array = np.stack(
            [
                id1,
                id2,
                id3,
                id4
            ], axis=1
        )
        
        return cls(
            pt_array, eta_array, phi_array, m_array, id_array,
            name_override=name_override, range_override=range_override
        )
    
    @functools.property
    def costhetastar(self):
        boost_x = -self.X.to_beta3() #to_beta3 is equivalent to ROOT's TLorentzVector BoostVector
        Z1_in_x_frame = self.Z1.boost(boost_x)
        # Z2_in_x_frame = self.Z2.boost(boost_x)
        Z1_in_x_frame = help.get_spatial(Z1_in_x_frame)
        cos_theta_star = Z1_in_x_frame.z/Z1_in_x_frame.mag
        
        return cos_theta_star
    
    @functools.property 
    def costheta1(self):
        boost_v1 = -1*self.Z1.to_beta3()
        np.where(boost_v1.mag>=1, boost_v1*0.9999/boost_v1.mag, boost_v1)
        
        l1_boosted = self.lep_1.boost(boost_v1)
        l3_boosted = self.lep_3.boost(boost_v1)
        l4_boosted = self.lep_4.boost(boost_v1)
        
        v2_boosted = l3_boosted + l4_boosted
        
        v2_boosted = help.get_spatial(v2_boosted)
        
        l1_boosted = help.get_spatial(l1_boosted)
        
        cos_theta_1 = -1*v2_boosted.unit().dot(l1_boosted.unit())
        
        cos_theta_1 = np.where(np.abs(self.lep_1_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_2_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_3_id)!=21, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_4_id)!=21, cos_theta_1, 0)
        
        cos_theta_1 = np.where(np.abs(self.lep_1_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_2_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_3_id)!=22, cos_theta_1, 0)
        cos_theta_1 = np.where(np.abs(self.lep_4_id)!=22, cos_theta_1, 0)
        
        return cos_theta_1
    
    @functools.property 
    def costheta2(self):
        boost_v2 = -1*self.Z2.to_beta3()
        
        l1_boosted = self.lep_1.boost(boost_v2)
        l2_boosted = self.lep_2.boost(boost_v2)
        l3_boosted = self.lep_3.boost(boost_v2)
        
        v1_boosted = l1_boosted + l2_boosted
        
        v1_boosted = help.get_spatial(v1_boosted)
        
        l3_boosted = help.get_spatial(l3_boosted)
        
        cos_theta_2 = -1*v1_boosted.unit().dot(l3_boosted.unit())
        
        cos_theta_2 = np.where(np.abs(self.lep_1_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_2_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_3_id)!=21, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_4_id)!=21, cos_theta_2, 0)
        
        cos_theta_2 = np.where(np.abs(self.lep_1_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_2_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_3_id)!=22, cos_theta_2, 0)
        cos_theta_2 = np.where(np.abs(self.lep_4_id)!=22, cos_theta_2, 0)
        
        return cos_theta_2
    
    @functools.property 
    def phi(self):
        boost_x = -1*self.X.to_beta3()
        l1_boosted = self.lep_1.boost(boost_x)
        l2_boosted = self.lep_2.boost(boost_x)
        l3_boosted = self.lep_3.boost(boost_x)
        l4_boosted = self.lep_4.boost(boost_x)
        
        v1_boosted = help.help.get_spatial(l1_boosted + l2_boosted).unit()
        
        normal_1_boosted = (help.get_spatial(l1_boosted).cross(help.get_spatial(l2_boosted))).unit()
        normal_2_boosted = (help.get_spatial(l3_boosted).cross(help.get_spatial(l4_boosted))).unit()
        
        temp_sign_phi = v1_boosted.dot(normal_1_boosted.cross(normal_2_boosted))
        sign_phi = np.where(np.abs(temp_sign_phi)>0,temp_sign_phi/np.abs(temp_sign_phi), 0)
        
        dot_boosted = normal_1_boosted.dot(normal_2_boosted)
        dot_boosted = np.where(np.abs(dot_boosted) >= 1, dot_boosted/np.abs(dot_boosted), dot_boosted)
        
        phi = sign_phi*np.arccos(-1*dot_boosted)
        
        return phi
    
    @functools.property
    def phi1(self):
        boost_x = -1*self.X.to_beta3()
        l1_boosted = self.lep_1.boost(boost_x)
        l2_boosted = self.lep_2.boost(boost_x)
        
        v1_boosted = help.get_spatial(l1_boosted + l2_boosted).unit()
        
        beam_axis = vector.array([(0,0,1)], dtype=[("x", float), ("y", float), ("z", float)])

        normal_1_boosted = (help.get_spatial(l1_boosted).cross(help.get_spatial(l2_boosted))).unit()
        normal_SC_boosted = (beam_axis.cross(v1_boosted)).unit()
        
        temp_sign_phi = v1_boosted.dot(normal_1_boosted.cross(normal_SC_boosted))
        sign_phi = np.where(np.abs(temp_sign_phi)>0,temp_sign_phi/np.abs(temp_sign_phi), 0)
        
        dot_boosted = normal_1_boosted.dot(normal_SC_boosted)
        dot_boosted = np.where(np.abs(dot_boosted) >= 1, dot_boosted/np.abs(dot_boosted), dot_boosted)
        
        phi1 = sign_phi*np.arccos(dot_boosted)
        
        return phi1
    
    @functools.property
    def pT_X(self):
        return self.X.pt
    
    @functools.property
    def pz_X(self):
        return self.X.pz
    
    @functools.property
    def py_X(self):
        return self.X.py
    
    @functools.property
    def px_X(self):
        return self.X.px
    
    
    def plot_quantity(self, quantity, fname, bins=20, clear_after=True, save=True, identifier="", norm=False,
                      abs=False, ax=None, color=None, fontsize=10, spacer=True, lw=2, loc='upper right',
                      show_stats=True, noplot=False, fig=None):
        plt.style.use(hep.style.ROOT)
        mpl.rcParams['axes.labelsize'] = 40
        mpl.rcParams['xaxis.labellocation'] = 'center'
        quantity = quantity.lower()
        
        if quantity not in self.quantities.keys():
            errortext = quantity + " not defined as a quantity in self.quantities!"
            errortext += "\nUse the name_override keyword to define quanties not predefined!"
            errortext += "self.quantities:\n "
            errortext += "\n".join(list(self.quantities.keys()))
            errortext = help.print_msg_box(errortext, title="ERROR")
            raise KeyError("\n"+errortext)
        
        if quantity not in self.ranges.keys():
            errortext = quantity + " not defined as a quantity in self.ranges!"
            errortext += "\nUse the range_override keyword to define ranges not predefined!"
            errortext += "self.ranges:\n "
            errortext += "\n".join(self.ranges.keys())
            errortext = help.print_msg_box(errortext, title="ERROR")
            raise KeyError("\n"+errortext)

        
        conversion = {
            "costhetastar":self.costhetastar,
            "costheta1":self.costheta1,
            "costheta2":self.costheta2,
            "phi":self.phi,
            "phi1":self.phi1,
            "pt":self.pT_X,
            "px":self.px_X,
            "py":self.py_X,
            "pz":self.pz_X
        }
        
        if abs:
            values = np.abs(conversion[quantity])
        else:
            values = conversion[quantity]
        
        
        if self.ranges[quantity] == None:
                variable_range = [values.min(), values.max()]
                
        else:
            variable_range = self.ranges[quantity]
        
        if isinstance(bins, int):
            _, bins = np.histogram([], bins, range=variable_range)
            
        

        hist, bins = np.histogram(values, bins=bins)
        hist = hist.astype(float)
        if norm:
            hist = help.scale(norm, hist)
        
        if identifier == "":
            identifier = self.quantities[quantity]
        
        if show_stats:
            labelstr = help.make_legend_label_hist(bins, hist, identifier, extra_space=spacer)
        else:
            labelstr = identifier
        
        if noplot:
            return hist, bins, labelstr
        
        if ax == None:
            ax = plt.gca()
        
        if color:
            hep.histplot(hist, bins, label=labelstr, lw=lw, ax=ax, color=color)
        else:
            hep.histplot(hist, bins, label=labelstr, lw=lw, ax=ax,)
        
        ax.set_xlabel(self.quantities[quantity])
        ax.legend(loc=loc, fontsize=fontsize)
        ax.set_xlim(variable_range)
        
        if fig == None:
            fig = plt.gcf()
        
        fig.tight_layout()
        if save:
            fig.savefig(fname)
        if clear_after:
            plt.cla()
            plt.close(fig)
            
        return hist, bins, labelstr