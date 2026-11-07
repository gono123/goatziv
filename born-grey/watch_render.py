"""Overnight helper for the user's PC: keeps checking GitHub for episodes that are ready, renders each one
on the GPU with Blender, and pushes the finished silent video back, so the cloud session can add the
voice, captions, sound effects and music. No questions asked, no clicks needed.

    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --python born-grey/watch_render.py

An episode is ready when its folder has a READY file (the cloud session pushes it with the final timing).
Result: born-grey/<episode>/render/<name>_silent.mp4. Safe to stop and start again.
"""
import os, shutil, subprocess, sys, time
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
EPISODES = [("balloon", "balloon"), ("robot", "robot"), ("phone", "phone")]
SETTINGS = ["--res", "1080x1920", "--samples", "8", "--mblur"]
BLENDER = bpy.app.binary_path


def git(*args, check=True):
    print("git", " ".join(args), flush=True)
    return subprocess.run(["git", "-C", REPO] + list(args), check=check)


def push(paths, msg):
    git("add", *paths)
    git("commit", "-m", msg, check=False)
    for attempt in range(5):
        git("pull", "--rebase", "--autostash", check=False)
        if git("push", check=False).returncode == 0:
            return True
        time.sleep(20 * (attempt + 1))
    return False


# 1) a first push right away, so GitHub asks for login now (while you are awake), not at 3 am
os.makedirs(os.path.join(HERE, "pc"), exist_ok=True)
with open(os.path.join(HERE, "pc", "heartbeat.txt"), "w") as f:
    f.write(time.strftime("watch_render started %Y-%m-%d %H:%M:%S\n"))
push([os.path.join(HERE, "pc", "heartbeat.txt")], "PC renderer: started")

# 2) render each episode as soon as it is ready
while True:
    git("pull", "--rebase", "--autostash", check=False)
    left = 0
    for d, name in EPISODES:
        ep = os.path.join(HERE, d)
        done = os.path.join(ep, "render", f"{name}_silent.mp4")
        if os.path.exists(done):
            continue
        left += 1
        if not os.path.exists(os.path.join(ep, "READY")):
            continue
        print(f"=== rendering {d} ({name}) ===", flush=True)
        t0 = time.time()
        subprocess.run([BLENDER, "-b", "--python", os.path.join(ep, "render_local.py"), "--"] + SETTINGS, check=True)
        os.makedirs(os.path.dirname(done), exist_ok=True)
        shutil.copy(os.path.join(ep, "out", f"{name}_silent.mp4"), done)
        push([done], f"PC render: {d} {name} ({(time.time() - t0) / 60:.0f} min)")
        left -= 1
    if left == 0:
        print("ALL EPISODES RENDERED", flush=True)
        break
    print(time.strftime("%H:%M  waiting for the next episode..."), flush=True)
    time.sleep(240)
