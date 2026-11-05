"""Builds the main character as a 3D file from the pose Roblox Studio exported (pose.json) and the hair mesh.
  python build.py      writes ../sam.glb, ../obj/sam.obj (+ .mtl, face.png) and src/face.png"""
import glob, json, os, re
import numpy as np, trimesh
from PIL import Image, ImageDraw, ImageFont

STUD = 0.28                      # metres per stud, so viewers show him at a sensible size
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open('pose.json'))
SKIN = (255, 189, 127)

def cf_matrix(c):
    x, y, z, *r = c
    m = np.eye(4); m[:3, :3] = np.array(r).reshape(3, 3); m[:3, 3] = (x, y, z); return m

def solid(mesh, rgb, rough=.55):
    uv = np.zeros((len(mesh.vertices), 2))
    lin = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]   # Roblox colours are sRGB, glTF factors are linear
    mat = trimesh.visual.material.PBRMaterial(baseColorFactor=[*lin, 1.0], metallicFactor=0.0, roughnessFactor=rough)
    mesh.visual = trimesh.visual.TextureVisuals(uv=uv, material=mat)
    return mesh

# face: redraws the Studio SurfaceGui (300x200 px over 1.5x1 studs) at 4x, skin all round so the head can wear it
def face_texture(vis):
    k = 4; W, H = 300 * k, 200 * k
    img = Image.new('RGB', (W, H), SKIN); d = ImageDraw.Draw(img)
    dark = (25, 20, 20)
    def oval(cx, cy, w, h, col): d.ellipse([(cx - w / 2) * k, (cy - h / 2) * k, (cx + w / 2) * k, (cy + h / 2) * k], fill=col)
    def rot_box(cx, cy, w, h, deg, col):
        t = Image.new('RGBA', (int(w * k * 1.6), int(w * k * 1.6)), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
        ox, oy = t.width / 2, t.height / 2
        td.rounded_rectangle([ox - w * k / 2, oy - h * k / 2, ox + w * k / 2, oy + h * k / 2], radius=h * k / 2, fill=col)
        t = t.rotate(-deg, resample=Image.BICUBIC)   # Roblox rotation is clockwise
        img.paste(t, (int(cx * k - ox), int(cy * k - oy)), t)
    if 'EyeL' in vis:
        oval(100, 84, 34, 50, dark); oval(200, 84, 34, 50, dark)
    if 'GlintL' in vis:
        oval(106, 70, 10, 14, (255, 255, 255)); oval(206, 70, 10, 14, (255, 255, 255))
    rot_box(98, 38, 52, 11, -6, dark); rot_box(202, 38, 52, 11, 6, dark)
    if 'Smile' in vis:
        fonts = glob.glob(os.path.expandvars(r'%LOCALAPPDATA%\Roblox\Versions\*\content\fonts\FredokaOne-Regular.ttf'))
        font = ImageFont.truetype(fonts[0] if fonts else 'arialbd.ttf', 74 * k)
        t = Image.new('RGBA', (120 * k, 120 * k), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
        td.text((t.width / 2, t.height / 2), ')', font=font, fill=dark, anchor='mm')
        t = t.rotate(-90, resample=Image.BICUBIC)
        img.paste(t, (int(150 * k - t.width / 2), int(150 * k - t.height / 2)), t)
    return img

# Roblox "Head" mesh: an upright cylinder with rounded edges, 1 stud per unit of mesh scale
def head_mesh(scale, face_dy, tex):
    r = h = .5 * scale; e = .2 * scale; n = 10
    prof = [(0, -h)]
    for a in np.linspace(-np.pi / 2, 0, n): prof.append((r - e + e * np.cos(a), -h + e + e * np.sin(a)))
    for a in np.linspace(0, np.pi / 2, n): prof.append((r - e + e * np.cos(a), h - e + e * np.sin(a)))
    prof.append((0, h))
    m = trimesh.creation.revolve(np.array(prof), sections=64)
    m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))   # revolve axis Z -> Y
    v = m.vertices
    uv = np.stack([-v[:, 0] / 1.5 + .5, (v[:, 1] - face_dy) / 1.0 + .5], 1)
    uv[v[:, 2] > 0] = (.01, .01)          # back half (a part's front is local -Z): plain skin, so the face is not printed twice
    mat = trimesh.visual.material.PBRMaterial(baseColorTexture=tex, metallicFactor=0.0, roughnessFactor=.6)
    m.visual = trimesh.visual.TextureVisuals(uv=uv, material=mat)
    return m

# Roblox mesh v1.00 (text): "[x,y,z][nx,ny,nz][u,v,w]" per corner; v1.00 positions are stored at double size
def roblox_mesh(path):
    txt = open(path).read().split('\n', 2)
    assert txt[0].startswith('version 1.0'), txt[0]
    nums = np.array([float(x) for x in re.findall(r'[-+0-9.eE]+', txt[2])]).reshape(-1, 9)
    pos = nums[:, 0:3] * (.5 if txt[0].strip() == 'version 1.00' else 1); uv = nums[:, 6:8].copy(); uv[:, 1] = 1 - uv[:, 1]
    faces = np.arange(len(pos)).reshape(-1, 3)
    m = trimesh.Trimesh(pos, faces, process=False)
    m.merge_vertices()
    return m

scene = trimesh.Scene()
face = face_texture(P['face']); face.save('face.png')
parts = {p['name']: p for p in P['parts']}
for p in P['parts']:
    name, sx, sy, sz = p['name'], *p['size']
    M = cf_matrix(p['cf']); col = p['color']
    if name == 'Face':
        continue                           # its drawing lives on the head texture
    if p.get('sm', {}).get('type') == 'Head':
        fdy = parts['Face']['cf'][1] - p['cf'][1]
        m = head_mesh(p['sm']['scale'][0], fdy, face)
    elif p['shape'] == 'Mesh':
        m = roblox_mesh('hair.mesh')
        lo, hi = m.bounds; m.apply_translation(-(lo + hi) / 2); m.apply_scale(np.array([sx, sy, sz]) / (hi - lo))
        m = solid(m, col, .7)
    elif p['shape'] == 'Cylinder':
        m = trimesh.creation.cylinder(radius=sy / 2, height=sx, sections=32)
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))   # Roblox cylinders run along X
        m = solid(m, col, .4)
    else:
        m = solid(trimesh.creation.box(extents=(sx, sy, sz)), col)
    m.apply_transform(M); m.apply_scale(STUD)
    scene.add_geometry(m, node_name=name, geom_name=name)

# stand him on the ground, centred
lo, hi = scene.bounds
scene.apply_translation([-(lo[0] + hi[0]) / 2, -lo[1], -(lo[2] + hi[2]) / 2])
print('height m', round(scene.bounds[1][1], 3), 'parts', len(scene.geometry))
scene.export('../sam.glb')
os.makedirs('../obj', exist_ok=True)
scene.export('../obj/sam.obj')
print('ok')
