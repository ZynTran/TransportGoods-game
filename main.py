import random
WIDTH=1000
HEIGHT=800
for _ in range (1,8):
    x1 = random.randint(88, WIDTH - 150)
    y1 = random.randint(88, HEIGHT - 110)

    if x1 >= 500:
        x2 = x1 - random.randint(300, x1 - 20)
    else:
        x2 = x1 + random.randint(300, WIDTH - x1 - 70)

    if y1 >= 400:
        y2 = y1 - random.randint(300, y1 - 88)
    else:
        y2 = y1 + random.randint(300, (HEIGHT - y1 -70))
    print(f"so1:({x1},{y1}), so2:({x2},{y2})")
