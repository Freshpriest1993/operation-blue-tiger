import sys, textwrap
sys.path.insert(0,'/home/claude/obt/layout3')
from mockd2 import *
from render_real import pre, visible_set
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
BR=with_d2(spec.BRANCHES); pos,_,_,_=positions(BR)
PS='TAI_su_dpp_pragmatic_sovereignty'; auto=pos[PS]; pos=dict(pos); pos[PS]=(5,19)
occ=[k for k,v in pos.items() if v==pos[PS] and k!=PS]; print('auto',auto,'final',pos[PS],'occupied by',occ)
F={f['id']:f for b in BR for f in b['focuses']}; A={f['id']:b['key'] for b in BR for f in b['focuses']}
ids=[i for i in F if A[i]=='dpp']
def segs(p):
    out=[]
    for fid in ids:
        for q in pre(F[fid]):
            if q in F and A[q]=='dpp':
                (a,b),(c,d)=p[q],p[fid]; m=(b+d)/2; out.append(((q,fid),[(a,b),(a,m)],[(a,m),(c,m)],[(c,m),(c,d)]))
    return out
def through(p):
    hits=[]
    for (q,fid),*ss in segs(p):
        for s in ss:
            (x1,y1),(x2,y2)=s
            for o in ids:
                if o in (q,fid): continue
                x,y=p[o]
                if x1==x2==x and min(y1,y2)<y<max(y1,y2): hits.append((q,fid,o))
                if y1==y2==y and min(x1,x2)<x<max(x1,x2): hits.append((q,fid,o))
    return sorted(set(hits))
autop=dict(pos); autop[PS]=auto
print('lines through a focus, automatic spot:',[h for h in through(autop) if PS in h[:2]])
print('lines through a focus, final spot:',[h for h in through(pos) if PS in h[:2]])
def panel(ax,vis,title,hl=()):
    for fid in ids:
        if fid not in vis: continue
        for q in pre(F[fid]):
            if q in vis and A[q]=='dpp':
                (a,b),(c,d)=pos[q],pos[fid]; new=F[fid].get('kind')
                ax.plot([a,a,c,c],[b,(b+d)/2,(b+d)/2,d],color="#2e86c1" if new else "#9aa4ad",lw=1.6 if new else 1,zorder=1)
    for fid in ids:
        x,y=pos[fid]
        if fid not in vis: ax.scatter([x],[y],s=150,marker="s",color="#f0f0f0",edgecolors="#dddddd",zorder=2); continue
        new=F[fid].get('kind'); col="#d6eaf8" if new else ("#e67e22" if fid in hl else "#8e44ad")
        ax.scatter([x],[y],s=300 if new or fid in hl else 150,marker="s",color=col,edgecolors="black" if new or fid in hl else "none",lw=1.5,zorder=3)
        ax.text(x,y+0.32,"\n".join(textwrap.wrap(F[fid]['name'],13)),fontsize=7,ha="center",va="top",zorder=4)
    xs=[pos[i][0] for i in ids]; ys=[pos[i][1] for i in ids]
    ax.set_xlim(min(xs)-1,max(xs)+1); ax.set_ylim(max(ys)+1.5,min(ys)-1); ax.set_aspect(1); ax.axis("off"); ax.set_title(title,fontsize=11,loc="left",weight="bold")
fig,axs=plt.subplots(1,3,figsize=(24,10),dpi=90)
panel(axs[0],set(F),"DPP branch: two new focuses (light blue), Pragmatic Sovereignty on the capstone row",hl=('TAI_su_dpp_status_quo','TAI_su_dpp_name_rectification'))
panel(axs[1],visible_set(BR,{'TAI_su_dpp_name_rectification'},set()),"After Reaffirm the Status Quo (hiding on)")
panel(axs[2],visible_set(BR,{'TAI_su_dpp_status_quo'},set()),"After Name Rectification (hiding on)")
plt.tight_layout(); plt.savefig('/home/claude/obt/d2/ps_final_dpp_positions.png')
