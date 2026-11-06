# Rendering Born Grey on your own PC (GPU)

Needs: Blender (latest, blender.org) and Git. Your GTX 1660 Super renders the film in ~15-30 min.

1. Get the project (once):
   git clone https://github.com/gono123/goatziv.git
   cd goatziv
   git checkout claude/awesome-newton-c610qw
   (later updates: git pull)
2. Render everything and build the silent video (one command, from the goatziv folder):
   "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" -b --python born-grey/v2/render_local.py
   (change "Blender 5.0" to the version folder you installed)
   Stop any time with Ctrl+C; running it again continues where it stopped.
3. Upload born-grey/v2/out/born_grey_v3_silent.mp4 to your Google Drive "gneef" folder.
   The cloud session adds captions, voice, sound effects and music.

Options: -- --res 720x1280 --samples 8 (faster preview), -- --only wash_face,pink_reveal (some shots).
