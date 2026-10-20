import render_ps_final as R
pos=dict(R.pos); PS=R.PS; ids=R.ids
xs=[pos[i][0] for i in ids if i!=PS]; ys=[pos[i][1] for i in ids if i!=PS]
taken={pos[i] for i in R.pos if i!=PS}
res=[]
for x in range(min(xs)-1,max(xs)+2):
    for y in range(pos['TAI_su_dpp_roc_taiwan'][1]+1,max(ys)+3):
        if (x,y) in taken: continue
        p=dict(pos); p[PS]=(x,y)
        h=[t for t in R.through(p) if PS in t[:2]]
        # line length to parents
        L=sum(abs(p[q][0]-x)+abs(p[q][1]-y) for q in R.pre(R.F[PS]))
        inside = min(xs)<=x<=max(xs) and y<=max(ys)
        res.append((len(h),not inside,L,(x,y),[t[2] for t in h]))
for r in sorted(res)[:8]: print(r)
print('dpp box',min(xs),min(ys),max(xs),max(ys))
