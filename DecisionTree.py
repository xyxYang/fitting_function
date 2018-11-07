#!/usr/bin/python
#encoding=utf-8


class Feature(object):
    def __init__(self):
        self.attribute_dic = {}
        self.result = None

    def set_attribute(self, name, value):
        if name not in self.attribute_dic:
            self.attribute_dic.setdefault(name, value)
            return True
        else:
            return False

    def set_result(self, res):
        self.result = res

    def get_attribute(self, name):
        if name in self.attribute_dic:
            return self.attribute_dic[name]
        else:
            return None

    def get_result(self):
        return self.result


class DTNode(object):
    def __init__(self):
        self.children = {}
        self.attribute = None


class DecisionTree(object):
    def __init__(self):
        self.attribute_names = []
        self.attribute_name_values = []
        self.root = DTNode()

    def __del__(self):
        pass
