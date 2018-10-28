#!/usr/bin/python
#encoding=utf-8

"""
author: albusyang
version: 1.0
"""

import numpy as np
import math

def sigma(pt1, pt2):
    x1, y1 = tuple(pt1)
    x2, y2 = tuple(pt2)
    delta_x = x1 - x2
    delta_y = y1 - y2
    d2 = delta_x**2 + delta_y**2
    if d2 == 0:
        return 0
    else:
        return d2 * math.log(d2)

class ThinPlateSpine(object):
    def __init__(self):
        self.input_pts = []
        self.output_values = []
        self.pt_num = 0
        self.w = None   # 1*N的系数矩阵，每个输入点的sigma函数的系数
        self.c = None   # 1*1的系数矩阵，放射变换的常数项
        self.a = None   # 1*2的系数矩阵，放射变换的自变量系数
        self.S = None   # N*N的sigma函数值矩阵

    def __del__(self):
        pass

    def set_points(self, input_pts, output_values):
        if len(input_pts) > len(output_values) or len(input_pts) < 3:
            print "[tps][error] input points number wrong!"
            raise (ValueError, "[tps][error] input points number wrong")
        if len(input_pts) < len(output_values):
            print "[tps][warning] input points less than output points!"

        self.pt_num = len(input_pts)
        self.input_pts = input_pts
        self.output_values = output_values

    def add_point(self, input_point, output_value):
        self.input_pts.append(input_point)
        self.output_values.append(output_value)
        self.pt_num += 1

    def train(self):
        #self.w = np.zeros(self.pt_num)
        #self.c = np.zeros(1)
        #self.a = np.zeros(2)
        self.S = np.zeros([self.pt_num, self.pt_num])

        input_matrix = np.array(self.input_pts)
        output_matrix = np.array(self.output_values)

        for i, pt1 in enumerate(self.input_pts):
            for j, pt2 in enumerate(self.input_pts):
                self.S[i, j] = sigma(pt1, pt2)

        A_matrix = np.vstack([
            np.hstack([
                self.S,
                np.ones([self.pt_num, 1]),
                input_matrix
            ]),
            np.hstack([
                np.ones([1, self.pt_num]),
                np.zeros([1, 1]),
                np.zeros([1, input_matrix.shape[1]])
            ]),
            np.hstack([
                input_matrix.T,
                np.zeros([input_matrix.shape[1], 1]),
                np.zeros([input_matrix.shape[1], input_matrix.shape[1]])
            ])
        ])

        b_matrix = np.hstack([
            output_matrix,
            np.zeros(input_matrix.shape[1] + 1)
        ])

        ret = np.linalg.solve(A_matrix, b_matrix)
        self.w = ret[:self.pt_num]
        self.c = ret[self.pt_num]
        self.a = ret[self.pt_num+1:self.pt_num+3]

    def get_value(self, pt):
        if None in [self.w, self.c, self.a]:
            return None

        ret = 0
        for i in range(self.pt_num):
            ret += self.w[i] * sigma(pt, self.input_pts[i])

        ret += np.dot(self.a, np.array(pt))
        ret += self.c

        return ret


class ThinPlateSpine_2D(object):
    def __init__(self):
        self.x_process = ThinPlateSpine()
        self.y_process = ThinPlateSpine()

    def __del__(self):
        pass

    def set_points(self, input_pts, output_pts):
        output_xs = [pt[0] for pt in output_pts]
        output_ys = [pt[1] for pt in output_pts]
        self.x_process.set_points(input_pts, output_xs)
        self.y_process.set_points(input_pts, output_ys)

    def add_points(self, input_pt, output_pt):
        self.x_process.add_point(input_pt, output_pt[0])
        self.y_process.add_point(input_pt, output_pt[1])

    def train(self):
        self.x_process.train()
        self.y_process.train()

    def get_point(self, pt):
        x = self.x_process.get_value(pt)
        y = self.y_process.get_value(pt)

        if None in [x, y]:
            return None
        else:
            return x, y

def test():
    process = ThinPlateSpine_2D()
    input_pts = [
        (0, 0),
        (1, 1),
        (4, 2),
        (5, 6)
    ]
    output_pts = [
        (0, 0),
        (1, 1),
        (3, 2),
        (5, 5)
    ]
    process.set_points(input_pts, output_pts)
    process.train()
    print process.get_point((5, 5))


if __name__ == '__main__':
    test()


