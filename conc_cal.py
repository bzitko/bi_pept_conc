from collections import OrderedDict

class Value(object):
    """
    Class containing value and error segment.

    For example 412+-3
    """

    @staticmethod
    def is_whole(num):
        return num == int(num)

    def __init__(self, eps, sd=0):
        """

        """
        self.eps = eps
        self.sd = sd

    @staticmethod
    def create(val):
        if isinstance(val, (int, float)):
            return Value(val)
        elif isinstance(val, Value):
            return val
        return Value(*val)

    def __str__(self):
        format_eps = "{:.0f}" if Value.is_whole(self.eps) else "{:.2f}"
        if self.sd == 0:
            return format_eps.format(self.eps)
        format_sd = "{:.0f}" if Value.is_whole(self.sd) else "{:.2f}"

        return (format_eps + " ± " + format_sd).format(self.eps, self.sd)

    def __repr__(self):
        return "{}({}, {})".format(Value.__name__, self.eps, self.sd)




class Model(object):

    AMINO_ACIDS = "ARNDCEQGHILKMFPSTUWYV"
    CTERMS = ["#", "*"]
    COUNTERIONS = OrderedDict([("Cl", 35.453), ("TFA", 114.02), ("Ac", 60.05)])

    MOL_MASSES = {"H": 1.00794, "OH": 17.008, "NH2": 16.02258}
    AA_MASSES = {
        "A":    71.0779,
        "R":    156.1857,
        "N":    114.1026,
        "D":    115.0874,
        "C":    103.1429,
        "E":    129.114,
        "Q":    128.1292,
        "G":    57.0513,
        "H":    137.1393,
        "I":    113.1576,
        "L":    113.1576,
        "K":    128.1723,
        "M":    131.1961,
        "F":    147.1739,
        "P":    97.1152,
        "S":    87.0773,
        "T":    101.1039,
        "U":    150.0379,
        "W":    186.2099,
        "Y":    163.1733,
        "V":    99.1311,
    }



    def __init__(self, name, color="", peptides={}, cterms={}, lys_args="", side_chain=0, peptide_bond=0, ss_bond=0):
        self.name = name
        self.color = color
        self._peptides = {key: Value.create(val) for key, val in peptides.items()}
        self._cterms = {key: Value.create(val) for key, val in cterms.items()}
        self._lys_args = lys_args
        self._side_chain = Value.create(side_chain)
        self._peptide_bond = Value.create(peptide_bond)
        self._ss_bond = Value.create(ss_bond)

        self._total_lys_args = 0
        self._total_mw = 0
        self._total_extinction = Value(0)

    def peptide(self, peptide):
        return self._peptides.get(peptide, Value(0, 0))

    def cterm(self, cterm):
        return self._cterms.get(cterm, Value(0, 0))

    def side_chain(self):
        return self._side_chain

    def peptide_bond(self):
        return self._peptide_bond

    def ss_bond(self):
        return self._ss_bond

    def _sum_for_extinction(self, peptide_seq, cterm=""):
        return Value(
            sum(self.peptide(p).eps for p in peptide_seq) \
            + self.cterm(cterm).eps,

            sum(self.peptide(p).sd ** 2 for p in peptide_seq) \
            + self.cterm(cterm).sd ** 2)

    def _sum_lys_args(self, peptide_seq):
        return sum(1 if p in self._lys_args else 0 for p in peptide_seq)

    def calc_extinction(self, peptide_seq, cterm="", num_ss_bridges=0):
        pept_len = len(peptide_seq)
        sum_ext = self._sum_for_extinction(peptide_seq, cterm)

        total_eps = (pept_len - 1) * self._peptide_bond.eps \
            + sum_ext.eps \
            + pept_len * self._side_chain.eps \
            + num_ss_bridges * self._ss_bond.eps

        total_sd = self._peptide_bond.sd**2 * (pept_len - 1 + num_ss_bridges) \
            + sum_ext.sd
        total_sd **= 0.5

        total_mw = sum(Model.AA_MASSES[aa] for aa in peptide_seq) + Model.MOL_MASSES["H"] + Model.MOL_MASSES[Constants.CTERMS[cterm]]

        self._total_lys_args = self._sum_lys_args(peptide_seq)
        self._total_extinction = Value(total_eps, total_sd)
        self._total_mw = Value(total_mw)

        return self._total_extinction, self._total_lys_args, self._total_mw

    def calc_pept_conc_by_weight(self, mw, weight, volume, counterion):
        if isinstance(mw, Value): mw = mw.eps
        mw_ci = mw + (1 + self._total_lys_args) * Model.COUNTERIONS.get(counterion)
        peptide1 = weight / volume
        peptide2 = weight / (mw_ci * volume) * 1000

        total_exp = (peptide2 / 1000) * self._total_extinction.eps
        return mw_ci, peptide1, peptide2, total_exp

    def calc_concetration(self, absorption, pathlength, dilution):
        eps = (absorption / (self._total_extinction.eps * pathlength)) * dilution * 1000
        sd = self._total_extinction.sd / self._total_extinction.eps * eps
        return Value(eps, sd)



class Constants(object):

    AMINO_ACIDS = "ARNDCEQGHILKMFPSTUWYV"
    CTERMS = OrderedDict([("#", "NH2"), ("*", "OH")])

def runtime_models():
    models = {
    214: Model(
        name=214,
        color="#fffb7e",
        peptides={
            "W": (29000, 4000),
            "Y": (5500, 500),
            "F": (5500, 500),
            "H": (5500, 500),
            "P": (2700, 150),
            "M": (1000, 50),
            "N": 100,
            "Q": 100,
            "D": 30,
            "E": 30},
        cterms={"#": 100},
        lys_args="RK",
        side_chain=30,
        peptide_bond=(950, 50),
        ss_bond=(1150, 50)),

    280: Model(
        name=280,
        color="#7effd5",
        peptides={
            "W": (5500, 150),
            "Y": (1250, 150)},
        lys_args="RK",
        cterms={},
        peptide_bond=0,
        ss_bond=(125, 50)),

    257: Model(
        name=257,
        color="#7e9aff",
        peptides={
            "W": (3200, 200),
            "Y": (480, 80),
            "F": (190, 20)},
        lys_args="RK",
        ss_bond=(320, 20)),
    }
    return models

def load_models():
    import json
    from pprint import pprint

    with open('models.json') as data_file:    
        data = json.load(data_file)

    models = {}
    for m in data:
        model_id = int(m["name"])
        model = Model(
            model_id,
            m["color"],
            m["peptides"],
            m.get('cterms', {}),
            m.get('lys_args', ""),
            m.get('side_chain', 0),
            m.get('peptide_bond', 0),
            m.get('ss_bond', 0)
            )

        models[model_id] = model
    return models


"""
**** DATA 1
I peptide_seq --> max_num_ss_bonds
I cterm
IC num_ss_bonds --> total_lys_args, total_extinctions

**** DATA 2
S1 total_extinctions
S1 total_lys_args
-----------------
I mw
I weight
I volume
I counterior --> mw_ci, peptide1, peptide2, total_exp

**** DATA 3
S1 total_extinctions
-----------------
I abpsorption
I pathlength
I dilution


"""

models = load_models()

if __name__ == '__main__':
    peptide_seq = None
    cterm = None
    num_ss_bridges = None

    peptide_seq = "FLGRFFRRTQAIFRGARQGWRKL"
    cterm = "#"
    peptide_seq = peptide_seq.strip().upper().replace(" ", "")

    peptide_len = len(peptide_seq) - 1

    max_ss_bridges = peptide_seq.count("C") // 2
    num_ss_bridges = 0

    models = runtime_models()

    MODEL_NUM = 214

    data = {214: (0.42, 1, 100), 280: (0.4, 1, 10), 257: (0, 1, 1)}


    # 1. CALCULATE EXTINCTION FOR PEPTIDE_SEQ, CTERM and NUM_SS_BRIDGES
    print(MODEL_NUM)
    x = models[MODEL_NUM].calc_extinction(peptide_seq, cterm)
    print(x)
    # 2. CALCULATE PEPTIDE CONCETRATION PER WEIGHT
    y = models[MODEL_NUM].calc_pept_conc_by_weight(2625.50, 2.30, 1.15, "Ac")
    print(y)
    # 3. CALCULATE CONCETRATION PER MODEL
    z = models[MODEL_NUM].calc_concetration(*data[MODEL_NUM])
    print(z)

    print("wer".isdigit())
    #load_models()
