"""Local narrated assembly; full recording frame and approved speech are preserved."""
from pathlib import Path
import argparse, json, math, shutil, subprocess
ROOT=Path(__file__).resolve().parent
FIT='scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2:reset_sar=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x061323,setsar=1,fps=24,format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS'
def binary(name):
    p=list((ROOT.parent/'tools').rglob(name+'.exe'))
    return str(p[0]) if p else shutil.which(name) or name
def meta(path):return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)],encoding='utf-8'))
def duration(path,kind):
    m=meta(path);s=next(s for s in m['streams'] if s['codec_type']==kind)
    return float(s.get('duration',m['format']['duration']))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--recording',required=True,type=Path);p.add_argument('--out',type=Path,default=ROOT/'insightgen_v3_2_full_narrated.mp4');p.add_argument('--dry-run',action='store_true');p.add_argument('--pad-tail',action='store_true',help='Explicitly extend the last recording frame if needed; internal cue synchronization still requires review.')
    a=p.parse_args();record=a.recording.resolve();out=a.out.resolve()
    opening=ROOT/'media/01_opening.mp4';under=ROOT/'media/03_under_the_hood_v3_2.mp4';demo=ROOT/'audio/02_demo_narration.wav'
    inputs=[opening,record,under,demo]
    if any(not x.is_file() for x in inputs):p.error('Complete recording and all approved narrated assets must exist.')
    if out.exists() or out in [x.resolve() for x in inputs]:p.error('Choose a new output path; no source or existing output is overwritten.')
    vd,ad=duration(record,'video'),duration(demo,'audio');tail=max(0,ad-vd)
    if tail>.04 and not a.pad_tail:p.error(f'Recording is {tail:.3f}s shorter than full approved narration. Align its holds first, or explicitly use --pad-tail after reviewing internal cues.')
    rec_duration=max(vd,ad);pad=f',tpad=stop_mode=clone:stop_duration={tail:.6f}' if tail else ''
    graph=f'[0:v]{FIT}[ov];[0:a]aresample=44100,aformat=channel_layouts=mono,asetpts=PTS-STARTPTS[oa];[1:v]{FIT}{pad}[rv];[3:a]aresample=44100,aformat=channel_layouts=mono,apad,atrim=duration={rec_duration:.8f},asetpts=PTS-STARTPTS[ra];[2:v]{FIT}[uv];[2:a]aresample=44100,aformat=channel_layouts=mono,asetpts=PTS-STARTPTS[ua];[ov][oa][rv][ra][uv][ua]concat=n=3:v=1:a=1[v][a]'
    cmd=[binary('ffmpeg'),'-hide_banner','-loglevel','error','-n']
    for x in inputs:cmd+=['-i',str(x)]
    cmd+=['-filter_complex',graph,'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-ar','44100','-ac','1','-movflags','+faststart',str(out)]
    report={'recording':str(record),'recording_seconds':vd,'demo_narration_seconds':ad,'recording_tail_hold_extension_seconds':tail,'speech_retimed':False,'ui_crop':False,'recording_overlays':False,'underhood_global_start':14+rec_duration,'planned_full_seconds':84+rec_duration,'cue_sync':'Owner review required against actual recording','command':cmd}
    if a.dry_run:print(json.dumps(report,indent=2));return
    subprocess.run(cmd,check=True);subprocess.run([binary('ffmpeg'),'-v','error','-i',str(out),'-f','null','-'],check=True)
    out.with_suffix('.assembly.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(out)
if __name__=='__main__':main()
