from graphq_trans.utils import *


class EntitySet:
    def __init__(self, var=None, label=None, concept=None):
        self._var = var
        self._label = label
        self._concept = concept
        self.__atom = ""
        self.init_atom()

        self.related_es = {}
        self.related_attr = {}

    def init_atom(self):
        if not self._label and not self._concept:
            self.__atom = "ones"
        elif not self._concept:
            self.__atom = "<E> {} </E>".format(self._label)
        elif not self._label:
            self.__atom = "<ES> <C> {} </C> </ES>".format(self._concept)
        else:
            self.__atom = "<ES> <C> {} </C> <E> {} </E> </ES>".format(self._concept, self._label)

    def add_related_es(self, predicate, edge_var, direction, es, qualifier_constraints: list):
        assert isinstance(es, EntitySet)
        if es not in self.related_es.keys():
            self.related_es[es] = {"predicate": predicate, "edge_var": edge_var, "direction": direction,
                                   "entitySet": es, "qualifier": qualifier_constraints}
        else:
            raise Exception("this entitySet has already been added!")

    def add_related_attr(self, attr, symOP, v_type, val):
        if attr == "name":
            self.set_label(val)
        else:
            if attr not in self.related_attr.keys():
                self.related_attr[attr] = []
            self.related_attr[attr].append([attr, symOP, v_type, val])

    def get_ir(self, forbidden=[]):
        atom = self.__atom
        filtersByAttr = sorted(list(self.related_attr.values()), key=lambda x: len(x), reverse=True)
        for filt in filtersByAttr:
            while len(filt) != 0:
                atom = "<ES> " + atom + " whose <A> {} </A> {} {} <V> {} </V> </ES>".format(*filt.pop())

        ir = ""

        for key in self.related_es.keys():
            if key not in forbidden:
                if self.related_es[key]["direction"] in ["forward", "backward"]:
                    new_ir = ""
                    ir_atom = atom + " that <R> {} </R> {} to {}".format(
                        self.related_es[key]["predicate"],
                        self.related_es[key]["direction"],
                        self.related_es[key]["entitySet"].get_ir([self])
                    )
                    ir_atoms = []
                    for attr, sym, v_type, val in self.related_es[key]["qualifier"]:
                        ir_atoms.append("<ES> " + ir_atom + " ( <Q> {} </Q> {} {} <V> {} </V> </ES> )".format(
                            attr, sym, v_type, val
                        ))

                    if len(ir_atoms) == 0:
                        new_ir = "<ES> {} </ES>".format(ir_atom)
                    else:
                        new_ir = ir_atoms.pop()
                        while len(ir_atoms):
                            new_ir = "<ES> {} and {} </ES>".format(new_ir, ir_atoms.pop())

                    if ir == "":
                        ir = new_ir
                    else:
                        ir = "<ES> {} and {} </ES>".format(ir, new_ir)
                else:
                    raise Exception("Current GraphQ IR does not support undirected edge!")

        if not ir:
            ir = atom

        return ir

    def set_label(self, label):
        self._label = label
        self.init_atom()

    def set_concept(self, concept):
        self._concept = concept
        self.init_atom()

    @property
    def label(self):
        return self._label

    @property
    def concept(self):
        return self._concept

    @property
    def var(self):
        return self._var

