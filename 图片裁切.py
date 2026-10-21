from PIL import Image, ImageOps
import os

Image.MAX_IMAGE_PIXELS = None

# ====== 只改这两行 ======
INPUT  = r"C:\Users\reze5\Desktop\高数答案.jpg"
OUTDIR = r"C:\Users\reze5\Desktop\切片输出"
# =======================

SLICE_HEIGHT = 1825   # 每片高度
OVERLAP      = 0    # 上下重叠，防公式被腰斩
JPEG_QUALITY = 95

def split_image():
    os.makedirs(OUTDIR, exist_ok=True)

    img = ImageOps.exif_transpose(Image.open(INPUT))
    w, h = img.size
    base = os.path.splitext(os.path.basename(INPUT))[0]
    ext  = os.path.splitext(INPUT)[1].lower()

    step = SLICE_HEIGHT - OVERLAP
    if step <= 0:
        raise ValueError("OVERLAP 必须小于 SLICE_HEIGHT")

    idx, top = 1, 0
    while top < h:
        bottom = min(top + SLICE_HEIGHT, h)
        piece = img.crop((0, top, w, bottom))

        if ext in (".jpg", ".jpeg"):
            out = os.path.join(OUTDIR, f"{base}_part{idx:03d}.jpg")
            if piece.mode in ("RGBA", "P"):
                piece = piece.convert("RGB")
            piece.save(out, quality=JPEG_QUALITY, subsampling=0)
        else:
            out = os.path.join(OUTDIR, f"{base}_part{idx:03d}.png")
            piece.save(out)

        print(f"[{idx:03d}] y={top}-{bottom} 高={bottom-top} -> {out}")
        if bottom >= h:
            break
        top += step
        idx += 1

    print(f"完成，共 {idx} 片，原图 {w}x{h}")

if __name__ == "__main__":
    split_image()