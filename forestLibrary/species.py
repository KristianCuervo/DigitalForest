import random
from .tree import Tree

class HondaTree(Tree):
    def __init__(self, genes, height_mod):
        axiom = [('A', 0.7, 0.3)]
        super().__init__(genes, height_mod, axiom=axiom)

    def production_rule(self, sym):
        r1 = self.genes['r1']
        r2 = self.genes['r2']
        alpha1 = self.genes['alpha1']
        alpha2 = self.genes['alpha2']
        phi1 = self.genes['phi1']
        phi2 = self.genes['phi2']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w1 = w * q**e
                w2 = w * (1 - q)**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha1), ('/', phi1), ('A', s * r1, w1), ']',
                    '[', ('+', alpha2), ('/', phi2), ('A', s * r2, w2), ']'
                ]
            case _:
                return [sym]
            
class ShrubTree(Tree):
    """
    Wide-first shrub: horizontal runners (`H`) split left/right until their
    length drops below `bushy_start`, then the node converts to a bushy
    shoot (`B`) that fills the local area with short branches.
    """
    def __init__(self, genes, height_mod):
        axiom = [('H', 0.5, 0.25)]               # start with one runner
        super().__init__(genes, height_mod, axiom=axiom)

    # ───────────────────────────────────────────────────────────────────
    def production_rule(self, sym):
        g = self.genes
        r_h, r_b  = g['r_horiz'], g['r_bush']
        alpha, phi= g['alpha'], g['phi']
        n_bushy   = int(g['n_bushy']) + 1
        bushy_thr = g['bushy_start']
        q, e      = g['q'], g['e']

        # equally spaced yaw angles for the later bushy shoots
        yaw_step  = 360 / n_bushy
        bushy_yaws= [i * yaw_step for i in range(n_bushy)]

        match sym:

            # ─────────────────────────────────────────────── Runner (H)
            case ('H', s, w):
                w_next = w * q**e
                out = [('!', w),                   # width for this segment
                       ('+', 90), ('/', phi),      # tilt horizontal once
                       ('F', s)]                   # move

                if s > bushy_thr:
                    # keep sending out two opposite runners
                    for sign in (+1, -1):
                        out += [
                            '[', ('+', sign * alpha),
                                  ('H', s * r_h, w_next), ']'
                        ]
                else:
                    # convert to a bushy shoot
                    out += [('B', s * r_b, w_next)]

                return out

            # ─────────────────────────────────────── Bushy shoot (phase 2)
            case ('B', s, w):
                if s < 0.05:                       # final twig
                    return [('!', w), ('F', s)]

                w_next = w * q**e
                out = [('!', w), ('F', s * 0.6)]   # short trunk

                # spread n_bushy short shoots radially
                for yaw in bushy_yaws:
                    out += [
                        '[', ('+', yaw), ('/', 60),
                              ('B', s * r_b, w_next), ']'
                    ]
                return out

            # ────────────────────────────────────────────────────────────
            case _:
                return [sym]
            

class PineTree(Tree):
    """
    Tall stem that starts branching only after the trunk narrows enough,
    with a bit of randomness for natural variation.
    """
    def __init__(self, genes, height_mod):
        axiom = [('T', 1.5, 0.25)]
        super().__init__(genes, height_mod, axiom=axiom)

    def production_rule(self, sym):
        g = self.genes
        r_t, r_b = g['r_trunk'], g['r_branch']
        
        # base angles
        base_alpha, base_phi = g['alpha'], g['phi']
        # how much to jitter them
        angle_var = g.get('angle_variation', 10)            # ±10° by default
        alpha = base_alpha + random.uniform(-angle_var, angle_var)
        phi   = base_phi   + random.uniform(-angle_var, angle_var)

        # branch‐count jitter
        target_branches = g.get('branch_count', 2)           # default 2
        branch_count   = target_branches + random.choice([-1, 0, 1])
        branch_count   = max(1, min(4, branch_count))        # clamp between 1 and 4

        # how much branch‐length can vary
        length_var = g.get('branch_length_variation', 0.2)   # ±20% by default

        q, e  = g['q'], g['e']
        s_min = g['min_branch_size']

        match sym:
            case ('T', s, w):
                # trunk symbol
                w_next = w * q**e
                out = [('!', w), ('F', s)]

                if s > s_min and self.age <= 8:
                    # keep growing straight
                    out += [('T', s * r_t, w_next)]
                else:
                    # time to branch!
                    for _ in range(branch_count):
                        sign = random.choice((+1, -1))
                        # jitter branch length
                        s_branch = (s / r_b) * random.uniform(1-length_var, 1+length_var)
                        out += [
                            '[', ('+', sign * alpha), ('/', phi),
                                  ('B', s_branch, w_next),
                            ']'
                        ]
                    # continue with a bit more trunk
                    out += [('T', s * r_t, w_next)]

                return out

            case ('B', s, w):
                # branch symbol: you can add similar jitter here if you like
                if s < 0.05:
                    return [('!', w), ('F', s)]

                w_next = w * q**e
                out = [('!', w), ('F', s),
                       ('B', s * r_b, w_next)]
                # optional side‐forks with jittered angles
                for sign in (+1, -1):
                    angle = random.uniform(20, 30)  # a little irregular
                    out += ['[', ('+', sign * angle), ('B', s * r_b, w_next), ']']
                return out

            case _:
                return [sym]
            

class FernTree(Tree):
    def __init__(self, genes, height_mod):
        axiom = [('A', 0.6, 0.1)]
        super().__init__(genes, height_mod, axiom=axiom)

    def production_rule(self, sym):
        r = self.genes['r1']
        alpha = self.genes['alpha1']
        phi = self.genes['phi1']
        q = self.genes['q']
        e = self.genes['e']

        match sym:
            case ('A', s, w):
                w_new = w * q**e
                return [
                    ('!', w), ('F', s),
                    '[', ('+', alpha), ('/', phi), ('A', s * r, w_new), ']',
                    ('F', s),
                    '[', ('-', alpha), ('/', -phi), ('A', s * r, w_new), ']',
                    ('F', s)
                ]
            case _:
                return [sym]
