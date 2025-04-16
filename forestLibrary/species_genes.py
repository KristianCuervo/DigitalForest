import random

SPECIES_DEFAULT_PARAMS = {
    "honda": {
        "r1": 0.78,
        "r2": 0.82,
        "alpha1": 29,
        "alpha2": -34,
        "phi1": 136,
        "phi2": 139,
        "q": 0.49,
        "e": 0.57
    },
    "pine": {
        "r1": 0.75,
        "r2": 0.80,
        "r3": 0.6,
        "alpha1": 25,
        "alpha2": -30,
        "alpha3": 0,
        "phi1": 140,
        "phi2": 145,
        "phi3": 180,
        "q": 0.50,
        "e": 0.60
    },
    "bush": {
        "r1": 0.65,
        "alpha1": 35,
        "phi1": 45,
        "q": 0.45,
        "e": 0.50
    },
    "fern": {
        "r1": 0.6,
        "alpha1": 25,
        "phi1": 90,
        "q": 0.4,
        "e": 0.5
    },
    "binary": {
        "r1": 0.7,
        "alpha1": 30,
        "phi1": 35,
        "q": 0.5,
        "e": 0.6
    },
    "stochastic": {
        "r1": 0.68,
        "alpha1": 33,
        "phi1": 38,
        "q": 0.52,
        "e": 0.58
    }
}
def get_species_params(species_name:str, stochastic_range=0.05) -> dict:
    """
    Returns a copy of the default params for a given species, 
    with a small random +/- variation on each parameter.
    """
    defaults = SPECIES_DEFAULT_PARAMS[species_name]
    new_params = {}
    for k, v in defaults.items():
        if isinstance(v, (float, int)):
            variation = v * random.uniform(-stochastic_range, stochastic_range)
            new_params[k] = v + variation
        else:
            # If parameter is not numeric, keep it as is
            # Could be colours, branch width. etc.
            new_params[k] = v
    return new_params