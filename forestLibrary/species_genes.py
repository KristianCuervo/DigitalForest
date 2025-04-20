import random

SPECIES_DEFAULT_PARAMS = {
    "honda": {
        "species": "honda",
        # branch‐length scalers
        "r1": 0.78, "r2": 0.82,
        # yaw (left/right) angles
        "alpha1": 30, "alpha2": -30,
        # pitch angles (tilt branches up)
        "phi1": 50,  # right branch up 50°
        "phi2": 40,  # left branch up 40°
        # thickness factor & exponent
        "q": 0.49, "e": 0.57
    },
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

def get_species_params(species_name: str, stochastic_range: float = 0.05) -> dict:
    """
    Returns a copy of the default params for a given species,
    with a small random +/- variation on each numeric parameter.
    """
    defaults = SPECIES_DEFAULT_PARAMS[species_name]
    new_params = {}
    for k, v in defaults.items():
        if isinstance(v, (float, int)):
            variation = v * random.uniform(-stochastic_range, stochastic_range)
            new_params[k] = v + variation
        else:
            new_params[k] = v
    return new_params
