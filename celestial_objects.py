import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt 
import densities
import rotations


#Each class of objects MUST HAVE integration bounds (region describing the object. Bounds of x must be constant, while bounds of y is function of x, and bounds of z is function of x AND y. 
# This is because scipy integration only allows dzdydx by default, so the order is important), mass, quadrupole moment
#and takes in (self, t, a, b, c, rho0, density, omega0, rotation) in init (rotation tensor and parameter preferrably initialised to state of no rotation until user manuaklly imputs a rotation tensor/parameter)

class ellipsoid_object:
    """
    Defines an ellipsoid object. 
    Note that we use natural units where c=G=km=1. As a result 1 time unit is 3e5 seconds (half a week)
    """
    def __init__(self, t, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating):
        self.t = t #Time parameter
        self.a=a
        self.b=b
        self.c=c 
        self.rho0 = rho0
        self.density = density #This is a callable
        self.omega0 = omega0 #This is the rotation parameter
        self.rotation = rotation #This is a function that returns the rotation tensor (3x3 matrix). Initialised to be the unit matrix 
    
    def __repr__(self):
        quad_str="Not Computed Yet"
        if hasattr(self, "quadMom_tensor"):
            quad_str=""
            for line in self.quadMom_tensor:
                quad_str+="\n"+str(np.array(line))
        mass_str="Not Computed Yet"
        if hasattr(self, "totalMass"):
            mass_str=str(self.totalMass)
        rotationText = "omega0="+str(self.omega0)
        if self.omega0==0 or np.array_equal(self.rotation(self.t, self.omega0), np.eye(3)):
            rotationText="The object is not rotating"
        with np.printoptions(precision=8):
            return(f"===Ellipsoid Object===\n\nAn ellipsoid defined with the equation x^2/a^2+y^2/b^2+z^2/c^2=1"+
                f"\nSimulation time: t={self.t}"+
                f"\n\nProperties:\nGeometric Parameters: a={self.a}, b={self.b}, c={self.c}"+
                f"\n\nDensity parameter: rho0={self.rho0}"+
                f"\nRotation parameter:{rotationText}"+
                f"\n\nTotal Mass: M={mass_str}"+
                f"\n\nQuadrupole Moment Tensor at Current Time: Q_ij={quad_str}")
    
    #The below code specifies the counds of the object. Currently it is set to an ellipse
    def xbounds(self):
        return -self.a, self.a

    def yboundsUpper(self, x):
        val = 1- x**2/self.a**2
        if val > 0:
            return self.b*np.sqrt(val)
        return 0

    def yboundsLower(self, x):
        val = 1- x**2/self.a**2
        if val > 0:
            return -self.b*np.sqrt(val)
        return 0

    def zboundsUpper(self,x,y):
        val = 1-(x**2/self.a**2+y**2/self.b**2)
        if val>0:
            return self.c*np.sqrt(val)
        return 0


    def zboundsLower(self, x,y):
        val = 1-(x**2/self.a**2+y**2/self.b**2)
        if val>0:
            return -self.c*np.sqrt(val)
        return 0
    

    #Compute properties
    def mass(self):
            """
            Compute the total mass of the object
            """
            def integrand(z,y,x):
                return self.density(z,y,x,self.rho0,self.a,self.b,self.c)
            totalMass=integrate.tplquad(integrand, *self.xbounds(), self.yboundsLower, self.yboundsUpper, self.zboundsLower, self.zboundsUpper)[0]
            self.totalMass=totalMass
            return totalMass
            #Notice *xbounds() return 2 things so it covers both the a,b inputs. The [0] extracts the integral value since the tplquad function returns a tuple (integral value, error)
    def quadrupole_Moment(self):
        """
        Compute the mass quadrupole tensor
        """
        i=1 
        rows=[]
        while i<=3:
            j=1
            col=[]
            while j<=3:
                def integrand(z,y,x):
                    vars = [x, y, z] #The diagonal follows this order
                    r=np.sqrt(x**2+y**2+z**2)
                    if i==j:
                        return self.density(z, y, x, self.rho0, self.a,self.b,self.c)*(vars[i-1]**2-(r**2) / 3)
                    else:
                        return self.density(z, y, x, self.rho0, self.a,self.b,self.c)*(vars[i-1]*vars[j-1])
                term = integrate.tplquad(integrand, *self.xbounds(), self.yboundsLower, self.yboundsUpper, self.zboundsLower, self.zboundsUpper)[0] #Notice *xbounds() return 2 things so it covers both the a,b inputs. The [0] extracts the integral value since the tplquad function returns a tuple (integral value, error)
                col.append(term)
                j+=1
            rows.append(np.array(col))
            i+=1
        tensor = np.array(rows)
        rotationTensor = self.rotation(self.t, self.omega0)
        tensor = rotationTensor @ (tensor @ rotationTensor.T)
        self.quadMom_tensor=tensor
        return tensor 
    
    
#Later add a class for binary stars
#print(curEllipsoid.diagonal())


#Testing region: comment out code in final release
#curEllipsoid = ellipsoid_object(1, 1, 1, 1,densities.const)

#curEllipsoid.quadrupole_Moment()
#curEllipsoid.mass()

#print(repr(curEllipsoid))

def func(obj, t, a, b, c, rho0, densityProfile, omega0, rotator):
    """
    We can use classes as variables
    This is a test function
    """
    object = obj(t, a,b,c,rho0,densityProfile, omega0, rotator)
    object.quadrupole_Moment()
    object.mass()
    return object

#print(func(ellipsoid_object,1, 1, 1, 1, 1, densities.const, 1, rotations.not_rotating))