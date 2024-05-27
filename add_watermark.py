from PIL import Image, ImageDraw, ImageFont
import os

def add_watermark(input_folder, output_folder, watermark_text, position=("left", "bottom"), font_path=None, font_size=20):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path).convert("RGBA")

            # Create watermark layer
            watermark = Image.new("RGBA", image.size)
            draw = ImageDraw.Draw(watermark)

            # Load font
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()

            # Calculate position
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if position[0] == "center":
                x = (image.width - text_width) // 2
            elif position[0] == "left":
                x = 10  # Adding a small margin from the edge
            elif position[0] == "right":
                x = image.width - text_width - 10  # Adding a small margin from the edge
            else:
                x = int(position[0])

            if position[1] == "center":
                y = (image.height - text_height) // 2
            elif position[1] == "top":
                y = 10  # Adding a small margin from the edge
            elif position[1] == "bottom":
                y = image.height - text_height - 10  # Adding a small margin from the edge
            else:
                y = int(position[1])

            # Add text to watermark layer
            draw.text((x, y), watermark_text, font=font, fill=(255, 0, 0, 128))  # Red text with half transparency

            # Combine original image with watermark
            watermarked_image = Image.alpha_composite(image, watermark)
            watermarked_image = watermarked_image.convert("RGB")  # Remove alpha for saving in jpg format

            # Save watermarked image
            output_path = os.path.join(output_folder, filename)
            watermarked_image.save(output_path)

            print(f"Watermarked {filename} and saved to {output_path}")

if __name__ == "__main__":
    input_folder = "input_images"  # Folder containing the images to be watermarked
    output_folder = "output_images"  # Folder to save the watermarked images
    watermark_text = "Sample Watermark"  # Text of the watermark
    position = ("left", "bottom")  # Position set to bottom left
    font_path = None  # Path to the font file (use built-in default if None)
    font_size = 20  # Size of the font

    add_watermark(input_folder, output_folder, watermark_text, position, font_path, font_size)
