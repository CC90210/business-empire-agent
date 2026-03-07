import os
import sys
from scripts.edit_content import edit_video

input_file = "media/raw/videos/IMG_0450.MP4"
srt_file = "media/raw/videos/IMG_0450.srt"
output_file = "media/exports/IMG_0450_bravo_edit.mp4"

# Let's add some "spices" if we can find them, or just run the base edit with captions.
# The user wants "Elite Edit", so let's ensure we use the best settings.

if __name__ == "__main__":
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        sys.exit(1)
        
    if not os.path.exists(srt_file):
        print(f"Warning: {srt_file} not found, proceeding without captions.")
        srt_file = None

    # Run elite edit
    edit_video(
        input_path=input_file,
        output_path=output_file,
        captions_path=srt_file,
        orientation="portrait",
        auto_caption=False # We already did it manually
    )
