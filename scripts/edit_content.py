import os
import subprocess
import json

# FFmpeg path (winget install location)
FFMPEG_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin")
FFMPEG = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE = os.path.join(FFMPEG_DIR, "ffprobe.exe")

# Fallback: try system PATH
if not os.path.exists(FFMPEG):
    FFMPEG = "ffmpeg"
    FFPROBE = "ffprobe"

# Brand colors
PRIMARY_COLOR = "&H00F5F9FA&"   # #faf9f5 in BGR
OUTLINE_COLOR = "&H00131414&"   # #141413 in BGR


def probe_video(input_path):
    """Get video metadata via ffprobe."""
    cmd = [FFPROBE, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", input_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.returncode == 0 else None


def transcribe_audio(input_path, output_srt=None):
    """Auto-transcribe video audio to SRT using Whisper."""
    try:
        import whisper
    except ImportError:
        print("Whisper not installed. Run: pip install openai-whisper")
        return None

    if output_srt is None:
        base = os.path.splitext(input_path)[0]
        output_srt = base + ".srt"

    print(f"Transcribing {input_path}...")
    model = whisper.load_model("base")
    result = model.transcribe(input_path)

    # Write SRT
    with open(output_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], 1):
            start = _format_timestamp(seg["start"])
            end = _format_timestamp(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"Transcription saved to {output_srt}")
    return output_srt


def _format_timestamp(seconds):
    """Convert seconds to SRT timestamp format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_voiceover(text, output_path, voice="Adam"):
    """Generate voiceover using ElevenLabs API."""
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        print("ElevenLabs not installed. Run: pip install elevenlabs")
        return None

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ELEVENLABS_API_KEY not set in .env.agents")
        return None

    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Voiceover saved to {output_path}")
    return output_path


def edit_video(input_path, output_path, overlays=None, captions_path=None,
               orientation="portrait", auto_caption=False, voiceover_path=None):
    """
    Elite Bravo Video Edit:
    - Portrait (1080x1920) or Landscape (1920x1080)
    - Branded captions (#faf9f5 primary, #141413 outline)
    - Image overlays with timing
    - Audio normalization
    - Auto-transcription via Whisper
    - Voiceover mixing via ElevenLabs
    """
    print(f"Starting ELITE EDIT on {input_path}...")

    # Auto-transcribe if requested
    if auto_caption and not captions_path:
        captions_path = transcribe_audio(input_path)

    # Resolution based on orientation
    if orientation == "portrait":
        w, h = 1080, 1920
    else:
        w, h = 1920, 1080

    video_filter = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"

    inputs = ["-i", input_path]
    filter_complex = f"[0:v]{video_filter}[vbase]"
    last_v = "vbase"
    # Add voiceover as additional input
    if voiceover_path and os.path.exists(voiceover_path):
        inputs.extend(["-i", voiceover_path])
        audio_input_idx = len(inputs) // 2  # track which input is the voiceover

    # Add overlays
    if overlays:
        overlay_start_idx = len(inputs) // 2
        for i, overlay in enumerate(overlays):
            inputs.extend(["-i", overlay["path"]])
            idx = overlay_start_idx + i
            ov_name = f"ov{i}"
            ov_width = overlay.get("width", 400)
            filter_complex += f";[{idx}:v]scale={ov_width}:-1[ovscaled{i}]"
            filter_complex += f";[{last_v}][ovscaled{i}]overlay={overlay['x']}:{overlay['y']}:enable='between(t,{overlay['start']},{overlay['end']})'[{ov_name}]"
            last_v = ov_name

    # Add subtitles
    if captions_path and os.path.exists(captions_path):
        safe_subs = captions_path.replace("\\", "/").replace(":", "\\:")
        font_size = 28 if orientation == "portrait" else 22
        margin_v = 100 if orientation == "portrait" else 40
        filter_complex += (
            f";[{last_v}]subtitles='{safe_subs}':"
            f"force_style='Alignment=2,FontSize={font_size},MarginV={margin_v},"
            f"PrimaryColour={PRIMARY_COLOR},OutlineColour={OUTLINE_COLOR},"
            f"Outline=2,Shadow=0,Bold=1'[vfinal]"
        )
        last_v = "vfinal"

    # Build command
    command = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{last_v}]",
    ]

    # Audio mapping — mix voiceover with original if present
    if voiceover_path and os.path.exists(voiceover_path):
        command.extend(["-map", "1:a"])  # use voiceover audio
    else:
        command.extend(["-map", "0:a?"])  # original audio (optional)

    command.extend([
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        output_path,
    ])

    try:
        subprocess.run(command, check=True)
        print(f"SUCCESS: Elite export -> {output_path}")

        # Report specs
        info = probe_video(output_path)
        if info:
            for s in info.get("streams", []):
                if s.get("codec_type") == "video":
                    print(f"  Resolution: {s['width']}x{s['height']}")
                    print(f"  Duration: {info['format'].get('duration', 'unknown')}s")
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  File size: {size_mb:.1f} MB")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: FFmpeg failed: {e}")


if __name__ == "__main__":
    # Usage examples:
    #
    # Basic portrait edit:
    #   edit_video("media/raw/clip.mp4", "media/exports/clip_v1.mp4")
    #
    # With auto-captions:
    #   edit_video("media/raw/clip.mp4", "media/exports/clip_v1.mp4", auto_caption=True)
    #
    # With overlays:
    #   overlays = [{"path": "media/raw/screenshot.png", "x": 340, "y": 200, "start": 5.0, "end": 10.0}]
    #   edit_video("media/raw/clip.mp4", "media/exports/clip_v1.mp4", overlays=overlays)
    #
    # Landscape for LinkedIn:
    #   edit_video("media/raw/clip.mp4", "media/exports/clip_linkedin.mp4", orientation="landscape")
    #
    # With ElevenLabs voiceover:
    #   generate_voiceover("Your script text here", "media/raw/voiceover.mp3")
    #   edit_video("media/raw/clip.mp4", "media/exports/clip_v1.mp4", voiceover_path="media/raw/voiceover.mp3")
    pass
