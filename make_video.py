#!/usr/bin/env python3
"""#4 demo: real dashboard screenshot -> slow scroll (~14s)."""
import os
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
def F(sz):
    for p in ["/System/Library/Fonts/PingFang.ttc","/System/Library/Fonts/Menlo.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except: pass
    return ImageFont.load_default()
W, H, FPS, DUR = 1280, 720, 28, 14.0
def main():
    rep = Image.open("output/demo.png").convert("RGB")
    sc = (W - 70) / rep.width; ri = rep.resize((int(rep.width * sc), int(rep.height * sc)))
    rw, rh = ri.size; frames = []; steps = int(DUR * FPS)
    maxscroll = max(0, rh - (H - 54))
    for k in range(steps):
        r = k / steps
        top = int(maxscroll * max(0, (r - 0.15) / 0.85)) if r > 0.15 else 0
        crop = ri.crop((0, top, rw, min(rh, top + (H - 54))))
        img = Image.new("RGB", (W, H), (13, 17, 23)); img.paste(crop, ((W - rw) // 2, 50))
        d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 50], fill=(35, 199, 122))
        d.text((18, 14), "StakeYield Copilot - Chain Staking Yield", font=F(20), fill=(10, 30, 18))
        frames.append(img)
    imageio.mimsave("output/demo.mp4", frames, fps=FPS)
    print("demo.mp4 saved, frames", len(frames))
main()
