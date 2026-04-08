import os
import sys
from moviepy import VideoFileClip

def crop_video_to_916(input_path, output_path):
    print(f"Loading video: {input_path}")
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    clip = VideoFileClip(input_path)
    w, h = clip.size
    print(f"Original Dimensions: {w}x{h}")

    # Target aspect ratio 9:16
    target_aspect = 9 / 16
    current_aspect = w / h

    if current_aspect > target_aspect:
        # Video is wider than 9:16 (Standard widescreen)
        # Crop the sides
        new_w = h * target_aspect
        x1 = (w - new_w) / 2
        x2 = x1 + new_w
        y1, y2 = 0, h
        print(f"Cropping sides: {int(new_w)}x{h} (centered)")
    else:
        # Video is skinnier than 9:16
        # Crop the top and bottom
        new_h = w / target_aspect
        y1 = (h - new_h) / 2
        y2 = y1 + new_h
        x1, x2 = 0, w
        print(f"Cropping top/bottom: {w}x{int(new_h)} (centered)")

    # MoviePy v2.x use cropped(x1, y1, x2, y2)
    cropped_clip = clip.cropped(x1=int(x1), y1=int(y1), x2=int(x2), y2=int(y2))
    
    print(f"Writing output to: {output_path}")
    # Using libx264 for compatibility, audio=True to keep sound
    cropped_clip.write_videofile(output_path, codec="libx264", audio=True)
    
    clip.close()
    cropped_clip.close()
    print("Done!")

if __name__ == "__main__":
    input_file = "input/WhatsApp Video 2026-04-05 at 4.55.06 PM.mp4"
    output_file = "input/WhatsApp_Video_916.mp4"
    crop_video_to_916(input_file, output_file)
