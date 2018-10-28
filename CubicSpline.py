import numpy as np

class CubicSpline(object):
    def __init__(self):
        self.x_list = None
        self.y_list = None
        self.a = None
        self.b = None
        self.c = None
        self.d = None

    def train(self, x_list, y_list):
        self.x_list = x_list
        self.y_list = y_list
        count = len(x_list)
        a = np.zeros(count)
        sigma = np.zeros(count)
        delta = np.zeros(count)

        for i in range(count-1):
            a[i] = y_list[i]
            sigma[i] = x_list[i+1] - x_list[i]
            delta[i] = y_list[i+1] - y_list[i]

        A = np.zeros((count, count))
        b = np.zeros(count)

        A[0, 0] = A[count-1, count-1] = 1
        for i in range(1, count-1):
            A[i, i-1] = sigma[i-1]
            A[i, i] = 2 * sigma[i-1] + 2 * sigma[i]
            A[i, i+1] = sigma[i]
            b[i] = 3 * (delta[i]/sigma[i] - delta[i-1]/sigma[i-1])

        c = np.linalg.solve(A, b)
        b = np.zeros(count)
        d = np.zeros(count)
        for i in range(count-1):
            d[i] = (c[i+1] - c[i])/(3*sigma[i])
            b[i] = delta[i]/sigma[i] - sigma[i]/3*(2*c[i] + c[i+1])

        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def cul(self, x):
        if self.a is None or self.b is None or self.c is None or self.d is None:
            return None

        self.x_list.sort()
        pos = -1
        for i in range(len(self.x_list)):
            if x <= self.x_list[i]:
                pos = i-1
                break

        delta = x - self.x_list[pos]
        print pos
        a = self.a[pos]
        b = self.b[pos]
        c = self.c[pos]
        d = self.d[pos]

        ret = a + b*delta + c*delta**2 + d*delta**3
        return ret


if __name__ == '__main__':
    x_list = [1, 2, 4, 5]
    y_list = [2, 1, 4, 3]
    cs = CubicSpline()
    cs.train(x_list, y_list)

    print cs.a
    print cs.b
    print cs.c
    print cs.d

    print cs.cul(4)

