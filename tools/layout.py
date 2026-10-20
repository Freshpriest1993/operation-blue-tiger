"""Tidy tree layout for the Taiwan focus tree: branches as compact trees, packed in tiers."""
from collections import defaultdict

GAP = 2


def _pre_ids(f):
    for p in f["pre"]:
        for q in (p if isinstance(p, tuple) else (p,)):
            yield q


def branch_layout(b):
    focs = {f["id"]: f for f in b["focuses"]}
    order = {fid: i for i, fid in enumerate(focs)}
    depth = {}

    def d(fid):
        if fid not in depth:
            ps = [q for q in _pre_ids(focs[fid]) if q in focs]
            depth[fid] = max((d(q) + 1 for q in ps), default=0)
        return depth[fid]

    for fid in focs:
        d(fid)
    parent = {}
    children = defaultdict(list)
    for fid, f in focs.items():
        ps = [q for q in _pre_ids(f) if q in focs]
        if ps:
            par = max(ps, key=lambda q: (depth[q], -order[q]))
            parent[fid] = par
            children[par].append(fid)
    for k in children:
        children[k].sort(key=lambda c: order[c])

    def place(fid):
        kids = children[fid]
        y = depth[fid]
        if not kids:
            return {fid: 0}, {y: (0, 0)}
        pos, contour = place(kids[0])
        kid_x = [0]
        for k in kids[1:]:
            kp, kc = place(k)
            shift = max((contour[lv][1] - kc[lv][0] + GAP for lv in kc if lv in contour), default=0)
            for n, x in kp.items():
                pos[n] = x + shift
            for lv, (a, c) in kc.items():
                if lv in contour:
                    contour[lv] = (min(contour[lv][0], a + shift), max(contour[lv][1], c + shift))
                else:
                    contour[lv] = (a + shift, c + shift)
            kid_x.append(shift)
        first, last = pos[kids[0]], pos[kids[-1]]
        px = (first + last) // 2
        pos[fid] = px
        contour[y] = (min(contour.get(y, (px, px))[0], px), max(contour.get(y, (px, px))[1], px))
        return pos, contour

    root = b["focuses"][0]["id"]
    pos, contour = place(root)
    orphans = [fid for fid in focs if fid not in pos]
    assert not orphans, orphans
    taken = {(x, depth[k]) for k, x in pos.items()}
    for fid in focs:
        ps = [q for q in _pre_ids(focs[fid]) if q in focs]
        if len(ps) < 2 or children[fid]:
            continue
        y = depth[fid]
        target = round(sum(pos[q] for q in ps) / len(ps))
        if all((target + dx, y) not in taken for dx in (-1, 0, 1)):
            taken.discard((pos[fid], y))
            pos[fid] = target
            taken.add((target, y))
    for fid, f in focs.items():  # optional fixed placement relative to another focus of the branch
        if "lay_anchor" in f:
            a, dx, dy = f["lay_anchor"]
            spot = (pos[a] + dx, depth[a] + dy)
            assert spot not in {(pos[k], depth[k]) for k in pos if k != fid}, (fid, spot)
            pos[fid], depth[fid] = spot
    mn = min(pos.values())
    pos = {k: v - mn for k, v in pos.items()}
    width = max(pos.values()) + 1
    height = max(depth.values()) + 1
    return {k: (pos[k], depth[k]) for k in pos}, width, height


def _slot_size(lay, part, sgap):
    if isinstance(part, tuple):
        return sum(lay[k][1] for k in part) + sgap * (len(part) - 1), max(lay[k][2] for k in part)
    return lay[part][1], lay[part][2]


def tree_layout(branches, tiers, gap=4, vgap=1, sgap=2, nudge=None):
    """tiers: list of rows, top to bottom. Each row is a list of slots placed left to right, `gap` columns apart.
    A slot is a branch key, or a list stacked top to bottom whose items are a branch key or a tuple of keys
    placed side by side `sgap` columns apart (used to tuck small branches under a shorter one)."""
    lay = {b["key"]: branch_layout(b) for b in branches}
    rows = []
    for row in tiers:
        slots = []
        for s in row:
            parts = s if isinstance(s, list) else [s]
            dims = [_slot_size(lay, p, sgap) for p in parts]
            slots.append((parts, dims, max(d[0] for d in dims), sum(d[1] for d in dims) + vgap * (len(parts) - 1)))
        rows.append(slots)
    widths = [sum(sl[2] for sl in slots) + gap * (len(slots) - 1) for slots in rows]
    total = max(widths)
    positions = {}
    y0 = 0
    for slots, w in zip(rows, widths):
        x0 = (total - w) // 2
        h = 0
        for parts, dims, sw, sh in slots:
            yy = y0
            for part, (pw, ph) in zip(parts, dims):
                xx = x0 + (sw - pw) // 2
                for k in (part if isinstance(part, tuple) else (part,)):
                    p, bw, bh = lay[k]
                    for fid, (x, y) in p.items():
                        positions[fid] = (xx + x, yy + y)
                    xx += bw + sgap
                yy += ph + vgap
            x0 += sw + gap
            h = max(h, sh)
        y0 += h + vgap
    if nudge:
        # Optional per-branch offsets (dx, dy) applied after packing, then normalised to start at 0.
        owner = {f["id"]: b["key"] for b in branches for f in b["focuses"]}
        for fid, (x, y) in list(positions.items()):
            dx, dy = nudge.get(owner[fid], (0, 0))
            positions[fid] = (x + dx, y + dy)
        mx = min(x for x, _ in positions.values())
        my = min(y for _, y in positions.values())
        positions = {k: (x - mx, y - my) for k, (x, y) in positions.items()}
        total = max(x for x, _ in positions.values()) + 1
        y0 = max(y for _, y in positions.values()) + 1
    return positions, {k: (v[1], v[2]) for k, v in lay.items()}, total, y0
