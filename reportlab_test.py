from reportlab.pdfgen.canvas import Canvas


def draw_string(c: Canvas, value: str) -> None:
    c.drawString(100, 100, value)


def main() -> None:
    c = Canvas("hello.pdf")
    draw_string(c, "Hello, World!")
    c.showPage()
    c.save()
    return


if __name__ == "__main__":
    main()
