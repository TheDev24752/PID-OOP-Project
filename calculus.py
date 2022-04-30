class Calculus:
    @staticmethod
    def riemann(data, dx):
        sigma = 0
        for y in data:
            sigma += y * dx

        return sigma

    @staticmethod
    def derivative(y1, y2, dx):
        return (y2 - y1) / dx
