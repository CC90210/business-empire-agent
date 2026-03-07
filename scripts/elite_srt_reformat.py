import textwrap
import os
import re

def elite_srt_reformat(file_path):
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split into blocks
    blocks = content.strip().split('\n\n')
    new_blocks = []
    
    counter = 1
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue
            
        timestamp = lines[1]
        text = ' '.join(lines[2:])
        
        # Break text into max 3 words per segment
        words = text.split()
        if not words:
            continue
            
        # Since we don't have true word-level timestamps without re-running whisper,
        # we interpolate the time for the "pop" effect.
        start_str, end_str = timestamp.split(' --> ')
        
        def to_ms(ts):
            h, m, s_ms = ts.split(':')
            s, ms = s_ms.split(',')
            return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)
            
        def from_ms(ms):
            h = ms // 3600000
            ms %= 3600000
            m = ms // 60000
            ms %= 60000
            s = ms // 1000
            ms %= 1000
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
            
        start_ms = to_ms(start_str)
        end_ms = to_ms(end_str)
        duration = end_ms - start_ms
        
        words_per_segment = 3
        chunked_words = [words[i:i + words_per_segment] for i in range(0, len(words), words_per_segment)]
        
        ms_per_word = duration / len(words)
        
        current_start = start_ms
        for i, chunk in enumerate(chunked_words):
            chunk_text = ' '.join(chunk).upper() # HIGH IMPACT CAPS
            chunk_duration = len(chunk) * ms_per_word
            current_end = current_start + chunk_duration
            
            # Ensure last chunk hits the end
            if i == len(chunked_words) - 1:
                current_end = end_ms
                
            new_blocks.append(f"{counter}\n{from_ms(int(current_start))} --> {from_ms(int(current_end))}\n{chunk_text}")
            counter += 1
            current_start = current_end

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_blocks))

if __name__ == "__main__":
    elite_srt_reformat('media/raw/videos/IMG_0450.srt')
