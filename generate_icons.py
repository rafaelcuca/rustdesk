import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_ICON = r"D:\Sistemas\RCRemote_Painel\public\icon-512.png"

def generate():
    print(f"Loading source icon from: {SOURCE_ICON}")
    src_img = Image.open(SOURCE_ICON).convert("RGBA")
    
    # Target sizes for multi-resolution ICO
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # 1. res/icon.ico
    res_ico_path = os.path.join(BASE_DIR, "res", "icon.ico")
    src_img.save(res_ico_path, format="ICO", sizes=ico_sizes)
    print(f"Generated: {res_ico_path}")
    
    # 2. res/tray-icon.ico
    tray_ico_path = os.path.join(BASE_DIR, "res", "tray-icon.ico")
    src_img.save(tray_ico_path, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48)])
    print(f"Generated: {tray_ico_path}")
    
    # 3. flutter/windows/runner/resources/app_icon.ico
    runner_ico_path = os.path.join(BASE_DIR, "flutter", "windows", "runner", "resources", "app_icon.ico")
    src_img.save(runner_ico_path, format="ICO", sizes=ico_sizes)
    print(f"Generated: {runner_ico_path}")
    
    # 4. res/icon.png (1024x1024)
    img_1024 = src_img.resize((1024, 1024), Image.Resampling.LANCZOS)
    img_1024.save(os.path.join(BASE_DIR, "res", "icon.png"), format="PNG")
    print("Generated: res/icon.png (1024x1024)")
    
    # 5. res/128x128@2x.png (256x256)
    img_256 = src_img.resize((256, 256), Image.Resampling.LANCZOS)
    img_256.save(os.path.join(BASE_DIR, "res", "128x128@2x.png"), format="PNG")
    print("Generated: res/128x128@2x.png (256x256)")
    
    # 6. res/128x128.png
    img_128 = src_img.resize((128, 128), Image.Resampling.LANCZOS)
    img_128.save(os.path.join(BASE_DIR, "res", "128x128.png"), format="PNG")
    print("Generated: res/128x128.png (128x128)")
    
    # 7. res/64x64.png
    img_64 = src_img.resize((64, 64), Image.Resampling.LANCZOS)
    img_64.save(os.path.join(BASE_DIR, "res", "64x64.png"), format="PNG")
    print("Generated: res/64x64.png (64x64)")
    
    # 8. res/32x32.png
    img_32 = src_img.resize((32, 32), Image.Resampling.LANCZOS)
    img_32.save(os.path.join(BASE_DIR, "res", "32x32.png"), format="PNG")
    print("Generated: res/32x32.png (32x32)")
    
    # 9. flutter/assets/icon.png (512x512)
    flutter_assets = os.path.join(BASE_DIR, "flutter", "assets")
    os.makedirs(flutter_assets, exist_ok=True)
    src_img.save(os.path.join(flutter_assets, "icon.png"), format="PNG")
    print("Generated: flutter/assets/icon.png (512x512)")
    
    # 10. Horizontal Logo (flutter/assets/logo.png, logo_light.png, logo_dark.png)
    # Width 220, Height 50, transparent background
    def make_logo(text_color, sub_color):
        logo_w, logo_h = 240, 56
        logo_img = Image.new("RGBA", (logo_w, logo_h), (0, 0, 0, 0))
        # icon thumbnail (48x48)
        icon_thumb = src_img.resize((48, 48), Image.Resampling.LANCZOS)
        logo_img.paste(icon_thumb, (4, 4), mask=icon_thumb)
        
        draw = ImageDraw.Draw(logo_img)
        # Try loading Arial bold or Segoe UI bold
        font_title = None
        font_sub = None
        for font_name in ["segoeuib.ttf", "arialbd.ttf", "arial.ttf"]:
            try:
                font_title = ImageFont.truetype(font_name, 26)
                font_sub = ImageFont.truetype(font_name, 10)
                break
            except Exception:
                pass
        if not font_title:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
        draw.text((62, 8), "RC DESK", font=font_title, fill=text_color)
        draw.text((64, 36), "ACESSO REMOTO", font=font_sub, fill=sub_color)
        return logo_img

    logo_dark_theme = make_logo((255, 255, 255, 240), (148, 163, 184, 220)) # Light text for dark mode
    logo_light_theme = make_logo((15, 23, 42, 240), (71, 85, 105, 220))    # Dark text for light mode
    
    logo_dark_theme.save(os.path.join(flutter_assets, "logo_dark.png"), format="PNG")
    logo_light_theme.save(os.path.join(flutter_assets, "logo_light.png"), format="PNG")
    logo_dark_theme.save(os.path.join(flutter_assets, "logo.png"), format="PNG")
    print("Generated: flutter/assets/logo.png, logo_dark.png, logo_light.png")

if __name__ == "__main__":
    generate()
