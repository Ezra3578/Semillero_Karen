import base64

def image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def load_image(path):
    with open(path, "rb") as f:
        img = f.read()
        return img