from PIL import Image, ImageDraw, ImageOps
import math, time



def resize_image(img, width, height):
    if img.size[0] != width or img.size[1] != height:
        img = img.resize((width, height), Image.LANCZOS)
    return img


def mm_to_px(mm, dpi):
    return int(mm * dpi / 25.4)


def images_to_pdf_grid( image_paths, output_pdf, page_size_mm, rows, cols, card_size_mm, offset_mm, bleed_mm, dpi, draw_cut_lines):
    page_w, page_h = map(lambda x: mm_to_px(x, dpi), page_size_mm)
    card_w, card_h = map(lambda x: mm_to_px(x, dpi), card_size_mm)
    offset_x, offset_y = map(lambda x: mm_to_px(x, dpi), offset_mm)
    bleed = mm_to_px(bleed_mm, dpi)

    full_w = card_w + 2 * bleed
    full_h = card_h + 2 * bleed

    images_per_page = rows * cols

    pages = []
    for page_idx in range(math.ceil(len(image_paths) / images_per_page)):
        page = Image.new("RGB", (page_w, page_h), "white")
        draw = ImageDraw.Draw(page)

        start = page_idx * images_per_page
        end = start + images_per_page

        for i, path in enumerate(image_paths[start:end]):
            if path == "Blank":
                continue

            try:
                img = Image.open(path)
                img = resize_image(img, card_w, card_h)
            except FileNotFoundError:
                splited = path.split("_")
                path = ""
                for i in range(len(splited) - 1):
                    path = path + splited[i] + "_"

                path = path + "0.png"
                img = Image.open(path)
                img = resize_image(img, card_w, card_h)

            img = img.convert("RGB")

            row = i // cols
            col = i % cols

            x = offset_x + col * full_w
            y = offset_y + row * full_h

            page.paste(img, (x, y))

        if draw_cut_lines:
            for c in range(cols + 1):
                x = offset_x + c * full_w
                draw.line([(x, 0), (x, page_h)], fill="black", width=1)

            for r in range(rows + 1):
                y = offset_y + r * full_h
                draw.line([(0, y), (page_w, y)], fill="black", width=1)

        pages.append(page)

    pages[0].save(output_pdf, "PDF", resolution=dpi, save_all=True, append_images=pages[1:])



if __name__ == "__main__":
    startTime = time.time()
    print("Preparing card data...")

    file = "CustomDeckDoPrintu - Copy.txt"
    with open("decks/" + file, "r", encoding="utf-8") as file:
        content = file.readlines()

    imgs = []
    for line in content:
        splited = line.strip().split(" ")
        count = int(splited[0])
        index = int(splited[-1])

        title = ""
        for i in range(1, len(splited) - 2):
            title = title + splited[i] + " "
        title = title + splited[len(splited) - 2]

        if title == "Blank":
            filename = "Blank"
        else:
            filename = f"imgs/{title}_{index}.png"

        imgs.append(filename)

    print("PDF generation is starting...")
    images_to_pdf_grid(
        image_paths=imgs,
        output_pdf="deck_ready_to_be_printed.pdf",
        page_size_mm=(210, 297),
        rows=3,
        cols=3,
        card_size_mm=(63, 88),
        offset_mm=(10.55, 15.5),
        bleed_mm=0,
        dpi=300,
        draw_cut_lines=True
    )

    endTime = time.time()

    print(f"Generating PDF took {round(endTime - startTime, 2)}s")
