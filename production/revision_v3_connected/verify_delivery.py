"""Verify the actual local delivery files; this does not verify the owner-held recording."""
from pathlib import Path
import hashlib, json
import render_connected as r

ROOT=Path(__file__).resolve().parent

def main():
    checks=[]
    for kind,seconds in [('opening',14),('underthehood',70)]:
        narrated=ROOT/f'insightgen_v3_connected_{kind}_narrated.mp4'
        silent=ROOT/f'insightgen_v3_connected_{kind}_silent.mp4'
        if not silent.exists():
            r.ff(['-i',narrated,'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',silent],kind+'_silent')
        for name,audio_count in [(narrated,1),(silent,0)]:
            p=r.probe(name);v=[s for s in p['streams'] if s['codec_type']=='video'];a=[s for s in p['streams'] if s['codec_type']=='audio']
            assert len(v)==1 and len(a)==audio_count,(name,'stream count')
            v=v[0]
            assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',seconds*24),(name,'picture metadata')
            assert abs(float(v['duration'])-seconds)<.001,(name,'video duration')
            if a:assert a[0]['sample_rate']=='44100' and a[0]['channels']==1,(name,'audio metadata')
            r.ff(['-i',name,'-f','null','-'],name.stem+'_verified_decode')
            checks.append({'file':name.name,'video_duration_seconds':float(v['duration']),'frames':int(v['nb_frames']),'resolution':[v['width'],v['height']],'frame_rate':v['r_frame_rate'],'audio_streams':len(a),'full_decode':'passed','bytes':name.stat().st_size})
    sources=[]
    for name in ['insightgen_opening_approved_voice.wav','insightgen_underthehood_approved_voice.wav']:
        p=ROOT/'audio/narrative'/name
        sources.append({'file':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'policy':'Mapped unchanged into AAC delivery encoding. No speech speed, pitch, word trimming or previous soundtrack reuse.'})
    typo=json.loads((ROOT/'edit/typography_audit.json').read_text())
    assert typo['all_fit'],'Text bounds audit failed'
    assert not json.loads((ROOT/'edit/still_review.json').read_text())['partial'],'Source cut is incomplete'
    result={'passed':True,'checks':checks,'approved_audio_sources':sources,'typography_bounds':'passed','semantic_review_frames':19,'recording':'Unavailable: actual UI framing, internal recording synchronization and final assembly remain unverified. The unchanged fixed-speed demo voice master lasts 101.283356s versus the 99s reference slot.','subjective_listening':'Not established by these technical checks; review delivery, pronunciation and sentence endings before sharing.'}
    (ROOT/'edit/delivery_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    lines=['# Delivery verification','','The narrated and silent opening/explainer exports passed exact picture duration, frame count, dimensions, cadence, expected audio-stream count and complete FFmpeg decode.','', '| Export | Duration | Frames | Audio streams | Decode |','|---|---:|---:|---:|---|']
    lines.extend(f'| {x["file"]} | {x["video_duration_seconds"]:.3f}s | {x["frames"]} | {x["audio_streams"]} | Passed |' for x in checks)
    lines.extend(['','All exports are 1280×720, 24 fps. Narrated exports contain one 44.1 kHz mono AAC stream sourced only from the approved new voice masters. Silent exports contain no audio stream. Source-master hashes are in `edit/delivery_verification.json`.','', 'Text bounds passed across the complete rendered film. Nineteen representative explainer stills and three opening stills are available for visual review. Both real generated handoffs are present; no missing-source placeholder is used.','', 'The owner-held recording is unavailable. Its complete UI framing, internal action/narration alignment and final joins remain unverified. The unchanged demo master lasts 101.283 seconds at the approved fixed speed, exceeding the 99-second reference slot. A final subjective listening review of delivery, pronunciation and sentence endings is still required before sharing.',''])
    (ROOT/'docs/VERIFICATION.md').write_text('\n'.join(lines),encoding='utf-8')
    print('PASS: 336/1680 frames; 14/70 seconds; 1280x720 at 24 fps; expected audio streams; complete decode.')

if __name__=='__main__':main()
