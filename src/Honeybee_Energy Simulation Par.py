# By Mostapha Sadeghipour Roudsari
# Sadeghipour@gmail.com
# Honeybee started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
EnergyPlus Shadow Parameters
-
Provided by Honeybee 0.0.56

    Args:
        timestep_: A number between 1 and 60 that represents the number of timesteps per hour at which the simulation will be run.  The default is set to 6 timesteps per hour, which means that the energy balance calculation is run every 10 minutes of the year.
        shadowCalcPar_: An optional set of shadow calculation parameters from the "Honeybee_ShadowPar" component.
        solarDistribution_: An optional text string or integer that sets the solar distribution calculation.  Choose from the following options:
            0 = "MinimalShadowing" - In this case, exterior shadowing is only computed for windows and not for other opaque surfaces that might have their surface temperature affected by the sun. All beam solar radiation entering the zone is assumed to fall on the floor. A simple window view factor calculation will be used to distribute incoming diffuse solar energy between interior surfaces.
            1 = "FullExterior" - The simulation will perform the solar calculation in a manner that only accounts for direct sun and whether it is blocked by surrounding context geometry.  For the inside of the building, all beam solar radiation entering the zone is assumed to fall on the floor. A simple window view factor calculation will be used to distribute incoming diffuse solar energy between interior surfaces.
            2 = "FullInteriorAndExterior" - The simulation will perform the solar calculation in a manner that models the direct sun (and wheter it is blocked by outdoor context goemetry.  It will also ray trace the direct sun on the interior of zones to distribute it correctly between interior surfaces.  Any indirect sun or sun bouncing off of objects will not be modled.
            3 = "FullExteriorWithReflections" - The simulation will perform the solar calculation in a manner that accounts for both direct sun and the light bouncing off outdoor surrounding context.  For the inside of the building, all beam solar radiation entering the zone is assumed to fall on the floor. A simple window view factor calculation will be used to distribute incoming diffuse solar energy between interior surfaces.
            4 = "FullInteriorAndExteriorWithReflections" - The simulation will perform the solar calculation in a manner that accounts for light bounces that happen both outside and inside the zones.  This is the most accurate method and is the one assigned by default.  Note that, if you use this method, EnergyPlus will give Severe warnings if your zones have concave geometry (or are "L"-shaped).  Such geometries mess up this solar distribution calculation and it is recommeded that you either break up your zones in this case or not use this solar distribution method.
        simulationControls_: An optional set of simulation controls from the "Honeybee_Simulation Control" component.
        ddyFile_: An optional file path to a .ddy file on your system.  This ddy file will be used to size the HVAC system before running the simulation.
        terrain_: An optional integer or text string to set the surrouning terrain of the building, which will be used to determine how wind speed around the building changes with height.  If no value is input here, the default is set to "City."  Choose from the following options:
            0 = City: large city centres, 50% of buildings above 21m over a distance of at least 2000m upwind.
            1 = Suburbs: suburbs, wooded areas.
            2 = Country: open, with scattered objects generally less than 10m high.
            3 = Ocean: Flat, unobstructed areas exposed to wind flowing over a large water body (no more than 500m inland).
        monthlyGrndTemps_: An optional list of 12 monthly ground temperatures to be used by those surfaces in contact with the ground in the simulation.  Please note that the EPW values out of the Import Ground Temp component are usually too extreme for a conditioned building.  If no values are input here, the model will attempt to estimate a reasonable starting base temperature from these results by using a value of 18C in cases of monthly ground temperatures below 18C, 24C in cases of monthly ground temperatures above 24C, and the actual ground temperature if the monthly average falls in between 18C and 24C.  Usually, ground temperatures will be about 2C lower than the overage indoor air temperature for a given month.
    Returns:
        energySimPar: Energy simulation parameters that can be plugged into the "Honeybee_ Run Energy Simulation" component.
"""

ghenv.Component.Name = "Honeybee_Energy Simulation Par"
ghenv.Component.NickName = 'EnergySimPar'
ghenv.Component.Message = 'VER 0.0.56\nAPR_11_2015'
ghenv.Component.Category = "Honeybee"
ghenv.Component.SubCategory = "09 | Energy | Energy"
#compatibleHBVersion = VER 0.0.56\nAPR_11_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "0"
except: pass


def main(timestep, shadowCalcPar, solarDistribution, simulationControls, ddyFile, terrain, monthlyGrndTemps):
    solarDist = {
                "0" : "MinimalShadowing",
                "1" : "FullExterior",
                "2" : "FullInteriorAndExterior",
                "3" : "FullExteriorWithReflections",
                "4" : "FullInteriorAndExteriorWithReflections",
                "MinimalShadowing" : "MinimalShadowing",
                "FullExterior" : "FullExterior",
                "FullInteriorAndExterior" : "FullInteriorAndExterior",
                "FullExteriorWithReflections" : "FullExteriorWithReflections",
                "FullInteriorAndExteriorWithReflections" : "FullInteriorAndExteriorWithReflections"
                }
    
    terrainDict = {
                "0" : "City",
                "1" : "Suburbs",
                "2" : "Country",
                "3" : "Ocean",
                "City" : "City",
                "Suburbs" : "Suburbs",
                "Country" : "Country",
                "Ocean" : "Ocean"
                }
    
    # I will add check for inputs later
    if timestep == None: timestep = 6
    if shadowCalcPar == []: shadowCalcPar = ["AverageOverDaysInFrequency", 30, 3000]
    if solarDistribution == None:
        solarDistribution = solarDist["4"]
    else:
        solarDistribution = solarDist[solarDistribution]
    if simulationControls == []: simulationControls= [True, True, True, False, True]
    if terrain == None:
        terrain = terrainDict["0"]
    else:
        terrain = terrainDict[terrain]
    
    if monthlyGrndTemps == [] or len(monthlyGrndTemps) == 12:
        return [timestep] + shadowCalcPar + [solarDistribution] + simulationControls + [ddyFile] + [terrain] + [monthlyGrndTemps]
    else:
        return None
        warning = 'monthlyGrndTemps_ must either be left blank or contain 12 values representing the average ground temperature for each month.'
        print warning
        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)

energySimPar = main(timestep_,
                   shadowCalcPar_,
                   solarDistribution_,
                   simulationControls_,
                   ddyFile_, terrain_, monthlyGrndTemps_)