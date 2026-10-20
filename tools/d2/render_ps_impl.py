import sys, os, textwrap, importlib, subprocess, json
sys.path.insert(0,'/home/claude/obt/layout3'); sys.path.insert(0,'/home/claude/obt/int/tools')
import render_real as RR
from nudge_metrics import cost
import spec
pos,_,t,h=RR.layout_of(spec); BR=spec.BRANCHES
# baseline (without the two focuses), built in a subprocess with OBT_SKIP_IDENTITY=1
code="import sys,json;sys.path.insert(0,'/home/claude/obt/layout3');sys.path.insert(0,'/home/claude/obt/int/tools');import render_real as RR,spec;from nudge_metrics import cost;p,_,t,h=RR.layout_of(spec);print(json.dumps([cost(spec.BRANCHES,p)[1],{k:list(v) for k,v in p.items()}]))"
out=subprocess.run([sys.executable,'-c',code],env=dict(os.environ,OBT_SKIP_IDENTITY='1'),capture_output=True,text=True).stdout.strip().splitlines()[-1]
m0,p0=json.loads(out); m1=cost(BR,pos)[1]
moved=[k for k in p0 if tuple(p0[k])!=tuple(pos[k])]
print('before',m0); print('after',m1); print('existing focuses moved:',moved)
NEW={'TAI_su_dpp_roc_taiwan','TAI_su_dpp_pragmatic_sovereignty'}
F={f['id']:f for b in BR for f in b['focuses']}; A={f['id']:b['key'] for b in BR for f in b['focuses']}
plt=RR.plt
fig=plt.figure(figsize=(24,26),dpi=80)
ax0=fig.add_axes([0.02,0.42,0.96,0.56]); ax1=fig.add_axes([0.02,0.01,0.96,0.39])
RR.draw(ax0,BR,pos,t,h,set(F),f"Whole tree with Pragmatic Sovereignty: {len(F)} focuses, grid {m1['grid']}, red-line crossings {m1['red_crossings']} (before: {m0['red_crossings']}), existing focuses moved: {len(moved)}")
for fid in NEW:
    x,y=pos[fid]; ax0.scatter([x],[y],s=160,marker="s",facecolor="none",edgecolors="black",lw=2,zorder=5)
ids=[i for i in F if A[i]=='dpp']
for fid in ids:
    for q in RR.pre(F[fid]):
        if A.get(q)=='dpp':
            (a,b),(c,d)=pos[q],pos[fid]; new=fid in NEW
            ax1.plot([a,a,c,c],[b,(b+d)/2,(b+d)/2,d],color="#2e86c1" if new else "#9aa4ad",lw=1.8 if new else 1,zorder=1)
for fid in ids:
    x,y=pos[fid]; new=fid in NEW; hl=fid in ('TAI_su_dpp_status_quo','TAI_su_dpp_name_rectification')
    ax1.scatter([x],[y],s=420 if new or hl else 220,marker="s",color="#d6eaf8" if new else ("#e67e22" if hl else "#8e44ad"),edgecolors="black" if new or hl else "none",lw=1.5,zorder=3)
    ax1.text(x,y+0.33,"\n".join(textwrap.wrap(F[fid]['name'],14)),fontsize=9,ha="center",va="top",zorder=4)
xs=[pos[i][0] for i in ids]; ys=[pos[i][1] for i in ids]
ax1.set_xlim(min(xs)-1,max(xs)+1); ax1.set_ylim(max(ys)+1.6,min(ys)-1); ax1.set_aspect(1); ax1.axis("off")
ax1.set_title("DPP branch as generated: the two new focuses in light blue; orange: the exclusive Status Quo / Name Rectification choice",fontsize=13,loc="left",weight="bold")
plt.savefig('/home/claude/obt/d2/ps_implemented_layout.png')
