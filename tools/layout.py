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
    mn = min(pos.values())
    pos = {k: v - mn for k, v in pos.items()}
    width = max(pos.values()) + 1
    height = max(depth.values()) + 1
    return {k: (pos[k], depth[k]) for k in pos}, width, height


def tree_layout(branches, tiers):
    """tiers: list of lists of branch keys, top to bottom."""
    lay = {b["key"]: branch_layout(b) for b in branches}
    positions = {}
    y0 = 0
    widths = []
    for tier in tiers:
        widths.append(sum(lay[k][1] for k in tier) + 4 * (len(tier) - 1))
    total = max(widths)
    for tier, w in zip(tiers, widths):
        x0 = (total - w) // 2
        h = 0
        for k in tier:
            p, bw, bh = lay[k]
            for fid, (x, y) in p.items():
                positions[fid] = (x0 + x, y0 + y)
            x0 += bw + 4
            h = max(h, bh)
        y0 += h + 1
    return positions, {k: (v[1], v[2]) for k, v in lay.items()}, total, y0
