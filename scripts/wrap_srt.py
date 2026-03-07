import textwrap
import os

def wrap_srt(file_path, width=40):
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = []
    for line in lines:
        stripped = line.strip()
        # If it's the sequence number or the timestamp, keep as is
        if stripped.isdigit() or '-->' in stripped or not stripped:
            out.append(line)
        else:
            # Wrap the text
            wrapped = textwrap.fill(stripped, width=width)
            out.append(wrapped + '\n')
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(out)

if __name__ == "__main__":
    wrap_srt('media/raw/videos/IMG_0450.srt')
