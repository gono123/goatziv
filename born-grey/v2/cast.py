"""v2 cast: the hero from the user's own 3D model (assets/sam.glb), side characters with textured faces.

Faces are textures (assets/faces*/<expression>.png). A character keeps one head per expression it uses and
shows one at a time (set_face), so a shot can change expression on any frame.
"""
import math, os
import bpy
from mathutils import Vector, Matrix
import blib as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLB = os.path.join(ROOT, "assets", "sam.glb")
STUD = 0.28                     # the model is in metres at 0.28 m per stud
MOUTH_TO_FACE = {"open": "happy", "o": "surprised", "flat": "calm"}


def faces_dir(skin=None):
    return os.path.join(ROOT, "assets", "faces" if not skin else "faces_" + skin)


def _import_glb():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB)
    return [o for o in bpy.data.objects if o not in before]


def _wbox(o):
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


_HEAD_MESH = None


def head_mesh():
    """The model's rounded Roblox head (with face UVs), in studs, bottom-centre at the origin."""
    global _HEAD_MESH
    if _HEAD_MESH is not None and _HEAD_MESH.name in bpy.data.meshes:
        return _HEAD_MESH
    objs = _import_glb()
    h = next(o for o in objs if o.name.startswith("Head"))
    me = h.data.copy()
    me.transform(h.matrix_world)
    lo = Vector((min(v.co.x for v in me.vertices), min(v.co.y for v in me.vertices), min(v.co.z for v in me.vertices)))
    hi = Vector((max(v.co.x for v in me.vertices), max(v.co.y for v in me.vertices), max(v.co.z for v in me.vertices)))
    me.transform(Matrix.Translation(Vector((-(lo.x + hi.x) / 2, -(lo.y + hi.y) / 2, -lo.z))))
    me.transform(Matrix.Scale(1 / STUD, 4))
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    _HEAD_MESH = me
    return me


def poly_xz(pts, depth, y, m, parent, name):
    o = B.poly(pts, depth, (0, y, 0), m, parent, name)
    return o


class Faces:
    """Mixin: textured heads, one per expression."""

    def init_faces(self, mesh, world, parent, fdir, wash=True, invert=False):
        self._fmesh, self._fworld, self._fparent, self._fdir, self._fwash, self._finv = mesh, world, parent, fdir, wash, invert
        bpy.context.view_layer.update()
        self._flocal = parent.matrix_world.inverted() @ world      # head placement relative to its pivot
        self.face_heads = {}
        self._wash_keys = []

    def _head_for(self, name):
        if name in self.face_heads:
            return self.face_heads[name]
        me = self._fmesh.copy()
        me.materials.clear()
        me.materials.append(B.mat((1, 1, 1), rough=0.55, wash=self._fwash, invert=getattr(self, "_finv", False), image=os.path.join(self._fdir, name + ".png")))
        o = bpy.data.objects.new(f"{self.name}_face_{name}", me)
        bpy.context.scene.collection.objects.link(o)
        for p in o.data.polygons:
            p.use_smooth = True
        # place it relative to the pivot, so faces added after the character moved still sit on its neck
        o.parent = self._fparent
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.matrix_basis = self._flocal
        o["wash_line"] = self.parts[0]["wash_line"] if self.parts else 0.0
        for f, v in self._wash_keys:
            o["wash_line"] = v
            o.keyframe_insert('["wash_line"]', frame=f)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=-200)
        self.parts.append(o)
        self.face_heads[name] = o
        return o

    def set_face(self, frame, name):
        self._head_for(name)
        for k, o in self.face_heads.items():
            o.hide_render = (k != name)
            o.keyframe_insert("hide_render", frame=frame)

    def faces(self, *keys):
        """keys: (frame, name), ..."""
        for f, n in keys:
            self.set_face(f, n)

    # compatibility with the v1 shot helpers
    def set_mouth(self, which, frame, talk=None):
        if not hasattr(self, "face_heads"):      # still inside the blib build (geometry face, about to be replaced)
            return B.Char.set_mouth(self, which, frame)
        self.set_face(frame, MOUTH_TO_FACE.get(which, which))

    def talk(self, f0, env, mouth="open", base=0.35, rest="calm"):
        last = None
        for i, e in enumerate(env):
            n = rest if e < 0.12 else ("talk_1" if e < 0.35 else "talk_2" if e < 0.65 else "talk_3")
            if n != last:
                self.set_face(f0 + i, n)
                last = n
        self.set_face(f0 + len(env) + 1, rest)

    def brow(self, *a, **k):
        pass

    def eyes_scale(self, *a, **k):
        pass

    def wash(self, f0, f1, top=None, bottom=None):
        z0 = top if top is not None else self.root.location.z + 6.0 * self.root.scale.z
        z1 = bottom if bottom is not None else self.root.location.z - 0.5
        self._wash_keys += [(f0, 100 - z0), (f1, 100 - z1)]
        B.Char.wash(self, f0, f1, z0, z1)

    def wash_keys(self, keys):
        """keys: (frame, world z of the wash line), top to bottom."""
        for f, z in keys:
            self._wash_keys.append((f, 100 - z))
            for o in self.parts:
                o["wash_line"] = 100 - z
                o.keyframe_insert('["wash_line"]', frame=f)


class Hero(Faces, B.Char):
    """The pink-suit hero, built from the user's 3D model and re-pivoted onto the blib joints."""

    def build(self, face="calm", **kw):
        objs = _import_glb()
        bpy.context.view_layer.update()
        S = Matrix.Scale(1 / STUD, 4)
        R = self.root.matrix_world.copy()
        by = {o.name.split(".")[0]: o for o in objs if o.type == "MESH"}
        # stand him with his feet at z=0 of the root
        lo_all = min(_wbox(o)[0].z for o in by.values())
        lift = Matrix.Translation(Vector((0, 0, -lo_all)))
        for o in objs:
            o.matrix_world = R @ S @ lift @ o.matrix_world
        bpy.context.view_layer.update()
        self.head = B.empty(self.name + "_head", (0, 0, 0), self.neck)
        bpy.context.view_layer.update()
        rl = self.root.matrix_world.inverted()

        def side(o):
            c = rl @ ((_wbox(o)[0] + _wbox(o)[1]) / 2)
            return 0 if c.x < 0 else 1

        base_pivot = {}
        for n, o in by.items():
            if n.startswith("Head") or n.startswith("HairMesh"):
                base_pivot[n] = self.head
            elif "Arm" in n or "Hand" in n:
                base_pivot[n] = self.sh[side(o)]
            elif "Leg" in n or "Shoe" in n:
                base_pivot[n] = self.hip[side(o)]
            elif n.startswith("Torso"):
                base_pivot[n] = self.body
        order = [n for n in by if any(k in n for k in ("Hand", "Shoe"))] + [n for n in by if any(k in n for k in ("Arm", "Leg"))] + \
                [n for n in by if n.startswith("Head")] + [n for n in by if n.startswith("Torso")]
        for n, o in by.items():
            if n.startswith("Suit"):
                lo, hi = _wbox(o)
                c = (lo + hi) / 2
                piv = self.body
                for bn in order:
                    blo, bhi = _wbox(by[bn])
                    e = 0.08
                    if all(blo[i] - e <= c[i] <= bhi[i] + e for i in range(3)):
                        piv = base_pivot[bn]
                        break
                base_pivot[n] = piv
        # washable materials, one per base colour
        cache = {}
        for n, o in by.items():
            if n.startswith("Head"):
                continue
            new = []
            for m in o.data.materials:
                col = (1, 1, 1)
                if m and m.use_nodes and "Principled BSDF" in m.node_tree.nodes:
                    col = tuple(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value[:3])
                k = tuple(round(c, 3) for c in col)
                if k not in cache:
                    cache[k] = B.mat(col, rough=0.6)
                new.append(cache[k])
            o.data.materials.clear()
            for m in new:
                o.data.materials.append(m)
        for n, o in by.items():
            piv = base_pivot.get(n, self.body)
            o.parent = piv
            o.matrix_parent_inverse = piv.matrix_world.inverted()
            if not n.startswith("Head"):
                self.add(o)
        head = by["Head"]
        self.init_faces(head.data, head.matrix_world.copy(), self.head, faces_dir(None))
        head.hide_render = True
        head.hide_viewport = True
        for o in objs:
            if o.type != "MESH":
                bpy.data.objects.remove(o, do_unlink=True)
        self.set_face(1, face)


class Side(Faces, B.Char):
    """A blocky side character (blib look) wearing a textured face in its skin tone."""

    def build(self, skin_key="light", face="calm", glasses=False, monocle=False, cheeks=None, lace=None, tie=None, **look):
        look.setdefault("face", "flat")
        B.Char.build(self, cheeks=None, **look)
        drop = ("eye", "glint", "brow", "mouth", "teeth", "tongue", "cheek", "head")
        keep = []
        for o in list(self.parts):
            base = o.name.split(".")[0]
            if any(base == d or base.startswith(d + "_") for d in drop) or base in ("mouth_open", "mouth_o", "mouth_flat"):
                bpy.data.objects.remove(o, do_unlink=True)
            else:
                keep.append(o)
        for p in list(self.eye_pivots) + [e for e, _ in self.brows] + [self.mouth_pivot]:
            for c in list(p.children):
                bpy.data.objects.remove(c, do_unlink=True)
            bpy.data.objects.remove(p, do_unlink=True)
        self.parts = keep
        self.mouths = {}
        bpy.context.view_layer.update()
        world = self.head.matrix_world @ Matrix.Translation(Vector((0, 0, 0.04)))
        self.init_faces(head_mesh(), world, self.head, faces_dir(skin_key), wash=look.get("wash", True), invert=look.get("invert", False))
        self.set_face(1, face)
        A = self.add
        if glasses:
            gm = B.mat("#151515", rough=0.3, wash=False)
            for x in (-0.25, 0.25):
                r = B.cyl(0.2, 0.05, (x, -0.66, 0.83), gm, self.head, verts=24, rot=(90, 0, 0), name="lens_rim")
                A(r)
                A(B.cyl(0.16, 0.06, (x, -0.67, 0.83), B.mat("#dfefff", rough=0.05, wash=False), self.head, verts=24, rot=(90, 0, 0), name="lens"))
            A(B.box((0.14, 0.04, 0.04), (0, -0.67, 0.86), gm, self.head, name="bridge"))
        if monocle:
            A(B.cyl(0.24, 0.05, (0.26, -0.67, 0.83), B.mat("#ffd700", metal=1, rough=0.2, wash=False, invert=True), self.head, verts=32, rot=(90, 0, 0), name="monocle"))
            A(B.cyl(0.2, 0.03, (0.26, -0.69, 0.83), B.mat("#ffffff", emit=3.0, wash=False), self.head, verts=32, rot=(90, 0, 0), name="glow"))
        if cheeks:
            cm = B.mat(cheeks, wash=False)
            for x in (-0.38, 0.38):
                y = -math.sqrt(max(0, 0.63 ** 2 - x * x))
                c = A(B.sphere(0.13, (x, y, 0.56), cm, self.head, scale=(1, 0.25, 0.7), name="cheekdisc"))
                c.rotation_euler.z = math.asin(x / 0.63)
        self.tie_objs = []
        if tie:    # collar + knot + blade on the shirt front (the knot and blade can be animated: tug, untie)
            y = -0.51
            A(poly_xz([(-0.42, 4.0), (0.42, 4.0), (0, 3.45)], 0.02, y, B.mat("#ffffff", rough=0.5), self.body, "collar"))
            tm = B.mat(tie, rough=0.4, emit=(0.6 if tie in ("#d4af37", "#ffd23f") else 0.0))
            knot = A(B.box((0.3, 0.07, 0.24), (0, y - 0.03, 3.86), tm, self.body, bevel=0.03, name="tieknot"))
            blade_piv = B.empty("tieblade", (0, y - 0.03, 3.74), self.body)
            blade = A(poly_xz([(-0.15, 0.0), (0.15, 0.0), (0.22, -1.05), (0, -1.25), (-0.22, -1.05)], 0.03, 0, tm, blade_piv, "tie"))
            self.tie_objs = [knot, blade]
            self.tie_pivot = blade_piv
        if lace:   # a single coloured shoelace that does not wash grey
            A(B.box((0.7, 0.08, 0.06), (0, -0.55, -1.78), B.mat(lace, emit=0.4, wash=False), self.hip[1], name="lace"))


# ----------------------------------------------------------------------------- the cast

def hero(loc=(0, 0, 0), rot=0, colored=True, face="calm"):
    h = Hero("hero", loc, rot, dict(face=face))
    h.colored(colored)
    return h


def mom(loc=(0, 0, 0), rot=0, face="calm"):
    return Side("mom", loc, rot, dict(skin_key="light", face=face, skin="#ffd6aa", top="#ffd23f", pants="#ffd23f",
                                      shoes="#8b4f2a", dress="#ffd23f", hair="#c0392b", hair_style="long"))


def pip(loc=(0, 0, 0), rot=0, face="calm", lace="#1e88ff", tie=None):
    return Side("pip", loc, rot, dict(skin_key="brown", face=face, skin="#965f38", top="#ff8a1e", pants="#ff7a00",
                                      shoes="#5a3a22", hair="#161616", hair_style="curly", glasses=True, lace=lace, tie=tie), scale=0.86)


def prism(loc=(0, 0, 0), rot=0, face="smug", scale=1.3):
    return Side("prism", loc, rot, dict(skin_key="pale", face=face, skin="#fae2c8", top="#ffffff", pants="#ffffff",
                                        shoes="#ffd700", rainbow=True, invert=True, hair="#ffffff", hair_style="none",
                                        hat="top", monocle=True), scale=scale)


def inspector(name, loc=(0, 0, 0), rot=0):
    return B.inspector(name, loc, rot)


TOWN_LOOKS = [
    dict(skin_key="tan", skin="#dea86e", top="#2ecc71", pants="#1f4e8c", hair="#111111", hair_style="short"),
    dict(skin_key="light", skin="#ffd6aa", top="#e74c3c", pants="#34495e", hair="#e67e22", hair_style="bun"),
    dict(skin_key="pale", skin="#fae2c8", top="#3498db", pants="#2c3e50", hair="#f1c40f", hair_style="short"),
    dict(skin_key="brown", skin="#965f38", top="#9b59b6", pants="#7f8c8d", hair="#2c1b0e", hair_style="cap"),
    dict(skin_key="light", skin="#ffd6aa", top="#e67e22", pants="#16a085", hair="#d35400", hair_style="long"),
    dict(skin_key="tan", skin="#dea86e", top="#1abc9c", pants="#c0392b", hair="#6d4c41", hair_style="curly"),
]


def townie(i, loc=(0, 0, 0), rot=0, face="calm", scale=1.0, **over):
    look = dict(TOWN_LOOKS[i % len(TOWN_LOOKS)]); look.update(over); look["face"] = face
    return Side("townie%d" % i, loc, rot, look, scale=scale)


def grandma(loc=(0, 0, 0), rot=0, face="calm"):
    return Side("grandma", loc, rot, dict(skin_key="pale", face=face, skin="#fae2c8", top="#b5838d", pants="#6d597a",
                                          shoes="#3a3a3a", hair="#e8e8e8", hair_style="bun"), scale=0.95)


def mailman(loc=(0, 0, 0), rot=0, face="happy"):
    return Side("mailman", loc, rot, dict(skin_key="light", face=face, skin="#ffd6aa", top="#3f6fb5", pants="#2b4a7a",
                                          shoes="#222222", hair="#2a3f6a", hair_style="cap", cheeks="#ff2b2b"))


UNIFORM = dict(top="#f4f4f4", pants="#1f2a44", shoes="#2a1a12", tie="#c62828")


def kid(i, loc=(0, 0, 0), rot=0, face="calm", scale=0.9, **over):
    """A school kid in uniform (white shirt, navy trousers, red tie)."""
    look = dict(TOWN_LOOKS[i % len(TOWN_LOOKS)]); look.update(UNIFORM); look.update(over); look["face"] = face
    c = Side("kid%d" % i, loc, rot, look, scale=scale)
    c.colored(True)
    return c


def knotley(loc=(0, 0, 0), rot=0, face="happy", scale=1.3):
    """Principal Knotley: tall, slick, dark purple suit, gold tie, never stops smiling."""
    c = Side("knotley", loc, rot, dict(skin_key="pale", face=face, skin="#fae2c8", top="#3d1f66", pants="#2e1850",
                                      shoes="#111111", hair="#1c1c1c", hair_style="short", tie="#d4af37"), scale=scale)
    c.colored(True)
    return c


def adult(i, loc=(0, 0, 0), rot=0, face="calm", tie="#1f3a93", **over):
    look = dict(TOWN_LOOKS[i % len(TOWN_LOOKS)]); look.update(dict(top="#5b6475", pants="#2c3340", tie=tie)); look.update(over); look["face"] = face
    c = Side("adult%d" % i, loc, rot, look, scale=1.08)
    c.colored(True)
    return c
