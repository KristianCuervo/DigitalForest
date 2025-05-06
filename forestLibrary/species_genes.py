import random

HONDA_GENES = [
{
        # D Tree
        "species": "oak",
        # branch‐length scalers
        "r1": 0.60, "r2": 0.85,
        # yaw (left/right) angles
        "alpha1": 25, "alpha2": -15,
        # pitch angles (tilt branches up)
        "phi1": 180,  # right branch up 50°
        "phi2": 180,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.45, "e": 0.50
        },
{
        # G Tree
        "species": "birch",
        # branch‐length scalers
        "r1": 0.80, "r2": 0.80,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.50, "e": 0.50
        },
{
        # I Tree
        "species": "oak",
        # branch‐length scalers
        "r1": 0.55, "r2": 0.95,
        # yaw (left/right) angles
        "alpha1": -5, "alpha2": 30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.40, "e": 0.00
        }

]

SHRUB_GENES = [
    {   # low, very broad cushion
        "species"       : "shrub",
        "r_horiz"       : 0.80,   # runner scale-down
        "r_bush"        : 0.60,   # bushy shoot scale-down
        "alpha"         : 45,     # yaw for new runners
        "phi"           : 90,      # 0 → keep runners horizontal
        "n_bushy"       : 2,      # branches per bushy shoot
        "bushy_start"   : 0.30,   # switch to B when s < 0.30
        "q"             : 0.50,   # thickness factor
        "e"             : 0.55,
    },
    {   # medium cushion
        "species":"shrub", "r_horiz":0.78, "r_bush":0.62,
        "alpha":35, "phi":90, "n_bushy":2, "bushy_start":0.25,
        "q":0.48, "e":0.55
    },
    {   # tighter, slightly taller mound
        "species":"shrub", "r_horiz":0.75, "r_bush":0.58,
        "alpha":30, "phi":90, "n_bushy":3, "bushy_start":0.28,
        "q":0.52, "e":0.55
    },
]


PINE_GENES = [
    { "species":"pine", "r_trunk":0.75, "r_branch":0.80,
      "alpha":80, "phi":110, "min_branch_size":0.40, "q":0.35, "e":0.50 },
    { "species":"pine", "r_trunk":0.70, "r_branch":0.78,
      "alpha":90, "phi":120, "min_branch_size":0.35, "q":0.32, "e":0.50 },
    { "species":"pine", "r_trunk":0.78, "r_branch":0.85,
      "alpha":75, "phi":105, "min_branch_size":0.45, "q":0.38, "e":0.50 },
]


reduced_SPECIES = {
    "honda": HONDA_GENES,
    "shrub": SHRUB_GENES,
    "pine": PINE_GENES
}




SPECIES_DEFAULT_PARAMS = {
    "honda": [
        {
        # D Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.60, "r2": 0.85,
        # yaw (left/right) angles
        "alpha1": 25, "alpha2": -15,
        # pitch angles (tilt branches up)
        "phi1": 180,  # right branch up 50°
        "phi2": 180,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.45, "e": 0.50
        },
        {
        # E Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.58, "r2": 0.83,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": 15,
        # pitch angles (tilt branches up)
        "phi1": 0,  # right branch up 50°
        "phi2": 180,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.40, "e": 0.50
        },
        {
        # G Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.80, "r2": 0.80,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.50, "e": 0.50
        },
        {
        # H Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.95, "r2": 0.80,
        # yaw (left/right) angles
        "alpha1": 5, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": -90,  # right branch up 50°
        "phi2": 90,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.60, "e": 0.45
        },
        {
        # I Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.55, "r2": 0.95,
        # yaw (left/right) angles
        "alpha1": -5, "alpha2": 30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.40, "e": 0.00
        },
        ],
    "pine": {
        "species": "pine",
        "r1": 0.75, "r2": 0.80, "r3": 0.65,
        "alpha1": 35, "alpha2": -35, "alpha3": 0,
        "phi1": 60,  # main fork up 60°
        "phi2": 55,  # secondary up 55°
        "phi3": 50,  # tertiary up 50°
        "q": 0.50, "e": 0.60
    },
    "bush": {
        "species": "bush",
        "r1": 0.65,
        "alpha1": 25,
        "phi1": 65,   # wide bushy upward sprout
        "q": 0.45, "e": 0.50
    },
    "fern": {
        "species": "fern",
        "r1": 0.60,
        "alpha1": 25,
        "phi1": 50,   # gentle frond lift
        "q": 0.40, "e": 0.50
    },
    "binary": {
        "species": "binary",
        "r1": 0.70,
        "alpha1": 30,
        "phi1": 75,   # steep binary split
        "q": 0.50, "e": 0.60
    },
    "stochastic": {
        "species": "stochastic",
        "r1": 0.68,
        "alpha1": 30,
        "phi1": 55,   # random‐style lift
        "q": 0.52, "e": 0.58
    }
}


SPECIES_DEFAULT_PARAMS = {
    "honda": [
        {
        # D Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.60, "r2": 0.85,
        # yaw (left/right) angles
        "alpha1": 25, "alpha2": -15,
        # pitch angles (tilt branches up)
        "phi1": 180,  # right branch up 50°
        "phi2": 180,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.45, "e": 0.50
        },
        {
        # E Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.58, "r2": 0.83,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": 15,
        # pitch angles (tilt branches up)
        "phi1": 0,  # right branch up 50°
        "phi2": 180,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.40, "e": 0.50
        },
        {
        # G Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.80, "r2": 0.80,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.50, "e": 0.50
        },
        {
        # H Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.95, "r2": 0.80,
        # yaw (left/right) angles
        "alpha1": 5, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": -90,  # right branch up 50°
        "phi2": 90,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.60, "e": 0.45
        },
        {
        # I Tree
        "species": "honda",
        # branch‐length scalers
        "r1": 0.55, "r2": 0.95,
        # yaw (left/right) angles
        "alpha1": -5, "alpha2": 30,
        # pitch angles (tilt branches up)
        "phi1": 137,  # right branch up 50°
        "phi2": 137,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.40, "e": 0.00
        },
        ],
    "pine": {
        "species": "pine",
        "r1": 0.75, "r2": 0.80, "r3": 0.65,
        "alpha1": 35, "alpha2": -35, "alpha3": 0,
        "phi1": 60,  # main fork up 60°
        "phi2": 55,  # secondary up 55°
        "phi3": 50,  # tertiary up 50°
        "q": 0.50, "e": 0.60
    },
    "bush": {
        "species": "bush",
        "r1": 0.65,
        "alpha1": 25,
        "phi1": 65,   # wide bushy upward sprout
        "q": 0.45, "e": 0.50
    },
    "fern": {
        "species": "fern",
        "r1": 0.60,
        "alpha1": 25,
        "phi1": 50,   # gentle frond lift
        "q": 0.40, "e": 0.50
    },
    "binary": {
        "species": "binary",
        "r1": 0.70,
        "alpha1": 30,
        "phi1": 75,   # steep binary split
        "q": 0.50, "e": 0.60
    },
    "stochastic": {
        "species": "stochastic",
        "r1": 0.68,
        "alpha1": 30,
        "phi1": 55,   # random‐style lift
        "q": 0.52, "e": 0.58
    }
}

def get_species_params(species_name: str, param_dict: dict, stochastic_range: float = 0.05) -> dict:
    """
    Returns a copy of the default params for a given species,
    with a small random +/- variation on each numeric parameter.
    """
    defaults = param_dict[species_name]
        
    if type(defaults) is list:
        defaults = random.choice(defaults)
            
    new_params = {}
    for k, v in defaults.items():
        if isinstance(v, (float, int)):
            variation = v * random.uniform(-stochastic_range, stochastic_range)
            new_params[k] = v + variation
        else:
            new_params[k] = v
    return new_params
