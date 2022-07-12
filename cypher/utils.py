from ..utils import *


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
        if self._label is None and self._concept is None:
            self.__atom = "ones"
        elif self._concept is None:
            self.__atom = "<E> {} </E>".format(self._label)
        elif self._label is None:
            self.__atom = "<ES> <C> {} </C> </ES>".format(self._concept)
        else:
            self.__atom = "<ES> <C> {} </C> <E> {} </E> </ES>".format(self._concept, self._label)

    def add_related_es(self, predicate, direction, es):
        assert isinstance(es, EntitySet)
        if es not in self.related_es.keys():
            self.related_es[es] = {"predicate": predicate, "direction": direction, "entitySet": es}
        else:
            raise Exception("this entitySet has already been added!")

    def add_related_attr(self, attr, symOP, val):
        if attr not in self.related_attr.keys():
            self.related_attr[attr] = []
        self.related_attr[attr].append([attr, symOP, val])

    def get_ir(self, forbidden=[]):
        atom = self.__atom
        filtersByAttr = sorted(list(self.related_attr.values()), key=lambda x: len(x), reverse=True)
        for filt in filtersByAttr:
            while len(filt) != 0:
                atom = "<ES> " + atom + " whose {} {} {} </ES>".format(*filt.pop())

        ir = ""

        for key in self.related_es.keys():
            if key not in forbidden:
                if self.related_es[key]["direction"] in ["forward", "backward"]:
                    if ir == "":
                        ir = "<ES> " + atom + " that {} {} to {} </ES>".format(
                            self.related_es[key]["predicate"],
                            self.related_es[key]["direction"],
                            self.related_es[key]["entitySet"].get_ir([self])
                        )
                    else:
                        ir = "<ES> " + ir + " and <ES> " + atom + " that {} {} to {} </ES> </ES>".format(
                            self.related_es[key]["predicate"],
                            self.related_es[key]["direction"],
                            self.related_es[key]["entitySet"].get_ir([self])
                        )
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
