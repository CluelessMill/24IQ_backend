from math import ceil, sqrt

import ultraimport
from PIL import Image, ImageDraw

test_function = ultraimport("api/decorators/functions.py", "test_function")

palette = [
    "#00272b",
    "#e0ff4f",
    "#007f5f",
    "#2b9348",
    "#55a630",
    "#80b918",
    "#aacc00",
    "#bfd200",
    "#d4d700",
]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def encode_string_to_image(text: str, image_size: int) -> Image.Image:
    square_count = ceil(sqrt(len(text)))
    image = Image.new(mode="RGB", size=(image_size, image_size), color="white")
    draw = ImageDraw.Draw(image)
    square_size = image_size // square_count
    for i, char in enumerate(iterable=text):
        row = i // square_count
        col = i % square_count
        x0 = col * square_size
        y0 = row * square_size
        x1 = x0 + square_size
        y1 = y0 + square_size
        color_index = ord(char) % len(palette)
        color = hex_to_rgb(hex_color=palette[color_index])
        draw.rectangle(xy=[x0, y0, x1, y1], fill=color)
    return image


@test_function
def generate_image():
    text_to_encode = "Bdacu Rwwdahuhud"
    image_size = 400
    encoded_image = encode_string_to_image(text=text_to_encode, image_size=image_size)
    encoded_image.save(fp="encoded_image_with_custom_palette.png")


if __name__ == "__main__":
    generate_image()
