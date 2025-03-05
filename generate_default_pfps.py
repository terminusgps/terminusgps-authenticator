from PIL import Image, ImageDraw

pfp_colors = {
    "red": (255, 0, 0),
    "orange": (255, 155, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "violet": (255, 0, 255),
}


def create_pfp(name: str, fill: tuple[int, int, int]) -> None:
    pfp_image = Image.new("RGB", (96, 96), (255, 255, 255))
    pfp_draw = ImageDraw.Draw(pfp_image)
    pfp_draw.ellipse((0, 0, 96, 96), fill=fill, outline=(0, 0, 0))
    pfp_image.save(f"default_{name.lower()}.jpg")


def main() -> None:
    for color, fill in pfp_colors.items():
        create_pfp(color, fill)
    return


if __name__ == "__main__":
    main()
