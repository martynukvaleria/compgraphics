import math

from PIL import Image, ImageDraw


def handle_method(x1, x2, y1, y2, x, y, r, method):
    im = Image.new('L', (300, 300), 255)
    draw = ImageDraw.Draw(im)

    if method == 'okr':
        if x.isdigit() and y.isdigit() and r.isdigit():
            x = int(x)
            y = int(y)
            R = int(r)
            draw.point(
                xy=f4(R, x, y),
                fill='black'
            )
    else:
        if x1.isdigit() and y1.isdigit() and x2.isdigit() and y2.isdigit():
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
        else:
            return 'Not int'

        if method == 'step':
            draw.point(
                xy=f1(x1, y1, x2, y2),
                fill='black'
            )
        elif method == 'brez':
            draw.point(
                xy=f2(x1, y1, x2, y2),
                fill='black'
            )
        elif method == 'kastl':
            draw.point(
                xy=f3(x1, y1, x2, y2),
                fill='black'
            )

    im.save('static/res/image.jpg', 'JPEG')


def f1(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    k = dy / dx
    x = x1
    y = y1
    answer = []
    while x <= x2:
        y += k
        x += 1
        answer.append((x, int(y)))

    return answer


def f2(x0, y0, x1, y1):
    deltax = abs(x1 - x0)
    deltay = abs(y1 - y0)
    error = 0
    deltaerr = (deltay + 1) / (deltax + 1)
    y = y0

    diry = y1 - y0

    if diry > 0:
        diry = 1

    if diry < 0:
        diry = -1

    answer = []

    for x in range(x0, x1 + 1):
        answer.append((x, y))
        error += deltaerr

        if error >= 1:
            y += diry
            error -= 1

    return answer


def f3(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    dx_squared = dx * dx
    dy_squared = dy * dy

    distance = math.sqrt(dx_squared + dy_squared)

    return distance

def f4(R, X1, Y1):
    x = 0
    y = R
    delta = 1 - 2 * R
    error = 0

    answer = []

    while y >= x:
        answer.append((X1 + x, Y1 + y))
        answer.append((X1 + x, Y1 - y))
        answer.append((X1 - x, Y1 + y))
        answer.append((X1 - x, Y1 - y))

        answer.append((X1 + y, Y1 + x))
        answer.append((X1 + y, Y1 - x))
        answer.append((X1 - y, Y1 + x))
        answer.append((X1 - y, Y1 - x))

        error = 2 * (delta + y) - 1

        if (delta < 0) and (error <= 0):
            x += 1
            delta += 2 * x + 1
            continue

        if (delta > 0) and (error > 0):
            y -= 1
            delta -= 2 * y + 1
            continue

        x += 1
        y -= 1

        delta += 2 * (x - y)

    return answer

