#!/usr/bin/env python3
"""Choose per-branch offsets (BRANCH_NUDGE) for the section layout.

Starts from sections_spec.TIERS packed by layout.tree_layout, then moves whole branches (left/right, and
up/down for non-party branches; the five party branches move up/down together) to reduce the length of
lines between branches and the number of crossings, without overlapping branches, keeping one empty
column and one empty row between them, and keeping every branch on the same side of its neighbours.
Writes nudge.json next to this file.

Usage (from the tools directory):  OBT_SKIP_SECTIONS=1 python3 -B sections/optimize_layout.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
os.environ["OBT_SKIP_SECTIONS"] = "1"
import spec  # noqa: E402
import layout  # noqa: E402
import sections_spec as SS  # noqa: E402

PARTY = {"kmt", "pfp", "dpp", "tsu", "gpt"}


def pre(f):
    for p in f["pre"]:
        for q in (p if isinstance(p, tuple) else (p,)):
            yield q


def cost(BR, pos):
    A = {f["id"]: b["key"] for b in BR for f in b["focuses"]}
    red, segs, lens = [], [], []
    for b in BR:
        for f in b["focuses"]:
            for q in pre(f):
                (x1, y1), (x2, y2) = pos[q], pos[f["id"]]
                ym = (y1 + y2) / 2
                s = [((x1, y1), (x1, ym)), ((x1, ym), (x2, ym)), ((x2, ym), (x2, y2))]
                segs += s
                if A[q] != b["key"]:
                    red += s
                    lens.append(abs(x1 - x2) + abs(y1 - y2))

    def inter(a, c):
        (ax1, ay1), (ax2, ay2) = a
        (bx1, by1), (bx2, by2) = c
        if ax1 == ax2 and by1 == by2:
            return min(bx1, bx2) < ax1 < max(bx1, bx2) and min(ay1, ay2) < by1 < max(ay1, ay2)
        if ay1 == ay2 and bx1 == bx2:
            return inter(c, a)
        return False
    n = sum(1 for r in red for s in segs if inter(r, s))
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    score = sum(lens) + 5 * n + 2 * max(lens) + 3 * max(0, w - 88) + 3 * max(0, h - 41)
    return score, dict(cross_len=sum(lens), max_len=max(lens), red_crossings=n, grid=f"{w}x{h}")


def boxes(BR, pos):
    out = {}
    for b in BR:
        xs = [pos[f["id"]][0] for f in b["focuses"]]
        ys = [pos[f["id"]][1] for f in b["focuses"]]
        out[b["key"]] = [min(xs), min(ys), max(xs), max(ys)]
    return out


def overlaps(a, b, gx=2, gy=2):
    return not (a[2] + gx <= b[0] or b[2] + gx <= a[0] or a[3] + gy <= b[1] or b[3] + gy <= a[1])


def allowed(bx, group, dx, dy):
    nb = {k: [bx[k][0] + dx, bx[k][1] + dy, bx[k][2] + dx, bx[k][3] + dy] for k in group}
    for k in group:
        if nb[k][1] < 0:
            return False
        for o in bx:
            if o in group:
                continue
            if overlaps(nb[k], bx[o]):
                return False
            v_old = not (bx[o][3] < bx[k][1] or bx[k][3] < bx[o][1])
            v_new = not (bx[o][3] < nb[k][1] or nb[k][3] < bx[o][1])
            if v_old and v_new and (bx[k][0] < bx[o][0]) != (nb[k][0] < bx[o][0]):
                return False
            h_new = not (bx[o][2] < nb[k][0] or nb[k][2] < bx[o][0])
            if h_new and (bx[k][1] < bx[o][1]) != (nb[k][1] < bx[o][1]):
                return False
    return True


def main():
    class _S:
        BRANCHES = copy.deepcopy(spec.BRANCHES)
    SS.split_national_army(_S)
    BR = _S.BRANCHES
    pos, _, _, _ = layout.tree_layout(BR, SS.TIERS, gap=3, vgap=2)
    members = {b["key"]: [f["id"] for f in b["focuses"]] for b in BR}
    groups = {(k,): [(dx, 0) for dx in range(-10, 11) if dx] for k in members}
    for k in members:
        if k not in PARTY:
            groups[(k,)] += [(dx, dy) for dx in range(-6, 7) for dy in range(-3, 4) if dy]
    groups[tuple(sorted(PARTY))] = [(0, dy) for dy in range(-4, 5) if dy]
    nudge = {k: [0, 0] for k in members}
    best, _ = cost(BR, pos)
    for _ in range(6):
        improved = False
        for g, opts in groups.items():
            bx = boxes(BR, pos)
            cand = None
            for dx, dy in opts:
                if not allowed(bx, g, dx, dy):
                    continue
                trial = dict(pos)
                for k in g:
                    for fid in members[k]:
                        trial[fid] = (pos[fid][0] + dx, pos[fid][1] + dy)
                c, _ = cost(BR, trial)
                if c < best - 0.5 and (cand is None or c < cand[0]):
                    cand = (c, dx, dy, trial)
            if cand:
                best, dx, dy, pos = cand
                improved = True
                for k in g:
                    nudge[k][0] += dx
                    nudge[k][1] += dy
        if not improved:
            break
    print(cost(BR, pos)[1])
    with open(os.path.join(HERE, "nudge.json"), "w", encoding="utf-8") as fh:
        json.dump({k: v for k, v in nudge.items() if v != [0, 0]}, fh, indent=1)


if __name__ == "__main__":
    main()
