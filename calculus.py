def riemann(data, dx):
    sigma = 0
    for i, y in enumerate(data)):
        sigma += y * (dx[min(len(dx) - 1, i)] - dx[i])  #dx becomes time between each sensor input, last sensor input is multiplied by 0

    return sigma

def derivative(y1, y2, dx):
    return (y2 - y1) / dx
