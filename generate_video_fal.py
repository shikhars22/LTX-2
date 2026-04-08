import os

# Set FAL_KEY (provided by user) at the very top
os.environ["FAL_KEY"] = "3ca947e8-341c-4171-9540-3869e54259b4:9645049b981114dfc8c5be9214136298"

import fal_client
import sys

# Configuration - Instagram Reels Format (9:16)
IMAGE_PATH = "input/input_image_916.jpeg"
OUTPUT_PATH = "outputs/dancing_girl_reels_15s.mp4"
PROMPT = (
    "A cinematic 9:16 vertical shot of a stunning woman with long flowing hair, "
    "performing rhythmic, alluring contemporary dance moves in a sun-drenched "
    "industrial loft. The camera maintains a smooth gimbal-stabilized orbit around "
    "her. She is lip-syncing passionately to a classic, soulful Hindi melody. "
    "Volumetric golden hour sunlight streams through floor-to-ceiling windows, "
    "creating high-contrast rim lighting. She wears a sheer silk dress that billows "
    "with every spin. Color graded with warm, filmic tones, deep shadows, and "
    "subtle highlights, Kodak Portra 400 aesthetic. High-fidelity audio sync."
)

def main():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    print(f"--- Step 1: Uploading cropped image {IMAGE_PATH} ---")
    try:
        image_url = fal_client.upload_file(IMAGE_PATH)
        print(f"Image uploaded successfully: {image_url}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return

    print("--- Step 2: Requesting 15s Instagram Reel (9:16) from Fal.ai ---")
    
    arguments = {
        "image_url": image_url,
        "prompt": PROMPT,
        "duration": 15,
        "resolution": "1080p", 
        "aspect_ratio": "9:16",
        "fps": 25,
        "generate_audio": True,
        "enhance_prompt": True
    }

    try:
        # Using the recommended LTX-2.3 image-to-video endpoint
        handler = fal_client.submit(
            "fal-ai/ltx-2.3/image-to-video",
            arguments=arguments
        )
        
        print("Job submitted. Waiting for result (this may take a few minutes)...")
        
        # Poll for logs and status
        for event in handler.iter_events():
            if isinstance(event, fal_client.InProgress):
                for log in event.logs:
                    print(f"[Fal Log]: {log['message']}")
            
        result = handler.get()
        video_url = result.get("video", {}).get("url")
        
        if video_url:
            print(f"Success! Video generated at: {video_url}")
            print(f"--- Step 3: Downloading to {OUTPUT_PATH} ---")
            import requests
            r = requests.get(video_url)
            with open(OUTPUT_PATH, "wb") as f:
                f.write(r.content)
            print("Download complete.")
        else:
            print("Error: No video URL found in result.")
            print(result)

    except Exception as e:
        print(f"An error occurred during generation: {e}")

if __name__ == "__main__":
    main()
