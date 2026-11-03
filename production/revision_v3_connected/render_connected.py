"""V3 connected edit: distinct v2 action plates + two generated handoffs + local lineage.

python render_connected.py --prepare --stills   # available plates and honest partial stills
python render_connected.py --render            # requires both handoffs and approved audio
No generation APIs, speech processing, music, or native audio reuse.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, shutil, subprocess, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
PRODUCTION=ROOT.parent
W,H,FPS,S=1280,720,24,2
WHITE='#EDF6FC'; CYAN='#6DDCF5'; GOLD='#EAC381'; MUTED='#B3C9D9'; NAVY='#061323'
FONTS={False:'C:/Windows/Fonts/segoeui.ttf', True:'C:/Windows/Fonts/seguisb.ttf'}
FONT_CACHE={}; TEXT_AUDIT={}
PLATES=[
 ('foundation',0,6,'revision_v2/film/clean/shot3.mp4',2,8),
 ('enterprise_difference',6,18,'revision_v2/film/clean/shot2.mp4',1,13),
 ('business_review_and_knowledge',18,26,'revision_v2/film/clean/shot4.mp4',0,6),
 ('knowledge_to_method',26,32,None,None,None),
 ('compose_the_skill',32,39,'revision_v2/film_refined/clean/shot5.mp4',4,11),
 ('skill_to_run_to_trace',39,47,None,None,None),
 ('observe_the_run',47,54,'revision_v2/film_refined/clean/shot6.mp4',1,8),
 ('diagnose_test_validate_return',54,65,'revision_v2/film_refined/clean/shot7.mp4',0,11),
 ('shared_capability_close',65,70,'revision_v2/film_refined/clean/shot7.mp4',11,15),
]

def binary(n):
    found=list((PRODUCTION/'tools').rglob(n+'.exe'))
    return str(found[0]) if found else shutil.which(n) or n

def probe(p):
    return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(p)],encoding='utf-8'))

def ff(args, log):
    with (ROOT/(log+'.log')).open('w',encoding='utf-8') as f:
        r=subprocess.run([binary('ffmpeg'),'-hide_banner','-loglevel','error','-y',*map(str,args)],stderr=f)
    if r.returncode: raise RuntimeError((ROOT/(log+'.log')).read_text(encoding='utf-8'))

def font(size,bold=False):
    key=(size,bold)
    if key not in FONT_CACHE: FONT_CACHE[key]=ImageFont.truetype(FONTS[bold],round(size*S))
    return FONT_CACHE[key]

def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)

def rgba(hex_,a=255):return (*bytes.fromhex(hex_.lstrip('#')),a)

def bezier(a,b,c,p):
    return ((1-p)**2*a[0]+2*(1-p)*p*b[0]+p*p*c[0],(1-p)**2*a[1]+2*(1-p)*p*b[1]+p*p*c[1])

class Layer:
    def __init__(self):self.im=Image.new('RGBA',(W*S,H*S));self.d=ImageDraw.Draw(self.im)
    def text(self,x,y,s,size=24,color=WHITE,bold=False,anchor='la',width=1160):
        f=font(size,bold);box=self.d.textbbox((x*S,y*S),s,font=f,anchor=anchor)
        ok=box[0]>=0 and box[1]>=0 and box[2]<=W*S and box[3]<=H*S and box[2]-box[0]<=width*S
        TEXT_AUDIT[(s,x,y,size,anchor)]={'text':s,'box':[round(z/S,2) for z in box],'size':size,'fits':ok}
        if not ok:raise ValueError(f'Text exceeds bounds: {s}')
        self.d.text(((x+1)*S,(y+1.2)*S),s,font=f,fill=(0,7,18,145),anchor=anchor)
        self.d.text((x*S,y*S),s,font=f,fill=color,anchor=anchor)
    def line(self,pts,color=CYAN,w=2):self.d.line([(round(x*S),round(y*S)) for x,y in pts],fill=color,width=max(1,round(w*S)),joint='curve')
    def dot(self,x,y,r,color):self.d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=color)
    def box(self,x,y,w,h,fill=None,outline=None,r=8,stroke=1):self.d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),r*S,fill=fill,outline=outline,width=max(1,round(stroke*S)))
    def check(self,x,y,color=GOLD):self.line([(x-7,y),(x-1,y+6),(x+11,y-10)],color,2.7)
    def role(self,x,y,scale=1):
        # Same business-team identity appears at curation and the question/run action.
        self.dot(x,y,27*scale,rgba(NAVY,235));self.d.ellipse(((x-27*scale)*S,(y-27*scale)*S,(x+27*scale)*S,(y+27*scale)*S),outline=CYAN,width=round(1.4*S))
        for dx,dy,r in [(0,-7,5),(-12,0,3.8),(12,0,3.8)]:
            self.dot(x+dx*scale,y+dy*scale,r*scale,CYAN)
            self.line([(x+(dx-6)*scale,y+(dy+15)*scale),(x+(dx-5)*scale,y+(dy+8)*scale),(x+(dx+5)*scale,y+(dy+8)*scale),(x+(dx+6)*scale,y+(dy+15)*scale)],WHITE,1.6)
    def cursor(self,x,y,color=WHITE):
        pts=[(x,y),(x+1,y+24),(x+8,y+17),(x+15,y+28),(x+20,y+25),(x+13,y+14),(x+24,y+13)]
        self.d.polygon([(a*S,b*S) for a,b in pts],fill=color,outline='#183149')
    def sprite(self,name,x,y,w,alpha=1):
        src=SPRITES[name];h=w*src.height/src.width
        key=(name,round(w*S))
        if key not in SPRITE_CACHE:SPRITE_CACHE[key]=src.resize((round(w*S),round(h*S)),Image.Resampling.LANCZOS)
        im=SPRITE_CACHE[key]
        if alpha<1:
            im=im.copy();im.putalpha(im.getchannel('A').point(lambda a:round(a*max(0,alpha))))
        self.im.alpha_composite(im,(round((x-w/2)*S),round((y-h/2)*S)))

SPRITES={};SPRITE_CACHE={}

def extract_frame(source,t,target):
    if not target.exists():ff(['-ss',t,'-i',source,'-frames:v',1,target],target.stem+'_extract')

def assets():
    specs=[('knowledge_source','revision_v2/film/clean/shot4.mp4',1),('skill_source','revision_v2/film_refined/clean/shot5.mp4',6.2),('aof_source','revision_v2/film_refined/clean/shot6.mp4',7.5),('platform_return_source','revision_v2/film_refined/clean/shot7.mp4',12.5),('agent_workspace_source','revision_v2/film_refined/clean/shot5.mp4',10.2)]
    for name,path,t in specs:extract_frame(PRODUCTION/path,t,ROOT/'assets'/(name+'.png'))
    def crop(name,source,box,poly=None,radius=0):
        im=Image.open(ROOT/'assets'/(source+'.png')).convert('RGBA');part=im.crop(box)
        mask=Image.new('L',part.size);d=ImageDraw.Draw(mask)
        if poly:d.polygon([(x-box[0],y-box[1]) for x,y in poly],fill=255)
        else:d.rounded_rectangle((0,0,part.width-1,part.height-1),radius,fill=255)
        part.putalpha(mask.filter(ImageFilter.GaussianBlur(.6)));part.save(ROOT/'assets'/(name+'.png'));SPRITES[name]=part
    crop('definition','knowledge_source',(145,165,416,553),[(150,194),(330,169),(382,213),(411,529),(165,548)])
    crop('skill','skill_source',(284,315,997,652),radius=8)
    crop('query_evidence','aof_source',(680,62,801,288),radius=9)
    crop('question','aof_source',(269,154,355,250),radius=7)
    crop('library','platform_return_source',(883,402,1190,612),[(894,495),(1073,409),(1181,453),(992,607)])
    crop('workspace','agent_workspace_source',(897,248,1175,660),[(898,252),(1115,250),(1117,566),(1171,602),(1168,654),(902,654)])
    (ROOT/'assets/extraction_notes.json').write_text(json.dumps({'source':'Original v2 frames; polygon masks selected after full-size visual inspection','definition':'Bookmarked business document','skill':'Same comparison/segmentation/test folder, used again only as an updated method instance','query_evidence':'Original AOF database/query icon and amber quality check','business_role':'Same local business-team illustration and cursor at review and agent use'},indent=2),encoding='utf-8')

def top(l,title=None,sub=None,contrast=False):
    for y in range(210 if contrast else 160):
        a=round(220*(1-max(0,(y-115)/95))) if contrast else round(180*max(0,1-y/160)**1.5)
        l.line([(0,y),(W,y)],(2,10,22,max(0,a)),1)
    l.text(48,22,'INSIGHTGEN  /  BLUE ORBIT',18,CYAN,True)
    if title:l.text(48,61,title,37,WHITE,True)
    if sub:l.text(50,112,sub,23,MUTED)

def compact(l,caption):
    # Keep execution quality checks and source nodes visible near the top edge.
    for y in range(70):l.line([(0,y),(W,y)],(2,10,22,round(175*max(0,1-y/70))),1)
    l.text(48,19,caption,25,WHITE,True,width=885)
    l.text(1230,23,'INSIGHTGEN / BLUE ORBIT',16,CYAN,True,'ra',270)

def bottom(l,caption,color=WHITE,size=27):
    for y in range(600,720):l.line([(0,y),(W,y)],(2,10,22,round(190*(y-600)/120)),1)
    l.text(640,651,caption,size,color,True,'ma',1170)

def opening_overlay(t):
    l=Layer();top(l)
    if .8<=t<4.8:
        l.text(48,66,'InsightGen',51,WHITE,True)
        l.text(50,128,'An evidence-backed business investigation',26,MUTED)
    if 4.8<=t<12.7:
        l.text(48,65,'Today’s demo',34,WHITE,True)
        # The moving report becomes pale behind the lower agenda near 11s.
        # An optical scrim keeps both rows readable throughout that camera move.
        for y in range(520,720):
            l.line([(0,y),(W,y)],(2,10,22,round(220*ease((y-520)/62))),1)
        l.text(640,571,'01  InsightGen in action',32,WHITE,True,'ma')
        if t>=6.0:l.text(640,622,'02  How we make it work at Amex',32,WHITE,True,'ma')
    return l.im.resize((W,H),Image.Resampling.LANCZOS)

def under_overlay(t):
    l=Layer()
    if t<6:
        top(l,'How we make it work at Amex','The shared enterprise foundation behind this investigation')
        bottom(l,'Blue Orbit  /  Shared foundation · Specialized agents')
    elif t<18:
        top(l,'Our differentiator: the enterprise system','Business-owned knowledge, expert methods, controlled access and a learning loop',contrast=True)
        for x,label,sub in [(320,'GENERAL-PURPOSE CAPABILITY','Reasoning + tools'),(960,'BLUE ORBIT ENTERPRISE SYSTEM','Business-owned · Reusable · Traceable')]:
            l.box(x-278,157,556,72,rgba(NAVY,225),None,7)
            l.text(x,165,label,22,WHITE,True,'ma',530);l.text(x,196,sub,20,MUTED,False,'ma',530)
        bottom(l,'Connect expertise and evidence into a reusable operating system',GOLD,26)
    elif t<26:
        top(l,'Business teams curate expertise','Enterprise Knowledge Foundation  /  Definitions · Policies · Context')
        l.role(1132,100);l.text(1090,141,'Business teams',18,CYAN,True,'ma',260)
        u=t-18
        steps=['Select the definition','Review the policy context','Publish governed knowledge']
        step=0 if u<2.3 else 1 if u<4.7 else 2
        bottom(l,steps[step],GOLD,28)
        if u<4.7:
            # Selection and review happen while the source documents still have stable positions.
            if u<2.3:
                l.line([(151,195),(330,169),(382,213),(411,529),(165,548),(151,195)],GOLD,2)
                x,y=bezier((1090,130),(720,160),(278,280),ease((u-.3)/1.3));l.cursor(x,y)
                if u>1.4:l.dot(280,280,8+4*math.sin(u*8),rgba(GOLD,110))
            else:
                x,y=bezier((280,280),(690,180),(995,250),ease((u-2.3)/1.2));l.cursor(x,y)
                l.dot(1030,224,17,rgba(NAVY,230));l.check(1030,224)
        else:
            p=ease((u-4.7)/3.0);x,y=bezier((280,350),(420,200),(630,260),p)
            l.line([(245,380),(x,y)],GOLD,2);l.sprite('definition',x,y,100+20*(1-p))
            if p>.65:
                l.box(450,155,117,59,rgba(NAVY,230),rgba(GOLD,170),6)
                l.text(460,158,'C-60',20,GOLD,True,width=100)
                l.text(460,184,'Definition',18,WHITE,True,width=100)
                l.line([(567,203),(x-30,y-15)],GOLD,1.3)
            l.check(1118,99)
    elif t<32:
        compact(l,'Enterprise Knowledge Foundation → Skill Foundry')
        l.text(49,56,'C-60 definition · Source-linked',19,GOLD,width=430)
        bottom(l,'Ground the method → Compare · Segment · Test',GOLD,26)
    elif t<39:
        compact(l,'Skill Foundry • Compose knowledge-grounded primitives')
        bottom(l,'Compose → Validate → Reuse',GOLD)
    elif t<47:
        compact(l,'InsightGen • Apply the team’s knowledge and skill')
        bottom(l,'Business question → Permitted data → Findings + Execution evidence',WHITE,25)
        if t<42.1:
            l.role(96,156);l.text(140,130,'Business teams',22,CYAN,True,width=260)
            l.box(140,169,248,45,rgba(NAVY,230),CYAN,7);l.text(264,175,'Ask InsightGen',23,WHITE,True,'ma',235)
            p=ease((t-39.3)/.7);l.cursor(400-80*p,223-33*p)
            if t>=40.1:
                p=ease((t-40.1)/1.8);x,y=bezier((385,195),(660,220),(935,300),p)
                l.sprite('question',x,y,37+14*p,1-ease((t-41.8)/.3));l.line([(388,195),(x,y)],CYAN,1.8)
        if 39.5<=t<42.0:
            # Copy this exact three-primitive method from the collection into the
            # selected report. The second leg follows its camera move to center.
            if t<40.15:
                p=ease((t-39.5)/.65)
                x,y=bezier((600,450),(720,535),(920,494),p)
                width=250-30*p
            else:
                p=ease((t-40.15)/1.15)
                x,y=bezier((920,494),(800,548),(640,514),p)
                width=220-35*p
            if t>=41.3:
                p=ease((t-41.3)/.7);x,y=640-24*p,514+7*p
            a=1-ease((t-41.65)/.35)
            l.sprite('skill',x,y,width,a)
            l.box(x-116,y+width*337/713/2+7,232,29,rgba(NAVY,220),None,6)
            l.text(x,y+width*337/713/2+8,'Same governed skill',18,GOLD,True,'ma',225)
            if t>=41.3:l.check(x+width/2-8,y-30,GOLD)
    elif t<54:
        compact(l,'Agent Observability Framework • Capture this run’s evidence')
        bottom(l,'Capture the run → Evaluate quality → Select a review',WHITE,26)
        if t>=50.7:
            l.text(936,488,'Query-method review',22,GOLD,True,'ma',430)
        if t>=51.8:
            p=ease((t-51.8)/2.2)
            x,y=bezier((741,154),(760,650),(1340,430),p)
            l.sprite('query_evidence',x,y,52);l.dot(x,y-61,5,GOLD)
    elif t<65:
        local=t-54
        if local<3:
            compact(l,'AOF → Harness Intelligence • Query-method review')
            p=ease(local/2.8);x,y=bezier((-60,430),(250,170),(680,300),p)
            l.sprite('query_evidence',x,y,52);l.dot(x,y-61,5,GOLD)
            if local>1:l.text(280,487,'Same run evidence',21,GOLD,True,width=300)
        elif local<8.2:
            compact(l,'Harness Intelligence • Test a candidate method change')
            if local>=4.1:
                l.sprite('skill',1068,419,233)
                l.text(1068,327,'Candidate method change',20,GOLD,True,'ma',325)
                l.box(957,375,69,78,None,GOLD,5,1.5)
                l.sprite('query_evidence',969,496,26)
        else:
            compact(l,'Return the validated skill')
            l.text(49,56,'Skill Foundry → Next agent run',20,MUTED,width=550)
        if local<8.2:bottom(l,'Evidence → Candidate change → Tests → Validation',WHITE,26)
    # Return connection persists over the change to the final wider platform plate.
    if 62.2<=t<67.4:
        a=1-ease((t-66.8)/.6)
        l.sprite('library',1075,493,233,a)
        l.text(1075,602,'Skill Foundry library',20,GOLD,True,'ma',350)
        l.sprite('workspace',1100,245,137,a)
        l.text(1100,355,'Next agent run',20,CYAN,True,'ma',280)
        if t<64.5:
            p=ease((t-62.2)/2.1);x,y=bezier((655,556),(800,400),(1065,480),p)
            l.line([(655,556),(800,450),(1065,480)],GOLD,2)
            l.sprite('skill',x,y,170-70*p,a);l.dot(x+70*(1-p),y-34*(1-p),12,GOLD);l.check(x+70*(1-p),y-34*(1-p),NAVY)
            l.text(x,y+55,'Updated skill',20,GOLD,True,'ma',250)
        else:
            l.sprite('skill',1065,480,92,a);l.check(1110,483)
            p=ease((t-64.5)/1.7);x,y=bezier((1065,480),(980,360),(1100,255),p)
            l.line([(1065,480),(1020,370),(1100,255)],GOLD,2)
            l.sprite('skill',x,y,66-24*p,a)
            if t>=66.2:
                l.check(1158,209,CYAN)
                for j in range(3):l.dot(1066+j*24,324,4,CYAN if (t-66.2)*3>j*.2 else rgba(CYAN,70))
    if t>=65:
        top(l)
        if t>=65.15:bottom(l,'Built once. Specialized many times. Improving continuously.',WHITE,29)
    return l.im.resize((W,H),Image.Resampling.LANCZOS)

def source_for(name,path):return ROOT/'raw'/(name+'.mp4') if path is None else PRODUCTION/path

def conform(name,start,end,path,src_start,src_end):
    source=source_for(name,path);target=ROOT/'clean'/(name+'.mp4');duration=end-start
    if not source.exists():return None
    if src_start is None:
        v=next(s for s in probe(source)['streams'] if s['codec_type']=='video');src_start=0;src_end=float(v['duration'])
    factor=duration/(src_end-src_start)
    signature={'source':str(source.resolve()),'mtime_ns':source.stat().st_mtime_ns,'source_range':[src_start,src_end],'target_seconds':duration,'setpts_factor':factor}
    cache=target.with_suffix('.json')
    if not target.exists() or not cache.exists() or json.loads(cache.read_text())!=signature:
        vf=f'trim=start={src_start}:end={src_end},setpts={factor:.12f}*(PTS-STARTPTS),scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2:reset_sar=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x061323,setsar=1,fps=24,format=yuv420p'
        ff(['-i',source,'-vf',vf,'-an','-frames:v',round(duration*FPS),'-c:v','libx264','-preset','medium','-crf',17,'-movflags','+faststart',target],name+'_conform')
        cache.write_text(json.dumps(signature,indent=2),encoding='utf-8')
    return target

def prepare():
    records=[]
    for row in PLATES:
        p=conform(*row);records.append({'id':row[0],'start':row[1],'end':row[2],'ready':p is not None,'file':str(p.relative_to(ROOT)).replace('\\','/') if p else None})
    conform('opening',0,14,'revision_v2/film/clean/shot1.mp4',0,10)
    with (ROOT/'edit/video_timeline.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    return records

def make_stills(records):
    targets=[3,11,20,22.5,25.7,29,35,40.5,41.3,44,50,53.5,54.1,56,59,62.5,64.8,66.5,68.5]
    created=[]
    for t in targets:
        rec=next(r for r in records if r['start']<=t<r['end'])
        if not rec['ready']:continue
        raw=ROOT/'frames'/f'base_{t:05.1f}.png';ff(['-ss',t-rec['start'],'-i',ROOT/rec['file'],'-frames:v',1,raw],f'still_{t}')
        with Image.open(raw) as im:out=Image.alpha_composite(im.convert('RGBA'),under_overlay(t))
        target=ROOT/'frames'/f'under_{t:05.1f}.png';out.convert('RGB').save(target);created.append(target.name)
    for t in [2.5,7,11]:
        raw=ROOT/'frames'/f'opening_base_{t:04.1f}.png';ff(['-ss',t,'-i',ROOT/'clean/opening.mp4','-frames:v',1,raw],f'opening_still_{t}')
        with Image.open(raw) as im:out=Image.alpha_composite(im.convert('RGBA'),opening_overlay(t))
        target=ROOT/'frames'/f'opening_{t:04.1f}.png';out.convert('RGB').save(target)
    (ROOT/'edit/still_review.json').write_text(json.dumps({'partial':not all(r['ready'] for r in records),'rendered_stills':created,'missing_handoffs':[r['id'] for r in records if not r['ready']]},indent=2),encoding='utf-8')
    print(f'{len(created)} honest production stills prepared; missing handoffs are skipped.',flush=True)

def concat(records):
    absent=[r['id'] for r in records if not r['ready']]
    if absent:raise RuntimeError('Cannot render final edit; missing generated handoffs: '+', '.join(absent))
    listing=ROOT/'edit/under_concat.txt'
    listing.write_text('\n'.join("file '"+(ROOT/r['file']).resolve().as_posix()+"'" for r in records)+'\n',encoding='utf-8')
    target=ROOT/'insightgen_v3_connected_underthehood_clean_silent.mp4'
    ff(['-f','concat','-safe',0,'-i',listing,'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',target],'base_concat')
    return target

def composite(kind,base,audio,duration):
    if not audio.exists():raise RuntimeError('Approved audio master is missing: '+str(audio))
    v=probe(audio);ad=float(v['format']['duration'])
    if abs(ad-duration)>.03:raise RuntimeError(f'Audio master is not exactly {duration}s: {ad}')
    target=ROOT/f'insightgen_v3_connected_{kind}_narrated.mp4'
    graph='[0:v][1:v]overlay=shortest=1:format=auto'
    if kind=='opening':graph+=',fade=t=in:st=0:d=0.65,fade=t=out:st=13.65:d=0.35'
    graph+='[v]'
    cmd=[binary('ffmpeg'),'-hide_banner','-loglevel','error','-y','-i',str(base),'-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(audio),'-filter_complex',graph,'-map','[v]','-map','2:a:0','-frames:v',str(duration*FPS),'-r',str(FPS),'-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','44100','-ac','1','-movflags','+faststart',str(target)]
    fn=opening_overlay if kind=='opening' else under_overlay
    with (ROOT/(kind+'_render.log')).open('w',encoding='utf-8') as log:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for n in range(duration*FPS):
                p.stdin.write(fn(n/FPS).tobytes())
                if n and n%(FPS*10)==0:print(f'{kind}: {n/FPS:.0f}/{duration}s',flush=True)
            p.stdin.close();code=p.wait()
        except BaseException:
            p.stdin.close();p.wait();raise
    if code:raise RuntimeError((ROOT/(kind+'_render.log')).read_text())
    ff(['-i',target,'-f','null','-'],kind+'_decode')
    ff(['-i',target,'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',ROOT/f'insightgen_v3_connected_{kind}_silent.mp4'],kind+'_silent')
    return target

def reports(records):
    audit=list(TEXT_AUDIT.values());(ROOT/'edit/typography_audit.json').write_text(json.dumps({'all_fit':all(x['fits'] for x in audit),'items':audit},indent=2),encoding='utf-8')
    actions={'business_role_identity':'Same three-person business-team illustration/cursor at curation and question launch','curation':{'select_definition':[18.3,20.3],'review_policy':[20.3,22.7],'publish':[22.7,26]},'question_initiated_by_business_team':[39.3,42.1],'same_composed_skill':{'copy_leaves_collection':39.5,'lands_in_selected_insightgen_report':41.3,'source_asset':'assets/skill.png','three_primitives_retained':'Compare, Segment, Test pictograms are carried as one actual v2-derived asset; original collection remains in the source scene'},'amber_evidence':{'meaning':'Query-method review: illustrative quality review of a contributing query method, not an asserted defect in the real recording','AOF_outgoing':[51.8,54],'Harness_incoming':[54,56.8]},'candidate_method_change':[58.1,62.2],'validation_before_release':62.2,'same_updated_skill':{'leaves_validated_action':[62.2,64.3],'lands_in_skill_foundry_library':64.3,'copy_enters_next_agent_run':[64.5,66.2],'receiving_run_reacts':[66.2,67.4]},'audio':'Approved source WAVs mapped unchanged; no tempo or pitch retiming; only AAC delivery encoding','source_excerpts':records}
    (ROOT/'edit/semantic_actions.json').write_text(json.dumps(actions,indent=2),encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');p.add_argument('--stills',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args()
    for d in ['assets','overlays','frames','clean','docs','edit']:(ROOT/d).mkdir(exist_ok=True)
    assets();records=prepare()
    if a.stills:make_stills(records)
    if a.render:
        base=concat(records)
        composite('opening',ROOT/'clean/opening.mp4',ROOT/'audio/narrative/insightgen_opening_approved_voice.wav',14)
        composite('underthehood',base,ROOT/'audio/narrative/insightgen_underthehood_approved_voice.wav',70)
    reports(records)
    print('Local edit ready. Source and narration are never generated or replaced by this script.',flush=True)

if __name__=='__main__':main()
