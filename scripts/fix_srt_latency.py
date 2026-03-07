import os

def shift_ts(ts, offset_ms):
    h, m, s_ms = ts.split(':')
    s, ms = s_ms.split(',')
    ms_total = int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms) + offset_ms
    if ms_total < 0:
        ms_total = 0
    h = ms_total // 3600000
    ms_total %= 3600000
    m = ms_total // 60000
    ms_total %= 60000
    s = ms_total // 1000
    ms = ms_total % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def fix_srt_latency(file_path, offset_ms=-800):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    out = []
    for line in lines:
        if '-->' in line:
            start, end = line.strip().split(' --> ')
            out.append(f"{shift_ts(start, offset_ms)} --> {shift_ts(end, offset_ms)}\n")
        else:
            out.append(line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(out)

if __name__ == "__main__":
    fix_srt_latency('media/raw/videos/IMG_0450.srt')
