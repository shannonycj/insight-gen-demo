# Self-contained media and source handoff

Extract the ZIP into any working directory, keeping its repository-relative folders. Start in `production/revision_v3_connected/`. The four final delivery MP4s, approved voice masters/stems, two generated connector MP4s, prompts, editable sprites, rendering/QC code, storyboard, timing documents and completed QC reports are included.

The renderer's seven original V2 dependencies are preserved at:

- `production/revision_v2/film/clean/shot1.mp4` through `shot4.mp4`.
- `production/revision_v2/film_refined/clean/shot5.mp4` through `shot7.mp4`.

The unchanged source narration is at the archive root as `insightGen_demo_narration_v2.md` and `insightGen_demo_voiceover_v2.txt`. Approved provenance references are at `production/voice_demo/insightgen_polished_american_demo.mp3` and `production/voice_demo/settings_polished_american.json`. That settings file records the historical sample-generation key name; all new generation manifests use `MINIMAX_KEY_2`. No secret key or credential file is included.

## Runtime dependencies

Tested on Windows with Python **3.14.7**, Pillow **12.2.0**, NumPy **2.4.4**, and FFmpeg/FFprobe **9.0.2**. Install the pinned Python packages from `requirements.txt`. FFmpeg and FFprobe executables are external dependencies and must be available on PATH. The scripts also recognize an optional local `production/tools/**/ffmpeg.exe` / `ffprobe.exe` installation; those binaries are excluded from the archive.

The renderer and storyboard use the Windows fonts `C:/Windows/Fonts/segoeui.ttf` and `C:/Windows/Fonts/seguisb.ttf`. These system fonts are not distributed. On another OS, configure equivalent installed font paths in `render_connected.py` and `build_handoff_docs.py` before rendering. The delivered MP4s, images, audio and PDF-independent Markdown do not require those fonts for playback.

```powershell
cd production/revision_v3_connected
python -m pip install -r requirements.txt
python verify_delivery.py
python verify_connected.py
python render_connected.py --render --stills
python build_handoff_docs.py
```

Local rendering, assembly and verification do not require any generation API or credentials. The optional audio-generation scripts require the separately installed `mmx` CLI and the owner's explicitly selected `MINIMAX_KEY_2`; credentials are deliberately absent. Reuse the already generated approved audio for normal rendering.

## Integrity and exclusions

`package_manifest.json` records every payload file's repository-relative path, byte size and SHA256. `package_checksums.sha256` covers the payload plus the manifest. Neither file hashes itself, and the manifest excludes the two checksum files to avoid a circular reference. The ZIP CRC and all listed hashes are tested after archive creation. The archive's own SHA256 and integrity report are supplied beside it.

```powershell
python production/revision_v3_connected/build_package.py --verify production/insightgen_v3_connected_package.zip
```

Conformed intermediate videos/cache files, transient logs, Python bytecode, executables, `.env` and credential files, and rejected V3 revisions are excluded. The renderer rebuilds its intermediate `clean/` directory from the included original source plates and connector files. The existing delivery files remain independently playable.

The owner-held recording is unavailable and is not included. Its reference slot is 99 seconds, while the unchanged approved-speed demo narration is 101.283 seconds. See `ASSEMBLY.md` and the actual cue CSV before assembling it. The recording's internal synchronization, complete UI framing and full-film joins remain unverified.
