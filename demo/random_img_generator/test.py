from math import ceil, sqrt
from PIL import Image, ImageDraw

palette = [
    "#00272b", "#003740", "#004755", "#00576a", "#00677f",
    "#e0ff4f", "#d8f045", "#d0e13b", "#c8d231", "#c0c327",
    "#007f5f", "#007049", "#006133", "#00521d", "#004307",
    "#2b9348", "#24833e", "#1d7334", "#16632a", "#0f531f",
    "#55a630", "#4d9527", "#45841e", "#3d7315", "#35620c",
    "#80b918", "#78a910", "#709908", "#688800", "#607700",
    "#aacc00", "#a2bc00", "#9aac00", "#929c00", "#8a8c00",
    "#bfd200", "#b7c200", "#afb200", "#a7a200", "#9f9200",
    "#d4d700", "#cccf00", "#c4c700", "#bcbe00", "#b4b600",
]

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], base=16) for i in (0, 2, 4))

def encode_text_to_image(text: str, image_size: int) -> Image.Image:
    """
    Encodes a string into an image with colored squares

    Parameters:
        text (str): The string to encode
        image_size (int): The size of the image in pixels

    Returns:
        Image.Image: The generated image
    """
    square_count = ceil(sqrt(len(text)))
    square_size = image_size // square_count

    image = Image.new(mode="RGB", size=(image_size, image_size), color="white")
    draw = ImageDraw.Draw(im=image)
    for i, char in enumerate(iterable=text):
        row = i // square_count
        col = i % square_count
        x0, y0 = col * square_size, row * square_size
        x1, y1 = x0 + square_size, y0 + square_size
        color_index = ord(char) % len(palette)
        color = hex_to_rgb(hex_color=palette[color_index])
        draw.rectangle(xy=[x0, y0, x1, y1], fill=color)
    return image

def generate_image(prompt : str) -> Image.Image:
    image_size = 400
    encoded_image = encode_text_to_image(text=prompt, image_size=image_size)
    return encoded_image

if __name__ == "__main__":
    image = generate_image(prompt="Bdacu Rwwdahuhud")
    image.save(fp="1232ge.png")
