"""Blender building blocks for the channel: materials, blocky characters, props, sets, cameras.

Everything is built from code (no .blend files). Units are "studs": a character is ~5.7 tall.
Characters face -Y (toward a camera placed at -Y) when their root rotation is 0.

The grey-paint effect: every washable material mixes a grey version of its colour with the real
colour. Colour shows where world Z is above (100 - L), L being the object's custom property
"wash_line" (missing = 0 = fully grey). Keyframe L upward to wash from the top down. A scene-wide
property "town_line" does the same for everything at once. invert=True materials (paint that rain
removes) do the opposite.
"""
import math, os
import bpy, bmesh
from mathutils import Vector, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "zero-fear", "engine", "fonts")
FPS = 24


# ----------------------------------------------------------------------------- scene

def reset(res=(720, 1280), samples=12):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    sc.eevee.taa_render_samples = samples
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    try:
        sc.eevee.use_shadows = True
        sc.eevee.shadow_ray_count = 1
        sc.eevee.shadow_step_count = 4
    except AttributeError:
        pass
    try:
        sc.eevee.shadow_resolution_scale = 0.5
    except AttributeError:
        pass
    sc["town_line"] = 0.0
    return sc


def world(top=(0.62, 0.66, 0.72), bottom=(0.80, 0.82, 0.85), strength=1.0, name="World"):
    w = bpy.data.worlds.new(name)
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (*bottom, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (*top, 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs[0], out.inputs[0])
    return w, ramp, bg


def sun(energy=3.2, rot=(50, 0, 35), color=(1, 0.97, 0.92), angle=8):
    d = bpy.data.lights.new("Sun", "SUN")
    d.energy = energy
    d.color = color
    d.angle = math.radians(angle)
    o = bpy.data.objects.new("Sun", d)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = [math.radians(a) for a in rot]
    return o


def point(loc, energy=200, color=(1, 1, 1), radius=0.5):
    d = bpy.data.lights.new("Point", "POINT")
    d.energy = energy
    d.color = color
    d.shadow_soft_size = radius
    d.use_shadow = False  # point-light shadows are slow in software Eevee; the sun casts the shadows
    o = bpy.data.objects.new("Point", d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


# ----------------------------------------------------------------------------- materials

def hexc(h):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb)


_MATS = {}


def _inp(node, name, kind=None):
    for i in node.inputs:
        if i.name == name and (kind is None or i.type == kind):
            return i
    raise KeyError(name)


def _out(node, name, kind=None):
    for o in node.outputs:
        if o.name == name and (kind is None or o.type == kind):
            return o
    raise KeyError(name)


def mat(color, rough=0.6, wash=True, invert=False, knit=False, emit=0.0, alpha=1.0, metal=0.0,
        rainbow=False, name=None, grey_tint=(0.97, 0.99, 1.05), grey_gain=0.95):
    """Cached material. color: '#rrggbb' or linear rgb tuple."""
    if isinstance(color, str):
        color = hexc(color)
    key = (tuple(round(c, 4) for c in color), rough, wash, invert, knit, emit, alpha, metal, rainbow, grey_gain)
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new(name or "m%d" % len(_MATS))
    m.use_nodes = True
    nt = m.node_tree
    N, L = nt.nodes, nt.links
    bsdf = N["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    try:
        bsdf.inputs["Specular IOR Level"].default_value = 0.35
    except KeyError:
        pass
    # colour source
    if rainbow:
        geo = N.new("ShaderNodeNewGeometry")
        sep = N.new("ShaderNodeSeparateXYZ")
        L.new(geo.outputs["Position"], sep.inputs[0])
        add = N.new("ShaderNodeMath"); add.operation = "MULTIPLY_ADD"
        L.new(sep.outputs["Z"], add.inputs[0]); add.inputs[1].default_value = 0.55
        L.new(sep.outputs["X"], add.inputs[2])
        fr = N.new("ShaderNodeMath"); fr.operation = "FRACT"
        L.new(add.outputs[0], fr.inputs[0])
        ramp = N.new("ShaderNodeValToRGB")
        cols = ["#ff2d55", "#ff9500", "#ffe600", "#34c759", "#00c7ff", "#5856d6", "#ff2dc8"]
        els = ramp.color_ramp.elements
        els[0].position, els[0].color = 0.0, (*hexc(cols[0]), 1)
        els[1].position, els[1].color = 1.0, (*hexc(cols[0]), 1)
        for i, c in enumerate(cols[1:], 1):
            e = els.new(i / len(cols)); e.color = (*hexc(c), 1)
        ramp.color_ramp.interpolation = "CONSTANT"
        L.new(fr.outputs[0], ramp.inputs[0])
        col_out = ramp.outputs["Color"]
    else:
        rgb = N.new("ShaderNodeRGB")
        rgb.outputs[0].default_value = (*color, 1)
        col_out = rgb.outputs[0]
    final = col_out
    if wash:
        bw = N.new("ShaderNodeRGBToBW")
        L.new(col_out, bw.inputs[0])
        gv = N.new("ShaderNodeMath"); gv.operation = "MULTIPLY_ADD"
        L.new(bw.outputs[0], gv.inputs[0]); gv.inputs[1].default_value = 0.42 * grey_gain; gv.inputs[2].default_value = 0.05
        g = N.new("ShaderNodeVectorMath"); g.operation = "MULTIPLY"
        L.new(gv.outputs[0], g.inputs[0])
        g.inputs[1].default_value = list(grey_tint)
        geo = N.new("ShaderNodeNewGeometry")
        sep = N.new("ShaderNodeSeparateXYZ")
        L.new(geo.outputs["Position"], sep.inputs[0])

        def wipe(attr_type, attr_name):
            a = N.new("ShaderNodeAttribute"); a.attribute_type = attr_type; a.attribute_name = attr_name
            thr = N.new("ShaderNodeMath"); thr.operation = "SUBTRACT"
            thr.inputs[0].default_value = 100.0
            L.new(a.outputs["Fac"], thr.inputs[1])
            d = N.new("ShaderNodeMath"); d.operation = "SUBTRACT"
            L.new(sep.outputs["Z"], d.inputs[0]); L.new(thr.outputs[0], d.inputs[1])
            mr = N.new("ShaderNodeMapRange"); mr.clamp = True
            L.new(d.outputs[0], mr.inputs["Value"])
            mr.inputs["From Min"].default_value = -0.12
            mr.inputs["From Max"].default_value = 0.12
            return mr.outputs["Result"]

        f1 = wipe("OBJECT", "wash_line")
        if invert:  # paint that rain removes: only this object's own wash matters
            fac = f1
        else:
            f2 = wipe("VIEW_LAYER", "town_line")
            mx = N.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
            L.new(f1, mx.inputs[0]); L.new(f2, mx.inputs[1])
            fac = mx.outputs[0]
        if invert:
            inv = N.new("ShaderNodeMath"); inv.operation = "SUBTRACT"
            inv.inputs[0].default_value = 1.0
            L.new(fac, inv.inputs[1]); fac = inv.outputs[0]
        mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"
        L.new(fac, _inp(mix, "Factor", "VALUE"))
        L.new(g.outputs[0], _inp(mix, "A", "RGBA"))
        L.new(col_out, _inp(mix, "B", "RGBA"))
        final = _out(mix, "Result", "RGBA")
    L.new(final, bsdf.inputs["Base Color"])
    if knit:
        tc = N.new("ShaderNodeTexCoord")
        wave = N.new("ShaderNodeTexWave")
        wave.wave_type = "BANDS"; wave.bands_direction = "X"
        wave.inputs["Scale"].default_value = 22
        wave.inputs["Distortion"].default_value = 3
        wave.inputs["Detail"].default_value = 2
        L.new(tc.outputs["Object"], wave.inputs["Vector"])
        noise = N.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 90
        L.new(tc.outputs["Object"], noise.inputs["Vector"])
        add = N.new("ShaderNodeMath"); add.operation = "ADD"
        L.new(wave.outputs["Fac"], add.inputs[0]); L.new(noise.outputs["Fac"], add.inputs[1])
        bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35
        bump.inputs["Distance"].default_value = 0.02
        L.new(add.outputs[0], bump.inputs["Height"])
        L.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    if emit:
        L.new(final, bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except AttributeError:
            m.blend_method = "BLEND"
    _MATS[key] = m
    return m


# ----------------------------------------------------------------------------- geometry

def _link(o, parent=None):
    bpy.context.scene.collection.objects.link(o)
    if parent is not None:
        o.parent = parent
    return o


def empty(name="E", loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    o.location = loc
    return _link(o, parent)


def mesh_obj(name, bm, m, parent=None, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    o.location = loc
    if m is not None:
        me.materials.append(m)
    return _link(o, parent)


def box(size, loc, m, parent=None, bevel=0.0, name="box", rot=(0, 0, 0)):
    """size (x,y,z); loc = centre."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    o = mesh_obj(name, bm, m, parent, loc)
    o.rotation_euler = [math.radians(a) for a in rot]
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width = bevel; b.segments = 3
        b.limit_method = "NONE"
    return o


def cyl(r, h, loc, m, parent=None, verts=24, name="cyl", rot=(0, 0, 0), r2=None, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts,
                          radius1=r, radius2=r if r2 is None else r2, depth=h)
    o = mesh_obj(name, bm, m, parent, loc)
    o.rotation_euler = [math.radians(a) for a in rot]
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width = bevel; b.segments = 3
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def sphere(r, loc, m, parent=None, scale=(1, 1, 1), name="sph", seg=24):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    o = mesh_obj(name, bm, m, parent, loc)
    o.scale = scale
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def poly(pts2d, depth, loc, m, parent=None, name="poly", plane="XZ"):
    """Extruded flat polygon. pts2d in the plane (x, z) for 'XZ'; extruded along -Y by depth."""
    bm = bmesh.new()
    vs = []
    for (a, b) in pts2d:
        vs.append(bm.verts.new((a, 0, b) if plane == "XZ" else (a, b, 0)))
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    off = Vector((0, -depth, 0)) if plane == "XZ" else Vector((0, 0, depth))
    bmesh.ops.translate(bm, vec=off, verts=[e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_obj(name, bm, m, parent, loc)


def text(body, loc, m, size=1.0, parent=None, font="Bungee-Regular.ttf", extrude=0.05, rot=(90, 0, 0), align="CENTER"):
    cu = bpy.data.curves.new("txt", "FONT")
    cu.body = body
    cu.size = size
    cu.extrude = extrude
    cu.align_x = align
    cu.align_y = "CENTER"
    fp = os.path.join(FONTS, font)
    if os.path.exists(fp):
        cu.font = bpy.data.fonts.load(fp, check_existing=True)
    o = bpy.data.objects.new("txt", cu)
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    cu.materials.append(m)
    return _link(o, parent)


def arch(r_out, r_in, loc, m, parent=None, depth=0.3, seg=32):
    """Upper half of a ring, in the XZ plane, facing -Y."""
    pts = [(r_out * math.cos(math.pi * i / seg), r_out * math.sin(math.pi * i / seg)) for i in range(seg + 1)]
    pts += [(r_in * math.cos(math.pi * i / seg), r_in * math.sin(math.pi * i / seg)) for i in range(seg, -1, -1)]
    return poly(pts, depth, loc, m, parent, "arch")


def letters(word, loc, size, colors, parent=None, extrude=0.25, gap=0.12, emit=1.2, font="Bungee-Regular.ttf"):
    """A word with every letter in its own colour, centred on loc (XZ plane, facing -Y)."""
    objs = []
    for i, ch in enumerate(word):
        if ch == " ":
            objs.append(None)
            continue
        objs.append(text(ch, (0, 0, 0), mat(colors[i % len(colors)], emit=emit, wash=False), size=size, parent=parent, extrude=extrude, align="LEFT"))
    bpy.context.view_layer.update()
    widths = [(o.dimensions.x if o else size * 0.45) for o in objs]
    total = sum(widths) + gap * size * (len(objs) - 1)
    x = loc[0] - total / 2
    for o, w in zip(objs, widths):
        if o:
            o.location = (x, loc[1], loc[2])
        x += w + gap * size
    return objs


def roof(w, d, h, loc, m, parent=None):
    """Triangular prism (gable roof) along Y."""
    pts = [(-w / 2, 0), (w / 2, 0), (0, h)]
    o = poly(pts, d, (loc[0], loc[1] + d / 2, loc[2]), m, parent, "roof")
    return o


# ----------------------------------------------------------------------------- characters

SKIN = "#f7dea0"
BLACK = "#141414"


class Char:
    """A blocky character. Parts hang off pivot empties so poses are simple rotations."""

    def __init__(self, name, loc=(0, 0, 0), rot=0, look=None, scale=1.0):
        self.name = name
        self.parts = []
        self.root = empty(name, loc)
        self.root.rotation_euler.z = math.radians(rot)
        self.root.scale = (scale,) * 3
        self.body = empty(name + "_body", (0, 0, 0), self.root)   # bob / lean
        self.neck = empty(name + "_neck", (0, 0, 4.0), self.body)
        self.sh = [empty(name + "_shL", (-1.5, 0, 3.92), self.body), empty(name + "_shR", (1.5, 0, 3.92), self.body)]
        self.hip = [empty(name + "_hipL", (-0.5, 0, 2.0), self.body), empty(name + "_hipR", (0.5, 0, 2.0), self.body)]
        self.mouths = {}
        self.brows = []
        self.eyes = []
        self.build(**(look or {}))

    def add(self, o):
        self.parts.append(o)
        o["wash_line"] = 0.0
        return o

    # ---- body
    def build(self, skin=SKIN, top="#9a9a9a", top_knit=False, pants="#6b6b6b", shoes="#3a3a3a",
              sleeve=None, cuff=None, hair="#4a3a2a", hair_style="spiky", suit=False, dress=None,
              face="smile", hat=None, cheeks=None, rainbow=False, invert=False, wash=True, helmet=False,
              coat=False, hair2=None):
        kw = dict(wash=wash, invert=invert)
        tm = mat(top, knit=top_knit, rainbow=rainbow, **kw)
        pm = mat(pants, knit=top_knit, rainbow=rainbow, **kw)
        sk = mat(skin, rough=0.5, **kw)
        A = self.add
        # torso
        A(box((2.0, 1.0, 2.0), (0, 0, 3.0), tm, self.body, bevel=0.03, name="torso"))
        # arms: sleeve, cuff, hand
        sm = mat(sleeve or top, knit=top_knit, rainbow=rainbow, **kw)
        for s, p in zip((-1, 1), self.sh):
            A(box((1.0, 1.0, 1.42), (0, 0, 0.08 - 0.71), sm, p, bevel=0.03, name="sleeve"))
            if cuff:
                A(box((1.01, 1.01, 0.16), (0, 0, 0.08 - 1.42 - 0.08), mat(cuff, **kw), p, name="cuff"))
                A(box((0.98, 0.98, 0.42), (0, 0, 0.08 - 1.58 - 0.21), sk, p, bevel=0.03, name="hand"))
            else:
                A(box((0.98, 0.98, 0.58), (0, 0, 0.08 - 1.42 - 0.29), sk, p, bevel=0.03, name="hand"))
        # legs
        for p in self.hip:
            A(box((0.99, 1.0, 1.72), (0, 0, -0.86), pm, p, bevel=0.02, name="leg"))
            A(box((1.02, 1.05, 0.3), (0, -0.01, -1.86), mat(shoes, rough=0.4, **kw), p, bevel=0.03, name="shoe"))
        if dress:
            dm = mat(dress, **kw)
            pts = [(-1.0, 0.0), (1.0, 0.0), (1.3, -1.35), (-1.3, -1.35)]
            o = A(poly(pts, 1.3, (0, 0.65, 2.05), dm, self.body, "skirt"))
        if coat:
            cm = mat(top, **kw)
            A(box((2.1, 1.08, 1.3), (0, 0, 1.45), cm, self.body, name="coat"))
            A(box((0.06, 1.1, 2.5), (0, -0.0, 2.6), mat("#2a2a2a", **kw), self.body, name="seam"))
        if suit:
            self.suit_details(kw)
        # head
        self.head = empty(self.name + "_head", (0, 0, 0), self.neck)
        A(cyl(0.66, 1.25, (0, 0, 0.68), sk, self.head, verts=32, name="head", bevel=0.2))
        self.make_face(kw, face, cheeks)
        self.make_hair(hair, hair_style, kw, hair2)
        if hat == "top":
            hm = mat("#1d1d1d", rough=0.3, rainbow=rainbow, **kw)
            A(cyl(0.95, 0.08, (0, 0, 1.34), hm, self.head, name="brim"))
            A(cyl(0.62, 1.1, (0, 0, 1.9), hm, self.head, name="hat"))
            A(cyl(0.63, 0.18, (0, 0, 1.48), mat("#f5c400", metal=0.8, rough=0.25, wash=wash, invert=invert), self.head, name="band"))
        if helmet:
            hm = mat("#6f7277", rough=0.35, **kw)
            A(sphere(0.78, (0, 0, 1.05), hm, self.head, scale=(1, 1, 0.75), name="helmet"))
            A(box((1.2, 0.2, 0.32), (0, -0.62, 0.78), mat("#0d0d0d", rough=0.15, wash=False), self.head, name="visor"))
            self.siren = A(cyl(0.16, 0.25, (0, 0, 1.68), mat("#ff1a1a", emit=3.0, wash=False), self.head, name="siren"))

    def suit_details(self, kw):
        """The hero's pink suit front: lapels, shirt, tie, buttons, pockets, pocket square."""
        A = self.add
        y = -0.505
        b = self.body
        white = mat("#ffffff", rough=0.5, **kw)
        lapel = mat("#ff3fa8", **kw)
        tie = mat("#c8124c", **kw)
        stripe = mat("#ff7fbf", **kw)
        dark = mat("#5a0d2a", rough=0.3, **kw)
        flap = mat("#ff4fb0", **kw)
        # shirt V
        A(poly([(-0.42, 4.0), (0.42, 4.0), (0, 3.05)], 0.02, (0, y + 0.0, 0), white, b, "shirt"))
        # lapels
        A(poly([(-0.62, 4.0), (-0.38, 4.0), (0.0, 2.98), (-0.12, 2.9)], 0.03, (0, y - 0.005, 0), lapel, b, "lapelL"))
        A(poly([(0.62, 4.0), (0.38, 4.0), (0.0, 2.98), (0.12, 2.9)], 0.03, (0, y - 0.005, 0), lapel, b, "lapelR"))
        # tie
        A(poly([(-0.1, 3.98), (0.1, 3.98), (0.13, 3.2), (0, 3.06), (-0.13, 3.2)], 0.02, (0, y - 0.012, 0), tie, b, "tie"))
        for z in (3.75, 3.55, 3.35):
            A(box((0.2, 0.01, 0.04), (0, y - 0.035, z), stripe, b, rot=(0, -28, 0), name="stripe"))
        # buttons
        for z in (2.72, 2.42):
            A(cyl(0.07, 0.03, (0, y - 0.02, z), dark, b, rot=(90, 0, 0), name="button"))
        # pocket flaps
        A(box((0.55, 0.02, 0.09), (-0.55, y - 0.01, 2.45), flap, b, name="pocket"))
        A(box((0.55, 0.02, 0.09), (0.55, y - 0.01, 2.45), flap, b, name="pocket"))
        A(box((0.4, 0.02, 0.06), (0.6, y - 0.01, 3.55), flap, b, name="chest"))
        A(poly([(0.45, 3.58), (0.75, 3.58), (0.62, 3.7), (0.55, 3.66)], 0.02, (0, y - 0.02, 0), white, b, "square"))
        # belt line
        A(box((2.02, 1.02, 0.04), (0, 0, 2.02), mat("#ff4fb0", **kw), b, name="hem"))
        # vertical centre line
        A(box((0.025, 0.01, 1.0), (0, y - 0.012, 2.5), mat("#e94b9a", **kw), b, name="seam"))

    def _face_pt(self, x, z):
        """A point on the front of the head cylinder (radius 0.66) and its yaw."""
        r = 0.665
        y = -math.sqrt(max(0.0, r * r - x * x))
        return (x, y, z), math.degrees(math.asin(max(-1, min(1, x / r))))

    def make_face(self, kw, face, cheeks):
        A = self.add
        h = self.head
        blk = mat(BLACK, rough=0.3, wash=False)
        wht = mat("#ffffff", rough=0.3, wash=False)
        self.eye_pivots = []
        for x in (-0.24, 0.24):
            p, yaw = self._face_pt(x, 0.82)
            e = empty("eye", p, h); e.rotation_euler.z = math.radians(yaw)
            A(sphere(0.1, (0, 0, 0), blk, e, scale=(1, 0.35, 1.45), name="eye"))
            A(sphere(0.035, (0.025, -0.03, 0.06), wht, e, scale=(1, 0.4, 1), name="glint"))
            self.eye_pivots.append(e)
        for s, x in ((-1, -0.25), (1, 0.25)):
            p, yaw = self._face_pt(x, 1.06)
            e = empty("brow", p, h); e.rotation_euler = (0, math.radians(-14 * s), math.radians(yaw))
            A(box((0.3, 0.05, 0.065), (0, 0, 0), blk, e, name="brow"))
            self.brows.append((e, s))
        # mouths: "open" smile (D-shape, scales with talking), "o" (shock), "flat"
        p, _ = self._face_pt(0, 0.5)
        self.mouth_pivot = empty("mouth", (p[0], p[1] + 0.02, p[2] + 0.06), h)
        pts = [(-0.2, 0.0)] + [(0.2 * math.cos(math.pi * t / 10), -0.2 * math.sin(math.pi * t / 10)) for t in range(0, 11)][::-1] + [(0.2, 0.0)]
        pts = [(0.2 * math.cos(math.pi + math.pi * t / 12), 0.17 * math.sin(math.pi + math.pi * t / 12)) for t in range(0, 13)]
        o = A(poly(pts, 0.05, (0, 0.0, 0), blk, self.mouth_pivot, "mouth_open"))
        A(poly([(-0.15, -0.005), (0.15, -0.005), (0.13, -0.05), (-0.13, -0.05)], 0.02, (0, -0.035, 0), wht, o, "teeth"))
        A(poly([(-0.08, -0.16), (0.08, -0.16), (0.1, -0.1), (-0.1, -0.1)], 0.02, (0, -0.035, 0), mat("#d94b5b", wash=False), o, "tongue"))
        self.mouths["open"] = o
        self.mouths["o"] = A(sphere(0.12, (0, -0.01, -0.07), blk, self.mouth_pivot, scale=(0.85, 0.3, 1.15), name="mouth_o"))
        self.mouths["flat"] = A(box((0.26, 0.04, 0.05), (0, 0, -0.06), blk, self.mouth_pivot, name="mouth_flat"))
        if cheeks:
            for x in (-0.4, 0.4):
                p, yaw = self._face_pt(x, 0.62)
                c = A(sphere(0.12, p, mat(cheeks, wash=False), h, scale=(1, 0.2, 0.7), name="cheek"))
                c.rotation_euler.z = math.radians(yaw)
        self.set_mouth(face, 1)

    def make_hair(self, hair, style, kw, hair2=None):
        if style == "none":
            return
        A = self.add
        hm = mat(hair, rough=0.75, **kw)
        h = self.head
        if style in ("spiky", "short", "long", "bun"):
            A(sphere(0.72, (0, 0.06, 1.18), hm, h, scale=(1.0, 1.0, 0.55), name="haircap"))
            A(box((1.42, 0.9, 0.42), (0, 0.22, 1.06), hm, h, bevel=0.15, name="hairback"))
        if style == "spiky":
            # front quiff + spikes, like the hero
            A(cyl(0.34, 0.5, (0, -0.32, 1.52), hm, h, r2=0.0, rot=(-28, 0, 0), name="spike"))
            for x, z, ry in ((-0.32, 1.42, -25), (0.32, 1.42, 25), (-0.15, 1.5, -10), (0.15, 1.5, 10)):
                A(cyl(0.26, 0.42, (x, -0.2, z), hm, h, r2=0.0, rot=(-20, ry, 0), name="spike"))
            dm = mat(hair2 or "#5c2c10", rough=0.8, **kw)
            for x in (-0.66, 0.66):
                A(box((0.08, 0.8, 0.5), (x, 0.08, 0.98), dm, h, name="sideburn"))
        if style == "long":
            A(box((1.5, 0.5, 1.6), (0, 0.45, 0.55), hm, h, bevel=0.15, name="hairlong"))
        if style == "bun":
            A(sphere(0.35, (0, 0.45, 1.55), hm, h, name="bun"))
        if style == "curly":
            for i in range(9):
                a = i / 9 * math.tau
                A(sphere(0.32, (0.5 * math.cos(a), 0.12 + 0.5 * math.sin(a), 1.25), hm, h, name="curl"))
            A(sphere(0.45, (0, 0.1, 1.42), hm, h, name="curl"))
        if style == "cap":
            cm = mat(hair, rough=0.5, **kw)
            A(sphere(0.71, (0, 0.04, 1.12), cm, h, scale=(1, 1, 0.62), name="cap"))
            A(box((0.9, 0.7, 0.06), (0, -0.62, 1.12), cm, h, bevel=0.03, name="visor"))

    # ---- state / animation
    def set_mouth(self, which, frame, talk=None):
        for k, o in self.mouths.items():
            for x in [o] + list(o.children):
                x.hide_render = (k != which)
                x.keyframe_insert("hide_render", frame=frame)

    def talk(self, f0, env, mouth="open", base=0.35):
        """Animate the open mouth's height with a 24 fps loudness envelope starting at frame f0."""
        self.set_mouth(mouth, f0)
        o = self.mouths[mouth]
        for i, e in enumerate(env):
            o.scale = (1, 1, base + (1.15 - base) * e)
            o.keyframe_insert("scale", frame=f0 + i)
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=f0 + len(env) + 2)

    def brow(self, frame, angle=14, lift=0.0):
        for e, s in self.brows:
            e.rotation_euler.y = math.radians(-angle * s)
            e.keyframe_insert("rotation_euler", frame=frame)
            e.location.z = 1.06 + lift
            e.keyframe_insert("location", frame=frame)

    def eyes_scale(self, frame, s=1.0):
        for e in self.eye_pivots:
            e.scale = (s, s, s)
            e.keyframe_insert("scale", frame=frame)

    def wash(self, f0, f1, top=None, bottom=None):
        """Grey -> colour wipe, top to bottom, between frames f0 and f1 (world-space Z)."""
        z0 = (top if top is not None else self.root.location.z + 6.2 * self.root.scale.z)
        z1 = (bottom if bottom is not None else self.root.location.z - 0.5)
        for o in self.parts:
            o["wash_line"] = 100 - z0
            o.keyframe_insert('["wash_line"]', frame=f0)
            o["wash_line"] = 100 - z1
            o.keyframe_insert('["wash_line"]', frame=f1)

    def colored(self, on=True):
        for o in self.parts:
            o["wash_line"] = 300.0 if on else 0.0

    def key_rot(self, obj, frame, x=0, y=0, z=0):
        obj.rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
        obj.keyframe_insert("rotation_euler", frame=frame)

    def pose(self, frame, name="idle", t=0.0):
        """Pose presets (arm/leg rotations in degrees)."""
        L, R = self.sh
        P = {
            "idle": ((0, 0, 0), (0, 0, 0)),
            # +X rotation swings an arm backward, -X forward; +Y moves the left arm outward, -Y the right
            "arms_out": ((0, 80, 0), (0, -80, 0)),
            "arms_up": ((0, 160, 0), (0, -160, 0)),
            "point": ((0, 0, 0), (-90, 0, 0)),
            "point_up": ((0, 0, 0), (-165, 0, 0)),
            "hold": ((-70, 0, 0), (-70, 0, 0)),
            "hands_face": ((-100, -14, 0), (-100, 14, 0)),
            "shield": ((0, 0, 0), (-145, 18, 0)),
            "scared": ((-150, 22, 0), (-150, -22, 0)),
            "wag": ((0, 0, 0), (-150, 12, 0)),
            "wave": ((0, 0, 0), (0, -150, 0)),
            "hips": ((0, 22, 0), (0, -22, 0)),
            "pull": ((-60, 0, 0), (-60, 0, 0)),
            "roll": ((-95, 0, 0), (-95, 0, 0)),
            "look_hands": ((-60, -22, 0), (-60, 22, 0)),
            "cheer": ((0, 150, 0), (0, -150, 0)),
            "thumb": ((0, 0, 0), (-80, 0, 0)),
            "sit_arms": ((-45, 0, 0), (-45, 0, 0)),
        }[name]
        self.key_rot(L, frame, *P[0])
        self.key_rot(R, frame, *P[1])

    def legs(self, frame, a=0):
        self.key_rot(self.hip[0], frame, a)
        self.key_rot(self.hip[1], frame, -a)

    def head_turn(self, frame, yaw=0, pitch=0, roll=0):
        self.key_rot(self.neck, frame, pitch, roll, yaw)

    def face_dir(self, frame, deg):
        self.root.rotation_euler.z = math.radians(deg)
        self.root.keyframe_insert("rotation_euler", frame=frame)

    def move(self, frame, loc):
        self.root.location = loc
        self.root.keyframe_insert("location", frame=frame)

    def idle(self, f0, f1, amp=0.05, period=48, phase=0.0, arms=True):
        """Breathing bob + small arm sway."""
        f = f0
        while f <= f1:
            ph = (f - f0) / period * math.tau + phase
            self.body.location.z = amp * (0.5 + 0.5 * math.sin(ph))
            self.body.keyframe_insert("location", frame=f)
            f += period // 4
        if arms:
            f = f0
            while f <= f1:
                ph = (f - f0) / period * math.tau + phase
                self.key_rot(self.sh[0], f, 3 * math.sin(ph), -4)
                self.key_rot(self.sh[1], f, -3 * math.sin(ph), 4)
                f += period // 2

    def walk(self, f0, f1, a, b, stride=8, swing=32, run=False, arms=True):
        """Walk (or run) from a to b between frames f0..f1, facing the travel direction."""
        a, b = Vector(a), Vector(b)
        d = b - a
        yaw = math.degrees(math.atan2(d.x, -d.y))
        self.face_dir(f0, yaw)
        self.move(f0, a)
        self.move(f1, b)
        for fc in self.root.animation_data.action.fcurves if hasattr(self.root.animation_data.action, "fcurves") else []:
            pass
        _linear(self.root, "location")
        if run:
            swing, stride = 55, 6
        f, k = f0, 0
        while f <= f1:
            s = swing * (1 if k % 2 == 0 else -1)
            self.legs(f, s)
            if arms:
                self.key_rot(self.sh[0], f, -s * 0.9)
                self.key_rot(self.sh[1], f, s * 0.9)
            self.body.location.z = 0.12 if run else 0.06
            self.body.keyframe_insert("location", frame=f)
            self.body.location.z = 0.0
            self.body.keyframe_insert("location", frame=f + stride // 2)
            if run:
                self.key_rot(self.body, f, 10)
            f += stride
            k += 1
        self.legs(f1 + 3, 0)
        if run:
            self.key_rot(self.body, f1 + 3, 0)


def _linear(obj, path):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    try:
        curves = ad.action.fcurves
    except AttributeError:
        curves = []
    if not curves:
        # Blender 5 layered actions
        try:
            for layer in ad.action.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        for fc in cb.fcurves:
                            if fc.data_path == path:
                                for kp in fc.keyframe_points:
                                    kp.interpolation = "LINEAR"
            return
        except AttributeError:
            return
    for fc in curves:
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def all_fcurves(obj_or_id):
    ad = getattr(obj_or_id, "animation_data", None)
    if not ad or not ad.action:
        return []
    out = []
    try:
        for layer in ad.action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    out.extend(cb.fcurves)
    except AttributeError:
        out = list(ad.action.fcurves)
    return out


# ----------------------------------------------------------------------------- cast

def hero(loc=(0, 0, 0), rot=0, colored=False):
    c = Char("hero", loc, rot, dict(skin=SKIN, top="#f27ab8", top_knit=True, pants="#ee6fb0", shoes="#6b3418",
                                    sleeve="#f27ab8", cuff="#bfe6f2", hair="#8a4418", hair_style="spiky", suit=True,
                                    face="open"))
    c.colored(colored)
    return c


def mom(loc=(0, 0, 0), rot=0):
    return Char("mom", loc, rot, dict(skin="#f2c48d", top="#ffd23f", pants="#ffd23f", shoes="#8b4f2a",
                                      dress="#ffd23f", hair="#c0392b", hair_style="long", face="open"))


def prism(loc=(0, 0, 0), rot=0, scale=1.12):
    return Char("prism", loc, rot, dict(skin="#e8c090", top="#ffffff", pants="#ffffff", shoes="#ffd700",
                                        rainbow=True, invert=True, hair="#ffffff", hair_style="none",
                                        hat="top", face="open"), scale=scale)


def inspector(name, loc=(0, 0, 0), rot=0):
    return Char(name, loc, rot, dict(skin="#8c8c8c", top="#5d6066", pants="#4a4d52", shoes="#222222",
                                     hair_style="none", helmet=True, coat=True, face="flat", wash=False), scale=1.15)


TOWNS = [  # side-character looks (real colours, shown grey until washed)
    dict(skin="#8d5524", top="#2ecc71", pants="#1f4e8c", hair="#111111", hair_style="curly"),
    dict(skin="#f1c27d", top="#e74c3c", pants="#34495e", hair="#e67e22", hair_style="bun"),
    dict(skin="#ffdbac", top="#3498db", pants="#2c3e50", hair="#f1c40f", hair_style="short"),
    dict(skin="#c68642", top="#9b59b6", pants="#7f8c8d", hair="#2c1b0e", hair_style="cap"),
    dict(skin="#e0ac69", top="#e67e22", pants="#16a085", hair="#d35400", hair_style="long"),
    dict(skin="#ffe0bd", top="#1abc9c", pants="#c0392b", hair="#6d4c41", hair_style="short"),
]


def townie(i, loc=(0, 0, 0), rot=0, scale=1.0, **over):
    look = dict(TOWNS[i % len(TOWNS)]); look.update(over)
    look.setdefault("face", "flat")
    return Char("townie%d" % i, loc, rot, look, scale=scale)


# ----------------------------------------------------------------------------- props & sets

def ground(size=400, color="#8e9196", loc=(0, 0, 0)):
    return box((size, size, 0.2), (loc[0], loc[1], loc[2] - 0.1), mat(color, rough=0.9), name="ground")


def house(x, y, w=10, d=8, h=8, wall="#c8c2b8", roof_c="#9c4a3a", rot=0, door="#6e4b32"):
    root = empty("house", (x, y, 0))
    root.rotation_euler.z = math.radians(rot)
    box((w, d, h), (0, 0, h / 2), mat(wall, rough=0.85), root, name="wall")
    roof(w + 1.0, d + 1.0, h * 0.45, (0, 0, h), mat(roof_c, rough=0.7), root)
    box((2.2, 0.3, 3.6), (0, -d / 2 - 0.1, 1.8), mat(door, rough=0.6), root, name="door")
    wm = mat("#3c4a5a", rough=0.15, metal=0.2)
    fm = mat("#f2f2f2")
    for wx in (-w / 2 + 2.2, w / 2 - 2.2):
        box((2.0, 0.3, 2.0), (wx, -d / 2 - 0.1, h * 0.55), wm, root, name="window")
        box((2.4, 0.2, 0.25), (wx, -d / 2 - 0.15, h * 0.55 - 1.1), fm, root, name="sill")
    return root


def lamp(x, y, h=9):
    m = mat("#3d3f43", rough=0.5)
    cyl(0.2, h, (x, y, h / 2), m)
    box((1.4, 0.6, 0.3), (x + 0.5, y, h), m)
    return sphere(0.35, (x + 0.9, y, h - 0.35), mat("#fff3c4", emit=1.5))


def tree(x, y, s=1.0, leaf="#3f8f3a"):
    cyl(0.5 * s, 4 * s, (x, y, 2 * s), mat("#6b4a2b"))
    box((4.5 * s, 4.5 * s, 4.5 * s), (x, y, 6 * s), mat(leaf, rough=0.9), bevel=0.4 * s)
    box((3 * s, 3 * s, 3 * s), (x + 0.5 * s, y - 0.4 * s, 8.5 * s), mat(leaf, rough=0.9), bevel=0.3 * s)


def street(length=200, y0=0, wall_cols=None):
    """A grey street running along X: road, sidewalks, houses on the far side, lamps."""
    box((length, 14, 0.1), (0, y0, 0.0), mat("#55585d", rough=0.9), name="road")
    for x in range(-int(length / 2), int(length / 2), 8):
        box((4, 0.4, 0.12), (x, y0, 0.03), mat("#d8d8d8"), name="dash")
    box((length, 6, 0.5), (0, y0 + 10, 0.25), mat("#a0a3a8"), name="walk")
    box((length, 6, 0.5), (0, y0 - 10, 0.25), mat("#a0a3a8"), name="walk")
    walls = wall_cols or ["#e8d5b5", "#b5d3e8", "#e8b5c8", "#c8e8b5", "#e8e1b5", "#d1b5e8"]
    roofs = ["#a33b2f", "#2f5ea3", "#3f8a3a", "#7a3fa3", "#a36b2f", "#2f8a8a"]
    for i, x in enumerate(range(-int(length / 2) + 8, int(length / 2), 16)):
        house(x, y0 + 19, w=11, d=9, h=7 + (i * 37 % 4), wall=walls[i % len(walls)], roof_c=roofs[i * 5 % len(roofs)])
    for x in range(-int(length / 2) + 4, int(length / 2), 20):
        lamp(x, y0 + 7.8)
        lamp(x + 10, y0 - 7.8)


def dome(r=260, center=(0, 0, -20), glass=False):
    """The Great Umbrella: a glass dome with ribs. Returns (left_half_root, right_half_root)."""
    gm = mat("#cfe3ff", rough=0.05, alpha=0.18, wash=False)
    rm = mat("#9aa6b4", rough=0.35, metal=0.6, wash=False)
    halves = []
    for side in (-1, 1):
        root = empty("domehalf", center)
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
        kill = [v for v in bm.verts if v.co.z < 0 or v.co.x * side < -0.01]
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        if glass:  # transparent glass is ~10x slower to render in software Eevee; ribs alone read as a dome
            o = mesh_obj("glass", bm, gm, root)
            for p in o.data.polygons:
                p.use_smooth = True
        else:
            bm.free()
        # ribs: meridians + rings
        for k in range(0, 13):
            a = math.radians(90 + side * 90 - side * k * 15)  # half circle of meridians
            for j in range(0, 18):
                t0 = math.radians(j * 5); t1 = math.radians((j + 1) * 5)
                p0 = Vector((r * math.cos(t0) * math.cos(a), r * math.cos(t0) * math.sin(a), r * math.sin(t0)))
                p1 = Vector((r * math.cos(t1) * math.cos(a), r * math.cos(t1) * math.sin(a), r * math.sin(t1)))
                _beam(p0, p1, 0.9, rm, root)
        halves.append(root)
    return halves


def _beam(p0, p1, th, m, parent):
    mid = (p0 + p1) / 2
    d = p1 - p0
    o = box((th, th, d.length), mid, m, parent, name="rib")
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return o


def rain(center, size=(30, 30), z=40, rate=4000, f0=1, f1=600, lifetime=40, speed=-55, mesh_scale=1.0, name="rain", z0=0.0):
    """Particle rain: streaks born anywhere inside a box from z0 to z, so it is raining from frame 1.
    rate = streaks per second; each lives `lifetime` frames moving at `speed` units/s."""
    # long axis along X: the particle rotation mode GLOB_Z points the instance's X axis down the Z axis
    drop = box((1.5 * mesh_scale, 0.028 * mesh_scale, 0.028 * mesh_scale), (0, 0, -500), mat("#dfe9f7", emit=0.35, alpha=0.4, wash=False), name="drop")
    em = box((size[0], size[1], z - z0), (center[0], center[1], (z + z0) / 2), None, name=name)
    ps = em.modifiers.new(name, "PARTICLE_SYSTEM").particle_system
    st = ps.settings
    em.show_instancer_for_render = False  # (hiding the emitter object would hide its particles too)
    em.show_instancer_for_viewport = False
    st.count = int(rate * (f1 - f0) / FPS)
    st.frame_start, st.frame_end = f0, f1
    st.emit_from = "VOLUME"
    st.distribution = "RAND"
    st.lifetime = lifetime
    st.normal_factor = 0.0
    st.object_align_factor = (0, 0, speed)
    st.effector_weights.gravity = 0.0
    st.render_type = "OBJECT"
    st.instance_object = drop
    st.particle_size = 1.0
    st.use_rotations = True
    st.rotation_mode = "GLOB_Z"
    st.physics_type = "NEWTON"
    return em


def sparkle_burst(loc, f0, n=14, color="#ffd1ea", spread=3.0):
    """Little glowing cubes that pop out and fade (shrink)."""
    import random
    rnd = random.Random(int(f0 * 7 + loc[0] * 13))
    m = mat(color, emit=4.0, wash=False)
    for i in range(n):
        o = box((0.25, 0.25, 0.25), loc, m, name="spark")
        d = Vector((rnd.uniform(-1, 1), rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 1))).normalized() * spread * rnd.uniform(0.6, 1.2)
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=f0 - 1)
        o.scale = (1,) * 3; o.location = Vector(loc); o.keyframe_insert("scale", frame=f0); o.keyframe_insert("location", frame=f0)
        o.location = Vector(loc) + d; o.rotation_euler = (rnd.random() * 6, rnd.random() * 6, 0)
        o.keyframe_insert("location", frame=f0 + 14); o.keyframe_insert("rotation_euler", frame=f0 + 14)
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=f0 + 20)


# ----------------------------------------------------------------------------- camera

def camera(lens=35, name="Cam"):
    d = bpy.data.cameras.new(name)
    d.lens = lens
    d.clip_end = 2000
    d.sensor_fit = "VERTICAL"
    d.sensor_height = 24
    o = bpy.data.objects.new(name, d)
    _link(o)
    tgt = empty(name + "_tgt", (0, 0, 0))
    c = o.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    bpy.context.scene.camera = o
    o["tgt"] = tgt.name
    return o, tgt


def cam_key(cam, tgt, frame, loc, look, lens=None):
    cam.location = loc
    cam.keyframe_insert("location", frame=frame)
    tgt.location = look
    tgt.keyframe_insert("location", frame=frame)
    if lens:
        cam.data.lens = lens
        cam.data.keyframe_insert("lens", frame=frame)


def shake(cam, f0, f1, amp=0.15, every=2):
    import random
    rnd = random.Random(f0)
    base = cam.location.copy()
    for f in range(f0, f1, every):
        bpy.context.scene.frame_set(f)
        b = cam.location.copy()
        cam.location = b + Vector((rnd.uniform(-amp, amp), rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)))
        cam.keyframe_insert("location", frame=f)
