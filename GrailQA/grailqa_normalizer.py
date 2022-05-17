import re
import json
import tqdm
from sparql.translator import Translator
from tqdm import tqdm
from ir.translator import Translator as IR_Translator
from kopl.translator import Translator as KOPL_Translator


ROOT = '../../../../ldata/sjd/UIR'



def grailqa_normalizer(q: str):

    dtype = {
        "<http://www.w3.org/2001/XMLSchema#float>": "xsd:float",
        "<http://www.w3.org/2001/XMLSchema#integer>": "xsd:int",
        "<http://www.w3.org/2001/XMLSchema#gYear>": "xsd:year",
        "<http://www.w3.org/2001/XMLSchema#gYearMonth>": "xsd:date",
        "<http://www.w3.org/2001/XMLSchema#date>": "xsd:date",
        "<http://www.w3.org/2001/XMLSchema#dateTime>": "xsd:time"
        # keep adding on ...
    }

    pv_count = 0
    var_mapping = {}
    # Match (and substitute if existed) the third SELECT-WHERE chunk
    match = re.search(r'\{\nSELECT \((MAX|MIN)\(\?y\d\) AS \?x\d\)  WHERE \{ \n[\s\S]*\}\n\}(?=\n(\?|.))', q)
    if match is not None:
        order = re.search(r'(?<=SELECT \()(MIN|MAX)(?=\(\?)', q).group(0)
        v = re.search(r'(?<={}\(\?y\d\) AS )(\?x\d)'.format(order), q).group(0)
        q = re.sub(r'\{\nSELECT \((MAX|MIN)\(\?y\d\) AS \?x\d\)  WHERE \{ \n[\s\S]*\}\n\}(?=\n(\?|.))', '', q)
        q = q.replace(v, '?pv')
        q = re.sub(r'(?<!FILTER[^\n])(?<=\?pv \. )\n', '\n?pv <pred:value> ?v .\n', q)
        pv_count += 1

    cls_count = 0
    lines = q.split('\n')
    lines = [lines[1]] + lines[3:-1]
    cls_mapping = {}

    new_lines = []

    # plain and simple string matching
    for line in lines:
        line = line.strip()
        new_line = []
        if "PREFIX" not in line:
            if "SELECT" in line:
                if line == "SELECT (?x0 AS ?value) WHERE {":
                    new_line.append("SELECT DISTINCT ?e WHERE {")
                elif line == "SELECT (COUNT(?x0) AS ?value) WHERE {":
                    new_line.append("SELECT (COUNT(DISTINCT ?e) AS ?count) WHERE {")
                elif line == "SELECT DISTINCT ?x0  WHERE { ":
                    pass
                else:
                    # print(q)
                    raise Exception

            elif line.endswith('.'):
                triple = line.split()[:3]
                if "?" in triple[1]:
                    raise Exception
                for i in range(3):
                    if triple[i].startswith("?"):
                        new_var = triple[i].replace("x", "e_").replace("_0", "")
                        line = line.replace(triple[i], new_var)

                if triple[1] == ":type.object.type":
                    line = line.replace(triple[1], "<pred:instance_of>")
                    cls_label = triple[2]
                    if cls_label not in cls_mapping.keys():
                        cls_var = "?c_{}".format(cls_count).replace("_0", "")
                        cls_mapping[cls_label] = cls_var
                        cls_count += 1
                        line = line.replace(triple[2], cls_var)
                        new_line.append(line)
                        new_line.append('{} <pred:name> {} .'.format(cls_var, cls_label))
                    else:
                        cls_var = cls_mapping[cls_label]
                        line = line.replace(triple[2], cls_var)
                        new_line.append(line)
                else:
                    new_line.append(line)
            elif line.startswith("VALUES"):
                _, head, _, tail, _ = line.split()
                replaced = False
                for key in dtype.keys():
                    if key in tail:
                        tail = tail.replace(key, dtype[key])
                        replaced = dtype[key][4:]
                        break

                if not replaced:
                    if head.startswith("?"):
                        head = head.replace("x", "e_").replace("_0", "")
                    new_line.append('{} <pred:name> {} .'.format(head, tail))
                else:
                    if head.startswith("?"):
                        head = head.replace("x", "e_").replace("_0", "")
                        var_mapping[head] = "?pv_{}".format(pv_count).replace("_0", "")
                    new_line.append('{} <pred:{}> {} .'.format(head, replaced, tail))

            elif line.startswith("FILTER"):
                if "?x0 != ?" in line:
                    pass
                else:
                    replaced = False
                    for key in dtype.keys():
                        if key in line:
                            line = line.replace(key, dtype[key])
                            replaced = True
                            break

                    if not replaced:
                        raise Exception

        new_lines.extend(new_line)

    new_lines.append('}')
    if match is not None:
        if order == 'MIN':
            new_lines.append('ORDER BY ?v LIMIT 1')
        else:
            new_lines.append('ORDER BY DESC(?v) LIMIT 1')

    new_q = ""
    for nl in new_lines:
        for key in var_mapping.keys():
            nl = nl.replace(key, var_mapping[key])
        new_q = new_q + ' ' + nl

    return new_q.strip()


def normalize(src: str):
    with open(src) as f:
        grail = json.load(f)

    tar_grail = []
    for idxs in tqdm(range(len(grail))):
        new_grail = grail[idxs]
        logical_form = grail[idxs]['sparql_query']
        logical_form = grailqa_normalizer(logical_form)
        for node in grail[idxs]['graph_query']['nodes']:
            if f" :{node['id']} " in logical_form:
                logical_form = logical_form.replace(f" :{node['id']} ", f" \"{node['friendly_name']}\" ")

        for edge in grail[idxs]['graph_query']['edges']:
            if f" :{edge['relation']} " in logical_form:
                logical_form = logical_form.replace(f" :{edge['relation']} ", f" <{edge['friendly_name']}> ")

        translator = Translator()

        ir = translator.to_ir(logical_form)
        new_grail['ir'] = ir
        tar_grail.append(new_grail)

    return tar_grail


