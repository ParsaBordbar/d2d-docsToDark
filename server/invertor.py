from PIL import Image, ImageOps
from pdf2image import convert_from_path

def negative_trans(img: Image.Image) -> Image.Image:
    return ImageOps.invert(img.convert("RGB"))

def invert_pdf_to_dark(input_path, output_path): 
    try:
        pages = convert_from_path(input_path)
        neg_images = []
        for i, page in enumerate(pages):
            page_rgb = page.convert("RGB")
            neg_img = negative_trans(page_rgb.copy())
            neg_images.append(neg_img)
        if neg_images:
            neg_images[0].save(output_path, save_all=True, append_images=neg_images[1:])
            print(f"Negative PDF saved to: {output_path}")
            return output_path

    except Exception as e:
        print(f"[Error] Failed to process PDF: {e}")


def invert_image_to_dark(input_path, output_path):
    image = Image.open(input_path)
    negative_img = negative_trans(image.copy());
    negative_img.save(output_path)
    return output_path

