from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import math

L = 40.0
number_of_cars = 20
cars_x = np.zeros(number_of_cars)
cars_v = np.zeros(number_of_cars)
car_img_path = "car_taxi_black.png"
c = 2.0
a = 1.0
dt = 0.5

steps = 200

def V(dx):
    return np.tanh(dx - c) + np.tanh(c)

def init():
    dx = L / number_of_cars
    iv = V(dx)
    x = 0.0
    for i in range(number_of_cars):
        cars_x[i] = x
        cars_v[i] = iv
        x += dx
        x += (np.random.rand() - 0.5) * 0.01


def draw_cars(size):

    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)

    cx = size * 0.5
    cy = size * 0.5
    r = size * 0.4
    cr = size * 0.02

    draw.ellipse((cx - r + cr, cy - r + cr, cx + r - cr, cy + r - cr), outline = "black")

    car_img = Image.open(car_img_path)
    car_img = car_img.resize((int(size * 0.1), int(size * 0.1)))
    car_img = ImageOps.mirror(car_img)
    car_img = car_img.rotate(-90)

    for i in range(number_of_cars):
        theta = 2.0 * math.pi / L * cars_x[i]
        x = r * math.cos(theta) + cx
        y = r * math.sin(theta) + cy

        # Rotate and place the car image
        rotated_car = car_img.rotate(-math.degrees(theta), resample=Image.BICUBIC, expand=True)
        car_position = (int(cx + r * math.cos(theta) - rotated_car.width / 2),
                        int(cy + r * math.sin(theta) - rotated_car.height / 2))
        image.paste(rotated_car, car_position, rotated_car)

    return image

def step():
    for i in range(number_of_cars):
        if i != number_of_cars - 1:
            dx = cars_x[i + 1] - cars_x[i]
        else:
            dx = cars_x[0] - cars_x[i]
        if dx < 0.0: dx += L
        if dx > L: dx -= L

        cars_v[i] += a * (V(dx) - cars_v[i]) * dt
        cars_x[i] += cars_v[i] * dt
        if cars_x[i] > L:
            cars_x[i] -= L
        elif cars_x[i] < 0.0:
            cars_x[i] += L



def main(steps):
    init()
    images = []
    for i in range(steps):
        step()
        images.append(draw_cars(800))
    
    images[0].save(
        "cars_animation.gif",
        save_all=True,
        append_images=images[1:],
        duration=100,  # フレームの表示時間（ミリ秒）
        loop=0  # 0は無限ループ
    )

    
if __name__ == "__main__":
    main(steps)