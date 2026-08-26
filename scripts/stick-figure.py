#!/usr/bin/env python3
"""3D stick-figure generator.

Everything is computed in 3D (x, y, z); projection to screen happens only
at draw time.  Six orthographic projections are available (default: side).
--export-3mf additionally writes a 3MF of the 3D wireframe (capped tube
mesh + head/hand spheres), structure matching the official lib3MF writer.

Orthographic projections (screen_x, screen_y):
  side   (right):  x, y        -- figure's right side facing viewer
  left:  -x, y     -- figure's left side facing viewer
  front:  z, y     -- figure faces right across the screen
  back:  -z, y     -- figure faces left across the screen
  top:    z, -x    -- looking down; figure faces up/away, right side right
  bottom: -z, x    -- looking up; figure faces down/toward, right side left

3D conventions:
  x = forward (screen right), y = down (SVG), z = toward the viewer.
  The figure faces +x, so its RIGHT side = +z = NEAR, left side = -z = FAR.

Coordinate frames (every point is specified relative to another piece of
the model, never as a plain absolute coordinate):
  ground  origin: the FRONT foot's ankle, declared in the pose file
          (0, 0, 0); y = 0 at ground level.  Foot points, knees and hips
          live here.
  spine    origin: the base of the spine (the hip center).  Hip points, the
          shoulder base, the shoulder points, the neck and the head live here.
  shoulder  origin: each shoulder.  That arm's hand and elbow live here; the
          sword's points live relative to the right hand (its grip).  The
          hand's z is addressed from the shoulder; a 4th element (a = true)
          addresses it from the body centerline (the shoulder base's z)
          instead.

Construction (the feet drive everything):
  1. Feet: the pose declares the front foot; its ankle is the ground-frame
     origin (0, 0, 0) at ground level.  The only foot input is the back
     foot's ground level ("feet": {"back_y": ...}, 0 = level ground); the
     back foot's x is computed in forward stance and the whole back foot in
     hanmi.  The toe is FOOT px ahead of the ankle along the foot direction.
  2. Stance ("hanmi" default, or "forward") sets the defaults:
        forward: hips level AND even (both hips share x and y; only z
                 differs; the back hip sits one hip-width away in z), both
                 feet point straight forward.  The front leg places the hip:
                 the knee sits "front_knee_offset" (default 7px) along the
                 foot from the heel, straight up the shin; the thigh leaves
                 the knee 45 deg (default, "front_thigh_angle") below
                 horizontal, up-and-back.  The hip is fully derived -- it is
                 NOT centered over the stride.  The back foot's x is
                 COMPUTED from the hip and the back leg (5 deg bend default,
                 knee in front of the foot); only the back foot's ground
                 level comes from the input.
        hanmi:   hips rotated 45 deg about the vertical axis (the forward
                 hip sits on the forward foot's side), front foot 0 deg,
                 back foot 45 deg out.  The front leg derives the hip
                 exactly as in the forward stance (knee offset + thigh
                 angle from horizontal).  The back foot is then COMPUTED:
                 behind the back hip by the back leg's span (15 deg bend
                 default), on the front foot's ground, at the side z one
                 hip-width from the front foot.  The deviation of the hip
                 center from being equidistant from both feet is printed
                 after calculation.
      Overrides: "hip_rot", per-foot "foot_rot", per-leg "knee_bend".
  3. Knees: two-circle IK (thigh/shin); the pick direction defaults to the
     foot direction, "knee_dir" overrides per knee.
  4. Spine, neck and head go straight up from the hip center (the base of
     the spine): the shoulder base is TORSO above it, the neck NECK above
     the shoulder base, the head center HEAD_R above that.
  5. The shoulders rotate by the same angle as the hips.
  6. One hand is given as [x, y], [x, y, z] or [x, y, z, a] relative to the
     shoulder on the same side; z is from the shoulder by default (0 = the
     shoulder's depth), or from the body centerline when a is true (the
     forward-stance grip sits on the centerline: [x, y, 0, true]).  The
     other hand is derived from the sword (or both must be given without a
     sword).
  7. Sword: fixed parts tsuka 45 / tsuba 11 / blade 115.  The fist
     (r 7.5) touches the back edge of the tsuba with its center on the
     sword axis; the left hand sits halfway between the right hand and
     the tsuka end.  Both distances are computed once from the parts and
     stored (RH_TO_KISSAKI, RH_TO_LHAND).
  8. Sword input: "angle_from_horizontal" (required; positive = up) and
     "angle_from_center" (default 0): an azimuth about the vertical axis
     measured from straight forward (+x); positive swings toward the
     viewer (+z).
  9. Elbows: two-sphere IK (upper arm about the shoulder, forearm about
      the hand); the solutions form a circle in 3D.  Take the point on that
      circle whose shoulder->elbow direction is closest to a supplied
      vector (default straight down); "elbow_dir" overrides per elbow.
  10. No stretching: a hand beyond arm reach (110px) or a foot beyond leg
     reach (160px) is a hard error -- no SVG is written.

Proportions (px; head = 40):
  head r 20, neck 20 (gap head->shoulders), torso 120
  shoulder width 80 (z +/-40), hip width 60 (z +/-30)
  upper arm 60, forearm 50
  open hand: oval 20 long x 5 wide; closed hand: filled dot 15 (r7.5)
  thigh 80, shin 80, foot 30 (side view, 0.75 head)
  sword: tsuka 45, tsuba 11, blade 115
  limb stroke 5, blade stroke 4, color #222

Depth shading: in a right-side view the near side (right, +z) and middle
(z=0: torso, head, neck, sword) draw black #222; the far side (left, -z:
left arm & leg) draws medium gray #888.

Pose JSON:
{
  "stance": "hanmi" | "forward",        # default "hanmi"
  "front_foot": "right" | "left",       # required; its ankle is (0, 0, 0),
                                        # y = 0 at ground level
  "feet": {"back_y": -2},              # optional: the back foot's ground
                                        # level relative to the front ankle
                                        # (0 = level ground; the only foot
                                        # input)
  "hip_rot": 45,                          # optional, degrees
  "foot_rot": {"left": 45},               # optional, per foot, degrees
  "knee_bend": {"left": 5},                # optional, per leg, degrees
                                                # (back leg in forward; both in hanmi)
  "front_knee_offset": 7,                    # optional, px along the foot
  "front_thigh_angle": 45,                     # optional, deg from horizontal
  "knee_dir": {"right": [1, 0, 0]},        # optional, per knee pick vector
  "hands": {"right": [x, y, z?, a?]} or {"left": [x, y, z?, a?]},
                                                # RELATIVE TO THE SHOULDER ON
                                                # THE SAME SIDE; z optional
                                                # (0 = the shoulder's depth);
                                                # a (default false) addresses
                                                # z from the body centerline
  "sword": {"angle_from_horizontal": 20,    # required with a sword
            "angle_from_center": 0},
  "elbow_dir": {"left": [0, 1, 0]},         # optional, per elbow: direction
                                              # the shoulder->elbow vector
                                              # should approach
  "hand_style": {"right": "closed"},          # optional: open | closed
  "hand_dir": {"right": -20}                  # optional open-hand angle (degrees)
}
"""

import argparse
import io
import json
import math
import sys
import zipfile

# ----------------------------------------------------------------- constants

HEAD = 40.0
HEAD_R = HEAD / 2                 # 20
NECK = HEAD * 0.5                 # 20 (space between head and shoulders)
TORSO = 120.0                     # shoulder center -> hip center
SHOULDER_HALF = HEAD * 2 / 2       # 40
HIP_HALF = HEAD * 1.5 / 2          # 30
UPPER_ARM = HEAD * 1.5             # 60
FOREARM = HEAD * 1.25              # 50
HAND_OPEN_L = HEAD * 0.5           # 20 (oval length)
HAND_OPEN_W = HAND_OPEN_L / 4      # 5 (oval width)
HAND_CLOSED_R = HEAD * 0.375 / 2   # 7.5
THIGH = HEAD * 2                   # 80
SHIN = HEAD * 2                    # 80
FOOT = HEAD * 0.75                 # 30 (side view)
TSUKA = 45.0
TSUBA = 11.0
BLADE = 115.0
ARM_REACH = UPPER_ARM + FOREARM    # 110
LEG_REACH = THIGH + SHIN           # 160
LIMB_W = 5.0
BLADE_W = 4.0
COLOR = "#222"        # near & middle (right side & center)
FAR_COLOR = "#888"       # medium gray: far side (left) limbs
DOWN = (0.0, 1.0, 0.0)

# Sword grip, computed once from the parts.  The fist (r HAND_CLOSED_R)
# touches the back edge of the tsuba with its center on the sword axis;
# the tsuka runs back from the tsuba; the left hand sits halfway between
# the right hand and the tsuka end.  All values are distances along the
# axis, measured from the right hand.
TSUBA_REAR = HAND_CLOSED_R                   # -> tsuba back edge   7.5
TSUKA_END = TSUBA_REAR - TSUKA                # -> tsuka end        -37.5
RH_TO_KISSAKI = TSUBA_REAR + TSUBA + BLADE     # -> kissaki          133.5
RH_TO_LHAND = TSUKA_END / 2                     # -> left hand         -18.75

# ----------------------------------------------------------------- vectors

def v3(p, default_z=0.0):
    p = list(p)
    if len(p) == 2:
        p.append(default_z)
    return (float(p[0]), float(p[1]), float(p[2]))

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def scl(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def length(a): return math.sqrt(dot(a, a))
def norm(a):
    l = length(a)
    if l < 1e-9:
        return (0.0, 0.0, 0.0)
    return scl(a, 1.0/l)

def rot_y(v, a):
    """Rotate about the vertical (y) axis."""
    c, s = math.cos(a), math.sin(a)
    return (v[0]*c + v[2]*s, v[1], -v[0]*s + v[2]*c)

def side_z(side, half):
    return half if side == "right" else -half

# ----------------------------------------------------------------- IK

class PoseError(Exception):
    pass

def two_circle(a, b, l1, l2, plane_dir, pick):
    """The joint j with |a-j|=l1, |j-b|=l2, in the plane spanned by (b-a)
    and plane_dir.  pick(j1, j2) chooses between the two solutions."""
    d = sub(b, a)
    D = length(d)
    if D > l1 + l2 + 1e-6 or D < abs(l1 - l2) - 1e-6:
        raise PoseError(f"two-circle IK out of range: {D:.1f}px vs "
                        f"{l1:.0f}+{l2:.0f}")
    ax = (l1*l1 - l2*l2 + D*D) / (2*D)
    h = math.sqrt(max(l1*l1 - ax*ax, 0.0))
    mid = add(a, scl(d, ax/D))
    dhat = scl(d, 1.0/D)
    u = sub(plane_dir, scl(dhat, dot(plane_dir, dhat)))
    if length(u) < 1e-6:            # degenerate: d parallel to plane_dir
        u = (1.0, 0.0, 0.0) if abs(dhat[1]) > 0.9 else (0.0, 1.0, 0.0)
        u = sub(u, scl(dhat, dot(u, dhat)))
    u = norm(u)
    return pick(add(mid, scl(u, h)), sub(mid, scl(u, h)))

def two_sphere(a, b, l1, l2, pick_dir):
    """The joint j with |a-j|=l1, |j-b|=l2, in full 3D.  The solutions are
    the circle where the two spheres intersect; return the point on it whose
    a->j direction is closest to pick_dir (largest dot)."""
    d = sub(b, a)
    D = length(d)
    if D > l1 + l2 + 1e-6 or D < abs(l1 - l2) - 1e-6:
        raise PoseError(f"two-sphere IK out of range: {D:.1f}px vs "
                        f"{l1:.0f}+{l2:.0f}")
    ax = (l1*l1 - l2*l2 + D*D) / (2*D)
    h = math.sqrt(max(l1*l1 - ax*ax, 0.0))
    dhat = scl(d, 1.0/D)
    mid = add(a, scl(dhat, ax))
    v = norm(pick_dir)
    w = sub(v, scl(dhat, dot(v, dhat)))      # pick_dir on the circle plane
    if length(w) < 1e-6:                     # pick_dir || a->b: all points tie
        w = (1.0, 0.0, 0.0) if abs(dhat[1]) > 0.9 else (0.0, 1.0, 0.0)
        w = sub(w, scl(dhat, dot(w, dhat)))
    return add(mid, scl(norm(w), h))

def dir_pick(anchor, vec):
    """pick(j1, j2): the candidate whose anchor->candidate direction is
    closest (largest dot) to vec."""
    v = norm(vec)
    def pick(j1, j2):
        s1 = dot(norm(sub(j1, anchor)), v)
        s2 = dot(norm(sub(j2, anchor)), v)
        return j1 if s1 >= s2 else j2
    return pick

# ----------------------------------------------------------------- build

def build(cfg):
    """Pose dict -> (skeleton in the ground frame, diagnostics lines)."""
    stance = cfg.get("stance", "hanmi")
    if stance not in ("forward", "hanmi"):
        raise PoseError(f'stance must be "forward" or "hanmi" (got {stance!r})')
    front = cfg.get("front_foot")
    if front not in ("right", "left"):
        raise PoseError('pose must declare "front_foot": "right" or "left"')
    back = "left" if front == "right" else "right"
    back_y = float(cfg.get("feet", {}).get("back_y", 0.0))

    # ground frame: origin at the front ankle, y = 0 at ground level
    feet = {front: (0.0, 0.0, 0.0)}
    back_z = side_z(back, HIP_HALF) - side_z(front, HIP_HALF)   # +/- 60

    hip_def = (45.0 if front == "right" else -45.0) if stance == "hanmi" else 0.0
    hip_rot = math.radians(float(cfg.get("hip_rot", hip_def)))
    u_hip = rot_y((0.0, 0.0, 1.0), hip_rot)

    foot_def = {"right": 0.0, "left": 0.0}
    if stance == "hanmi":
        foot_def[back] = 45.0 if back == "left" else -45.0
    foot_rot = {s: math.radians(float(cfg.get("foot_rot", {}).get(s, foot_def[s])))
               for s in ("right", "left")}
    foot_dir = {s: rot_y((1.0, 0.0, 0.0), foot_rot[s]) for s in ("right", "left")}

    # The front bend is not an input in either stance: it falls out of the
    # knee offset + thigh angle.  knee_bend sets the BACK leg (5 deg forward,
    # 15 deg hanmi).
    bend_def = {"forward": (None, 5.0), "hanmi": (None, 15.0)}[stance]
    knee_bend = {}
    for s, d in ((front, bend_def[0]), (back, bend_def[1])):
        if d is not None:
            knee_bend[s] = math.radians(
                float(cfg.get("knee_bend", {}).get(s, d)))

    off = float(cfg.get("front_knee_offset", 7.0))
    th = math.radians(float(cfg.get("front_thigh_angle", 45.0)))
    if off >= SHIN - 1e-9:
        raise PoseError(f"front_knee_offset {off:.1f}px >= shin {SHIN:.0f}px")

    def front_leg(af, fd):
        """Knee `off` px along the foot from the heel, straight up the shin;
        hip up-and-back from the knee `th` below horizontal.  Both stances
        use this to place the front leg's hip."""
        knee = (af[0] + off*fd[0], af[1] - math.sqrt(SHIN*SHIN - off*off),
               af[2] + off*fd[2])
        hip = (knee[0] - THIGH*math.cos(th)*fd[0],
              knee[1] - THIGH*math.sin(th),
              knee[2] - THIGH*math.cos(th)*fd[2])
        return knee, hip

    diag = [f"stance={stance} front={front} hip_rot={math.degrees(hip_rot):.1f}"]
    deviation = None

    def bend_of(s):
        c = length(sub(hi[s], feet[s])) / LEG_REACH
        return math.degrees(2.0*math.acos(max(-1.0, min(1.0, c))))

    af = (0.0, 0.0, 0.0)
    knee_f, hi_f = front_leg(af, foot_dir[front])
    if stance == "forward":
        # The front leg places the hip.  The back hip shares its x and y and
        # sits one hip-width away in z; the back foot's x is then COMPUTED
        # from the hip and the back leg (its ground level is the only input
        # part).
        hip_b = (hi_f[0], hi_f[1], back_z)
        dy = back_y - hip_b[1]
        chord_b = LEG_REACH * math.cos(knee_bend[back] / 2.0)
        h2 = chord_b*chord_b - dy*dy
        if h2 < 0:
            raise PoseError(f"{back} leg out of reach: hip is {dy:.1f}px "
                           f"above the {back} ankle, leg spans {chord_b:.1f}px")
        fdb = norm((foot_dir[back][0], 0.0, foot_dir[back][2]))
        feet[back] = (hip_b[0] - math.sqrt(h2)*fdb[0], back_y,
                     hip_b[2] - math.sqrt(h2)*fdb[2])
    else:  # hanmi
        # The front leg derives the hip exactly as in the forward stance
        # (knee offset + thigh angle).  The back foot is then COMPUTED:
        # behind the back hip by the back leg's span, on the front foot's
        # ground, at the side z one hip-width from the front foot.  The
        # deviation of the hip center from being equidistant from both feet
        # is printed.
        chord_f = length(sub(hi_f, af))
        if chord_f > LEG_REACH + 1e-6:
            raise PoseError(f"front leg stretched: hip is {chord_f:.1f}px "
                           f"from the {front} ankle, leg spans "
                           f"{LEG_REACH:.0f}px")
        sg = 1.0 if front == "right" else -1.0
        hip_b = sub(hi_f, scl(u_hip, 2.0*HIP_HALF*sg))
        dy = af[1] - hip_b[1]
        dz = back_z - hip_b[2]
        chord_b = LEG_REACH * math.cos(knee_bend[back] / 2.0)
        h2 = chord_b*chord_b - dy*dy - dz*dz
        if h2 < 0:
            raise PoseError(f"{back} leg out of reach: hip is "
                           f"{math.hypot(dy, dz):.1f}px from the {back} "
                           f"ankle in height/depth, leg spans {chord_b:.1f}px")
        feet[back] = (hip_b[0] - math.sqrt(h2), af[1], back_z)
    hi = {front: hi_f, back: hip_b}
    kn = {front: knee_f,
          back: two_circle(hi[back], feet[back], THIGH, SHIN, DOWN,
                         dir_pick(hi[back], cfg.get("knee_dir", {}).get(
                             back, foot_dir[back])))}
    if stance == "forward":
        diag.append(f"legs: {front} bend {bend_of(front):.1f} deg "
                   f"(thigh {math.degrees(th):.1f} deg from horizontal, "
                   f"knee offset {off:.1f}px), {back} bend "
                   f"{bend_of(back):.1f} deg (set "
                   f"{math.degrees(knee_bend[back]):.1f}), back foot x "
                   f"computed {feet[back][0]:.1f}")
    else:
        C = tuple(sum(hi[s][i] for s in ("right", "left"))/2.0
                for i in range(3))
        d_f, d_b = length(sub(C, af)), length(sub(C, feet[back]))
        deviation = d_f - d_b
        diag.append(f"equidistant: front {d_f:.1f} vs back {d_b:.1f} "
                   f"(deviation {abs(deviation):.1f} px)")
        diag.append(f"legs: {front} bend {bend_of(front):.1f} deg "
                   f"(thigh {math.degrees(th):.1f} deg from horizontal, "
                   f"knee offset {off:.1f}px), {back} bend "
                   f"{bend_of(back):.1f} deg (set "
                   f"{math.degrees(knee_bend[back]):.1f}), back heel x "
                   f"computed {feet[back][0]:.1f}")

    # spine frame: origin at the base of the spine (the hip center)
    hi_c = (sum(hi[s][i] for s in ("right", "left"))/2.0 for i in range(3))
    hi_c = tuple(hi_c)
    sh_c = (hi_c[0], hi_c[1] - TORSO, hi_c[2])
    head = (sh_c[0], sh_c[1] - (HEAD_R + NECK), sh_c[2])
    neck = (head[0], head[1] + HEAD_R, head[2])
    sh = {"right": add(sh_c, scl(u_hip, SHOULDER_HALF)),
          "left":  sub(sh_c, scl(u_hip, SHOULDER_HALF))}

    # ---- hands + sword (hands are specified relative to their shoulder)
    def hand_point(shoulder, spec):
        """[x, y, z?, a?] from the shoulder.  z is addressed from the
        shoulder (default; 0 = the shoulder's depth); when a is true it is
        addressed from the body centerline (the shoulder base's z) instead."""
        p = list(spec)
        center = bool(p[3]) if len(p) > 3 else False
        x, y, z = v3(p[:3], 0.0)
        if center:
            z = sh_c[2] + z - shoulder[2]
        return add(shoulder, (x, y, z))

    hands_in = cfg.get("hands", {})
    sword = None
    if "sword" in cfg:
        sw = cfg["sword"]
        if "angle_from_horizontal" not in sw:
            raise PoseError('sword needs "angle_from_horizontal"')
        e = math.radians(float(sw["angle_from_horizontal"]))
        a = math.radians(float(sw.get("angle_from_center", 0.0)))
        axis = rot_y((math.cos(e), -math.sin(e), 0.0), -a)
        if "right" in hands_in:
            rh = hand_point(sh["right"], hands_in["right"])
            lh = add(rh, scl(axis, RH_TO_LHAND))
        elif "left" in hands_in:
            lh = hand_point(sh["left"], hands_in["left"])
            rh = add(lh, scl(axis, -RH_TO_LHAND))
        else:
            raise PoseError("a sword pose needs one of hands.right / hands.left")
        sword = dict(axis=axis,
                    tsuba=add(rh, scl(axis, TSUBA_REAR + TSUBA/2.0)),
                    tsuka_end=add(rh, scl(axis, TSUKA_END)),
                    kissaki=add(rh, scl(axis, RH_TO_KISSAKI)))
    else:
        for s in ("right", "left"):
            if s not in hands_in:
                raise PoseError(f"missing {s} hand (no sword to derive it from)")
        rh = hand_point(sh["right"], hands_in["right"])
        lh = hand_point(sh["left"], hands_in["left"])
    hands = {"right": rh, "left": lh}

    # ---- elbows (shoulder frame)
    elbows = {}
    for s in ("right", "left"):
        h, shp = hands[s], sh[s]
        D = length(sub(h, shp))
        if D > ARM_REACH + 1e-6:
            raise PoseError(f"{s} hand is {D:.1f}px from the {s} shoulder; "
                            f"arm reach is {ARM_REACH:.0f}px (no stretching)")
        vec = v3(cfg.get("elbow_dir", {}).get(s, DOWN))
        elbows[s] = two_sphere(shp, h, UPPER_ARM, FOREARM, vec)
    diag.append("arm reach: " + ", ".join(
        f"{s} {length(sub(hands[s], sh[s])):.1f}/{ARM_REACH:.0f}"
        for s in ("right", "left")))

    # ---- build trace: every computed point in its own frame
    P = lambda p: f"({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f})"
    tr = [f"== ground (origin: {front} ankle, y 0 at ground) =="]
    tr.append(f"{front} ankle {P((0.0, 0.0, 0.0))}")
    tr.append(f"{back} ankle (computed) {P(feet[back])}")
    for s in ("right", "left"):
        tr.append(f"{s} toe {P(add(feet[s], scl(foot_dir[s], FOOT)))}")
    for s in ("right", "left"):
        tr.append(f"{s} knee {P(kn[s])}")
    for s in ("right", "left"):
        tr.append(f"{s} hip {P(hi[s])}")
    tr.append(f"hip center {P(hi_c)}")
    tr.append("== spine (origin: hip center) ==")
    for s in ("right", "left"):
        tr.append(f"{s} hip {P(sub(hi[s], hi_c))}")
    tr.append(f"shoulder base {P(sub(sh_c, hi_c))}")
    for s in ("right", "left"):
        tr.append(f"{s} shoulder {P(sub(sh[s], hi_c))}")
    tr.append(f"neck {P(sub(neck, hi_c))}")
    tr.append(f"head {P(sub(head, hi_c))}")
    for s in ("right", "left"):
        tr.append(f"== {s} shoulder ==")
        tag = "" if s in hands_in else " (computed)"
        tr.append(f"hand{tag} {P(sub(hands[s], sh[s]))}")
        tr.append(f"elbow {P(sub(elbows[s], sh[s]))}")
    if sword:
        tr.append("== sword (origin: right hand) ==")
        for name in ("tsuba", "tsuka_end", "kissaki"):
            tr.append(f"{name.replace('_', ' ')} {P(sub(sword[name], rh))}")
    for line in tr:
        print(line, file=sys.stderr)

    sk = dict(head=head, neck=neck, sh_c=sh_c, hi_c=hi_c, sh=sh, hi=hi,
              u_hip=u_hip, hands=hands, elbows=elbows, front=front, back=back)
    for s in ("right", "left"):
        sk[s + "_knee"] = kn[s]
        sk[s + "_ankle"] = feet[s]
        sk[s + "_footdir"] = foot_dir[s]
    if sword:
        sk["sword"] = sword
    return sk, diag

# ----------------------------------------------------------------- svg

class Canvas:
    def __init__(self):
        self.items = []   # (depth, rank, svg_text, bounds_points)
                          # depth = 3rd component of projected point

    def add(self, depth, rank, text, pts):
        self.items.append((depth, rank, text, pts))

    def poly(self, depth, rank, pts3, cls):
        pts = [f"{p[0]:.1f},{p[1]:.1f}" for p in pts3]
        return self.add(depth, rank,
                        f'<polyline points="{" ".join(pts)}" class="{cls}"/>',
                        pts3)

    def line(self, depth, rank, a, b, cls):
        return self.add(depth, rank,
            f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" '
            f'y2="{b[1]:.1f}" class="{cls}"/>', [a, b])

    def dot(self, depth, rank, c, r, cls):
        return self.add(depth, rank,
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" class="{cls}"/>',
            [(c[0]-r, c[1]-r), (c[0]+r, c[1]+r)])

    def oval(self, depth, rank, c, rx, ry, ang_deg, cls):
        return self.add(depth, rank,
            f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'transform="rotate({ang_deg:.1f} {c[0]:.1f} {c[1]:.1f})" class="{cls}"/>',
            [(c[0]-rx, c[1]-rx), (c[0]+rx, c[1]+rx)])

# Projection functions: each returns (screen_x, screen_y, depth_value)
# depth_value is used for z-sorting (draw far parts first).
# For side/front/back views depth = z (horizontal depth).
# For top view depth = -y (higher y = closer to viewer = draws first in asc sort).
# For bottom view depth = y (lower y = farther = draws first in asc sort).

def proj_side(p):   # right side view: x → right, y → down
    return (p[0], p[1], p[2])

def proj_left(p):   # left side view: -x → right, y → down
    return (-p[0], p[1], -p[2])

def proj_front(p):  # front view: z → right, y → down
    return (p[2], p[1], p[0])

def proj_back(p):   # back view: -z → right, y → down
    return (-p[2], p[1], -p[0])

def proj_top(p):    # top view: z → right, -x → down; depth = -y (higher y = closer)
    return (p[2], -p[0], -p[1])

def proj_bottom(p): # bottom view: -z → right, x → down; depth = y (lower y = farther)
    return (-p[2], p[0], p[1])

PROJECTIONS = {
    "side": proj_side,
    "left": proj_left,
    "front": proj_front,
    "back": proj_back,
    "top": proj_top,
    "bottom": proj_bottom,
}

def project(p, proj_fn, skew):
    sx, sy, sz = proj_fn(p)
    # Skew applies only to side views (adds depth along screen_x)
    if proj_fn in (proj_side, proj_left):
        sx = sx + skew * sz
    return (sx, sy, sz)

# ----------------------------------------------------------------- 3MF export

BEAM_LATTICE_NS = "urn:three-mesh-bfx:beamlattice:1.0.0"
DEFAULT_RADIUS = 2.0

# Skeleton connections: (label_a, label_b) — flattened keys into the skeleton dict
# Nested dicts use dot notation: "hi.right" -> sk["hi"]["right"]
BEAM_CONNECTIONS = [
    # legs
    ("right_ankle", "right_knee"),
    ("left_ankle", "left_knee"),
    ("right_knee", "hi.right"),
    ("left_knee", "hi.left"),
    # torso
    ("hi.right", "hi.left"),
    ("hi.right", "sh_c"),
    ("hi.left", "sh_c"),
    ("sh_c", "neck"),
    ("neck", "head"),
    # shoulders
    ("sh.right", "sh.left"),
    ("sh.right", "sh_c"),
    ("sh.left", "sh_c"),
    # arms
    ("sh.right", "elbows.right"),
    ("elbows.right", "hands.right"),
    ("sh.left", "elbows.left"),
    ("elbows.left", "hands.left"),
    # sword (if present)
]

def _f3(p):
    return (round(p[0], 3), round(p[1], 3), round(p[2], 3))

def _cylinder_vertices(ax, ay, az, bx, by, bz, r, segments=12):
    """Generate (vertices, indices) for a cylinder from (ax,ay,az) to (bx,by,bz)."""
    dx, dy, dz = bx - ax, by - ay, bz - az
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length < 1e-9:
        return [], []
    ux, uy, uz = dx/length, dy/length, dz/length
    # Build orthonormal basis
    if abs(ux) < 0.9:
        cx, cy, cz = 1.0, 0.0, 0.0
    else:
        cx, cy, cz = 0.0, 1.0, 0.0
    ex = cy*uz - cz*uy
    ey = cz*ux - cx*uz
    ez = cx*uy - cy*ux
    el = math.sqrt(ex*ex + ey*ey + ez*ez) or 1.0
    ex, ey, ez = ex/el, ey/el, ez/el
    fx = ey*uz - ez*uy
    fy = ez*ux - ex*uz
    fz = ex*uy - ey*ux
    verts = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        ca, sa = math.cos(a), math.sin(a)
        nx = ex*ca + fx*sa
        ny = ey*ca + fy*sa
        nz = ez*ca + fz*sa
        verts.append((ax + nx*r, ay + ny*r, az + nz*r))
        verts.append((bx + nx*r, by + ny*r, bz + nz*r))
    ca_idx, cb_idx = 2*segments, 2*segments+1
    verts.append((ax, ay, az))   # start cap center
    verts.append((bx, by, bz))   # end cap center
    idx = []
    for i in range(segments):
        a, b, c, d = i*2, i*2+1, ((i+1)%segments)*2, ((i+1)%segments)*2+1
        idx += [a, c, b, b, c, d]           # side, outward after Z-up transform
        idx += [ca_idx, c, a]                # start cap (faces -u)
        idx += [cb_idx, b, d]                 # end cap (faces +u)
    return verts, idx

def _tsuba_disk(ax, ay, az, bx, by, bz, r=10.5, thick=3.0):
    """Thin square disk at point A, perpendicular to AB, for the tsuba guard.

    4 corners x 2 faces + 4 sides x 2 triangles = 16 triangles total.
    All windings verified for outward-facing normals.
    """
    dx, dy, dz = bx - ax, by - ay, bz - az
    L = math.sqrt(dx*dx + dy*dy + dz*dz)
    if L < 1e-9:
        return [], []
    ux, uy, uz = dx/L, dy/L, dz/L
    if abs(ux) < 0.9:
        cx, cy, cz = 1.0, 0.0, 0.0
    else:
        cx, cy, cz = 0.0, 1.0, 0.0
    ex = cy*uz - cz*uy
    ey = cz*ux - cx*uz
    ez = cx*uy - cy*ux
    el = math.sqrt(ex*ex + ey*ey + ez*ez) or 1.0
    ex, ey, ez = ex/el, ey/el, ez/el
    fx = ey*uz - ez*uy
    fy = ez*ux - ex*uz
    fz = ex*uy - ey*ux
    h = thick / 2.0

    verts = []
    idx = []

    cr = r * 0.7071  # cos(45)
    corners = [
        (cr*ex + cr*fx, cr*ey + cr*fy, cr*ez + cr*fz),
        (-cr*ex + cr*fx, -cr*ey + cr*fy, -cr*ez + cr*fz),
        (-cr*ex - cr*fx, -cr*ey - cr*fy, -cr*ez - cr*fz),
        (cr*ex - cr*fx, cr*ey - cr*fy, cr*ez - cr*fz),
    ]

    # Front face (+u): corners offset by +h*u
    for cxv, cyv, czv in corners:
        verts.append((ax + cxv + h*ux, ay + cyv + h*uy, az + czv + h*uz))
    # Back face (-u): SAME corners offset by -h*u (pure translation, so the
    # two squares are parallel and the side quads are planar parallelograms)
    for cxv, cyv, czv in corners:
        verts.append((ax + cxv - h*ux, ay + cyv - h*uy, az + czv - h*uz))

    # Front: [0,2,3], [0,1,3]  Back: [4,7,6], [4,6,5]
    # Sides (quad F_i, F_{i+1}, B_{i+1}, B_i), reversed for outward normals:
    idx += [0, 2, 3, 0, 1, 3]       # front
    idx += [4, 7, 6, 4, 6, 5]       # back
    idx += [0, 4, 1, 1, 4, 5]       # side 0->1 (outward: +f)
    idx += [1, 5, 2, 2, 5, 6]       # side 1->2 (outward: -e)
    idx += [2, 6, 3, 3, 6, 7]       # side 2->3 (outward: -f)
    idx += [3, 7, 0, 0, 7, 4]       # side 3->0 (outward: +e)

    return verts, idx

def _sphere_vertices(cx, cy, cz, r, segments=12, rings=8):
    """UV sphere in skeleton space; outward-facing after the Z-up transform."""
    top = (cx, cy - r, cz)
    bottom = (cx, cy + r, cz)
    ring_verts = []
    for i in range(1, rings):
        phi = math.pi * i / rings
        ring = []
        for j in range(segments):
            th = 2.0 * math.pi * j / segments
            ring.append((cx + r*math.sin(phi)*math.cos(th),
                        cy - r*math.cos(phi),
                        cz + r*math.sin(phi)*math.sin(th)))
        ring_verts.append(ring)
    verts = [top, bottom]
    for ring in ring_verts:
        verts.extend(ring)
    def ri(i, j): return 2 + i*segments + j
    idx = []
    for j in range(segments):
        idx += [0, ri(0, (j+1) % segments), ri(0, j)]           # top fan
    for i in range(len(ring_verts) - 1):
        for j in range(segments):
            a, b = ri(i, j), ri(i, (j+1) % segments)
            c, d = ri(i+1, j), ri(i+1, (j+1) % segments)
            idx += [a, b, c, b, d, c]
    last = len(ring_verts) - 1
    for j in range(segments):
        idx += [1, ri(last, j), ri(last, (j+1) % segments)]           # bottom fan
    return verts, idx

def export_3mf(sk, radius=DEFAULT_RADIUS):
    """Build a valid 3MF ZIP with actual cylinder mesh geometry for the wireframe."""
    # Flatten nested skeleton keys for lookup
    flat = {}
    for k, v in sk.items():
        if isinstance(v, dict):
            for sk2, v2 in v.items():
                if isinstance(v2, (list, tuple)) and len(v2) == 3:
                    flat[f"{k}.{sk2}"] = v2
        elif isinstance(v, (list, tuple)) and len(v) == 3:
            flat[k] = v

    # Collect all points
    points = {}
    for a, b in BEAM_CONNECTIONS:
        if a in flat and a not in points:
            points[a] = _f3(flat[a])
        if b in flat and b not in points:
            points[b] = _f3(flat[b])
    sword_keys = [k for k in flat if k.startswith("sword.")]
    if sword_keys:
        for key in ("sword.tsuba", "sword.kissaki", "sword.tsuka_end"):
            if key in flat and key not in points:
                points[key] = _f3(flat[key])

    # Build all beam segments with radii
    beam_specs = []
    for a, b in BEAM_CONNECTIONS:
        if a in points and b in points:
            beam_specs.append((points[a], points[b], radius))
    for s in ("right", "left"):           # feet: ankle -> toe
        key = s + "_ankle"
        if key in points:
            toe = _f3(add(points[key], scl(sk[s + "_footdir"], FOOT)))
            beam_specs.append((points[key], toe, radius))
    tsuba_disk = False
    if sword_keys:
        for a, b in [("sword.tsuka_end", "sword.tsuba"), ("sword.tsuba", "sword.kissaki")]:
            if a in points and b in points:
                beam_specs.append((points[a], points[b], radius * 0.8))
        tsuba_disk = True

    # Spheres: head and hands
    sphere_specs = [(_f3(sk["head"]), HEAD_R)]
    for s in ("right", "left"):
        r = HAND_CLOSED_R if sk_style(sk, s) == "closed" else HAND_OPEN_L / 2
        sphere_specs.append((_f3(sk["hands"][s]), r))

    # Generate mesh (beam cylinders + spheres)
    all_verts = []
    all_idx = []
    vert_offset = 0
    for pa, pb, r in beam_specs:
        verts, idx = _cylinder_vertices(pa[0], pa[1], pa[2], pb[0], pb[1], pb[2], r)
        if verts:
            all_verts.extend(verts)
            all_idx.extend([i + vert_offset for i in idx])
            vert_offset += len(verts)
    if tsuba_disk:
        ta = points["sword.tsuba"]
        te = points.get("sword.tsuka_end") or points.get("sword.kissaki")
        if te:
            dv, di = _tsuba_disk(ta[0], ta[1], ta[2], te[0], te[1], te[2])
            if dv:
                all_verts.extend(dv)
                all_idx.extend([i + vert_offset for i in di])
                vert_offset += len(dv)
    for c, r in sphere_specs:
        verts, idx = _sphere_vertices(c[0], c[1], c[2], r)
        all_verts.extend(verts)
        all_idx.extend([i + vert_offset for i in idx])
        vert_offset += len(verts)

    # Build 3MF (structure matches the official lib3MF writer)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _ct_types())
        zf.writestr("_rels/.rels", _root_rels())
        zf.writestr("3D/3dmodel.model", _model_xml(all_verts, all_idx))
    return buf.getvalue()

def _ct_types():
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '  <Default Extension="jpeg" ContentType="image/jpeg"/>\n'
        '  <Default Extension="jpg" ContentType="image/jpeg"/>\n'
        '  <Default Extension="model" '
        '            ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
        '  <Default Extension="png" ContentType="image/png"/>\n'
        '  <Default Extension="rels" '
        '            ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '  <Default Extension="texture" '
        '            ContentType="application/vnd.ms-package.3dmanufacturing-3dmodeltexture"/>\n'
        '</Types>\n'
    )

def _root_rels():
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" '
        'Target="/3D/3dmodel.model" Id="rel0"/>\n'
        '</Relationships>\n'
    )

def _to_3mf(p):
    """Skeleton (x forward, y down, z toward viewer) -> 3MF right-handed
    (x right, y into screen, z up)."""
    return (p[0], -p[2], -p[1])

def _model_xml(verts, idx):
    v_str = " ".join(
        f'<vertex x="{v[0]:.3f}" y="{v[1]:.3f}" z="{v[2]:.3f}"/>'
        for v in (_to_3mf(v) for v in verts))
    t_str = "\n        ".join(
        f'<triangle v1="{idx[k]}" v2="{idx[k+1]}" v3="{idx[k+2]}"/>'
        for k in range(0, len(idx), 3)
    )
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'unit="millimeter">\n'
        '  <resources>\n'
        '    <basematerials id="1">\n'
        '      <base name="Blue" displaycolor="#0099FF"/>\n'
        '    </basematerials>\n'
        '    <object id="2" type="model" name="skeleton" pid="1" pindex="0">\n'
        '      <mesh>\n'
        '        <vertices>\n'
        f'          {v_str}\n'
        '        </vertices>\n'
        '        <triangles>\n'
        f'          {t_str}\n'
        '        </triangles>\n'
        '      </mesh>\n'
        '    </object>\n'
        '  </resources>\n'
        '  <build>\n'
        '    <item objectid="2"/>\n'
        '  </build>\n'
        '</model>\n'
    )

def render(sk, o):
    cw = Canvas()
    P = lambda p: project(p, o.proj_fn, o.skew)
    hands = sk["hands"]
    hand_dir = sk.get("_hand_dir", {})

    # screen angle of the blade (open hands align with it by default)
    sword_ang = None
    sw = sk.get("sword")
    if sw:
        t0, k0 = P(sw["tsuba"]), P(sw["kissaki"])
        if math.hypot(k0[0]-t0[0], k0[1]-t0[1]) > 1e-6:
            sword_ang = math.degrees(math.atan2(k0[1]-t0[1], k0[0]-t0[0]))

    for s in ("left", "right"):
        z3d = side_z(s, SHOULDER_HALF)
        rank = 0 if s == "left" else 1
        style = sk_style(sk, s)
        el = P(sk["elbows"][s])
        hd = P(hands[s])
        shd = P(sk["sh"][s])
        depth = shd[2]
        far = " far" if z3d < 0 else ""
        if style == "closed":
            # forearm stops at the fist's edge (the wrist side), not its center
            dl = math.hypot(hd[0]-el[0], hd[1]-el[1]) or 1.0
            edge = (hd[0] + (el[0]-hd[0])/dl*HAND_CLOSED_R,
                    hd[1] + (el[1]-hd[1])/dl*HAND_CLOSED_R, hd[2])
            cw.line(depth, rank, shd, el, "limb"+far)
            cw.line(depth, rank, el, edge, "limb"+far)
        else:
            cw.poly(depth, rank, [shd, el, hd], "limb"+far)
        if style == "closed":
            cw.dot(depth, rank+0.5, hd, HAND_CLOSED_R,
                   "fist" + (" farfist" if z3d < 0 else ""))
        else:
            # open hand: oval 20 x 5.  Long axis: per-hand override, else the
            # blade direction, else the forearm direction.  The wrist end of
            # the oval sits at the end of the forearm.
            if s in hand_dir:
                ang = hand_dir[s]
            elif sword_ang is not None:
                ang = sword_ang
            else:
                ref = el
                ang = math.degrees(math.atan2(hd[1]-ref[1], hd[0]-ref[0]))
            a = math.radians(ang)
            c = (hd[0] + math.cos(a)*HAND_OPEN_L/2,
                hd[1] + math.sin(a)*HAND_OPEN_L/2, hd[2])
            cw.oval(depth, rank+0.5, c, HAND_OPEN_L/2, HAND_OPEN_W/2, ang,
                   "limb openhand"+far)

    # neck (head -> shoulders), shoulder/hip bars, then torso
    cw.line(0, 0, P(sk["neck"]), P(sk["sh_c"]), "limb")
    for a, b in ((sk["sh"]["left"], sk["sh"]["right"]),
                (sk["hi"]["left"], sk["hi"]["right"])):
        pa, pb = P(a), P(b)
        if math.hypot(pb[0]-pa[0], pb[1]-pa[1]) > 0.5:
            cw.line(0, 0, pa, pb, "limb")   # visible only under skew
    cw.line(0, 0, P(sk["sh_c"]), P(sk["hi_c"]), "limb")
    cw.dot(0, 1, P(sk["head"]), HEAD_R, "limb head")

    for s in ("left", "right"):
        z3d = side_z(s, HIP_HALF)
        hip = P(sk["hi"][s])
        kn = P(sk[s+"_knee"])
        an = P(sk[s+"_ankle"])
        depth = hip[2]
        far = " far" if s == "left" else ""
        cw.poly(depth, 0, [hip, kn, an], "limb"+far)
        cw.line(depth, 0, an, P(add(sk[s+"_ankle"], scl(sk[s+"_footdir"], FOOT))),
               "limb"+far)

    sw = sk.get("sword")
    if sw:
        ptsuba = P(sw["tsuba"])
        tsuba, kissaki = ptsuba, P(sw["kissaki"])
        tsuka_end = P(sw["tsuka_end"])
        depth = ptsuba[2]
        cw.line(depth, 0, tsuka_end, tsuba, "limb")          # tsuka
        d2 = (kissaki[0]-tsuba[0], kissaki[1]-tsuba[1])
        l2 = math.hypot(*d2) or 1.0
        t = ((-d2[1]/l2)*(TSUBA/2), d2[0]/l2*(TSUBA/2))
        cw.line(depth, 0, (tsuba[0]-t[0], tsuba[1]-t[1], 0),
                      (tsuba[0]+t[0], tsuba[1]+t[1], 0), "limb")   # tsuba
        cw.line(depth, 0, tsuba, kissaki, "blade")

    cw.items.sort(key=lambda it: (it[0], it[1]))
    body = "\n  ".join(it[2] for it in cw.items)

    xs = [p[0] for it in cw.items for p in it[3]]
    ys = [p[1] for it in cw.items for p in it[3]]
    pad = o.pad
    x0, y0 = min(xs)-pad, min(ys)-pad
    w, h = (max(xs)-min(xs)) + 2*pad, (max(ys)-min(ys)) + 2*pad
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" '
           f'width="{w:.0f}" height="{h:.0f}">\n'
           f'  <style>\n'
           f'    .limb {{ stroke: {COLOR}; stroke-width: {LIMB_W}; '
             f'stroke-linecap: round; stroke-linejoin: round; fill: none; }}\n'
             f'    .far {{ stroke: {FAR_COLOR}; }}\n'
             f'    .blade {{ stroke: {COLOR}; stroke-width: {BLADE_W}; '
             f'stroke-linecap: round; }}\n'
             f'    .head {{ fill: #fff; }}\n'
              f'    .openhand {{ fill: #fff; }}\n'
              f'    .fist {{ fill: {COLOR}; }}\n'
              f'    .farfist {{ fill: {FAR_COLOR}; }}\n'
           f'  </style>\n  '
           f"{body}\n</svg>\n")
    return svg

def sk_style(sk, s):
    hs = sk.get("_hand_style", {})
    if s in hs:
        return hs[s]
    return "closed" if "sword" in sk else "open"

# ----------------------------------------------------------------- render-all

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "assets" / "data"
FIG_DIR = ROOT / "assets" / "figures" / "examples"

def build_pose(cfg):
    """cfg (pose dict) -> (skeleton, diagnostics); stashes render extras."""
    hand_style = cfg.pop("hand_style", {})
    sk, diag = build(cfg)
    sk["_hand_style"] = hand_style
    sk["_hand_dir"] = cfg.get("hand_dir", {})
    return sk, diag

def render_all(o):
    files = sorted(DATA_DIR.glob("*.json"))
    if not files:
        sys.exit(f"no pose JSONs in {DATA_DIR}")
    append_view = o.view is not None
    # render-all: default to "side" view (the existing default)
    if o.view is None:
        o.view = "side"
    o.proj_fn = PROJECTIONS[o.view]
    bad = 0
    for f in files:
        try:
            sk, diag = build_pose(json.loads(f.read_text()))
        except Exception as e:      # skip-and-report during JSON migration
            print(f"skip {f.name}: {e}", file=sys.stderr)
            bad += 1
            continue
        for line in diag:
            print(f"{f.stem}: {line}", file=sys.stderr)
        suffix = f"-{o.view}" if append_view else ""
        out = FIG_DIR / (f.stem + suffix + ".svg")
        out.write_text(render(sk, o))
        print(out)
        if o.export_3mf:
            out_3mf = FIG_DIR / (f.stem + suffix + ".3mf")
            out_3mf.write_bytes(export_3mf(sk))
            print(out_3mf)
    return bad

# ----------------------------------------------------------------- dump

def dump_frames(sk):
    """The computed skeleton, nested by coordinate frame."""
    f3 = lambda p: [round(c, 1) for c in p]
    front, back = sk["front"], sk["back"]
    sh, hi, hi_c = sk["sh"], sk["hi"], sk["hi_c"]
    d = {
      "front_foot": front,
      "ground": {
        "origin": f"{front} ankle (y 0 at ground)",
        front + "_ankle": [0.0, 0.0, 0.0],
        back + "_ankle": f3(sk[back + "_ankle"]),
        "right_toe": f3(add(sk["right_ankle"], scl(sk["right_footdir"], FOOT))),
        "left_toe": f3(add(sk["left_ankle"], scl(sk["left_footdir"], FOOT))),
        "right_knee": f3(sk["right_knee"]),
        "left_knee": f3(sk["left_knee"]),
        "right_hip": f3(hi["right"]),
        "left_hip": f3(hi["left"]),
        "hip_center": f3(hi_c),
      },
      "spine": {
        "origin": "hip center (base of spine)",
        "right_hip": f3(sub(hi["right"], hi_c)),
        "left_hip": f3(sub(hi["left"], hi_c)),
        "shoulder_base": f3(sub(sk["sh_c"], hi_c)),
        "right_shoulder": f3(sub(sh["right"], hi_c)),
        "left_shoulder": f3(sub(sh["left"], hi_c)),
        "neck": f3(sub(sk["neck"], hi_c)),
        "head": f3(sub(sk["head"], hi_c)),
      },
      "right_arm": {
        "origin": "right shoulder",
        "hand": f3(sub(sk["hands"]["right"], sh["right"])),
        "elbow": f3(sub(sk["elbows"]["right"], sh["right"])),
      },
      "left_arm": {
        "origin": "left shoulder",
        "hand": f3(sub(sk["hands"]["left"], sh["left"])),
        "elbow": f3(sub(sk["elbows"]["left"], sh["left"])),
      },
    }
    if "sword" in sk:
        rh, sw = sk["hands"]["right"], sk["sword"]
        d["right_arm"]["sword"] = {
          "origin": "right hand",
          "tsuba": f3(sub(sw["tsuba"], rh)),
          "tsuka_end": f3(sub(sw["tsuka_end"], rh)),
          "kissaki": f3(sub(sw["kissaki"], rh))}
    return d

# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pose", nargs="?", help="pose JSON file, or - for stdin")
    ap.add_argument("-o", "--out", help="output SVG file")
    ap.add_argument("--pad", type=float, default=20.0, help="viewBox padding")
    ap.add_argument("--skew", type=float, default=0.0,
                    help="depth skew, side views only: screen_x = base + skew*z")
    ap.add_argument("--view",
                    choices=["side", "left", "front", "back", "top", "bottom"],
                    default=None,
                    help="orthographic projection (default: side if --skew, else front)")
    ap.add_argument("--dump", action="store_true", help="print computed skeleton")
    ap.add_argument("--render-all", action="store_true",
                   help="render every assets/data/*.json into assets/figures/examples/")
    ap.add_argument("--export-3mf", action="store_true",
                   help="export 3D wireframe as 3MF with Beam Lattice Extension")
    o = ap.parse_args()

    if o.render_all:
        sys.exit(1 if render_all(o) else 0)

    # Resolve view: --skew implies "side"; default to "front" otherwise
    if o.view is None:
        o.view = "side" if o.skew != 0.0 else "front"
    o.proj_fn = PROJECTIONS[o.view]

    if not o.pose:
        ap.error("pose JSON required (or --render-all)")
    raw = sys.stdin.read() if o.pose == "-" else open(o.pose).read()
    label = "-" if o.pose == "-" else Path(o.pose).stem
    try:
        sk, diag = build_pose(json.loads(raw))
    except (PoseError, json.JSONDecodeError, KeyError, TypeError) as e:
        sys.exit(f"error: {e}")
    for line in diag:
        print(f"{label}: {line}", file=sys.stderr)

    svg = render(sk, o)
    if o.out:
        if o.export_3mf:
            out_3mf = Path(o.out).with_suffix(".3mf")
            data = export_3mf(sk)
            with open(out_3mf, "wb") as f:
                f.write(data)
            print(out_3mf)
        with open(o.out, "w") as f:
            f.write(svg)
        print(o.out)
    else:
        sys.stdout.write(svg)
    if o.export_3mf and not o.out:
        data = export_3mf(sk)
        label = "-" if o.pose == "-" else Path(o.pose).stem
        out_3mf = Path(label + ".3mf")
        with open(out_3mf, "wb") as f:
            f.write(data)
        print(out_3mf)
    if o.dump:
        print(json.dumps(dump_frames(sk), indent=1))

if __name__ == "__main__":
    main()
