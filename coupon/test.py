from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
import base64

def generate_coupon(coupon):
    
    print("starting now")
    
    template = Image.open("coupon.png")
    draw = ImageDraw.Draw(template)

    font_size = 36
    text = coupon
    position = (210, 253)
    text_color = "black"

    qr = qrcode.QRCode(box_size=6)
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    qr_img.save("qr_code.png")

    try:
        font = ImageFont.truetype("arialbd.ttf", size=font_size)
        stroke_w = 1
    except IOError:
        font = ImageFont.load_default()
        stroke_w = 2 

    draw.text(
        position, 
        text, 
        fill=text_color, 
        font=font, 
        stroke_width=stroke_w, 
        stroke_fill=text_color
    )


    template.paste(qr_img, (80,380))

    print("for going to base64")
    img_byte_arr = io.BytesIO()
    template.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    base64_encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

    template.save('cSeopnknd.png')

    test_bytes = base64.b64decode(base64_encoded_image)
    with open("mailjet_test.png", "wb") as f:
        f.write(test_bytes)

    print("BASE64 CREATED")

    test_bytes = base64.b64decode(base64_encoded_image)

    with open("mailjet_test.png", "wb") as f:
        f.write(test_bytes)

    print("MAILJET TEST IMAGE SAVED")
    
    return base64_encoded_image

generate_coupon("SADHYA-G4EBN9")
