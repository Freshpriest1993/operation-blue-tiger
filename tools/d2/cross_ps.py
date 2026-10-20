import render_ps_final as R
PS=R.PS
def cr(p):
    S=R.segs(p); mine=[s for s in S if s[0][1]==PS]; other=[s for s in S if s[0][1]!=PS]
    n=0
    for _,*a in mine:
        for k,*b in other:
            for (p1,p2) in a:
                for (q1,q2) in b:
                    h1=p1[1]==p2[1]; h2=q1[1]==q2[1]
                    if h1==h2: continue
                    H,V=((p1,p2),(q1,q2)) if h1 else ((q1,q2),(p1,p2))
                    y=H[0][1]; x=V[0][0]
                    if min(H[0][0],H[1][0])<x<max(H[0][0],H[1][0]) and min(V[0][1],V[1][1])<y<max(V[0][1],V[1][1]): n+=1
    return n
for c in [(8,18),(9,18),(11,18),(6,19),(5,19),(4,19)]:
    p=dict(R.pos); p[PS]=c
    print(c,'through-focus',[t[2] for t in R.through(p) if PS in t[:2]],'crossings',cr(p))
