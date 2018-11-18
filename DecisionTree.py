#!/usr/bin/python
#encoding=utf-8

"""
这是一个决策树代码，该代码主要针对离散属性进行分类
"""

import math

zero_threshold = 0.0000001


def calc_entropy(features):
    if features is None or len(features) == 0:
        return 0

    result_dic = {}
    for feature in features:
        result = feature.get_result()
        if result not in result_dic:
            result_dic.setdefault(result, 0)
        result_dic[result] += 1.0

    result_p_list = [float(count) / float(len(features)) for count in result_dic.values()]
    entropy = - sum([p * math.log(p, 2) for p in result_p_list])
    return entropy


def get_attribute_features(features, attribute_name):
    attribute_feature_dic = {}
    for feature in features:
        attribute_value = feature.get_attribute(attribute_name)
        if attribute_value not in attribute_feature_dic:
            attribute_feature_dic.setdefault(attribute_value, [])
        attribute_feature_dic[attribute_value].append(feature)
    return attribute_feature_dic


def calc_entropy_gain(features, attribute_name):
    if features is None or len(features) == 0:
        return 0

    all_entropy = calc_entropy(features)
    attribute_feature_dic = get_attribute_features(features, attribute_name)

    value_entropy = 0.0
    for value_features in attribute_feature_dic.values():
        entropy = calc_entropy(value_features)
        value_entropy += entropy * len(value_features)
    value_entropy /= len(features)
    return all_entropy - value_entropy


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
        self.features = []
        self.attribute = None
        self.entropy = 0.0
        self.result = None

    def train(self, features, attribute_names):
        if features is None or len(features) == 0:
            self.features = []
            self.attribute = None
            self.entropy = 0.0
            self.result = None
            return
        if attribute_names is None or len(attribute_names) == 0:
            self.features = features
            self.attribute = None
            self.entropy = calc_entropy(features)
            self.result = self.get_probably_result(features)
            return

        max_attribute_gain = float('-inf')
        max_attribute_name = None
        for attribute_name in attribute_names:
            attribute_gain = calc_entropy_gain(features, attribute_name)
            if attribute_gain > max_attribute_gain:
                max_attribute_gain = attribute_gain
                max_attribute_name = attribute_name

        if max_attribute_gain < zero_threshold:
            self.features = features
            self.attribute = None
            self.entropy = calc_entropy(features)
            self.result = self.get_probably_result(features)
            return

        self.features = features
        self.attribute = max_attribute_name
        self.entropy = calc_entropy(features)
        self.result = self.get_probably_result(features)
        attribute_feature_dic = get_attribute_features(features, self.attribute)
        new_attribute_name = [name for name in attribute_names if name != self.attribute]
        for attribute_value, value_features in attribute_feature_dic.items():
            child = DTNode()
            child.train(value_features, new_attribute_name)
            self.children.setdefault(attribute_value, child)

    def get_result(self, feature):
        """
        :param feature: 传入特征数据
        :return: 返回训练好的模型得到的结果数据
        """
        if self.attribute is None:
            return self.result
        attribute_value = feature.get_attribute(self.attribute)
        return self.children[attribute_value].get_result(feature)

    @staticmethod
    def get_probably_result(features):
        result_num_dic = {}
        for feature in features:
            result = feature.get_result()
            if result not in result_num_dic:
                result_num_dic.setdefault(result, 0)
            result_num_dic[result] += 1

        ret = None
        max_num = float('-inf')
        for result, num in result_num_dic.items():
            if num > max_num:
                ret = result
                max_num = num
        return ret


class DecisionTree(object):
    def __init__(self):
        self.attribute_names = []
        self.attribute_name_values = {}
        self.features = []
        self.root = DTNode()

    def __del__(self):
        pass

    def set_features(self, features, attribute_names):
        self.features = features
        self.attribute_names = attribute_names

    def train(self):
        self.root.train(self.features, self.attribute_names)

    def get_tree(self):
        return self.root

    def get_result(self, feature):
        return self.root.get_result(feature)


def test():
    features = []
    feature = Feature()
    feature.set_attribute("id", 1)
    feature.set_attribute("name", "j")
    feature.set_result(True)
    features.append(feature)

    feature = Feature()
    feature.set_attribute("id", 2)
    feature.set_attribute("name", "j")
    feature.set_result(False)
    features.append(feature)

    feature = Feature()
    feature.set_attribute("id", 1)
    feature.set_attribute("name", "p")
    feature.set_result(True)
    features.append(feature)

    feature = Feature()
    feature.set_attribute("id", 2)
    feature.set_attribute("name", "j")
    feature.set_result(False)
    features.append(feature)

    tree = DecisionTree()
    tree.set_features(features, ["id", "name"])
    tree.train()


    print tree.get_result(feature)

if __name__ == '__main__':
    test()
