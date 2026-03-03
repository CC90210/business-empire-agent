"""End-to-end test of the video production pipeline."""
import os
import sys
import subprocess

# Paths
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin")
FFMPEG = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE = os.path.join(FFMPEG_DIR, "ffprobe.exe")

if not os.path.exists(FFMPEG):
    FFMPEG = "ffmpeg"
    FFPROBE = "ffprobe"

RAW_DIR = os.path.join(PROJECT_DIR, "media", "raw")
EXPORT_DIR = os.path.join(PROJECT_DIR, "media", "exports")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

test_clip = os.path.join(RAW_DIR, "test_clip.mp4")
test_output = os.path.join(EXPORT_DIR, "test_output.mp4")


def step(name):
    print(f"\n{'='*60}")
    print(f"  STEP: {name}")
    print(f"{'='*60}")


def main():
    print("BRAVO VIDEO PIPELINE — END-TO-END TEST")
    print(f"FFmpeg: {FFMPEG}")
    print(f"FFprobe: {FFPROBE}")

    # Step 1: Generate test clip
    step("1. Generate synthetic test clip (5s, 1080x1920, with audio)")
    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi", "-i", "color=c=0x141413:s=1080x1920:d=5",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=5",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
        test_clip
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL: {result.stderr[-500:]}")
        return False
    size = os.path.getsize(test_clip) / 1024
    print(f"OK — {test_clip} ({size:.1f} KB)")

    # Step 2: Probe video
    step("2. Probe video metadata (ffprobe)")
    sys.path.insert(0, os.path.join(PROJECT_DIR, "scripts"))
    from edit_content import probe_video
    info = probe_video(test_clip)
    if info:
        for s in info.get("streams", []):
            if s.get("codec_type") == "video":
                print(f"OK — Video: {s['width']}x{s['height']}, codec={s['codec_name']}")
            elif s.get("codec_type") == "audio":
                print(f"OK — Audio: {s.get('sample_rate')}Hz, codec={s['codec_name']}")
        print(f"OK — Duration: {info['format'].get('duration', 'unknown')}s")
    else:
        print("FAIL — Could not probe video")
        return False

    # Step 3: Edit video (portrait, no captions — basic pipeline)
    step("3. Edit video (portrait mode, scale+pad, quality encode)")
    from edit_content import edit_video
    edit_video(test_clip, test_output, orientation="portrait")

    if os.path.exists(test_output):
        size_mb = os.path.getsize(test_output) / (1024 * 1024)
        print(f"OK — Output: {test_output} ({size_mb:.2f} MB)")
    else:
        print("FAIL — Output file not created")
        return False

    # Step 4: Verify Whisper import
    step("4. Verify Whisper (transcription engine)")
    try:
        import whisper
        print(f"OK — Whisper imported successfully")
        # Don't actually transcribe the sine wave — just verify import
    except ImportError as e:
        print(f"FAIL — {e}")

    # Step 5: Verify ElevenLabs import
    step("5. Verify ElevenLabs (voiceover engine)")
    try:
        import elevenlabs  # noqa: F401
        print(f"OK — ElevenLabs imported successfully")
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if api_key:
            print(f"OK — API key found ({api_key[:8]}...)")
        else:
            print("WARN — ELEVENLABS_API_KEY not set (voiceover will need this)")
    except ImportError as e:
        print(f"FAIL — {e}")

    # Step 6: Check Remotion
    step("6. Verify Remotion (animation engine)")
    remotion_pkg = os.path.join(PROJECT_DIR, "node_modules", "@remotion", "cli")
    if os.path.isdir(remotion_pkg):
        pkg_json = os.path.join(remotion_pkg, "package.json")
        if os.path.exists(pkg_json):
            import json
            with open(pkg_json) as f:
                ver = json.load(f).get("version", "unknown")
            print(f"OK — Remotion CLI v{ver} installed")
        else:
            print("OK — Remotion CLI directory found")
    else:
        print("WARN — Remotion not found in node_modules")

    # Summary
    print(f"\n{'='*60}")
    print("  PIPELINE TEST COMPLETE")
    print(f"{'='*60}")
    print(f"  Test clip: {test_clip}")
    print(f"  Test output: {test_output}")
    print()

    # Cleanup option
    print("Test files preserved for inspection. Delete manually when done.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
