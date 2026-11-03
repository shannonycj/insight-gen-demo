"""Build the storyboard and timed handoff from the actual local edit and voice cues."""
from pathlib import Path
import csv, json, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
FONT='C:/Windows/Fonts/segoeui.ttf'
BOLD='C:/Windows/Fonts/seguisb.ttf'

def seconds(x):
    return f'{float(x):.3f}'

def main():
    story=json.loads((ROOT/'edit/story.json').read_text(encoding='utf-8'))
    cues=list(csv.DictReader((ROOT/'audio/narrative/narrative_cues_actual.csv').open(encoding='utf-8')))
    byid={c['id']:c for c in cues}
    md=['# Timed narration — approved fixed voice', '',
        'Opening and under-the-hood times below are local to their separate exports. Actual speech placements preserve every word at the approved synthesis speed 1.04 and pitch −1; there is no speech retiming. The master durations are 14 and 70 seconds.', '',
        '## Opening', '', f'**0.000–13.192 seconds** — {story["opening"]["narration"]}', '',
        'Two agenda items appear before the recording: “InsightGen in action” and “How we make it work at Amex.”', '',
        '## Under the hood', '']
    for c in story['under_the_hood']['cues']:
        a=byid[c['id']]
        md.extend([f'**{seconds(a["actual_start_seconds"])}–{seconds(a["actual_end_seconds"])} seconds — {c["id"].replace("_"," ")}**', '', c['narration'], '', c['meaning'], ''])
    md.extend(['## Owner-held recording', '',
        'The unchanged v2 demo narration and its nine actual placements are in `audio/demo/demo_cues_actual.csv`. Reference boundaries remain 0, 12, 23, 33, 47, 58, 67, 80, 92 and 99 seconds. At the approved fixed speed, paragraphs 7 and 9 exceed their reference windows; the complete narration master is 101.283 seconds. The real recording is unavailable, so its internal synchronization and complete UI framing require owner verification. See `ASSEMBLY.md`.', ''])
    (ROOT/'docs/TIMED_NARRATION.md').write_text('\n'.join(md),encoding='utf-8')
    rows=[
        ('Opening',0,14,14,'insightgen_v3_connected_opening_narrated.mp4','Approved narration included'),
        ('Owner-held recording — reference slot',14,113,99,'OWNER_RECORDING_NOT_PROVIDED','Reference only; actual narration requires 101.283 seconds at the fixed approved speed'),
        ('Under the hood — reference position',113,183,70,'insightgen_v3_connected_underthehood_narrated.mp4','Rebase start to 14 + actual aligned recording duration'),
    ]
    with (ROOT/'edit/assembly_timeline.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['section','reference_global_start','reference_global_end','duration_seconds','source','note']);w.writerows(rows)
    board=[
        ('opening_02.5.png','OPENING · 2.5s','A business question invites an evidence-backed investigation.'),
        ('opening_07.0.png','OPENING · 7s','Both agenda items are established before the recording.'),
        ('under_003.0.png','UNDER THE HOOD · 3s','The investigation lives on the shared Blue Orbit foundation.'),
        ('under_011.0.png','11s · OUR DIFFERENTIATOR','Reasoning and tools are connected to business-owned enterprise foundations.'),
        ('under_020.0.png','20s · BUSINESS CURATION','The business team selects a definition and reviews the policy context.'),
        ('under_025.7.png','25.7s · PUBLISH KNOWLEDGE','The approved C-60 definition retains its source identity.'),
        ('under_029.0.png','29s · KNOWLEDGE → METHOD','The bookmarked source physically grounds analytical primitives.'),
        ('under_035.0.png','35s · COMPOSE A SKILL','Compare, Segment and Test become one reusable method.'),
        ('under_041.3.png','41.3s · BUSINESS TEAM → RUN','The team asks InsightGen; the same three-method skill lands in its report.'),
        ('under_044.0.png','44s · RUN → EXECUTION TRACE','The agent run emits the trace that the next component receives.'),
        ('under_050.0.png','50s · OBSERVE QUALITY','AOF captures the run and selects a query-method quality review.'),
        ('under_056.0.png','56s · SAME EVIDENCE → HARNESS','The same amber query evidence crosses the cut into diagnosis.'),
        ('under_059.0.png','59s · TEST THE CANDIDATE','That review informs a change inside the same method folder.'),
        ('under_064.8.png','64.8s · VALIDATE → REUSE','The validated skill lands in Skill Foundry before its next use.'),
        ('under_066.5.png','66.5s · COMPLETE THE LOOP','A copy enters the next agent workspace, whose input visibly reacts.'),
    ]
    tw,th=640,360;pad=26;cw=tw+pad;ch=450
    im=Image.new('RGB',(3*cw+pad,5*ch+110),'#071421');d=ImageDraw.Draw(im)
    d.text((pad,23),'INSIGHTGEN V3 · CONNECTED CINEMATIC EDIT',font=ImageFont.truetype(BOLD,33),fill='#EDF6FC')
    d.text((pad,66),'Actual frames · 14-second opening + owner-held recording + 70-second explainer',font=ImageFont.truetype(FONT,22),fill='#AFC9D8')
    lines=['# Storyboard — actual complete cut', '', 'Every frame below comes from the conformed v2 plates or the two real generated handoffs, with final local action overlays. No missing-source placeholders are shown. See `storyboard_contact.jpg` for the visual sequence.', '']
    for i,(name,heading,caption) in enumerate(board):
        x=pad+(i%3)*cw;y=110+(i//3)*ch
        frame=Image.open(ROOT/'frames'/name).convert('RGB');frame=frame.resize((tw,th),Image.Resampling.LANCZOS);im.paste(frame,(x,y))
        d.text((x,y+365),heading,font=ImageFont.truetype(BOLD,20),fill='#EAC381')
        d.multiline_text((x,y+393),'\n'.join(textwrap.wrap(caption,65)),font=ImageFont.truetype(FONT,18),fill='#EDF6FC',spacing=4)
        lines.extend([f'**{heading}** — {caption}', '', f'![{heading}](../frames/{name})', ''])
    im.save(ROOT/'docs/storyboard_contact.jpg',quality=94)
    (ROOT/'docs/STORYBOARD.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Complete-cut storyboard, timed narration and reference assembly timeline written.')

if __name__=='__main__':main()
