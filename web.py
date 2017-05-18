from bottle import route, run, template, static_file, request
import json
from conc_cal import *




@route('/_calc')
def _calc():
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    data = {"errors": {}, 
            "htmls": {},
            "values": {}}




    # 1. GET DATA
    peptide_seq = request.params.get('peptide_seq', '', type=str)
    cterm = request.params.get('cterm', '', type=str)
    max_ss_bonds = request.params.get('num_ss_bonds', 0, type=int)
    num_ss_bonds = request.params.get('num_ss_bonds', 0, type=int)


    # 1. VALIDATE DATA
    peptide_seq = peptide_seq.replace(" ", "").upper()
    not_valid1 = ",".join(sorted(set(peptide_seq) - set(Constants.AMINO_ACIDS)))
    if not_valid1:
        data["errors"]["peptide_seq"] = "{} are not valid amino acids".format(not_valid1)

    calculate1 = (not not_valid1) and peptide_seq


    data["values"]["peptide_seq"] = peptide_seq

    # 1. HTML DATA
    new_max_ss_bonds = peptide_seq.upper().count("C") // 2
    new_num_ss_bonds = num_ss_bonds
    if new_num_ss_bonds > new_max_ss_bonds:
        new_num_ss_bonds = 0

    if (new_num_ss_bonds, new_max_ss_bonds) != (num_ss_bonds, max_ss_bonds):
        num_ss_bonds, max_ss_bonds = new_num_ss_bonds, new_max_ss_bonds        
        html = "\n".join('<option value="{}">{}</option>'.format(i, i) 
            for i in range(max_ss_bonds + 1))
        data["htmls"]["num_ss_bonds"] = html
        data["values"]["num_ss_bonds"] = num_ss_bonds


    # 1. CALCULATE DATA
    mw = 0
    for model_num, model in models.items():
        if calculate1:
            extinction, _, mw = model.calc_extinction(peptide_seq, cterm, num_ss_bonds)
        else:
            extinction, mw = "", ""
        data["values"]["m{}_extinction".format(model_num)] = str(extinction)
        data["values"]["mw"] = str(mw)
        print("**** MW", mw)

    # 2. GET DATA
    calculate2 = calculate1
    columns2 = ["weight", "volume"]
    data2 = {"counterion": request.params.get("counterion", type=str),
             "mw": mw}
    for item in columns2:
        val = request.params.get(item, type=str).replace(",", ".")
        if not val:
            calculate2 = False
        else:
            if isfloat(val):
                val = float(val)
                data2[item] = val
                data["values"][item] = str(val)
            else:
                calculate2 = False
                data["errors"][item] = "not a number"

    # 2. CALCULATE DATA
    for model_id, model in models.items():
        if calculate2:
            mw_ci, peptide1, peptide2, total_exp = model.calc_pept_conc_by_weight(
                data2["mw"], data2["weight"], data2["volume"], data2["counterion"])
            data["values"]["mw_ci"] = "{:.02f}".format(mw_ci)
            data["values"]["peptide1"] = "{:.02f}".format(peptide1)
            data["values"]["peptide2"] = "{:.02f}".format(peptide2)  
            data["values"]["m{}_expected".format(model_id)] = "{:.02f}".format(total_exp)
        else:
            data["values"]["mw_ci"] = ""
            data["values"]["peptide1"] = ""
            data["values"]["peptide2"] = ""
            data["values"]["m{}_expected".format(model_id)] = ""


    # 3. GET DATA
    calculate3 = {model_id: calculate1 for model_id in models}
    data3 = {model_id: {"absorption":"", "pathlength":"", "dilution":""} for model_id in models}
    for model_id, model_data in data3.items():
        for item in model_data:
            arr_item = "m{}_{}".format(model_id, item)
            val = request.params.get(arr_item, type=str).replace(",",".")
            if not val:
                calculate3[model_id] = False
            else:
                if isfloat(val):
                    val = float(val)
                    model_data[item] = val
                    data["values"][arr_item] = str(val)
                else:
                    calculate3[model_id] = False
                    data["errors"][arr_item] = "not a number"

    # 3. CALCULATE DATA
    for model_id, model in models.items():
        model_data = data3[model_id]
        if calculate3[model_id]:
            extinction = data["values"]["m{}_extinction".format(model_id)]
            absorption = model_data["absorption"]
            pathlength = model_data["pathlength"]
            dilution = model_data["dilution"]

            if extinction != "0":
                c = model.calc_concetration(absorption, pathlength, dilution)
            else:
                c = ""
                data["errors"]["m{}_extinction".format(model_id)] = "division by zero"
            data["values"]["m{}_c".format(model_id)] = str(c)
        else:
            data["values"]["m{}_c".format(model_id)] = ""
    
    
    return json.dumps(data)


@route('/run')
def index():
    return template(open("web.tpl").read(),
        request=request,
        models=models,
        Model=Model,
        Constants=Constants)

@route('/css/<filename>.css')
def stylesheets(filename):
    return static_file('{}.css'.format(filename), root='css')

#print(models)

run(host='0.0.0.0', port=8080)
