import render_ps_final as R
PS=R.PS; ids=R.ids
def path_pts(a,b,c,d,m):
    pts=set()
    for y in [b+i*0.5 for i in range(int((m-b)*2)+1)]: pts.add((a,y))
    for x in range(min(a,c),max(a,c)+1): pts.add((x,m))
    for y in [m+i*0.5 for i in range(int((d-m)*2)+1)]: pts.add((c,y))
    return pts
def hits(p,model):
    out=set()
    for q in R.pre(R.F[PS]):
        (a,b),(c,d)=p[q],p[PS]
        m=(b+d)/2 if model=='mid' else d-0.5
        P=path_pts(a,b,c,d,m)
        for o in ids:
            if o in (q,PS): continue
            if tuple(p[o]) in P: out.add(o)
    return sorted(out)
taken={tuple(v) for k,v in R.pos.items() if k!=PS}
for c in [(6,19),(5,19),(4,19),(11,18),(9,18),(7,19),(6,20),(5,20),(7,20),(9,19),(9,20),(11,19),(11,20),(12,18),(12,19)]:
    if c in taken: print(c,'occupied'); continue
    p=dict(R.pos); p[PS]=c; print(c,'mid:',hits(p,'mid'),'near-child:',hits(p,'near'))
