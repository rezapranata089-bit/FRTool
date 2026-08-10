#!/usr/bin/env python3
import sys,shutil,os,subprocess,difflib,json,termios,tty,re,zipfile,signal,select,time,urllib.request,urllib.error
from datetime import datetime
_rc_map={}
_df_bit=[False]
_vkey='c7dce73a81fb5c4c64604838fba7cbf4ae63d068cde88086aca0cb8be65a71fb'
_blk_ref = "f0915b17b082a765f57daccc43f9acdfd4477b8e977b6f8b396b96d36d59154c"
_aux_ref = ["1ec2e83491a8263bbbb2930a40788807ffcfdeda474ebe57a4d56f6ed8516ba2", "3d101929ff1a6ee9004a02c90c7ad20ebd9b86ecf125208e21c4f4468eff3a82"]
def _init_blk():
	_tampered=False
	try:
		import inspect as _ins,hashlib as _hl;_chk=[('_sys_auth',_blk_ref),('_rc_ok',_aux_ref[0]),('_vf',_aux_ref[1])]
		for(_n,_h)in _chk:
			if not _h:continue
			try:_fn=globals().get(_n);_ok=_fn is not None and _hl.sha256(_ins.getsource(_fn).encode()).hexdigest()==_h
			except Exception:_ok=False
			if not _ok:_tampered=True;break
	except Exception:_tampered=True
	if _tampered:
		_df_bit[0]=True;import os as _os,time as _tm
		if int(_tm.time())%2==0:_os._exit(1)
		while True:_tm.sleep(60)
def _rc_ok():
	if _df_bit[0]:return False
	try:
		import inspect as _i,hashlib as _h;_r = "b0f18ef538c67210c767df6291dc13d292c19196946fa9e0bbe517a539a1f9db";_f=globals().get('_init_blk')
		if not _f:return False
		if _r and _h.sha256(_i.getsource(_f).encode()).hexdigest()!=_r:return False
	except Exception:return False
	return _rc_map.get('_v')is True and _rc_map.get('_t',0)>0
def _vf():
	try:
		import inspect as _i,hashlib as _h;_r = "b0f18ef538c67210c767df6291dc13d292c19196946fa9e0bbe517a539a1f9db";_f=globals().get('_init_blk')
		if _r:
			if not _f or _h.sha256(_i.getsource(_f).encode()).hexdigest()!=_r:print('\n  \x1b[31m[ERROR]\x1b[0m Inisialisasi runtime gagal.');return False
	except Exception:print('\n  \x1b[31m[ERROR]\x1b[0m Inisialisasi runtime gagal.');return False
	if _rc_ok():return True
	print('\n  \x1b[31m[ERROR]\x1b[0m Inisialisasi runtime gagal.');return False
def _mix_seed(extra=b''):
	_base=_rc_map.get('_k')
	if not isinstance(_base,(bytes,bytearray))or len(_base)!=32:raise RuntimeError('sesi kerja belum siap')
	import hashlib as _h;return _h.sha256(_base+extra).digest()
def _fold_tag(*parts):_joined='\x1f'.join(str(p)for p in parts).encode();return _mix_seed(_joined).hex()[:16]
def _hb_sync(force=False):
	import time as _tm;_now=int(_tm.time())
	if not force and _now-_rc_map.get('_hb',0)<900:return _rc_map.get('_v')is True
	hwid=_rc_map.get('_id')
	if not hwid:return False
	try:
		import urllib.request as _ur,urllib.parse as _up,json as _js,hmac as _hm,hashlib as _hs;_url=f"https://frtools-users-default-rtdb.asia-southeast1.firebasedatabase.app/users/{_up.quote(hwid)}.json";_req=_ur.Request(_url,headers={'User-Agent':'Mozilla/5.0'})
		with _ur.urlopen(_req,timeout=8)as _resp:_data=_js.loads(_resp.read().decode('utf-8'))
		_status=_data.get('status','')if isinstance(_data,dict)else'';_exp=_data.get('expired_at','')if isinstance(_data,dict)else'';_sig_rcv=_data.get('sig','')if isinstance(_data,dict)else'';_sig_exp=_hm.new(bytes.fromhex(_vkey),f"{hwid}|{_status}|{_exp}".encode(),_hs.sha256).hexdigest();_ok=_hm.compare_digest(_sig_exp,_sig_rcv)and _status=='active'
		if _ok and _exp:
			try:
				if datetime.now()>datetime.strptime(_exp,'%Y-%m-%d').replace(hour=23,minute=59,second=59):_ok=False
			except Exception:pass
		if _ok:_rc_map['_k']=_hm.new(bytes.fromhex(_vkey),f"{hwid}|{_status}|{_exp}".encode(),_hs.sha256).digest();_rc_map['_hb']=_now
		else:_rc_map['_v']=False
		return _ok
	except Exception:return _rc_map.get('_v')is True and _now-_rc_map.get('_hb',0)<3600
AI_CONFIG_PATH=os.path.expanduser('~/.frtool_config.json')
HISTORY_PATH=os.path.expanduser('~/.frtool_history.json')
AMEND_SESSION_PATH=os.path.expanduser('~/.frtool_amend_session.json')
def load_recent_dirs():
	if os.path.exists(HISTORY_PATH):
		try:
			with open(HISTORY_PATH,'r')as f:return json.load(f)
		except:pass
	return[]
def save_recent_dir(path):
	if not path or not os.path.isdir(path):return
	dirs=load_recent_dirs()
	if path in dirs:dirs.remove(path)
	dirs.insert(0,path);dirs=dirs[:5]
	try:
		with open(HISTORY_PATH,'w')as f:json.dump(dirs,f,indent=2)
	except:pass
if len(sys.argv)>1:_arg_path=os.path.abspath(os.path.expanduser(sys.argv[1]));SOURCE_ROOT=_arg_path if os.path.isdir(_arg_path)else os.getcwd()
else:SOURCE_ROOT=os.getcwd()
VERSION='v5.2'
SELF_TOOL_ROOT='/storage/emulated/0/Download/FRTool/dev'
def _is_self_tool_root():
	try:return os.path.normpath(os.path.abspath(SOURCE_ROOT))==os.path.normpath(os.path.abspath(SELF_TOOL_ROOT))
	except Exception:return False
CAPROJ_EXPORT_BASE='/storage/emulated/0/Download/Project-App'
CAPROJ_EXPORT_SKIP_DIRS={'.git','build','.gradle','.idea','__pycache__'}
CAPROJ_MODE_ON=False
def _is_caproj_project(root):
	try:return os.path.isfile(os.path.join(root,'manifest.json'))and os.path.isfile(os.path.join(root,'project','app','module.toml'))
	except Exception:return False
def _slugify_caproj_name(name):words=re.split('[^a-z0-9]+',name.lower());first_word=next((w for w in words if w),'project');return first_word
def _export_caproj(root):
	try:
		manifest_path=os.path.join(root,'manifest.json')
		with open(manifest_path,'r',encoding='utf-8')as f:manifest_data=json.load(f)
		proj_name=manifest_data.get('name')or os.path.basename(root);clean_name=_slugify_caproj_name(proj_name);export_dir=os.path.join(CAPROJ_EXPORT_BASE,clean_name);os.makedirs(export_dir,exist_ok=True);out_path=os.path.join(export_dir,f"{clean_name}.caproj")
		if os.path.isfile(out_path):os.remove(out_path)
		with zipfile.ZipFile(out_path,'w',zipfile.ZIP_DEFLATED)as zf:
			zf.write(manifest_path,'manifest.json');icon_path=os.path.join(root,'icon.png')
			if os.path.isfile(icon_path):zf.write(icon_path,'icon.png')
			project_dir=os.path.join(root,'project')
			for(dirpath,dirnames,filenames)in os.walk(project_dir):
				dirnames[:]=[d for d in dirnames if d not in CAPROJ_EXPORT_SKIP_DIRS]
				for fn in filenames:full=os.path.join(dirpath,fn);arcname=os.path.relpath(full,root);zf.write(full,arcname)
		try:subprocess.run(['termux-media-scan',out_path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=5)
		except Exception:pass
		return True,out_path,None
	except Exception as e:return False,None,str(e)
C_PURPLE=166
C_VIOLET=209
C_CYAN=215
C_CYAN2=223
C_WHITE=255
C_GRAY=244
C_DGRAY=240
C_BORDER=166
_GRAY_SEP='\x01'
_SCROLL_SEP='\x02'
RGB_TERRACOTTA_DARK=181,101,59
RGB_TERRACOTTA_LIGHT=240,178,138
RGB_PATCH_DARK=199,92,58
RGB_PATCH_LIGHT=247,188,140
RGB_DELTA_DARK=91,33,182
RGB_DELTA_LIGHT=196,164,255
RGB_FULL_DARK=181,101,59
RGB_FULL_LIGHT=240,178,138
RGB_DIR_DARK=181,136,41
RGB_DIR_LIGHT=255,214,122
LOGO=['  ███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ','  ██╔════╝██╔══██╗       ██║   ██╔═══██╗██╔═══██╗██║     ','  █████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║     ','  ██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║     ','  ██║     ██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗','  ╚═╝     ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝']
LOGO_PATCH=['  ██████╗  █████╗ ████████╗ ██████╗██╗  ██╗','  ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║','  ██████╔╝███████║   ██║   ██║     ███████║','  ██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║','  ██║     ██║  ██║   ██║   ╚██████╗██║  ██║','  ╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝']
LOGO_AI_SETUP=['   █████╗ ██╗    ███████╗███████╗████████╗██╗   ██╗██████╗ ','  ██╔══██╗██║    ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗','  ███████║██║    ███████╗█████╗     ██║   ██║   ██║██████╔╝','  ██╔══██║██║    ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ ','  ██║  ██║██║    ███████║███████╗   ██║   ╚██████╔╝██║     ','  ╚═╝  ╚═╝╚═╝   ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ']
LOGO_DELTA=['  ██████╗ ███████╗██╗     ████████╗ █████╗ ','  ██╔══██╗██╔════╝██║     ╚══██╔══╝██╔══██╗','  ██║  ██║█████╗  ██║        ██║   ███████║','  ██║  ██║██╔══╝  ██║        ██║   ██╔══██║','  ██████╔╝███████╗███████╗   ██║   ██║  ██║','  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝']
LOGO_FULL=['  ███████╗██╗   ██╗██╗     ██╗     ','  ██╔════╝██║   ██║██║     ██║     ','  █████╗  ██║   ██║██║     ██║     ','  ██╔══╝  ██║   ██║██║     ██║     ','  ██║     ╚██████╔╝███████╗███████╗','  ╚═╝      ╚═════╝ ╚══════╝╚══════╝']
LOGO_GIT=['   ██████╗ ██╗████████╗','  ██╔════╝ ██║╚══██╔══╝','  ██║  ███╗██║   ██║   ','  ██║   ██║██║   ██║   ','  ╚██████╔╝██║   ██║   ','   ╚═════╝ ╚═╝   ╚═╝   ']
LOGO_DIR=['  ████╗  ██╗ ████╗  █████╗ █████╗ █████╗  ████╗ ████╗  ██╗ ██╗','  ██╔═██╗██║ ██╔═██╗██╔══╝ ██╔══╝ ╚═██╔╝ ██╔═██╗██╔═██╗╚████╔╝','  ██║ ██║██║ ████╔╝ ████╗  ██║      ██║  ██║ ██║████╔╝  ╚██╔╝ ','  ██║ ██║██║ ██╔═██╗██╔═╝  ██║      ██║  ██║ ██║██╔═██╗  ██║  ','  █████╔╝██║ ██║ ██║█████╗ ╚█████╗  ██║  ╚████╔╝██║ ██║  ██║  ','  ╚════╝ ╚═╝ ╚═╝ ╚═╝╚════╝  ╚════╝  ╚═╝   ╚═══╝ ╚═╝ ╚═╝  ╚═╝  ']
MASCOT_MINI_FRAMES=[['     ✦     ','     │     ','◢█████████◣','█  ◉   ◉  █','◥█████████◤','   ╲___╱   '],['     ✦     ','     │     ','◢█████████◣','█  ─   ─  █','◥█████████◤','   ╲___╱   ']]
_MASCOT_ACCENT_CHARS={'◉','✦','─'}
def _render_mascot_frame(frame,rgb_start,rgb_end,accent_rgb,bold=True):
	import math;bold_code='1;'if bold else'';max_len=max((len(l)for l in frame),default=0);t=time.time()*2.2;pulse=(math.sin(t*1.6)+1)/2;out_lines=[]
	for line in frame:
		out=[]
		for(i,ch)in enumerate(line):
			if ch in _MASCOT_ACCENT_CHARS:r=int(accent_rgb[0]*(.55+.45*pulse));g=int(accent_rgb[1]*(.55+.45*pulse));b=int(accent_rgb[2]*(.55+.45*pulse))
			else:wave=(math.sin(t-i*.35)+1)/2;r,g,b=_interp_rgb(rgb_start,rgb_end,wave)
			out.append(f"[{bold_code}38;2;{r};{g};{b}m{ch}")
		out.append('\x1b[0m');out_lines.append(''.join(out))
	return out_lines
_MASCOT_BLINK_PERIOD=3.
_MASCOT_BLINK_DURATION=.25
def _get_mascot_frame():phase=time.time()%_MASCOT_BLINK_PERIOD;is_blinking=phase>_MASCOT_BLINK_PERIOD-_MASCOT_BLINK_DURATION;return MASCOT_MINI_FRAMES[1]if is_blinking else MASCOT_MINI_FRAMES[0]
def _ground_line(width):
	if width<=0:return''
	tile='‿ψ‿ψo‿ψ‿ψ‿';raw=(tile*(width//len(tile)+2))[:width];out=[]
	for ch in raw:
		if ch==' ':out.append(' ')
		elif ch=='o':r,g,b=_GROUND_ROCK_RGB;out.append(f"[38;2;{r};{g};{b}m{ch}[0m")
		else:r,g,b=_GROUND_GRASS_RGB;out.append(f"[38;2;{r};{g};{b}m{ch}[0m")
	return''.join(out)
def _interp_rgb(start,end,t):return tuple(round(start[i]+(end[i]-start[i])*t)for i in range(3))
def gradient_ascii_lines(lines,rgb_start,rgb_end,bold=True):
	bold_code='1;'if bold else'';max_len=max((len(l)for l in lines),default=0);out_lines=[]
	for line in lines:
		out=[]
		for(i,ch)in enumerate(line):t=i/max(max_len-1,1);r,g,b=_interp_rgb(rgb_start,rgb_end,t);out.append(f"[{bold_code}38;2;{r};{g};{b}m{ch}")
		out.append('\x1b[0m');out_lines.append(''.join(out))
	return out_lines
def print_gradient_ascii(lines,rgb_start,rgb_end,bold=True):
	for line in gradient_ascii_lines(lines,rgb_start,rgb_end,bold):print(line)
def print_gradient_ascii_centered(lines,rgb_start,rgb_end,term_cols,bold=True):
	rendered=gradient_ascii_lines(lines,rgb_start,rgb_end,bold);content_w=max((_vlen(l)for l in rendered),default=0);margin=' '*max(0,(term_cols-content_w)//2)
	for line in rendered:print(margin+line)
_resize_pending=False
def _on_resize(signum,frame):global _resize_pending;_resize_pending=True
def clear():os.system('clear')
def _term_size():
	try:return os.get_terminal_size(sys.stdout.fileno())
	except(OSError,AttributeError):return shutil.get_terminal_size()
def fast_clear():sys.stdout.write('\x1b[H\x1b[2J');sys.stdout.flush()
import re as _re
_ANSI_RE=_re.compile('\\x1b\\[[0-9;]*m')
_VS_RE=_re.compile('[︀-️]')
_WIDE_CHARS={'📁','📄'}
def _char_w(ch):return 2 if ch in _WIDE_CHARS else 1
def _vlen(s):s=_ANSI_RE.sub('',s);s=_VS_RE.sub('',s);return sum(_char_w(c)for c in s)
def _pad_cell(colored,width,center=False):
	vis=_vlen(colored)
	if center:lpad=max(0,(width-vis)//2);return' '*lpad+colored+' '*max(0,width-vis-lpad)
	return colored+' '*max(0,width-vis)
def _wrap_plain_text(text,width):
	if width<=0:return[text]
	words=text.split(' ');lines,cur=[],''
	for w in words:
		if not cur:cur=w
		elif len(cur)+1+len(w)<=width:cur+=' '+w
		else:lines.append(cur);cur=w
		while len(cur)>width:lines.append(cur[:width]);cur=cur[width:]
	if cur:lines.append(cur)
	return lines or['']
def show_welcome():
	global SOURCE_ROOT;recent=load_recent_dirs();items=[]
	for p in recent:label=p if len(p)<=40 else'…'+p[-39:];items.append(('recent',label,p))
	items.append(('manual','Masukkan path manual...',None));sel_idx=0;msg='';_last_welcome_size=None;_home=os.path.abspath(os.path.expanduser('~'));_cwd=os.path.abspath(os.getcwd())
	while True:
		term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines;size_changed=_last_welcome_size is not None and _last_welcome_size!=(term_cols,term_lines);_last_welcome_size=term_cols,term_lines;W2=max(22,min(term_cols-2,int(term_cols*.95)));B=f"[38;5;{C_BORDER}m";R='\x1b[0m';BL=f"{B}│{R}";TL=f"  {B}┌{"─"*W2}┐{R}";BT=f"  {B}└{"─"*W2}┘{R}";buf=[];buf.append('');_welcome_safe_logo=[l[:max(10,term_cols-2)]for l in LOGO];buf.extend(gradient_ascii_lines(_welcome_safe_logo,RGB_TERRACOTTA_DARK,RGB_TERRACOTTA_LIGHT));buf.append('');W=max(22,min(72,term_cols-2));raw_top=f"  ╔{"═"*W}╗";buf.append(f"  [38;5;{C_BORDER}m╔{"═"*W}╗[0m");tag='Find & Replace Patch Engine for Developers'
		if len(tag)>W-2:tag=tag[:max(0,W-5)]+'...'
		tag_pad=max(0,(W-len(tag))//2);buf.append(f"  [38;5;{C_BORDER}m║[0m{" "*tag_pad}[1;38;5;{C_WHITE}m{tag}[0m{" "*max(0,W-tag_pad-len(tag))}[38;5;{C_BORDER}m║[0m");ver_line=f"Version {VERSION}  ·  Python CLI  ·  FR Tool"
		if len(ver_line)>W-2:ver_line=ver_line[:max(0,W-5)]+'...'
		ver_pad=max(0,(W-len(ver_line))//2);buf.append(f"  [38;5;{C_BORDER}m║[0m{" "*ver_pad}[38;5;{C_GRAY}m{ver_line}[0m{" "*max(0,W-ver_pad-len(ver_line))}[38;5;{C_BORDER}m║[0m");buf.append(f"  [38;5;{C_BORDER}m╚{"═"*W}╝[0m");buf.append('');root_short=SOURCE_ROOT if len(SOURCE_ROOT)<=48 else'…'+SOURCE_ROOT[-47:];root_disp=f"  [38;5;{C_GRAY}mDIR :[0m [38;5;{C_CYAN}m{root_short}[0m";buf.append(root_disp);buf.append('');buf.append(TL)
		for(i,(itype,label,path))in enumerate(items):
			is_sel=i==sel_idx;marker='❯'if is_sel else' ';raw=f" {marker} {label}";pad=max(0,W2-len(_ANSI_RE.sub('',raw)))
			if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {label}{" "*pad}[0m"
			elif itype=='recent':row=f"   [38;5;{C_CYAN}m{label}[0m{" "*pad}"
			else:row=f"   [1;38;5;{C_VIOLET}m{label}[0m{" "*pad}"
			buf.append(f"  {BL}{row}{BL}")
		buf.append(BT);buf.append('')
		if msg:buf.append(f"  {msg}");buf.append('')
		content_height=len(buf)
		if content_height<term_lines:available_v=term_lines-content_height;top_pad=available_v//3;buf=['']*top_pad+buf
		buf.append(f"  [38;5;{C_DGRAY}m> ↑↓ pilih   Enter konfirmasi   M = manual path   ESC pakai default[0m");buf.append('');_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
		if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
		if len(buf)>term_lines:buf=buf[:max(1,term_lines-1)]
		clear_prefix='\x1b[2J'if size_changed else'';sys.stdout.write('\x1b[?2026h'+clear_prefix+'\x1b[H'+'\n'.join(line+'\x1b[K'for line in buf)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();msg='';k=get_key()
		if k=='UP':sel_idx=(sel_idx-1)%len(items)
		elif k=='DOWN':sel_idx=(sel_idx+1)%len(items)
		elif k=='ENTER':
			itype,label,path=items[sel_idx]
			if itype=='manual':
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();print(f"  [38;5;{C_GRAY}mPath direktori target:[0m");print(f"  [38;5;{C_DGRAY}m(Enter = pakai direktori saat ini: {SOURCE_ROOT})[0m")
				if recent:
					print(f"  [38;5;{C_DGRAY}mRiwayat tersedia:[0m")
					for(j,rp)in enumerate(recent,1):print(f"  [38;5;240m[{j}][0m [38;5;244m{rp}[0m")
				print(f"  [1;38;5;{C_CYAN}m▶ [0m",end='')
				try:raw=input().strip()
				except(EOFError,KeyboardInterrupt):break
				if raw=='':save_recent_dir(SOURCE_ROOT);return
				if recent and raw.isdigit():
					idx=int(raw)-1
					if 0<=idx<len(recent):
						if os.path.isdir(recent[idx]):SOURCE_ROOT=recent[idx];save_recent_dir(SOURCE_ROOT);return
						else:msg=f"[31m[GAGAL][0m Direktori tidak ditemukan: {recent[idx]}";continue
				path=os.path.abspath(os.path.expanduser(raw))
				if os.path.isdir(path):SOURCE_ROOT=path;save_recent_dir(SOURCE_ROOT);return
				else:msg=f"[31m[GAGAL][0m Path tidak ditemukan: {path}";continue
			elif os.path.isdir(path):SOURCE_ROOT=path;save_recent_dir(SOURCE_ROOT);break
			else:
				msg=f"[31m[GAGAL][0m Direktori tidak ditemukan: {path}"
				if path in recent:recent.remove(path);items=[(t,l,p)for(t,l,p)in items if p!=path]
				sel_idx=min(sel_idx,len(items)-1);continue
		elif k in('m','M'):sel_idx=len(items)-1
		elif k in('ESC','q','Q','0'):save_recent_dir(SOURCE_ROOT);break
		elif k=='RESIZE':continue
def pilih_folder():
	global SOURCE_ROOT
	def _print_dir_head():term_cols=_term_size().columns;safe_logo=[l[:max(10,term_cols-2)]for l in LOGO_DIR];print_gradient_ascii_centered(safe_logo,RGB_TERRACOTTA_DARK,RGB_TERRACOTTA_LIGHT,term_cols);header('Ubah Direktori Target');print(f"  Direktori aktif saat ini:\n    {SOURCE_ROOT}\n")
	clear();_print_dir_head();recent=load_recent_dirs();recent_clean=[p for p in recent if p!=SOURCE_ROOT]
	if not recent_clean:
		print('Tidak ada riwayat direktori.');print('\nTekan Enter untuk input path manual, atau ESC untuk membatalkan...');k=get_key()
		if k in('ESC','q','Q','0'):return False
		print(f"Masukkan path direktori baru:");print(f"(biarkan kosong lalu Enter untuk membatalkan)");print(f"Path: ",end='')
		try:path=input().strip()
		except(EOFError,KeyboardInterrupt):return False
		if path==''or path.lower()in('exit','q','0','batal'):return False
		path=os.path.abspath(os.path.expanduser(path))
		if not os.path.isdir(path):print(f"\n[GAGAL] Direktori tidak ditemukan: {path}");input('\nTekan Enter untuk melanjutkan...');return False
		SOURCE_ROOT=path;save_recent_dir(SOURCE_ROOT);print(f"\n[OK] Direktori target berhasil diubah ke:\n  {path}");input('\nTekan Enter untuk melanjutkan...');return True
	items=[]
	for p in recent_clean:label=p if len(p)<=48 else'…'+p[-47:];items.append(('recent',label,p))
	items.append(('manual','[M] Ketik path baru',None));sel_idx=0;msg='';_last_pick_size=None;_first_pick_draw=True
	while True:
		term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines;size_changed=_last_pick_size is not None and _last_pick_size!=(term_cols,term_lines);_last_pick_size=term_cols,term_lines;W2=max(22,min(term_cols-2,int(term_cols*.95)));B=f"[38;5;{C_BORDER}m";R='\x1b[0m';BL=f"{B}│{R}";TL=f"  {B}┌{"─"*W2}┐{R}";BT=f"  {B}└{"─"*W2}┘{R}";full_clear=_first_pick_draw or size_changed;sys.stdout.write('\x1b[?2026h'+('\x1b[2J\x1b[3J\x1b[H'if full_clear else'\x1b[H'));_print_dir_head();_first_pick_draw=False;buf=[];buf.append(TL)
		for(i,(itype,label,path))in enumerate(items):
			is_sel=i==sel_idx;marker='❯'if is_sel else' ';raw=f" {marker} {label}";pad=max(0,W2-len(_ANSI_RE.sub('',raw)))
			if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {label}{" "*pad}[0m"
			elif itype=='recent':row=f"   [38;5;{C_CYAN}m{label}[0m{" "*pad}"
			else:row=f"   [1;38;5;{C_VIOLET}m{label}[0m{" "*pad}"
			buf.append(f"  {BL}{row}{BL}")
		buf.append(BT);buf.append('')
		if msg:buf.append(f"  {msg}");buf.append('')
		buf.append(f"  [38;5;{C_DGRAY}m> ↑↓ pilih   Enter konfirmasi   M = ketik path   ESC kembali[0m");buf.append('');_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
		if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
		if len(buf)>term_lines:buf=buf[:max(1,term_lines-1)]
		sys.stdout.write('\n'.join(line+'\x1b[K'for line in buf)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();msg='';k=get_key()
		if k=='UP':sel_idx=(sel_idx-1)%len(items)
		elif k=='DOWN':sel_idx=(sel_idx+1)%len(items)
		elif k=='ENTER':
			itype,label,path=items[sel_idx]
			if itype=='manual':
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();print(f"Direktori aktif saat ini:\n  {SOURCE_ROOT}\n");print('Masukkan path direktori baru:');print('(biarkan kosong lalu Enter untuk membatalkan)');print('Path: ',end='')
				try:path=input().strip()
				except(EOFError,KeyboardInterrupt):return False
				if path==''or path.lower()in('exit','q','0','batal'):return False
				path=os.path.abspath(os.path.expanduser(path))
				if not os.path.isdir(path):print(f"\n[GAGAL] Direktori tidak ditemukan: {path}");input('\nTekan Enter untuk melanjutkan...');return False
				SOURCE_ROOT=path;save_recent_dir(SOURCE_ROOT);print(f"\n[OK] Direktori target berhasil diubah ke:\n  {path}");input('\nTekan Enter untuk melanjutkan...');return True
			elif os.path.isdir(path):SOURCE_ROOT=path;save_recent_dir(SOURCE_ROOT);print(f"\n[OK] Direktori target berhasil diubah ke:\n  {SOURCE_ROOT}");input('\nTekan Enter untuk melanjutkan...');return True
			else:
				msg=f"[31m[GAGAL][0m Direktori tidak ditemukan lagi: {path}"
				if path in recent_clean:recent_clean.remove(path);items=[(t,l,p)for(t,l,p)in items if p!=path]
				sel_idx=min(sel_idx,len(items)-1);continue
		elif k in('m','M'):sel_idx=len(items)-1
		elif k in('ESC','q','Q','0'):return False
		elif k=='RESIZE':continue
IGNORE_DIRS={'node_modules','.git','.next','dist','build','__pycache__','.expo','.patch_backups','.vercel','.cache','.turbo','venv','.venv','env','.env','ios','android','auth_info'}
IGNORE_EXTS={'.bak','.log','.tmp','.swp','.orig','.pyc'}
BASE_IGNORE_DIRS=frozenset(IGNORE_DIRS)
BASE_IGNORE_EXTS=frozenset(IGNORE_EXTS)
def _read_frignore_raw():
	frignore_path=os.path.join(SOURCE_ROOT,'.frignore');entries=[]
	if os.path.exists(frignore_path):
		try:
			with open(frignore_path,'r',encoding='utf-8')as f:
				for line in f:
					line=line.strip()
					if not line or line.startswith('#'):continue
					entries.append(line)
		except Exception:pass
	return entries
def _write_frignore_raw(entries):
	frignore_path=os.path.join(SOURCE_ROOT,'.frignore')
	try:
		with open(frignore_path,'w',encoding='utf-8')as f:
			f.write('# Folder/ekstensi tambahan yang di-skip FR Tool saat scan & patch\n');f.write('# Format: satu nama folder per baris, atau *.ext untuk ekstensi\n')
			for e in entries:f.write(e+'\n')
	except Exception:pass
def load_frignore():
	global IGNORE_DIRS,IGNORE_EXTS;IGNORE_DIRS=set(BASE_IGNORE_DIRS);IGNORE_EXTS=set(BASE_IGNORE_EXTS)
	for line in _read_frignore_raw():
		if line.startswith('*.'):IGNORE_EXTS.add(line[1:])
		else:IGNORE_DIRS.add(line.strip('/'))
MIN_TERM_COLS=26
MIN_TERM_LINES=16
_last_draw_size=None
AUTO_ANCHOR_TOLERANCE=20
AUTO_ANCHOR_MAX_GAP=150
PARTIAL_MIN_SCORE=.3
THRESHOLD_CONFIG_PATH=os.path.expanduser('~/.frtool_thresholds.json')
def load_thresholds():
	global AUTO_ANCHOR_TOLERANCE,AUTO_ANCHOR_MAX_GAP,PARTIAL_MIN_SCORE
	if os.path.exists(THRESHOLD_CONFIG_PATH):
		try:
			with open(THRESHOLD_CONFIG_PATH,'r')as f:t=json.load(f)
			AUTO_ANCHOR_TOLERANCE=int(t.get('auto_anchor_tolerance',AUTO_ANCHOR_TOLERANCE));AUTO_ANCHOR_MAX_GAP=int(t.get('auto_anchor_max_gap',AUTO_ANCHOR_MAX_GAP));PARTIAL_MIN_SCORE=float(t.get('partial_min_score',PARTIAL_MIN_SCORE))
		except Exception:pass
def save_thresholds():
	with open(THRESHOLD_CONFIG_PATH,'w')as f:json.dump({'auto_anchor_tolerance':AUTO_ANCHOR_TOLERANCE,'auto_anchor_max_gap':AUTO_ANCHOR_MAX_GAP,'partial_min_score':PARTIAL_MIN_SCORE},f,indent=2)
GIT_IDENTITY_CONFIG_PATH=os.path.expanduser('~/.frtool_git_identity.json')
GIT_USER_EMAIL='frtool@local'
GIT_USER_NAME='FR Tool'
def load_git_identity():
	global GIT_USER_EMAIL,GIT_USER_NAME
	if os.path.exists(GIT_IDENTITY_CONFIG_PATH):
		try:
			with open(GIT_IDENTITY_CONFIG_PATH,'r')as f:g=json.load(f)
			GIT_USER_EMAIL=g.get('email')or GIT_USER_EMAIL;GIT_USER_NAME=g.get('name')or GIT_USER_NAME
		except Exception:pass
def save_git_identity():
	with open(GIT_IDENTITY_CONFIG_PATH,'w')as f:json.dump({'email':GIT_USER_EMAIL,'name':GIT_USER_NAME},f,indent=2)
def log_fail_event(block_label,layer,filename=''):
	log_path=os.path.join(SOURCE_ROOT,'.patch_backups','fail_log.json');os.makedirs(os.path.dirname(log_path),exist_ok=True);logs=[]
	if os.path.exists(log_path):
		try:
			with open(log_path,'r')as f:logs=json.load(f)
		except Exception:logs=[]
	logs.append({'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'block':block_label,'layer':layer,'file':filename})
	try:
		with open(log_path,'w')as f:json.dump(logs[-500:],f,indent=2)
	except Exception:pass
def normalize(text):lines=text.replace('\r\n','\n').splitlines();return'\n'.join(line.strip()for line in lines).strip()
def _indent_len(line,tab_width=4):
	n=0
	for ch in line:
		if ch==' ':n+=1
		elif ch=='\t':n+=tab_width
		else:break
	return n
def _structural_lines(raw_lines):
	clean=[l for l in raw_lines if l.strip()]
	if not clean:return[]
	base=_indent_len(clean[0]);return[f"{_indent_len(l)-base}|{l.strip()}"for l in clean]
def _window_end_for_clean_count(content_lines,start,target_clean_count):
	count=0;idx=start;n=len(content_lines)
	while idx<n and count<target_clean_count:
		if content_lines[idx].strip():count+=1
		idx+=1
	return idx
def _best_window_at(content_lines,i,base_w_size,find_sig,tol=6):
	lo=max(1,base_w_size-tol);hi=base_w_size+tol;best_score,best_end=0,-1;count=0;idx=i;n=len(content_lines)
	while idx<n and count<hi:
		is_content=bool(content_lines[idx].strip());idx+=1
		if is_content:
			count+=1
			if count>=lo:
				chunk_sig='\n'.join(_structural_lines(content_lines[i:idx]));score=difflib.SequenceMatcher(None,find_sig,chunk_sig).ratio()
				if score>best_score:best_score,best_end=score,idx
	return best_score,best_end
def _reindent_relative(replace_text,base_indent):
	lines=replace_text.splitlines();non_empty=[l for l in lines if l.strip()]
	if not non_empty:return replace_text
	min_indent=min(_indent_len(l)for l in non_empty);out=[]
	for l in lines:
		if not l.strip():out.append('');continue
		delta=max(0,_indent_len(l)-min_indent);out.append(base_indent+' '*delta+l.strip())
	return'\n'.join(out)
def _has_ellipsis(find_text):return any(l.strip()in(':skip','...')for l in find_text.splitlines())
def _split_ellipsis(find_text):
	lines=find_text.splitlines();idx=next(i for(i,l)in enumerate(lines)if l.strip()in(':skip','...'));head=[l.strip()for l in lines[:idx]];tail=[l.strip()for l in lines[idx+1:]]
	while head and not head[0]:head.pop(0)
	while head and not head[-1]:head.pop()
	while tail and not tail[0]:tail.pop(0)
	while tail and not tail[-1]:tail.pop()
	return head,tail
def _match_lines(pattern_stripped,content_lines,start_from=0):
	if not pattern_stripped:return-1
	for i in range(start_from,len(content_lines)):
		if content_lines[i].strip()==pattern_stripped[0]:
			matched=all(i+j<len(content_lines)and content_lines[i+j].strip()==pattern_stripped[j]for j in range(len(pattern_stripped)))
			if matched:return i
	return-1
def find_head_tail(find_text,content,block_label=None):
	head,tail=_split_ellipsis(find_text)
	if not head or not tail:return
	content_lines=content.splitlines();is_fuzzy=False;head_start=_match_lines(head,content_lines)
	if head_start==-1:
		import difflib;clean_lines=[l.strip()for l in content_lines];head_str='\n'.join(head);best_h_idx,best_h_score=-1,0
		for i in range(len(clean_lines)-len(head)+1):
			chunk='\n'.join(clean_lines[i:i+len(head)]);score=difflib.SequenceMatcher(None,head_str,chunk).ratio()
			if score>best_h_score:best_h_score=score;best_h_idx=i
		if best_h_score>=.7:head_start=best_h_idx;is_fuzzy=True
		else:return
	head_end=head_start+len(head);tail_candidates=[];scan_from=head_end
	while True:
		pos=_match_lines(tail,content_lines,start_from=scan_from)
		if pos==-1:break
		tail_candidates.append(pos);scan_from=pos+1
	if not tail_candidates:
		import difflib;clean_lines=[l.strip()for l in content_lines];tail_str='\n'.join(tail);best_t_idx,best_t_score=-1,0
		for i in range(head_end,len(clean_lines)-len(tail)+1):
			chunk='\n'.join(clean_lines[i:i+len(tail)]);score=difflib.SequenceMatcher(None,tail_str,chunk).ratio()
			if score>best_t_score:best_t_score=score;best_t_idx=i
		if best_t_score>=.7:tail_candidates.append(best_t_idx);is_fuzzy=True
	if not tail_candidates:return
	if len(tail_candidates)==1 or block_label is None:tail_start=tail_candidates[0]
	else:
		opts=[(str(idx),f"Baris {pos+1}")for(idx,pos)in enumerate(tail_candidates)];msg_lines=[f"Blok #{block_label}: baris akhir (tail) ditemukan di",f"{len(tail_candidates)} lokasi berbeda. Pilih yang benar:"];pilihan=popup_confirm('⚠️ TAIL AMBIGU',msg_lines,opts,default=0,layout='vertical')
		try:tail_start=tail_candidates[int(pilihan)]
		except(ValueError,IndexError):tail_start=tail_candidates[0]
	tail_end=tail_start+len(tail);return head_start,tail_end,'head_tail_fuzzy'if is_fuzzy else'head_tail'
def find_in_content(find_text,content,block_label=None):
	if _has_ellipsis(find_text):result=find_head_tail(find_text,content,block_label=block_label);return result
	idx=content.find(find_text)
	if idx!=-1:return idx,idx+len(find_text),'exact'
	find_lines_exact=[l.strip()for l in find_text.splitlines()]
	while find_lines_exact and not find_lines_exact[0]:find_lines_exact.pop(0)
	while find_lines_exact and not find_lines_exact[-1]:find_lines_exact.pop()
	content_lines=content.splitlines();head_start=_match_lines(find_lines_exact,content_lines)
	if head_start!=-1:lines_keep=content.splitlines(keepends=True);start_char=sum(len(l)for l in lines_keep[:head_start]);end_i=head_start+len(find_lines_exact)-1;end_char=sum(len(l)for l in lines_keep[:end_i+1]);return start_char,end_char,'fuzzy'
	import re as _re_match;tokens=_re_match.findall('\\w+|[^\\w\\s]',find_text)
	if tokens and len(tokens)<100:
		regex_pattern='\\s*'.join(_re_match.escape(t)for t in tokens);match=_re_match.search(regex_pattern,content)
		if match:return match.start(),match.end(),'regex'
	find_lines_clean=[l.strip()for l in find_text.splitlines()if l.strip()]
	if len(find_lines_clean)>=3:
		content_lines=content.splitlines();clean_map=[(idx,l.strip())for(idx,l)in enumerate(content_lines)if l.strip()]
		for anchor_size in(3,2):
			if len(find_lines_clean)<anchor_size*2:continue
			head_anchor=find_lines_clean[:anchor_size];tail_anchor=find_lines_clean[-anchor_size:];h_idx=-1
			for i in range(len(clean_map)-anchor_size+1):
				if all(clean_map[i+j][1]==head_anchor[j]for j in range(anchor_size)):h_idx=i;break
			if h_idx!=-1:
				best_t_idx=-1;best_diff=float('inf')
				for i in range(h_idx+anchor_size,len(clean_map)-anchor_size+1):
					if all(clean_map[i+j][1]==tail_anchor[j]for j in range(anchor_size)):
						actual_gap=clean_map[i+anchor_size-1][0]-clean_map[h_idx][0];diff=abs(actual_gap-len(find_lines_clean))
						if diff<best_diff:best_diff=diff;best_t_idx=i
				if best_t_idx!=-1:
					real_h=clean_map[h_idx][0];real_t=clean_map[best_t_idx+anchor_size-1][0];gap=real_t-real_h
					if gap<=len(find_lines_clean)+AUTO_ANCHOR_TOLERANCE:return real_h,real_t+1,'auto_anchor'
					elif gap<=AUTO_ANCHOR_MAX_GAP:return real_h,real_t+1,'auto_anchor_confirm'
	if not _has_ellipsis(find_text):
		import difflib;find_lines_clean=[l.strip()for l in find_text.splitlines()if l.strip()]
		if len(find_lines_clean)>=2:
			content_lines=content.splitlines();find_sig='\n'.join(_structural_lines(find_text.splitlines()));w_size=len(find_lines_clean);first_clean=find_lines_clean[0];last_clean=find_lines_clean[-1];candidates=[]
			for i in range(len(content_lines)):
				line_i=content_lines[i].strip()
				if not line_i:continue
				if difflib.SequenceMatcher(None,line_i,first_clean).ratio()<.45 and difflib.SequenceMatcher(None,line_i,last_clean).ratio()<.45:continue
				score,end_i=_best_window_at(content_lines,i,w_size,find_sig)
				if end_i==-1:continue
				if score>=.8:candidates.append((score,i,end_i))
			if candidates:
				candidates.sort(key=lambda c:c[0],reverse=True);best_score,best_i,best_end=candidates[0];rivals=[c for c in candidates[1:]if best_score-c[0]<=.05];anchor_generic=len(find_lines_clean[0])<=3 or len(find_lines_clean[-1])<=3;reason='baris jangkar kurang unik'if anchor_generic else f"{len(rivals)} kandidat lain mirip"
				if(anchor_generic or rivals)and block_label is not None:
					if not _confirm_fuzzy_block(best_score,best_i,best_end-best_i,content_lines,block_label,reason):return
				lines_keep=content.splitlines(keepends=True);start_c=sum(len(l)for l in lines_keep[:best_i]);end_c=sum(len(l)for l in lines_keep[:best_end]);return start_c,end_c,'fuzzy_block'
def replace_in_content(content,find_text,replace_text,mode='first'):
	if _has_ellipsis(find_text):
		result=find_head_tail(find_text,content)
		if result is None:return content,0
		line_start,line_end,_=result;content_lines=content.splitlines(keepends=True);indent=''
		for ch in content_lines[line_start]:
			if ch in(' ','\t'):indent+=ch
			else:break
		replace_lines=replace_text.splitlines();indented_replace='\n'.join(indent+l if l.strip()else l for l in replace_lines);new_lines=content_lines[:line_start]+[indented_replace+'\n']+content_lines[line_end:];return''.join(new_lines),1
	if mode=='all':return content.replace(find_text,replace_text),content.count(find_text)
	if find_text in content:return content.replace(find_text,replace_text,1),1
	import re as _re_match;tokens=_re_match.findall('\\w+|[^\\w\\s]',find_text)
	if tokens and len(tokens)<100:
		regex_pattern='\\s*'.join(_re_match.escape(t)for t in tokens);match=_re_match.search(regex_pattern,content)
		if match:
			start_idx=match.start();end_idx=match.end();nl_idx=content.rfind('\n',0,start_idx);indent=''
			if nl_idx!=-1:
				for ch in content[nl_idx+1:start_idx]:
					if ch in(' ','\t'):indent+=ch
					else:break
			replace_lines=replace_text.splitlines()
			if len(replace_lines)<=1 and'\n'not in content[start_idx:end_idx]:new_content=content[:start_idx]+replace_text+content[end_idx:]
			else:indented_replace='\n'.join(l if i==0 else indent+l if l.strip()else l for(i,l)in enumerate(replace_lines));new_content=content[:start_idx]+indented_replace+content[end_idx:]
			return new_content,1
	find_lines_exact=[l.strip()for l in find_text.splitlines()]
	while find_lines_exact and not find_lines_exact[0]:find_lines_exact.pop(0)
	while find_lines_exact and not find_lines_exact[-1]:find_lines_exact.pop()
	content_lines=content.splitlines(keepends=True);content_lines_clean=[l.rstrip('\n')for l in content_lines];start_i=_match_lines(find_lines_exact,content_lines_clean)
	if start_i!=-1:
		indent=''
		for ch in content_lines[start_i]:
			if ch in(' ','\t'):indent+=ch
			else:break
		replace_lines=replace_text.splitlines();indented_replace='\n'.join(indent+l if l.strip()else l for l in replace_lines);new_lines=content_lines[:start_i]+[indented_replace+'\n']+content_lines[start_i+len(find_lines_exact):];return''.join(new_lines),1
	find_lines_stripped=[l.strip()for l in find_text.splitlines()if l.strip()]
	if len(find_lines_stripped)>=3:
		clean_map=[(idx,l.strip())for(idx,l)in enumerate(content_lines)if l.strip()]
		for anchor_size in(3,2):
			if len(find_lines_stripped)<anchor_size*2:continue
			head_anchor=find_lines_stripped[:anchor_size];tail_anchor=find_lines_stripped[-anchor_size:];h_idx=-1
			for i in range(len(clean_map)-anchor_size+1):
				if all(clean_map[i+j][1]==head_anchor[j]for j in range(anchor_size)):h_idx=i;break
			if h_idx!=-1:
				best_t_idx=-1;best_diff=float('inf')
				for i in range(h_idx+anchor_size,len(clean_map)-anchor_size+1):
					if all(clean_map[i+j][1]==tail_anchor[j]for j in range(anchor_size)):
						actual_gap=clean_map[i+anchor_size-1][0]-clean_map[h_idx][0];diff=abs(actual_gap-len(find_lines_stripped))
						if diff<best_diff:best_diff=diff;best_t_idx=i
				if best_t_idx!=-1:
					real_h=clean_map[h_idx][0];real_t=clean_map[best_t_idx+anchor_size-1][0];jarak=real_t-real_h
					if jarak<=len(find_lines_stripped)+AUTO_ANCHOR_MAX_GAP:
						indent=''
						for ch in content_lines[real_h]:
							if ch in(' ','\t'):indent+=ch
							else:break
						replace_lines=replace_text.splitlines();indented_replace='\n'.join(indent+l if l.strip()else l for l in replace_lines);new_lines=content_lines[:real_h]+[indented_replace+'\n']+content_lines[real_t+1:];return''.join(new_lines),1
	if mode=='fuzzy_block':
		import difflib;find_lines_clean=[l.strip()for l in find_text.splitlines()if l.strip()];content_lines=content.splitlines(keepends=True);find_sig='\n'.join(_structural_lines(find_text.splitlines()));best_score=0;best_i=-1;best_end=-1;w_size=len(find_lines_clean);first_clean=find_lines_clean[0];last_clean=find_lines_clean[-1]
		for i in range(len(content_lines)):
			line_i=content_lines[i].strip()
			if not line_i:continue
			if difflib.SequenceMatcher(None,line_i,first_clean).ratio()<.45 and difflib.SequenceMatcher(None,line_i,last_clean).ratio()<.45:continue
			score,end_i=_best_window_at(content_lines,i,w_size,find_sig)
			if end_i==-1:continue
			if score>best_score:best_score=score;best_i=i;best_end=end_i
		if best_score>=.8:
			indent=''
			for ch in content_lines[best_i]:
				if ch in(' ','\t'):indent+=ch
				else:break
			indented_replace=_reindent_relative(replace_text,indent);new_lines=content_lines[:best_i]+[indented_replace+'\n']+content_lines[best_end:];return''.join(new_lines),1
	return content,0
def _frcache_path(root):return os.path.join(root,'.patch_backups','project_cache.json')
def _load_disk_cache(root):
	path=_frcache_path(root)
	if not os.path.exists(path):return{}
	try:
		with open(path,'r',encoding='utf-8')as f:raw=json.load(f)
		if not isinstance(raw,dict)or raw.get('_v')!=1:return{}
		return raw.get('files',{})
	except Exception:return{}
def _save_disk_cache(root,disk_entries):
	path=_frcache_path(root)
	try:
		os.makedirs(os.path.dirname(path),exist_ok=True)
		with open(path,'w',encoding='utf-8')as f:json.dump({'_v':1,'files':disk_entries},f)
	except Exception:pass
def _build_project_cache(root=None):
	import re as _re2,sys
	if root is None:root=SOURCE_ROOT
	old_disk_cache=_load_disk_cache(root);new_disk_cache={};total_files=0
	for(dirpath,dirs,files)in os.walk(root):
		dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]
		for fname in files:
			if os.path.splitext(fname)[1].lower()not in IGNORE_EXTS:total_files+=1
	import time;start_index_time=time.time();entries=[];processed=0;reused=0;sys.stdout.write('\x1b[?25l')
	for(dirpath,dirs,files)in os.walk(root):
		dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]
		for fname in files:
			_,ext=os.path.splitext(fname)
			if ext.lower()in IGNORE_EXTS:continue
			full=os.path.join(dirpath,fname);processed+=1;global _GLOBAL_TIMER_START
			if _GLOBAL_TIMER_START==.0:_GLOBAL_TIMER_START=start_index_time
			elapsed_idx=time.time()-_GLOBAL_TIMER_START;pct=processed/max(1,total_files);bar_len=25;filled=int(bar_len*pct);bar='█'*filled+'░'*(bar_len-filled);sys.stdout.write(f"\r  [1;38;5;129m[INDEXING][0m Membangun index project... {bar} {processed}/{total_files} [K\n");sys.stdout.write(f"\r      [38;5;244m↳ ⏱  {elapsed_idx:.1f}s [38;5;244m(cache: {reused})[0m[K");sys.stdout.write('\x1b[1A');sys.stdout.flush();rel=os.path.relpath(full,root)
			try:st=os.stat(full)
			except OSError:continue
			cached=old_disk_cache.get(rel)
			if cached and cached.get('mtime')==st.st_mtime and cached.get('size')==st.st_size:content=cached['content'];norm=cached['norm'];file_toks=frozenset(cached['toks']);reused+=1
			else:
				try:
					with open(full,'r',encoding='utf-8')as f:content=f.read()
				except(PermissionError,IsADirectoryError,UnicodeDecodeError):continue
				norm=normalize(content);file_toks=frozenset(t for t in _re2.split('[\\s{};,()\\"\\\'\\[\\]=:.<>!&|@]+',content)if len(t)>3)
			new_disk_cache[rel]={'mtime':st.st_mtime,'size':st.st_size,'content':content,'norm':norm,'toks':list(file_toks)};entries.append({'full':full,'rel':rel,'content':content,'norm':norm,'toks':file_toks})
	sys.stdout.write('\r\x1b[K\n\r\x1b[K\x1b[1A\x1b[?25h');sys.stdout.flush();_save_disk_cache(root,new_disk_cache);return entries
def cari_file_berisi_kode(find_text,root=None,cache=None):
	if root is None:root=SOURCE_ROOT
	hasil=[];has_ell=_has_ellipsis(find_text)
	if has_ell:head,tail=_split_ellipsis(find_text);search_text='\n'.join(head);tail_text='\n'.join(tail);norm_tail=normalize(tail_text)
	else:search_text=find_text;tail_text=None;norm_tail=None
	norm_find=normalize(search_text)
	def _head_tail_present(raw_content,norm_content):
		head_ok=search_text in raw_content or norm_find in norm_content
		if not has_ell:return head_ok
		tail_ok=tail_text in raw_content or norm_tail in norm_content;return head_ok and tail_ok
	if cache is not None:
		for entry in cache:
			if _head_tail_present(entry['content'],entry['norm']):hasil.append(entry['rel'])
		return hasil
	for(dirpath,dirs,files)in os.walk(root):
		dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]
		for fname in files:
			_,ext=os.path.splitext(fname)
			if ext.lower()in IGNORE_EXTS:continue
			full=os.path.join(dirpath,fname)
			try:
				with open(full,'r',encoding='utf-8')as f:content=f.read()
			except(PermissionError,IsADirectoryError,UnicodeDecodeError):continue
			if _head_tail_present(content,normalize(content)):hasil.append(os.path.relpath(full,root))
	return hasil
def _find_best_block(find_text,content,window_extra=12):
	import re as _re2;find_lines=[l.strip()for l in find_text.splitlines()if l.strip()];n_find=max(len(find_lines),5);c_lines=content.splitlines();n_c=len(c_lines)
	if n_c==0:return content[:600]
	find_toks={t for t in _re2.split('[\\s{};,()\\"\\\'\\[\\]=:.<>!&|@]+',find_text)if len(t)>3}
	if not find_toks:return content[:600]
	best_score,best_start=0,0;step=max(1,n_find//2)
	for i in range(0,max(1,n_c-n_find+1),step):
		chunk='\n'.join(c_lines[i:i+n_find]);chunk_toks={t for t in _re2.split('[\\s{};,()\\"\\\'\\[\\]=:.<>!&|@]+',chunk)if len(t)>3};score=len(find_toks&chunk_toks)/len(find_toks)
		if score>best_score:best_score,best_start=score,i
	ctx_s=max(0,best_start-2);ctx_e=min(n_c,best_start+n_find+window_extra);return'\n'.join(c_lines[ctx_s:ctx_e])
def cari_file_partial(find_text,root=None,top_n=3,min_score=None,cache=None):
	import re as _re2
	if min_score is None:min_score=PARTIAL_MIN_SCORE
	if root is None:root=SOURCE_ROOT
	find_toks={t for t in _re2.split('[\\s{};,()\\"\\\'\\[\\]=:.<>!&|@]+',find_text)if len(t)>3}
	if not find_toks:return[]
	results=[]
	if cache is not None:
		for entry in cache:
			file_toks=entry['toks']
			if not file_toks:continue
			score=len(find_toks&file_toks)/len(find_toks)
			if score>=min_score:block=_find_best_block(find_text,entry['content']);results.append((entry['full'],score,block,entry['rel']))
		results.sort(key=lambda x:x[1],reverse=True);return results[:top_n]
	for(dirpath,dirs,files)in os.walk(root):
		dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]
		for fname in files:
			_,ext=os.path.splitext(fname)
			if ext.lower()in IGNORE_EXTS:continue
			full=os.path.join(dirpath,fname)
			try:
				with open(full,'r',encoding='utf-8')as f:content=f.read()
			except(PermissionError,IsADirectoryError,UnicodeDecodeError):continue
			file_toks={t for t in _re2.split('[\\s{};,()\\"\\\'\\[\\]=:.<>!&|@]+',content)if len(t)>3}
			if not file_toks:continue
			score=len(find_toks&file_toks)/len(find_toks)
			if score>=min_score:block=_find_best_block(find_text,content);rel=os.path.relpath(full,root);results.append((full,score,block,rel))
	results.sort(key=lambda x:x[1],reverse=True);return results[:top_n]
def _extract_patch_title(text):
	import re
	for line in text.splitlines():
		m=re.match('^:\\s*title\\s+(.+)$',line.strip(),re.IGNORECASE)
		if m:return m.group(1).strip()
def parse_patch(text):
	if any(l.strip()=='===FIND==='for l in text.splitlines()):return parse_patch_lama(text)
	results={};current_file='__AUTO__';current_find=None;state='idle';buffer=[];import re;lines=text.splitlines()
	for line in lines:
		stripped=line.strip();tag_check=stripped.lower();match_file=re.match('^:\\s*file\\s+(.+)$',stripped,re.IGNORECASE)
		if match_file:
			if state=='replace'and current_find is not None:_add_pair(results,current_file,current_find,'\n'.join(buffer));buffer=[];state='idle';current_find=None
			current_file=match_file.group(1).strip();state='idle';current_find=None;buffer=[]
		elif re.match('^:\\s*find$',tag_check):
			if state=='replace'and current_find is not None:_add_pair(results,current_file,current_find,'\n'.join(buffer));buffer=[];current_find=None
			state='find';buffer=[]
		elif re.match('^:\\s*new_file$',tag_check):
			if state=='replace'and current_find is not None:_add_pair(results,current_file,current_find,'\n'.join(buffer));buffer=[]
			current_find='__NEW_FILE__';state='after_find'
		elif re.match('^:\\s*end_find$',tag_check):
			if state=='find':current_find='\n'.join(buffer);buffer=[];state='after_find'
		elif re.match('^:\\s*replace$',tag_check):
			if state in('find','after_find'):
				if state=='find':current_find='\n'.join(buffer)
				buffer=[];state='replace'
		elif re.match('^:\\s*(end_replace|end)$',tag_check):
			if state=='replace'and current_find is not None:_add_pair(results,current_file,current_find,'\n'.join(buffer));buffer=[];state='idle';current_find=None
		elif state in('find','replace'):buffer.append(line)
	if state=='replace'and current_find is not None and buffer:_add_pair(results,current_file,current_find,'\n'.join(buffer))
	return results
def _add_pair(results,filename,find,replace):
	if filename not in results:results[filename]=[]
	results[filename].append((find,replace))
def parse_patch_lama(text):
	if'===FILE==='not in text:text='===FILE===\n__AUTO__\n'+text
	results={};blocks=text.split('===FILE===')
	for block in blocks[1:]:
		if'===FIND==='not in block:continue
		file_part,rest=block.split('===FIND===',1);filename=file_part.strip();sub_blocks=('===FIND==='+rest).split('===FIND===');pairs=[]
		for sub in sub_blocks[1:]:
			if'===REPLACE==='not in sub:continue
			find_part,rest2=sub.split('===REPLACE===',1);replace_part=rest2.split('===END===')[0]if'===END==='in rest2 else rest2;pairs.append((find_part.strip('\n'),replace_part.strip('\n')))
		if filename and pairs:
			if filename not in results:results[filename]=[]
			results[filename].extend(pairs)
	return results
def copy_to_clipboard(text):
	cmds=[['termux-clipboard-set'],['xclip','-selection','clipboard'],['xsel','--clipboard','--input'],['clip.exe'],['pbcopy']]
	for cmd in cmds:
		try:
			r=subprocess.run(cmd,input=text.encode('utf-8'),timeout=5,capture_output=True)
			if r.returncode==0:return True
		except(FileNotFoundError,subprocess.TimeoutExpired,OSError):continue
	if os.path.isdir('/data/data/com.termux'):print('\n  [INFO] Untuk mengaktifkan auto-copy di Termux:');print('         1. Install Termux:API dari F-Droid atau Google Play');print('         2. Jalankan: pkg install termux-api');print('         Setelah itu, clipboard akan bekerja otomatis.\n')
	return False
def load_ai_config():
	if os.path.exists(AI_CONFIG_PATH):
		try:
			with open(AI_CONFIG_PATH,'r')as f:return json.load(f)
		except:pass
	return{}
def save_ai_config(cfg):
	with open(AI_CONFIG_PATH,'w')as f:json.dump(cfg,f,indent=2)
def ai_fix_find(find_text,replace_text,file_content,filename):
	cfg=load_ai_config();provider=cfg.get('provider','openai');api_key_raw=cfg.get('api_key','');api_keys=[k.strip()for k in api_key_raw.split(',')if k.strip()];model=cfg.get('model','gpt-4o-mini')
	if not _rc_ok()or not _hb_sync():return None,'Inisialisasi gagal. Jalankan ulang tool.'
	if not api_keys:return None,'API key belum dikonfigurasi. Pilih menu [6] AI Setup.'
	PROVIDER_URLS={'openai':'https://api.openai.com/v1/chat/completions','groq':'https://api.groq.com/openai/v1/chat/completions','openrouter':'https://openrouter.ai/api/v1/chat/completions','local':'http://127.0.0.1:4891/v1/chat/completions'};api_url=PROVIDER_URLS.get(provider,PROVIDER_URLS['openai'])
	if provider=='local'and cfg.get('local_url','').strip():api_url=cfg['local_url'].strip()
	MAX_CONTENT=35000;import re as _re
	if len(file_content)>MAX_CONTENT:
		tokens_set=set(t for t in _re.split('[\\s{};,()\\"\\\'\\[\\]=:]+',find_text)if len(t)>3);file_lines=file_content.splitlines();best_start,best_score=0,0;window_size=min(40,max(10,len(find_text.splitlines())+5))
		for i in range(len(file_lines)-window_size+1):
			window_text='\n'.join(file_lines[i:i+window_size]);window_tokens=set(t for t in _re.split('[\\s{};,()\\"\\\'\\[\\]=:]+',window_text)if len(t)>3);score=len(tokens_set.intersection(window_tokens))
			if score>best_score:best_score=score;best_start=i
		if best_score>0:start_ctx=max(0,best_start-100);end_ctx=min(len(file_lines),best_start+window_size+100);snippet='\n'.join(file_lines[start_ctx:end_ctx]);file_snippet=f"[...potongan file dari baris {start_ctx+1} hingga {end_ctx} (Algoritma Semantic Chunking)...]\n{snippet}"
		else:file_snippet=file_content[:MAX_CONTENT]+'\n[...dipotong karena file terlalu besar dan pencarian token gagal...]'
	else:file_snippet=file_content
	find_lines_clean=[l.strip()for l in find_text.splitlines()if l.strip()];first_line_hint=find_lines_clean[0]if find_lines_clean else'';last_line_hint=find_lines_clean[-1]if find_lines_clean else'';line_count=len(find_lines_clean);system_prompt="Kamu adalah mesin pencari kode (Fuzzy Code Matcher) tingkat lanjut yang sangat akurat.\nTugasmu adalah menemukan potongan kode ASLI di dalam sebuah file berdasarkan 'Teks Pencarian' yang diberikan oleh user. Teks Pencarian tersebut mungkin rusak, mengandung typo (contoh: 'apalah kau ni'), atau kehilangan spasi/enter.\n\nATURAN KETAT:\n1. KEMBALIKAN HANYA BARIS KODE YANG DIMINTA. JANGAN MENAMBAH BARIS KODE APA PUN SEBELUM ATAU SESUDAHNYA!\n2. Patokan Awal: Harus dimulai tepat di baris yang mirip dengan baris pertama Teks Pencarian.\n3. Patokan Akhir: Harus berhenti tepat di baris yang mirip dengan baris terakhir Teks Pencarian.\n4. Kembalikan HANYA potongan kode ASLI dari file tersebut persis seperti aslinya (pertahankan indentasi aslinya jika ada).\n5. JANGAN tambahkan penjelasan, JANGAN gunakan blok markdown (```javascript), langsung teks kodenya saja!";user_prompt=f"""[CONTEXT FILE ASLI ({filename})]:
{file_snippet}
{"="*40}

[TEKS PENCARIAN YANG RUSAK / TYPO]:
{find_text}
{"="*40}

Tugas: Tolong temukan bentuk ASLI dari Teks Pencarian di atas di dalam [CONTEXT FILE ASLI], lalu cetak kode aslinya saja.
WAJIB 1: Dimulai dari baris yang menyerupai: `{first_line_hint}`
WAJIB 2: Berakhir tepat di baris: `{last_line_hint}`
WAJIB 3: Hasilnya harus sekitar {line_count} baris. JANGAN kebablasan menyalin kode di bawahnya!""";payload=json.dumps({'model':model,'messages':[{'role':'system','content':system_prompt},{'role':'user','content':user_prompt}],'max_tokens':1500,'temperature':.0}).encode('utf-8');last_error=None
	for(idx,current_key)in enumerate(api_keys):
		headers={'Content-Type':'application/json','Authorization':f"Bearer {current_key}",'User-Agent':'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'}
		if provider=='openrouter':headers['HTTP-Referer']='https://github.com/frtool';headers['X-Title']='FR Patch Tool'
		req=urllib.request.Request(api_url,data=payload,headers=headers,method='POST')
		try:
			with urllib.request.urlopen(req,timeout=90)as resp:
				data=json.loads(resp.read().decode('utf-8'));result=data['choices'][0]['message']['content'].strip()
				if result.startswith('```'):
					lines=result.splitlines();inner=[];skip_first=True
					for ln in lines:
						if skip_first and ln.startswith('```'):skip_first=False;continue
						if ln.strip()=='```':break
						inner.append(ln)
					result='\n'.join(inner).strip()
				try:
					f_clean=[l.strip()for l in find_text.splitlines()if l.strip()]
					if f_clean and result:
						first_f=f_clean[0];last_f=f_clean[-1];r_lines=result.splitlines();end_idx=len(r_lines)-1
						for i in range(len(r_lines)-1,-1,-1):
							if r_lines[i].strip()==last_f:end_idx=i;break
						if end_idx<len(r_lines)-1:result='\n'.join(r_lines[:end_idx+1])
						r_clean=[l.strip()for l in result.splitlines()if l.strip()]
						if r_clean and r_clean[-1]!=last_f and len(last_f)<=10 and not last_f[0].isalpha():
							idx=file_content.find(result)
							if idx!=-1:
								sisa_teks=file_content[idx+len(result):]
								if sisa_teks.lstrip(' \t\r\n').startswith(last_f):end_idx=sisa_teks.find(last_f)+len(last_f);result+=sisa_teks[:end_idx]
				except Exception:pass
				return result,None
		except urllib.error.HTTPError as e:
			body=e.read().decode('utf-8',errors='replace')
			try:msg=json.loads(body).get('error',{}).get('message',body)
			except:msg=body[:200]
			last_error=f"HTTP {e.code}: {msg}"
			if e.code in(429,401,403,500,503)and idx<len(api_keys)-1:import sys;sys.stdout.write(f"\r  [33m[API Limit][0m Key #{idx+1} gagal (HTTP {e.code}). Fallback ke Key #{idx+2}... [K");sys.stdout.flush();continue
			else:break
		except(urllib.error.URLError,ConnectionRefusedError,OSError)as e:
			reason=getattr(e,'reason',e);recovered=None
			for _retry in range(2):
				time.sleep(2)
				try:
					with urllib.request.urlopen(req,timeout=90)as resp:recovered=json.loads(resp.read().decode('utf-8'))
					break
				except Exception:continue
			if recovered:
				try:
					result=recovered['choices'][0]['message']['content'].strip()
					if result.startswith('```'):
						rlines=result.splitlines();inner=[];skip_first=True
						for ln in rlines:
							if skip_first and ln.startswith('```'):skip_first=False;continue
							if ln.strip()=='```':break
							inner.append(ln)
						result='\n'.join(inner).strip()
					return result,None
				except Exception:pass
			last_error=f"Gagal konek ke server AI ({api_url}). Pastikan server lokal/9Router sedang aktif & port-nya benar. Detail: {reason}"
			if idx<len(api_keys)-1:continue
			break
		except Exception as e:
			last_error=str(e)
			if idx<len(api_keys)-1:continue
			break
	return None,last_error
def cek_syntax_ai(content_baru,filename):
	import ast,tempfile,re
	if filename.endswith('.py'):
		try:ast.parse(content_baru);return'AMAN'
		except SyntaxError as e:return f"ERROR: Baris {e.lineno}, {e.msg}"
	elif filename.endswith('.json'):
		try:json.loads(content_baru);return'AMAN'
		except json.JSONDecodeError as e:return f"ERROR: Baris {e.lineno}, {e.msg}"
	elif filename.endswith('.js')or filename.endswith('.html')or filename.endswith('.htm'):
		try:subprocess.run(['node','-v'],capture_output=True);has_node=True
		except FileNotFoundError:has_node=False
		js_code=content_baru
		if filename.endswith('.html')or filename.endswith('.htm'):
			lines=content_baru.splitlines();js_lines=[];in_script=False
			for line in lines:
				line_low=line.lower()
				if'<script'in line_low and'</script>'in line_low:match=re.search('(?i)<script[^>]*>(.*?)</script>',line);js_lines.append(match.group(1)if match else'')
				elif'<script'in line_low:in_script=True;js_lines.append('')
				elif'</script>'in line_low:in_script=False;js_lines.append('')
				elif in_script:js_lines.append(line)
				else:js_lines.append('')
			js_code='\n'.join(js_lines)
			if not js_code.strip():return'AMAN'
		if has_node:
			fd,temp_path=tempfile.mkstemp(suffix='.mjs')
			with os.fdopen(fd,'w',encoding='utf-8')as f:f.write(js_code)
			try:
				res=subprocess.run(['node','--check',temp_path],capture_output=True,text=True)
				if res.returncode==0:return'AMAN'
				else:
					err=res.stderr.strip();err_lines=err.splitlines();err_msg='Syntax Error';snippet=''
					for el in err_lines:
						if'SyntaxError:'in el:err_msg=el.strip();break
					for(i,el)in enumerate(err_lines):
						if'^'in el and el.lstrip().startswith('^'):
							if i>=1:code_line=err_lines[i-1].replace('\t','    ');pointer_line=el.replace('\t','    ');snippet=f"\n             [38;5;244m|[0m {code_line}\n             [38;5;244m|[0m [1;31m{pointer_line}[0m"
							break
					m=re.search(':(\\d+)',err_lines[0])if err_lines else None;baris=f"Baris {m.group(1)} - "if m else'';return f"ERROR: {baris}{err_msg}{snippet}"
			finally:os.remove(temp_path)
		content_baru=js_code
	cfg=load_ai_config();api_keys=[k.strip()for k in cfg.get('api_key','').split(',')if k.strip()]
	if not api_keys:return'SKIP'
	lines=content_baru.splitlines()
	if len(lines)>600:snippet='// ... kode atas diabaikan ...\n'+'\n'.join(lines[-600:])
	else:snippet=content_baru
	prompt=f"""Bertindaklah sebagai Linter JavaScript/Python yang sangat ketat. Periksa kode dari {filename} berikut.
Cari KESALAHAN SINTAKS FATAL yang menyebabkan kegagalan parse (contoh: kurang koma antar property object, kurang tutup kurung, Unexpected identifier, dll).
Abaikan error logika, undefined variables (seperti window/document), atau peringatan best practice.

WAJIB Jawab dengan format ini:
Jika benar-benar aman: AMAN
Jika ada error sintaks: ERROR: [Letak Baris] - [Pesan Error Singkat]

KODE:
{snippet}""";payload=json.dumps({'model':cfg.get('model','gpt-4o-mini'),'messages':[{'role':'user','content':prompt}],'max_tokens':150,'temperature':.0}).encode('utf-8');PROVIDER_URLS={'openai':'https://api.openai.com/v1/chat/completions','groq':'https://api.groq.com/openai/v1/chat/completions','openrouter':'https://openrouter.ai/api/v1/chat/completions','local':'http://127.0.0.1:4891/v1/chat/completions'};api_url=PROVIDER_URLS.get(cfg.get('provider','openai'),PROVIDER_URLS['openai'])
	if cfg.get('provider')=='local'and cfg.get('local_url','').strip():api_url=cfg['local_url'].strip()
	last_err=''
	for(idx,current_key)in enumerate(api_keys):
		headers={'Content-Type':'application/json','Authorization':f"Bearer {current_key}",'User-Agent':'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'}
		if cfg.get('provider')=='openrouter':headers['HTTP-Referer']='https://github.com/frtool';headers['X-Title']='FR Patch Tool'
		req=urllib.request.Request(api_url,data=payload,headers=headers,method='POST')
		try:
			with urllib.request.urlopen(req,timeout=60)as resp:data=json.loads(resp.read().decode('utf-8'));return data['choices'][0]['message']['content'].strip()
		except urllib.error.HTTPError as e:
			body=e.read().decode('utf-8',errors='replace')
			try:msg=json.loads(body).get('error',{}).get('message',body)
			except:msg=body[:100]
			last_err=f"SKIP_ERR_HTTP: {e.code} - {msg}"
			if e.code in(429,401,403,500,503)and idx<len(api_keys)-1:sys.stdout.write(f"\r  [33m[API Limit][0m Key #{idx+1} gagal saat cek syntax. Fallback... [K");sys.stdout.flush();continue
			else:break
		except Exception as e:
			last_err=f"SKIP_ERR_NET: {str(e)}"
			if idx<len(api_keys)-1:continue
			break
	return last_err
_GLOBAL_TIMER_START=.0
def _spinner_start(msg,color='36'):
	import threading,time;global _GLOBAL_TIMER_START
	if _GLOBAL_TIMER_START==.0:_GLOBAL_TIMER_START=time.time()
	stop_event=threading.Event();frames=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
	try:term_cols=_term_size().columns
	except Exception:term_cols=80
	prefix_len=4;timer_len=10;max_msg=max(10,term_cols-prefix_len-timer_len-2)
	if len(msg)>max_msg:msg=msg[:max_msg-1]+'…'
	def _run():
		sys.stdout.write('\x1b[?25l');i=0
		while not stop_event.is_set():elapsed=time.time()-_GLOBAL_TIMER_START;sys.stdout.write(f"\r  [1;38;5;{color}m{frames[i%len(frames)]}[0m {msg} [K\n");sys.stdout.write(f"\r      [38;5;244m↳ ⏱  {elapsed:.1f}s[0m[K");sys.stdout.write('\x1b[1A');sys.stdout.flush();time.sleep(.08);i+=1
		sys.stdout.write('\r\x1b[K\n\r\x1b[K\x1b[1A\x1b[?25h');sys.stdout.flush()
	t=threading.Thread(target=_run,daemon=True);t.start();return stop_event,t
def _spinner_stop(stop_event,thread):stop_event.set();thread.join()
_WORD_TOKEN_RE=None
def _tokenize_line(line):
	global _WORD_TOKEN_RE
	if _WORD_TOKEN_RE is None:import re;_WORD_TOKEN_RE=re.compile('\\w+|\\s+|[^\\w\\s]')
	return _WORD_TOKEN_RE.findall(line)
def _char_diff_segments(old_line,new_line):
	if old_line==new_line:return None,None
	old_tokens=_tokenize_line(old_line);new_tokens=_tokenize_line(new_line);sm=difflib.SequenceMatcher(None,old_tokens,new_tokens,autojunk=False)
	if sm.quick_ratio()<.25:return None,None
	old_segs,new_segs=[],[]
	for(tag,i1,i2,j1,j2)in sm.get_opcodes():
		if i2>i1:old_segs.append((''.join(old_tokens[i1:i2]),tag!='equal'))
		if j2>j1:new_segs.append((''.join(new_tokens[j1:j2]),tag!='equal'))
	return old_segs,new_segs
_SYNTAX_TOKENS_CACHE={}
def _get_syntax_tokens(lang):
	if lang in _SYNTAX_TOKENS_CACHE:return _SYNTAX_TOKENS_CACHE[lang]
	import re,keyword as kwmod;KW,STR,NUM,CMT,DECO,FUNC,CLS,BLT,TAG,ATTR,SEL,PROP='\x1b[38;5;176m','\x1b[38;5;180m','\x1b[38;5;173m','\x1b[38;5;242m','\x1b[38;5;214m','\x1b[38;5;149m','\x1b[38;5;222m','\x1b[38;5;80m','\x1b[38;5;110m','\x1b[38;5;115m','\x1b[38;5;204m','\x1b[38;5;150m';tokens=[]
	if lang=='python':py_builtins='print','len','range','isinstance','str','int','float','bool','list','dict','set','tuple','type','super','open','input','enumerate','zip','map','filter','sorted','sum','min','max','abs','round','any','all','iter','next','getattr','setattr','hasattr','property','staticmethod','classmethod','repr','vars','issubclass';kw_alt='|'.join(sorted(kwmod.kwlist,key=len,reverse=True));tokens=[(re.compile('#.*'),CMT),(re.compile('(?:[rRbBfFuU]{1,2})?(?:\\\'\\\'\\\'.*?\\\'\\\'\\\'|""".*?"""|\\\'(?:[^\\\'\\\\]|\\\\.)*\\\'|"(?:[^"\\\\]|\\\\.)*")'),STR),(re.compile('@[\\w.]+'),DECO),(re.compile('(?<=\\bdef )\\w+'),FUNC),(re.compile('(?<=\\bclass )\\w+'),CLS),(re.compile('\\b(?:'+kw_alt+')\\b'),KW),(re.compile('\\b(?:'+'|'.join(py_builtins)+')\\b(?=\\s*\\()'),BLT),(re.compile('\\b\\d+\\.?\\d*\\b'),NUM),(re.compile('\\b[A-Za-z_]\\w*(?=\\s*\\()'),FUNC)]
	elif lang=='javascript':js_kw='const','let','var','function','return','if','else','for','while','do','switch','case','default','break','continue','class','extends','new','this','super','import','export','from','as','try','catch','finally','throw','async','await','yield','typeof','instanceof','in','of','void','delete','null','undefined','true','false','static','get','set','interface','type','enum','implements','public','private','protected','readonly','namespace';js_builtins='console','document','window','Math','JSON','Array','Object','String','Number','Boolean','Promise','Map','Set','WeakMap','WeakSet','Symbol','Date','RegExp','Error','parseInt','parseFloat','isNaN','isFinite','setTimeout','setInterval','clearTimeout','clearInterval','fetch','require','process';tokens=[(re.compile('//.*'),CMT),(re.compile('/\\*.*?\\*/'),CMT),(re.compile('</?[a-zA-Z][\\w-]*'),TAG),(re.compile('[a-zA-Z-][\\w-]*(?=\\s*=)'),ATTR),(re.compile('`(?:[^`\\\\]|\\\\.)*`'),STR),(re.compile('"(?:[^"\\\\]|\\\\.)*"'),STR),(re.compile("'(?:[^'\\\\]|\\\\.)*'"),STR),(re.compile('(?<=\\bfunction )\\w+'),FUNC),(re.compile('(?<=\\bclass )\\w+'),CLS),(re.compile('[a-zA-Z_$][\\w$]*(?=\\s*:)'),PROP),(re.compile('\\b(?:'+'|'.join(sorted(js_kw,key=len,reverse=True))+')\\b'),KW),(re.compile('\\b(?:'+'|'.join(js_builtins)+')\\b'),BLT),(re.compile('\\b\\d+\\.?\\d*\\b'),NUM),(re.compile('\\b[A-Za-z_$][\\w$]*(?=\\s*\\()'),FUNC)]
	elif lang=='css':tokens=[(re.compile('/\\*.*?\\*/'),CMT),(re.compile('"(?:[^"\\\\]|\\\\.)*"'),STR),(re.compile("'(?:[^'\\\\]|\\\\.)*'"),STR),(re.compile('@[\\w-]+'),DECO),(re.compile('#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\\b'),NUM),(re.compile('::?[a-zA-Z-]+'),SEL),(re.compile('\\.[a-zA-Z_-][\\w-]*'),SEL),(re.compile('#[a-zA-Z_-][\\w-]*'),SEL),(re.compile('[a-zA-Z_-][\\w-]*(?=\\s*:)'),PROP),(re.compile('\\b\\d+\\.?\\d*(?:px|em|rem|%|vh|vw|vmin|vmax|s|ms|deg|fr)?(?:\\b|(?=\\W|$))'),NUM)]
	elif lang=='html':js_kw_basic='const','let','var','function','return','if','else','for','while','class','import','export','document','window','console';tokens=[(re.compile('<!--.*?-->'),CMT),(re.compile('/\\*.*?\\*/'),CMT),(re.compile('//.*'),CMT),(re.compile('<!DOCTYPE[^>]*>',re.IGNORECASE),TAG),(re.compile('</?[a-zA-Z][\\w-]*'),TAG),(re.compile('"(?:[^"\\\\]|\\\\.)*"'),STR),(re.compile("'(?:[^'\\\\]|\\\\.)*'"),STR),(re.compile('`(?:[^`\\\\]|\\\\.)*`'),STR),(re.compile('[a-zA-Z-][\\w-]*(?=\\s*=)'),ATTR),(re.compile('[a-zA-Z_-][\\w-]*(?=\\s*:)'),PROP),(re.compile('\\.[a-zA-Z_-][\\w-]*'),SEL),(re.compile('#[a-zA-Z_-][\\w-]*'),SEL),(re.compile('\\b(?:'+'|'.join(sorted(js_kw_basic,key=len,reverse=True))+')\\b'),KW),(re.compile('\\b\\d+\\.?\\d*(?:px|em|rem|%|vh|vw|vmin|vmax|s|ms|deg|fr)?(?:\\b|(?=\\W|$))'),NUM),(re.compile('\\b[A-Za-z_$][\\w$]*(?=\\s*\\()'),FUNC)]
	_SYNTAX_TOKENS_CACHE[lang]=tokens;return tokens
def _syntax_color_map(line,lang):
	n=len(line);colors=[None]*n;tokens=_get_syntax_tokens(lang)
	if not tokens:return colors
	pos=0
	while pos<n:
		matched=False
		for(pattern,color)in tokens:
			m=pattern.match(line,pos)
			if m and m.end()>pos:colors[pos:m.end()]=[color]*(m.end()-pos);pos=m.end();matched=True;break
		if not matched:pos+=1
	return colors
def _diff_stat_bar(plus,minus,slots=10):
	total=plus+minus
	if total==0:return'\x1b[38;5;238m'+'▪'*slots+'\x1b[0m'
	green_n=round(slots*plus/total)
	if plus and green_n==0:green_n=1
	if minus and green_n==slots:green_n=slots-1
	red_n=slots-green_n;return f"[38;5;71m{"▪"*green_n}[38;5;167m{"▪"*red_n}[0m"
def _trailing_ws_run(line):
	import re
	if not line.strip():return
	m=re.search('[ \\t]+$',line);return(m.start(),m.end())if m else None
def tampilkan_diff(content_lama,content_baru,filepath,capture=False):
	rel=os.path.relpath(filepath,SOURCE_ROOT);_lang={'.py':'python','.js':'javascript','.jsx':'javascript','.mjs':'javascript','.cjs':'javascript','.ts':'javascript','.tsx':'javascript','.html':'html','.htm':'html','.css':'css'}.get(os.path.splitext(rel)[1].lower());import re;stop_ev,t=_spinner_start('Menyiapkan pratinjau baris kode...');a_lines=content_lama.splitlines();b_lines=content_baru.splitlines();sm=difflib.SequenceMatcher(None,a_lines,b_lines);groups=list(sm.get_grouped_opcodes(3));total_plus=sum(j2-j1 for(tag,i1,i2,j1,j2)in sm.get_opcodes()if tag in('insert','replace'));total_minus=sum(i2-i1 for(tag,i1,i2,j1,j2)in sm.get_opcodes()if tag in('delete','replace'));_spinner_stop(stop_ev,t)
	if not groups:
		if capture:return['  (tidak ada perubahan)']
		print('  (tidak ada perubahan)');return
	num_width=max(len(str(len(a_lines))),len(str(len(b_lines))),4);term_cols=_term_size().columns;bar_w=max(20,min(term_cols-2,int(term_cols*.95)));content_w=max(term_cols-(num_width+7),20);B,R=f"[38;5;{C_BORDER}m",'\x1b[0m';out=[]
	def _pad(text,width):vis=_vlen(text);return text+' '*(width-vis)if vis<width else text
	def _print_line(num,code,kind,segments=None,ws_only=False):
		num_str=str(num).rjust(num_width)
		if segments:
			hl=[]
			for(seg_text,changed)in segments:hl.extend([changed]*len(seg_text))
		else:hl=[False]*len(code)
		synmap=_syntax_color_map(code,_lang)if _lang else None;ws_run=_trailing_ws_run(code)if kind in('add','ctx')else None;chunks=[code[i:i+content_w]for i in range(0,max(len(code),1),content_w)]or[''];hl_chunks=[hl[i:i+content_w]for i in range(0,max(len(hl),1),content_w)]or[[]]
		while len(hl_chunks)<len(chunks):hl_chunks.append([])
		for(idx,chunk)in enumerate(chunks):
			hlc=hl_chunks[idx]or[False]*len(chunk);base_off=idx*content_w
			if idx==0:
				if kind=='del':sym,sym_c=('≈','\x1b[1;38;5;244m')if ws_only else('-','\x1b[1;38;2;196;120;120m');gutter=f"[48;2;72;38;38m[1;38;2;214;190;190m {num_str} {sym_c}{sym}[0m"
				elif kind=='add':sym,sym_c=('≈','\x1b[1;38;5;244m')if ws_only else('+','\x1b[1;38;2;140;186;140m');gutter=f"[48;2;36;56;40m[1;38;2;196;214;196m {num_str} {sym_c}{sym}[0m"
				else:gutter=f"[38;5;240m {num_str}  [0m"
			else:
				blank=' '*num_width
				if kind=='del':gutter=f"[48;2;72;38;38m[1;38;2;214;190;190m {blank} [1;38;2;196;120;120m [0m"
				elif kind=='add':gutter=f"[48;2;36;56;40m[1;38;2;196;214;196m {blank} [1;38;2;140;186;140m [0m"
				else:gutter=f"[38;5;240m {blank}  [0m"
			if kind=='del':base='\x1b[48;2;72;38;38m\x1b[38;2;214;190;190m';hi='\x1b[48;2;140;44;44m\x1b[1;38;2;255;218;218m';bg_only='\x1b[48;2;72;38;38m'
			elif kind=='add':base='\x1b[48;2;36;56;40m\x1b[38;2;196;214;196m';hi='\x1b[48;2;38;122;62m\x1b[1;38;2;218;255;218m';bg_only='\x1b[48;2;36;56;40m'
			else:base='\x1b[38;5;250m';hi=base;bg_only=''
			ws_marker='\x1b[4;38;5;167m';pieces=[]
			for(pos,ch)in enumerate(chunk):
				on=hlc[pos]if pos<len(hlc)else False;abs_pos=base_off+pos;syn=synmap[abs_pos]if synmap and abs_pos<len(synmap)else None
				if ws_run and ws_run[0]<=abs_pos<ws_run[1]:color,disp=ws_marker,'·'
				elif on:color,disp=hi,ch
				elif syn:color,disp=bg_only+syn,ch
				else:color,disp=base,ch
				if pieces and pieces[-1][0]==color:pieces[-1]=color,pieces[-1][1]+disp
				else:pieces.append((color,disp))
			body_txt=''.join(color+text for(color,text)in pieces);pad_n=content_w-len(chunk);body=f"{base} {body_txt}{" "*max(0,pad_n)}[0m";out.append(f"  {gutter}{body}")
	stat_bar=_diff_stat_bar(total_plus,total_minus);out.append(f"\n  {B}┌{"─"*bar_w}┐{R}");out.append(f"  {B}│{R} [1;38;5;{C_CYAN}m✎ {rel}[0m");out.append(f"  {B}│{R} [1;38;5;46m+{total_plus}[0m baris ditambah   [1;38;5;203m-{total_minus}[0m baris dihapus   {stat_bar}");out.append(f"  {B}└{"─"*bar_w}┘{R}\n")
	for(gi,group)in enumerate(groups):
		if gi>0:prev_i2=groups[gi-1][-1][2];skip_n=max(0,group[0][1]-prev_i2);label=f"⋮ {skip_n} baris tidak berubah "if skip_n>0 else'⋮ ';dash_n=max(0,bar_w-1-len(label));out.append(f"  {B}  {label}{"─"*dash_n}{R}")
		for(tag,i1,i2,j1,j2)in group:
			if tag=='equal':
				for k in range(i2-i1):_print_line(j1+k+1,a_lines[i1+k],'ctx')
			elif tag=='delete':
				for k in range(i1,i2):_print_line(k+1,a_lines[k],'del')
			elif tag=='insert':
				for k in range(j1,j2):_print_line(k+1,b_lines[k],'add')
			elif tag=='replace':
				seg_del,seg_add,ws_del,ws_add={},{},{},{}
				if i2-i1==j2-j1:
					for k in range(i2-i1):
						old_l,new_l=a_lines[i1+k],b_lines[j1+k];o_segs,n_segs=_char_diff_segments(old_l,new_l)
						if o_segs is not None:seg_del[i1+k]=o_segs;seg_add[j1+k]=n_segs
						if old_l!=new_l and re.sub('\\s+','',old_l)==re.sub('\\s+','',new_l):ws_del[i1+k]=True;ws_add[j1+k]=True
				for k in range(i1,i2):_print_line(k+1,a_lines[k],'del',segments=seg_del.get(k),ws_only=ws_del.get(k,False))
				for k in range(j1,j2):_print_line(k+1,b_lines[k],'add',segments=seg_add.get(k),ws_only=ws_add.get(k,False))
	out.append('')
	if capture:return out
	print('\n'.join(out))
_SYN_CAT={'\x1b[38;5;176m':'kw','\x1b[38;5;180m':'str','\x1b[38;5;173m':'num','\x1b[38;5;242m':'cmt','\x1b[38;5;214m':'deco','\x1b[38;5;149m':'func','\x1b[38;5;222m':'cls','\x1b[38;5;80m':'blt','\x1b[38;5;110m':'tag','\x1b[38;5;115m':'attr','\x1b[38;5;204m':'sel','\x1b[38;5;150m':'prop'}
def build_diff_data(content_lama,content_baru,filepath):
	rel=os.path.relpath(filepath,SOURCE_ROOT);_lang={'.py':'python','.js':'javascript','.jsx':'javascript','.mjs':'javascript','.cjs':'javascript','.ts':'javascript','.tsx':'javascript','.html':'html','.htm':'html','.css':'css'}.get(os.path.splitext(rel)[1].lower());a_lines=content_lama.splitlines();b_lines=content_baru.splitlines();sm=difflib.SequenceMatcher(None,a_lines,b_lines);groups=list(sm.get_grouped_opcodes(3));total_plus=sum(j2-j1 for(tag,i1,i2,j1,j2)in sm.get_opcodes()if tag in('insert','replace'));total_minus=sum(i2-i1 for(tag,i1,i2,j1,j2)in sm.get_opcodes()if tag in('delete','replace'))
	if not groups:return{'rel':rel,'lang':_lang,'plus':0,'minus':0,'rows':[],'empty':True}
	def _tokens(code,kind,segments=None):
		if segments:
			hl=[]
			for(seg_text,changed)in segments:hl.extend([changed]*len(seg_text))
		else:hl=[False]*len(code)
		synmap=_syntax_color_map(code,_lang)if _lang else[None]*len(code);ws_run=_trailing_ws_run(code)if kind in('add','ctx')else None;toks=[]
		for(i,ch)in enumerate(code):
			if ws_run and ws_run[0]<=i<ws_run[1]:key='ws',False
			else:changed=hl[i]if i<len(hl)else False;cat=_SYN_CAT.get(synmap[i])if synmap and i<len(synmap)and synmap[i]else None;key=cat,changed
			if toks and toks[-1][0]==key:toks[-1]=key,toks[-1][1]+ch
			else:toks.append((key,ch))
		return[{'cat':None if k[0]=='ws'else k[0],'ws':k[0]=='ws','ch':k[1],'t':t}for(k,t)in toks]
	rows=[]
	for(gi,group)in enumerate(groups):
		if gi>0:prev_i2=groups[gi-1][-1][2];skip_n=max(0,group[0][1]-prev_i2);rows.append({'type':'sep','skip':skip_n})
		for(tag,i1,i2,j1,j2)in group:
			if tag=='equal':
				for k in range(i2-i1):rows.append({'type':'line','kind':'ctx','old_no':i1+k+1,'new_no':j1+k+1,'tokens':_tokens(a_lines[i1+k],'ctx')})
			elif tag=='delete':
				for k in range(i1,i2):rows.append({'type':'line','kind':'del','old_no':k+1,'new_no':None,'tokens':_tokens(a_lines[k],'del')})
			elif tag=='insert':
				for k in range(j1,j2):rows.append({'type':'line','kind':'add','old_no':None,'new_no':k+1,'tokens':_tokens(b_lines[k],'add')})
			elif tag=='replace':
				seg_del,seg_add={},{}
				if i2-i1==j2-j1:
					for k in range(i2-i1):
						old_l,new_l=a_lines[i1+k],b_lines[j1+k];o_segs,n_segs=_char_diff_segments(old_l,new_l)
						if o_segs is not None:seg_del[i1+k]=o_segs;seg_add[j1+k]=n_segs
				for k in range(i1,i2):rows.append({'type':'line','kind':'del','old_no':k+1,'new_no':None,'tokens':_tokens(a_lines[k],'del',segments=seg_del.get(k))})
				for k in range(j1,j2):rows.append({'type':'line','kind':'add','old_no':None,'new_no':k+1,'tokens':_tokens(b_lines[k],'add',segments=seg_add.get(k))})
	return{'rel':rel,'lang':_lang,'plus':total_plus,'minus':total_minus,'rows':rows,'empty':False}
def tampilkan_preview_pencarian(matched_content,filepath,r0,r1,rtype,line_no,ctx_n=4):
	import bisect;rel=os.path.relpath(filepath,SOURCE_ROOT);_lang={'.py':'python','.js':'javascript','.jsx':'javascript','.mjs':'javascript','.cjs':'javascript','.ts':'javascript','.tsx':'javascript','.html':'html','.htm':'html','.css':'css'}.get(os.path.splitext(rel)[1].lower());lines_no_end=matched_content.splitlines();n_total=len(lines_no_end);hl_ranges={}
	if rtype.startswith('head_tail'):
		match_start_idx=r0;match_end_idx=max(r0,r1-1)
		for i in range(match_start_idx,min(match_end_idx,n_total-1)+1):hl_ranges[i]=0,len(lines_no_end[i])
	else:
		offsets=[];pos=0
		for l in matched_content.splitlines(keepends=True):offsets.append(pos);pos+=len(l)
		end_pos=max(r0,r1-1);match_start_idx=max(0,bisect.bisect_right(offsets,r0)-1);match_end_idx=max(match_start_idx,bisect.bisect_right(offsets,end_pos)-1)
		for i in range(match_start_idx,min(match_end_idx,n_total-1)+1):line_off=offsets[i];line_text=lines_no_end[i];hl_ranges[i]=max(0,r0-line_off),max(0,min(len(line_text),r1-line_off))
	ctx_from=max(0,match_start_idx-ctx_n);ctx_to=min(n_total,match_end_idx+1+ctx_n);num_w=len(str(max(ctx_to,1)));term_cols=_term_size().columns;bar_w=max(20,min(term_cols-2,int(term_cols*.95)));content_w=max(term_cols-(num_w+6),20);B,R=f"[38;5;{C_BORDER}m",'\x1b[0m';HI='\x1b[48;2;110;84;18m\x1b[1;38;2;255;236;179m';BG_RESET='\x1b[49m';out=[];out.append(f"\n  {B}┌{"─"*bar_w}┐{R}");out.append(f"  {B}│{R} [1;38;5;{C_CYAN}m🔎 {rel}[0m");out.append(f"  {B}│{R} [38;5;244mkode cocok di baris {line_no}[0m");out.append(f"  {B}└{"─"*bar_w}┘{R}\n")
	if ctx_from>0:out.append(f"  [38;5;240m{"⋮":>{num_w+2}}[0m")
	for i in range(ctx_from,ctx_to):
		code=lines_no_end[i];is_match=i in hl_ranges;synmap=_syntax_color_map(code,_lang)if _lang else None;chunks=[code[k:k+content_w]for k in range(0,max(len(code),1),content_w)]or['']
		for(cidx,chunk)in enumerate(chunks):
			base_off=cidx*content_w;blank=' '*num_w
			if cidx==0:
				if is_match:gutter=f"[48;2;58;46;18m[1;38;2;255;214;120m {i+1:>{num_w}} »[0m"
				else:gutter=f"[38;5;240m {i+1:>{num_w}}  [0m"
			elif is_match:gutter=f"[48;2;58;46;18m[1;38;2;255;214;120m {blank} [0m"
			else:gutter=f"[38;5;240m {blank}  [0m"
			pieces=[]
			for(pos_c,ch)in enumerate(chunk):
				abs_pos=base_off+pos_c;syn=synmap[abs_pos]if synmap and abs_pos<len(synmap)else None
				if is_match and hl_ranges[i][0]<=abs_pos<hl_ranges[i][1]:color=HI
				elif syn:color=BG_RESET+syn
				else:color=BG_RESET+'\x1b[38;5;250m'
				if pieces and pieces[-1][0]==color:pieces[-1]=color,pieces[-1][1]+ch
				else:pieces.append((color,ch))
			body_txt=''.join(c+t for(c,t)in pieces);out.append(f"  {gutter} {body_txt}[0m")
	if ctx_to<n_total:out.append(f"  [38;5;240m{"⋮":>{num_w+2}}[0m")
	out.append('');print('\n'.join(out))
def ambil_konteks_file(find_text,content,n_lines=20):
	import re;lines=content.splitlines()
	if _has_ellipsis(find_text):head,_=_split_ellipsis(find_text);search_lines=head
	else:search_lines=[l.strip()for l in find_text.splitlines()if l.strip()]
	anchor=_match_lines(search_lines,[l.rstrip()for l in lines])
	if anchor!=-1:start=max(0,anchor-2);end=min(len(lines),anchor+n_lines);context='\n'.join(lines[start:end]);return anchor+1,context
	func_list=[];pattern=re.compile('^\\s*(async\\s+)?function\\s+\\w+|^\\s*(export\\s+)?(default\\s+)?(class|const|let|var)\\s+\\w+\\s*[=(]|^\\s*def\\s+\\w+|^\\s*[.#][\\w\\-]+[\\w\\-\\s:,>~+\\[\\]="\\\'\\.#]*\\{|^\\s*@(media|keyframes|font-face|layer|supports)[^{]*\\{|^\\s*[\\w\\-]+[\\w\\-\\s:,>~+\\[\\]="\\\'\\.#]*\\{(?!\\s*/)')
	for(i,line)in enumerate(lines,1):
		if pattern.match(line):func_list.append(f"  • {line.strip()[:70]}  (baris {i})")
	func_str='\n'.join(func_list[:20])if func_list else'  (tidak ada fungsi/class yang terdeteksi)';return None,func_str
def paste_patch(dry_run=False):
	sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();print();_pp_term_cols=_term_size().columns
	def _c(text):vlen=_vlen(text);pad=max(0,(_pp_term_cols-vlen)//2);return' '*pad+text
	_pp_safe_logo=[l[:max(10,_pp_term_cols-2)]for l in LOGO_PATCH];_pp_dir_short=SOURCE_ROOT if len(SOURCE_ROOT)<=48 else'…'+SOURCE_ROOT[-47:];_pp_buf=[]
	for l in gradient_ascii_lines(_pp_safe_logo,RGB_PATCH_DARK,RGB_PATCH_LIGHT):_pp_buf.append(_c(l))
	_pp_buf.append('')
	if dry_run:_pp_buf.append(_c('\x1b[48;5;234m\x1b[1;38;5;45m  ⚠  MODE DRY-RUN — Tidak ada file yang akan diubah  ⚠  \x1b[0m'));_pp_buf.append('')
	_pp_buf.append(_c(f"[38;5;244mDIR[0m [1;38;5;45m{_pp_dir_short}[0m"));_pp_buf.append('')
	if _amend_target_valid()and not dry_run:_pp_judul_amend=_git_head_subject()or'(tanpa pesan commit)';_pp_buf.append(_c(f'[48;5;234m[1;97m ⚠ PERUBAHAN INI AKAN MENGGANTIKAN COMMIT:[0m[48;5;234m[1;38;5;{C_VIOLET}m "{_pp_judul_amend}" [0m'));_pp_buf.append('')
	left_lines=['\x1b[1;38;5;215m:file\x1b[0m src/App.js','\x1b[1;38;5;215m:find\x1b[0m','kode lama','\x1b[1;38;5;215m:end_find\x1b[0m','\x1b[1;38;5;215m:replace\x1b[0m','kode baru','\x1b[1;38;5;215m:end_replace\x1b[0m'];right_lines=['\x1b[1;38;5;215m:file\x1b[0m src/New.js','\x1b[1;38;5;46m:new_file\x1b[0m','\x1b[1;38;5;215m:replace\x1b[0m','kode file baru','\x1b[1;38;5;215m:end_replace\x1b[0m'];is_side_by_side=_pp_term_cols>=66
	if is_side_by_side:
		while len(right_lines)<len(left_lines):right_lines.append('')
		while len(left_lines)<len(right_lines):left_lines.append('')
	W_BOX=27;left_box=['\x1b[1;38;5;215m▸ Format Edit File:\x1b[0m'];left_box.append(f"[38;5;208m┌{"─"*W_BOX}┐[0m")
	for text in left_lines:left_box.append(f"[38;5;208m│[0m {_pad_cell(text,W_BOX-1)}[38;5;208m│[0m")
	left_box.append(f"[38;5;208m└{"─"*W_BOX}┘[0m");right_box=['\x1b[1;38;5;46m▸ File Baru (:new_file):\x1b[0m'];right_box.append(f"[38;5;46m┌{"─"*W_BOX}┐[0m")
	for text in right_lines:right_box.append(f"[38;5;46m│[0m {_pad_cell(text,W_BOX-1)}[38;5;46m│[0m")
	right_box.append(f"[38;5;46m└{"─"*W_BOX}┘[0m")
	if is_side_by_side:
		for(l,r)in zip(left_box,right_box):_pp_buf.append(_c(_pad_cell(l,33)+r))
	else:
		for l in left_box:_pp_buf.append(_c(l))
		_pp_buf.append('')
		for r in right_box:_pp_buf.append(_c(r))
	_pp_buf.append('');info_lines=['\x1b[38;5;208m✎\x1b[0m Tambahkan \x1b[1;38;5;215m":title <judul>"\x1b[0m di baris paling atas patch agar jadi nama commit.','\x1b[38;5;244mFormat lama didukung:\x1b[0m \x1b[38;5;215m:replace/:end\x1b[0m dan \x1b[38;5;215m===FIND===/===REPLACE===\x1b[0m','\x1b[38;5;244mℹ Ketik DONE setelah selesai. Ketik Q atau Enter 2x untuk batal\x1b[0m','\x1b[1;38;5;46m✨ KETIK :clip UNTUK PASTE DARI CLIPBOARD (ANTI-LAG UNTUK KODE RIBUAN BARIS)\x1b[0m']
	for line in info_lines:_pp_buf.append(_c(line))
	_pp_buf.append('');_pp_buf.append(_c('\x1b[1;38;5;215m↓ SILAKAN PASTE (TEMPEL) KODE PATCH DI BAWAH INI ↓\x1b[0m'));_pp_sep_w=max(20,min(_pp_term_cols-2,74));_pp_buf.append(_c(f"[38;5;208m{"─"*_pp_sep_w}[0m"))
	for _pp_line in _pp_buf:print(_pp_line)
	lines=[];empty_count=0
	while True:
		try:
			line=sys.stdin.readline()
			if not line:break
			line=line.strip('\n')
		except(EOFError,KeyboardInterrupt):return
		stripped=line.strip()
		if stripped==':clip':
			try:
				r=subprocess.run(['termux-clipboard-get'],capture_output=True,text=True,timeout=5)
				if r.returncode==0 and r.stdout:lines.extend(r.stdout.splitlines());print(f"  [32m[+] Berhasil mengambil {len(r.stdout.splitlines())} baris dari clipboard.[0m");empty_count=0;continue
			except Exception:pass
			print('  \x1b[31m[!] Gagal membaca clipboard. Pastikan Termux:API terinstall.\x1b[0m');continue
		if stripped=='DONE':break
		if stripped.lower()in('exit','q','0','batal'):return
		lines.append(line)
		if stripped=='':
			empty_count+=1
			if empty_count>=2 and all(l.strip()==''for l in lines):return
			if empty_count==2:
				non_empty=[l for l in lines if l.strip()!='']
				if non_empty and non_empty[-1].strip().lower()in(':end_replace',':end'):break
		else:empty_count=0
	return'\n'.join(lines)
def popup_confirm(title,message_lines,options,default=0,layout='horizontal'):
	import shutil,sys;W_POP_MAX=54;sel_idx=default;sys.stdout.write('\x1b[?25l');sys.stdout.flush();BG_BOX='\x1b[48;5;234m';FG_TXT='\x1b[38;5;250m';FG_BDR='\x1b[38;5;239m';RST='\x1b[0m';btn_lines=len(options)if layout=='vertical'else 1;box_height=4+len(message_lines)+btn_lines;print('\n'*box_height,end='');_cleared_for_zoom=False
	while True:
		term_w,term_h=_term_size()
		if term_w<MIN_TERM_COLS or term_h<MIN_TERM_LINES:warn=['  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_w} kolom x {term_h} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) terminal...[0m"];sys.stdout.write('\n'*term_h+f"[{len(warn)+2}A\r[?2026h\n"+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();_cleared_for_zoom=True;get_key();continue
		w_pop=min(W_POP_MAX,term_w-4)
		if w_pop<20:w_pop=20
		if box_height>=term_h or _cleared_for_zoom:print('\n'*box_height,end='');_cleared_for_zoom=False
		sys.stdout.write(f"[{box_height}A\r");buf=[];pad_global=' '*max(2,(term_w-(w_pop+2))//2);buf.append(f"{pad_global}{BG_BOX}{FG_BDR}┌{"─"*w_pop}┐{RST}[K");clean_title=_ANSI_RE.sub('',title)
		if len(clean_title)>w_pop-4:clean_title=clean_title[:w_pop-7]+'...'
		pad_l=(w_pop-len(clean_title))//2;pad_r=w_pop-len(clean_title)-pad_l;t_color='\x1b[1;38;5;220m'if'⚠'in title or'PERINGATAN'in title else'\x1b[1;38;5;255m';buf.append(f"{pad_global}{BG_BOX}{FG_BDR}│{BG_BOX}{" "*pad_l}{t_color}{clean_title}{BG_BOX}{" "*pad_r}{FG_BDR}│{RST}[K")
		for line in message_lines:
			clean_line=_ANSI_RE.sub('',line)
			if len(clean_line)>w_pop-2:line=clean_line[:w_pop-5]+'...';clean_line=line
			pad_r=max(0,w_pop-len(clean_line)-2);styled_line=line.replace('\x1b[',f"{BG_BOX}[")if'\x1b['in line else f"{FG_TXT}{line}";buf.append(f"{pad_global}{BG_BOX}{FG_BDR}│ {BG_BOX}{styled_line}{BG_BOX}{" "*pad_r} {FG_BDR}│{RST}[K")
		buf.append(f"{pad_global}{BG_BOX}{FG_BDR}│{BG_BOX}{" "*w_pop}{FG_BDR}│{RST}[K")
		if layout=='vertical':
			_max_label=max(len(text)for(_,text)in options);_btn_vis=_max_label+4;_pad_l_btn=max(0,(w_pop-_btn_vis)//2);_pad_r_btn=max(0,w_pop-_btn_vis-_pad_l_btn)
			for(i,(ret,text))in enumerate(options):
				label=text.ljust(_max_label)
				if i==sel_idx:btn=f"[48;2;110;60;35m[1;38;2;230;210;255m ❯ {label} [0m"
				else:btn=f"[48;5;238m[38;5;244m   {label} [0m"
				buf.append(f"{pad_global}{BG_BOX}{FG_BDR}│{BG_BOX}{" "*_pad_l_btn}{btn}{BG_BOX}{" "*_pad_r_btn}{FG_BDR}│{RST}[K")
		else:
			btns=[];vis_len=0
			for(i,(ret,text))in enumerate(options):
				label=f" {text} "
				if i==sel_idx:btn=f"[48;2;110;60;35m[1;38;2;230;210;255m{label}[0m"
				else:btn=f"[48;5;238m[38;5;244m{label}[0m"
				btns.append(btn);vis_len+=len(text)+2
			gap_count=max(0,len(options)-1);gap=f"{BG_BOX}   ";vis_len+=gap_count*3;_pad_l_btn=max(0,(w_pop-vis_len)//2);_pad_r_btn=max(0,w_pop-vis_len-_pad_l_btn);btns_str=gap.join(btns);buf.append(f"{pad_global}{BG_BOX}{FG_BDR}│{BG_BOX}{" "*_pad_l_btn}{btns_str}{BG_BOX}{" "*_pad_r_btn}{FG_BDR}│{RST}[K")
		buf.append(f"{pad_global}{BG_BOX}{FG_BDR}└{"─"*w_pop}┘{RST}[K");sys.stdout.write('\n'.join(buf)+'\n');sys.stdout.flush();k=get_key()
		if k in('UP','LEFT'):sel_idx=(sel_idx-1)%len(options)
		elif k in('DOWN','RIGHT'):sel_idx=(sel_idx+1)%len(options)
		elif k=='ENTER':break
		elif k in('q','Q','ESC'):sel_idx=len(options)-1;break
		else:
			for(i,(ret,_))in enumerate(options):
				if k.lower()==str(ret).lower():
					sel_idx=i;sys.stdout.write(f"[{box_height}A\r")
					for _ in range(box_height):sys.stdout.write('\x1b[K\n')
					sys.stdout.write(f"[{box_height}A\r");sys.stdout.write('\x1b[?25h');sys.stdout.flush();return options[i][0]
	sys.stdout.write(f"[{box_height}A\r")
	for _ in range(box_height):sys.stdout.write('\x1b[K\n')
	sys.stdout.write(f"[{box_height}A\r");sys.stdout.write('\x1b[?25h');sys.stdout.flush();return options[sel_idx][0]
def _confirm_far_anchor(head_idx,tail_idx,find_lines,content_lines,block_label):gap=tail_idx-head_idx;preview=[];preview.extend(content_lines[head_idx:head_idx+2]);preview.append(f"   ⋮  ({max(0,gap-4)} baris di tengah ikut terganti)");preview.extend(content_lines[max(head_idx+2,tail_idx-2):tail_idx+2]);msg_lines=[f"Blok #{block_label}: jarak head-tail {gap} baris",f"(toleransi aman cuma {AUTO_ANCHOR_TOLERANCE} baris).",'Preview area yang akan ikut diganti:'];msg_lines+=[f"  {l.strip()[:44]}"for l in preview];pilih=popup_confirm('⚠️ JARAK ANCHOR JAUH',msg_lines,[('y','Ya, Lanjutkan'),('n','Batalkan Blok Ini')]);return pilih=='y'
HEAD_TAIL_CONFIRM_THRESHOLD=15
def _confirm_head_tail_skip(result,content,block_label):
	line_start,line_end,_=result;content_lines=content.splitlines();skip_count=max(0,line_end-line_start)
	if skip_count<=HEAD_TAIL_CONFIRM_THRESHOLD:return True
	preview=content_lines[line_start:line_start+2];preview.append(f"   ⋮  ({skip_count-4} baris di tengah ikut diganti/terhapus)");preview+=content_lines[max(line_start+2,line_end-2):line_end];msg_lines=[f"Blok #{block_label}: format head...tail akan mengganti",f"total {skip_count} baris (termasuk bagian tengah yang di-skip).",'Preview area yang akan diganti:'];msg_lines+=[f"  {l.strip()[:44]}"for l in preview];pilih=popup_confirm('⚠️ CEK SKIP HEAD...TAIL',msg_lines,[('y','Ya, Lanjutkan'),('n','Batalkan Blok Ini')]);return pilih=='y'
def _confirm_fuzzy_block(best_score,best_i,w_size,content_lines,block_label,reason):preview=content_lines[best_i:best_i+min(4,w_size)];msg_lines=[f"Blok #{block_label}: Fuzzy Block cocok {best_score:.0%} ({reason}).",'Preview lokasi yang akan diganti:'];msg_lines+=[f"  {l.strip()[:44]}"for l in preview];pilih=popup_confirm('⚠️ FUZZY BLOCK PERLU KONFIRMASI',msg_lines,[('y','Ya, Lanjutkan'),('n','Batalkan Blok Ini')]);return pilih=='y'
def _validate_python_syntax(filepath,new_content):
	if not filepath.endswith('.py'):return True,None
	try:compile(new_content,filepath,'exec');return True,None
	except SyntaxError as e:return False,f"SyntaxError baris {e.lineno}: {e.msg}"
def _snapshot_backup_self(preview_map):
	ts=datetime.now().strftime('%Y%m%d_%H%M%S');snap_root=os.path.join(SOURCE_ROOT,'.patch_backups','snapshot');snap_dir=os.path.join(snap_root,ts)
	try:
		for(filepath,(orig_content,_new))in preview_map.items():
			rel=os.path.relpath(filepath,SOURCE_ROOT);dst=os.path.join(snap_dir,rel);os.makedirs(os.path.dirname(dst),exist_ok=True)
			with open(dst,'w',encoding='utf-8')as f:f.write(orig_content)
	except Exception as e:print(f"  [33m[PERINGATAN][0m Gagal membuat snapshot backup fisik: {e}");return
	try:
		semua=sorted(os.listdir(snap_root))
		for lama in semua[:-15]:shutil.rmtree(os.path.join(snap_root,lama),ignore_errors=True)
	except Exception:pass
	return snap_dir
def _ensure_rescue_script():
	path=os.path.join(SOURCE_ROOT,'pulihkan_darurat.py');content='#!/usr/bin/env python3\n"""Pemulihan darurat FR Tool.\n\nBerdiri sendiri, TIDAK mengimpor apapun dari frtool.py — supaya tetap bisa\ndipakai walau frtool.py sendiri rusak/gagal start.\n\nCara pakai (dari Termux, di folder ini):\n    python3 pulihkan_darurat.py\n"""\nimport os, shutil\n\nROOT = os.path.dirname(os.path.abspath(__file__))\nBACKUP_ROOT = os.path.join(ROOT, ".patch_backups", "snapshot")\n\n\ndef main():\n    if not os.path.isdir(BACKUP_ROOT):\n        print("Belum ada folder snapshot backup:", BACKUP_ROOT)\n        return\n    snaps = sorted(os.listdir(BACKUP_ROOT), reverse=True)\n    if not snaps:\n        print("Belum ada snapshot backup tersimpan.")\n        return\n    print("Snapshot tersedia (paling baru di atas):\\n")\n    for i, s in enumerate(snaps):\n        print(f"  [{i}] {s}")\n    try:\n        pilih = input("\\nPilih nomor snapshot untuk dipulihkan (Enter = 0/terbaru): ").strip()\n    except (EOFError, KeyboardInterrupt):\n        return\n    idx = int(pilih) if pilih else 0\n    if idx < 0 or idx >= len(snaps):\n        print("Nomor tidak valid.")\n        return\n    src_dir = os.path.join(BACKUP_ROOT, snaps[idx])\n    restored = 0\n    for dirpath, _dirs, files in os.walk(src_dir):\n        for fn in files:\n            src = os.path.join(dirpath, fn)\n            rel = os.path.relpath(src, src_dir)\n            dst = os.path.join(ROOT, rel)\n            os.makedirs(os.path.dirname(dst) or ROOT, exist_ok=True)\n            shutil.copy2(src, dst)\n            print("  [OK] dipulihkan:", rel)\n            restored += 1\n    print(f"\\nSelesai. {restored} file dipulihkan dari snapshot {snaps[idx]}.")\n\n\nif __name__ == "__main__":\n    main()\n'
	try:
		existing=None
		if os.path.exists(path):
			with open(path,'r',encoding='utf-8')as f:existing=f.read()
		if existing!=content:
			with open(path,'w',encoding='utf-8')as f:f.write(content)
	except Exception:pass
def tanya_mode_replace(count,label):print(f"  [PERHATIAN] Blok #{label} ditemukan sebanyak {count} kali dalam file ini.");print(f"      [A] Ganti semua kemunculan   [S] Ganti hanya yang pertama");print('      Pilihan Anda: ',end='');jawab=input().strip().upper();return'all'if jawab=='A'else'first'
def _is_path_inside_root(path):
	try:root=os.path.realpath(SOURCE_ROOT);target=os.path.realpath(path);return target==root or target.startswith(root+os.sep)
	except Exception:return False
def _resolve_create_dir(filename):
	clean=filename.replace('\\','/').lstrip('/');parts=[p for p in clean.split('/')if p not in('','.','..')]
	if not parts:return SOURCE_ROOT,filename
	base=parts[-1];target_dir_parts=parts[:-1]
	if not target_dir_parts:return SOURCE_ROOT,base
	existing_dirs=['']
	for(dirpath,dirnames,_files)in os.walk(SOURCE_ROOT):dirnames[:]=[d for d in dirnames if d not in IGNORE_DIRS];rel=os.path.relpath(dirpath,SOURCE_ROOT);existing_dirs.append(''if rel=='.'else rel.replace('\\','/'))
	target_dir_str='/'.join(target_dir_parts)
	if target_dir_str in existing_dirs:return os.path.join(SOURCE_ROOT,target_dir_str),base
	best_score=0;scores={}
	for cand in existing_dirs:
		cand_parts=[p for p in cand.split('/')if p];score=0
		for(a,b)in zip(reversed(target_dir_parts),reversed(cand_parts)):
			if a.lower()==b.lower():score+=1
			else:break
		scores[cand]=score
		if score>best_score:best_score=score
	best_dirs=[d for(d,s)in scores.items()if s==best_score]
	if best_score>0 and len(best_dirs)==1:return os.path.join(SOURCE_ROOT,best_dirs[0]),base
	cands=best_dirs if best_score>0 else existing_dirs;cands.sort(key=lambda x:(x.count('/'),x.lower()));sel=0
	while True:
		hint='↑↓ Pilih  ·  Enter Konfirmasi  ·  Esc Batal'
		if best_score>0:judul='FOLDER TUJUAN MERAGUKAN (TIE)';extra=[f"[33mFolder tujuan tidak bisa dipastikan secara otomatis.[0m",f"Path dari AI: [36m{target_dir_str}[0m",f"Pilih salah satu dari {len(cands)} kecocokan terdekat:"]
		else:judul='FOLDER TUJUAN TIDAK DITEMUKAN';extra=[f"[31mPath dari AI sama sekali tidak mirip dengan folder project.[0m",f"Path dari AI: [36m{target_dir_str}[0m",f"Pilih folder tujuan yang tepat:"]
		_draw_pilih_list(sel,cands,judul,hint,lambda i,d:f"📁 {d}/"if d else'📁 / (Root Project)',extra_top=extra);k=get_key(animate=True)
		if k=='ANIMATE'or k=='RESIZE':continue
		if k=='UP':sel=(sel-1)%len(cands)
		elif k=='DOWN':sel=(sel+1)%len(cands)
		elif k=='ENTER':sys.stdout.write('\x1b[2J\x1b[H');sys.stdout.flush();return os.path.join(SOURCE_ROOT,cands[sel]),base
		elif k in('ESC','q','Q','0'):sys.stdout.write('\x1b[2J\x1b[H');sys.stdout.flush();return None,base
def _resolve_path_by_suffix(filename,root):
	target_parts=[p for p in filename.replace('\\','/').split('/')if p]
	if not target_parts:return[]
	base=target_parts[-1];hasil=[]
	for(dirpath,dirs,files)in os.walk(root):
		dirs[:]=[d for d in dirs if d not in IGNORE_DIRS]
		for fname in files:
			if fname!=base:continue
			full=os.path.join(dirpath,fname);rel=os.path.relpath(full,root);rel_parts=rel.replace('\\','/').split('/')
			if rel_parts[-len(target_parts):]==target_parts:hasil.append(rel)
	return hasil
def scan_dan_apply(patch_text,dry_run=False):
	import time;global _GLOBAL_TIMER_START;start_time=time.time();_GLOBAL_TIMER_START=start_time;clear();_sa_term_cols=_term_size().columns;_sa_sep_w=max(20,min(_sa_term_cols-2,int(_sa_term_cols*.95)));file_patches=parse_patch(patch_text);_patch_title=_extract_patch_title(patch_text)
	if not file_patches:print('[GAGAL] Tidak ada blok patch yang valid ditemukan.');print();print('Pastikan patch menggunakan salah satu format berikut:');print('  :find / :replace / :end');print('  atau format lama: ===FIND=== ===REPLACE=== ===END===');input('\nTekan Enter untuk kembali ke menu...');return
	if _df_bit[0]or not _rc_ok():print('[GAGAL] Terjadi kesalahan internal.');input('\nTekan Enter untuk kembali ke menu...');return
	if dry_run:header('Hasil Analisis \x1b[33m[MODE DRY-RUN]\x1b[0m')
	else:header('Hasil Analisis')
	all_ok=True;plan=[];failed_blocks=[];_proj_cache_ref=[None]
	def _get_proj_cache():
		if _proj_cache_ref[0]is None:_proj_cache_ref[0]=_build_project_cache(SOURCE_ROOT)
		return _proj_cache_ref[0]
	_claimed_matches={}
	for(filename,pairs)in file_patches.items():
		auto_mode=filename=='__AUTO__';print(f"📄 {"[Deteksi otomatis file]"if auto_mode else filename}")
		if not auto_mode and not _is_path_inside_root(os.path.join(SOURCE_ROOT,filename)):print(f"  [31m[DITOLAK][0m Path [1m{filename}[0m mengarah KELUAR folder project — dianggap tidak valid, semua blok di file ini dilewati.");log_fail_event(0,'path_outside_project',filename);all_ok=False;continue
		content,path_ok,filepath='',False,None
		if not auto_mode:
			filepath=os.path.join(SOURCE_ROOT,filename);path_ok=os.path.exists(filepath)
			if path_ok:
				with open(filepath,'r',encoding='utf-8')as f:content=f.read()
			else:
				suffix_hits=_resolve_path_by_suffix(filename,SOURCE_ROOT)
				if len(suffix_hits)==1:
					filepath=os.path.join(SOURCE_ROOT,suffix_hits[0])
					with open(filepath,'r',encoding='utf-8')as f:content=f.read()
					path_ok=True;_claimed_matches[suffix_hits[0]]=filename;print(f"  [36m[Auto-Resolve][0m Path header tidak persis, dicocokkan via nama file ke: [1m{suffix_hits[0]}[0m")
				else:print(f"  [INFO] Path tidak ditemukan, mencari di seluruh direktori...")
		total_pairs_in_file=len(pairs)
		for(i,(find,replace))in enumerate(pairs,1):
			print(f"  [38;5;244m— Memproses blok {i}/{total_pairs_in_file} —[0m");find_stripped=find.strip('\n');replace_stripped=replace.strip('\n');matched_file=None;match_type='exact';match_line_no=None;replace_mode='first';matched_content='';context_for_fail=None;final_match_result=None
			def _line_from_result(res,content_str):
				if res is None:return
				if res[2].startswith('head_tail'):return res[0]+1
				return content_str[:res[0]].count('\n')+1
			is_explicit_new=find_stripped=='__NEW_FILE__'
			if is_explicit_new:
				new_dir,new_base=_resolve_create_dir(filename)
				if new_dir is None:print(f"  [31m[BATAL][0m Auto-Create dibatalkan oleh user.");log_fail_event(i,'auto_create_cancelled',filename);failed_blocks.append((filename,find_stripped,replace_stripped,context_for_fail));all_ok=False;continue
				new_filepath=os.path.join(new_dir,new_base)
				if not _is_path_inside_root(new_filepath):print(f"  [31m[DITOLAK][0m Auto-Create dibatalkan — target di luar folder project: [1m{filename}[0m");print(f"  [GAGAL] Blok #{i} — File baru ditolak.");log_fail_event(i,'auto_create_outside_project',filename);failed_blocks.append((filename,find_stripped,replace_stripped,context_for_fail));all_ok=False;continue
				rel_new=os.path.relpath(new_filepath,SOURCE_ROOT);print(f"  [36m[Auto-Create][0m File baru akan dibuat (via :new_file): [1;36m{rel_new}[0m");matched_file=new_filepath;matched_content='';match_type='new_file';match_line_no=None;final_match_result=0,0,'new_file';find_stripped='';filepath=new_filepath;path_ok=True;content=replace_stripped
			else:
				if path_ok:
					stop_ev_m0,t_m0=_spinner_start(f"Mencocokkan blok #{i}/{len(pairs)}...",color='214');result=find_in_content(find_stripped,content,block_label=i);_spinner_stop(stop_ev_m0,t_m0)
					if result and result[2]=='auto_anchor_confirm':
						h_idx,t_idx,_=result
						if _confirm_far_anchor(h_idx,t_idx,find_stripped.splitlines(),content.splitlines(),i):result=h_idx,t_idx,'auto_anchor'
						else:result=None
					if result and result[2].startswith('head_tail'):
						if not _confirm_head_tail_skip(result,content,i):result=None
					if result:_,_,match_type=result;match_line_no=_line_from_result(result,content);matched_file=filepath;matched_content=content;final_match_result=result
					else:context_for_fail=filepath,content;print(f"  [33m[Fallback 1: Directory Scan][0m Blok #{i} tidak cocok di file target, memindai seluruh folder...")
				if matched_file is None:
					stop_ev_sc,t=_spinner_start(f"Menjalankan Fallback 1 (Exact/Fuzzy/Regex) untuk blok #{i}/{len(pairs)}...");raw_matches=cari_file_berisi_kode(find_stripped,cache=_get_proj_cache());_spinner_stop(stop_ev_sc,t);matches=[m for m in raw_matches if _claimed_matches.get(m,filename)==filename]
					if not matches:matches=raw_matches
					if len(matches)==1:
						temp_file=os.path.join(SOURCE_ROOT,matches[0])
						with open(temp_file,'r',encoding='utf-8')as f:temp_content=f.read()
						stop_ev_m1,t_m1=_spinner_start(f"Mencocokkan blok #{i}/{len(pairs)} di {matches[0]}...",color='214');result=find_in_content(find_stripped,temp_content,block_label=i);_spinner_stop(stop_ev_m1,t_m1)
						if result and result[2]=='auto_anchor_confirm':
							h_idx,t_idx,_=result
							if _confirm_far_anchor(h_idx,t_idx,find_stripped.splitlines(),temp_content.splitlines(),i):result=h_idx,t_idx,'auto_anchor'
							else:result=None
						if result and result[2].startswith('head_tail'):
							if not _confirm_head_tail_skip(result,temp_content,i):result=None
						if result:matched_file=temp_file;matched_content=temp_content;match_type=result[2];match_line_no=_line_from_result(result,matched_content);final_match_result=result;_claimed_matches[matches[0]]=filename
						else:context_for_fail=temp_file,temp_content
					elif len(matches)>1:
						print(f"  [33m[PILIHAN][0m Blok #{i} ditemukan di [1m{len(matches)}[0m file berbeda:")
						for(j,m)in enumerate(matches,1):tag=' \x1b[38;5;244m(sudah dipakai utk file lain)\x1b[0m'if m in _claimed_matches else'';print(f"      [36m[{j}][0m {m}{tag}")
						print(f"      [36m[A][0m SEMUA — terapkan blok ini ke file yang kodenya [1mbenar-benar identik[0m (exact match saja)");print('      Masukkan nomor file yang dituju (atau A untuk semua): ',end='')
						try:
							pilih_raw=input().strip()
							if pilih_raw.lower()in('a','semua','all'):
								ga_matched,ga_skipped=[],[]
								for m in matches:
									temp_file=os.path.join(SOURCE_ROOT,m)
									try:
										with open(temp_file,'r',encoding='utf-8')as f:temp_content=f.read()
									except Exception:ga_skipped.append((m,'gagal dibaca'));continue
									if find_stripped not in temp_content:ga_skipped.append((m,'kode tidak identik'));continue
									ga_matched.append((m,temp_file,temp_content))
								print(f"\n  [36m[GANTI SEMUA][0m Blok #{i} — hasil deteksi exact match:")
								for(_gm,_gf,_gc)in ga_matched:print(f"      [32m[✓][0m {_gm}")
								for(_gm,_alasan)in ga_skipped:print(f"      [33m[✗][0m {_gm} [38;5;244m({_alasan})[0m")
								if not ga_matched:print(f"  [31m[GAGAL][0m Tidak ada file dengan exact match — blok #{i} dilewati.");all_ok=False;continue
								print(f"  [1mTerapkan ke [38;5;46m{len(ga_matched)}[0m[1m file di atas? [Y/n]: [0m",end='');ga_confirm=input().strip().lower()
								if ga_confirm not in('','y','ya'):print(f"  [33m[BATAL][0m Ganti semua dibatalkan — blok #{i} dilewati.");all_ok=False;continue
								applied_n=0
								for(_gm,_gf,_gc)in ga_matched:ga_st=_gc.find(find_stripped);ga_en=ga_st+len(find_stripped);plan.append((_gf,find_stripped,replace_stripped,'first',_gc,'exact',ga_st,ga_en));_claimed_matches[_gm]=filename;applied_n+=1
								print(f"  [36m[GANTI SEMUA][0m Blok #{i} → [1m{applied_n}[0m file diterapkan.");continue
							pilih=int(pilih_raw);temp_file=os.path.join(SOURCE_ROOT,matches[pilih-1])
							with open(temp_file,'r',encoding='utf-8')as f:temp_content=f.read()
							stop_ev_m2,t_m2=_spinner_start(f"Mencocokkan blok #{i}/{len(pairs)} di {matches[pilih-1]}...",color='214');result=find_in_content(find_stripped,temp_content,block_label=i);_spinner_stop(stop_ev_m2,t_m2)
							if result and result[2]=='auto_anchor_confirm':
								h_idx,t_idx,_=result
								if _confirm_far_anchor(h_idx,t_idx,find_stripped.splitlines(),temp_content.splitlines(),i):result=h_idx,t_idx,'auto_anchor'
								else:result=None
							if result and result[2].startswith('head_tail'):
								if not _confirm_head_tail_skip(result,temp_content,i):result=None
							if result:matched_file=temp_file;matched_content=temp_content;match_type=result[2];match_line_no=_line_from_result(result,matched_content);final_match_result=result;_claimed_matches[matches[pilih-1]]=filename
							else:context_for_fail=temp_file,temp_content
						except:print(f"  [31m[GAGAL][0m Blok #{i} — Pilihan tidak valid, blok dilewati.");all_ok=False;continue
					if matched_file is None:
						if context_for_fail is None and not auto_mode:
							try:
								with open(os.path.join(SOURCE_ROOT,filename),'r',encoding='utf-8')as f:context_for_fail=os.path.join(SOURCE_ROOT,filename),f.read()
							except:pass
						if context_for_fail is None:
							stop_ev_p,tp=_spinner_start('Menjalankan Fallback 2: Partial Token Scan (Mencari file yang paling mirip)...',color='129');partial_hits=cari_file_partial(find_stripped,cache=_get_proj_cache());_spinner_stop(stop_ev_p,tp)
							if partial_hits:
								best_fp,best_score,best_block,best_rel=partial_hits[0];print(f"  [35m[Fallback 2: Partial Scan][0m Kandidat terdekat: [1;36m{best_rel}[0m [38;5;129m[Token Similarity: {best_score:.0%}][0m")
								try:
									with open(best_fp,'r',encoding='utf-8')as f:context_for_fail=best_fp,f.read()
								except:pass
							else:print(f"  [33m[Fallback 2: Partial Scan][0m Tidak ada kandidat file yang mirip ditemukan.")
						if matched_file is None and context_for_fail is not None:
							cand_fp,cand_content=context_for_fail;stop_ev_fb,t_fb=_spinner_start(f"Menjalankan Fuzzy Block Matcher untuk blok #{i}/{len(pairs)}...",color='214');cand_result=find_in_content(find_stripped,cand_content,block_label=i);_spinner_stop(stop_ev_fb,t_fb)
							if cand_result and cand_result[2]=='auto_anchor_confirm':
								h_idx,t_idx,_=cand_result
								if _confirm_far_anchor(h_idx,t_idx,find_stripped.splitlines(),cand_content.splitlines(),i):cand_result=h_idx,t_idx,'auto_anchor'
								else:cand_result=None
							if cand_result and cand_result[2].startswith('head_tail'):
								if not _confirm_head_tail_skip(cand_result,cand_content,i):cand_result=None
							if cand_result:matched_file=cand_fp;matched_content=cand_content;match_type=cand_result[2];match_line_no=_line_from_result(cand_result,matched_content);final_match_result=cand_result
						if matched_file is None:
							if not auto_mode and not path_ok and context_for_fail is None:
								new_dir,new_base=_resolve_create_dir(filename)
								if new_dir is None:print(f"  [31m[BATAL][0m Auto-Create dibatalkan oleh user.");log_fail_event(i,'auto_create_cancelled',filename);failed_blocks.append((filename,find_stripped,replace_stripped,context_for_fail));all_ok=False;continue
								new_filepath=os.path.join(new_dir,new_base)
								if not _is_path_inside_root(new_filepath):
									print(f"  [31m[DITOLAK][0m Auto-Create dibatalkan — target di luar folder project: [1m{filename}[0m");print(f"  [GAGAL] Blok #{i} — Kode tidak ditemukan di file manapun.")
									for pl in find_stripped.splitlines():print(f"          │ {pl}")
									log_fail_event(i,'auto_create_outside_project',filename);failed_blocks.append((filename,find_stripped,replace_stripped,context_for_fail));all_ok=False;continue
								rel_new=os.path.relpath(new_filepath,SOURCE_ROOT);print(f"  [36m[Auto-Create][0m File belum ada di project — akan dibuat baru: [1;36m{rel_new}[0m");matched_file=new_filepath;matched_content='';match_type='new_file';match_line_no=None;final_match_result=0,0,'new_file';find_stripped='';filepath=new_filepath;path_ok=True;content=replace_stripped
							else:
								print(f"  [GAGAL] Blok #{i} — Kode tidak ditemukan di file manapun.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m")
								for pl in find_stripped.splitlines():print(f"          │ {pl}")
								log_fail_event(i,'not_found_in_project',filename);failed_blocks.append((filename,find_stripped,replace_stripped,context_for_fail));all_ok=False;continue
			if match_type.startswith('head_tail'):replace_mode='first'
			else:
				count_exact=matched_content.count(find_stripped);count_total=count_exact if count_exact>0 else 1
				if count_total>1:replace_mode=tanya_mode_replace(count_total,i)
				else:replace_mode='first'
			if match_type=='exact':method_label=' \x1b[38;5;46m[Exact Match]\x1b[0m'
			elif match_type=='regex':method_label=' \x1b[38;5;39m[Regex Whitespace-Agnostic]\x1b[0m'
			elif match_type=='fuzzy':method_label=' \x1b[33m[Smart Fuzzy Match]\x1b[0m'
			elif match_type=='head_tail':_htres=find_head_tail(find_stripped,matched_content);_skip_n=_htres[1]-_htres[0]if _htres else 0;method_label=f" [35m[Exact Head...Tail, ~{_skip_n} baris][0m"
			elif match_type=='head_tail_fuzzy':_htres=find_head_tail(find_stripped,matched_content);_skip_n=_htres[1]-_htres[0]if _htres else 0;method_label=f" [38;5;208m[Fuzzy 70% Head...Tail, ~{_skip_n} baris][0m"
			elif match_type=='auto_anchor':method_label=' \x1b[38;5;208m[Smart Auto-Anchor]\x1b[0m'
			elif match_type=='fuzzy_block':method_label=' \x1b[38;5;214m[Fuzzy Block >80%]\x1b[0m'
			elif match_type=='new_file':method_label=' \x1b[38;5;46m[File Baru — Auto-Create]\x1b[0m'
			else:method_label=f" [38;5;244m[{match_type}][0m"
			rel=os.path.relpath(matched_file,SOURCE_ROOT);line_label=f" [33m(baris {match_line_no})[0m"if match_line_no else'';print(f"  [32m[OK][0m Blok [1m#{i}[0m → [1;36m{rel}[0m{line_label}{method_label}");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");c_st,c_en=0,0
			if final_match_result:
				st,en,mt=final_match_result
				if mt.startswith('head_tail')or mt.startswith('auto_anchor'):lines_k=matched_content.splitlines(keepends=True);c_st=sum(len(l)for l in lines_k[:st]);c_en=sum(len(l)for l in lines_k[:en])
				else:c_st,c_en=st,en
			plan.append((matched_file,find_stripped,replace_stripped,replace_mode,matched_content,match_type,c_st,c_en));print()
	print('─'*_sa_sep_w);ai_fixed_pairs=[];ai_fixed_indices=set()
	if failed_blocks:
		print(f"\n  [33m[PERINGATAN][0m {len(failed_blocks)} blok patch gagal — kode tidak ditemukan di project.");cfg=load_ai_config();ai_tersedia=bool(cfg.get('api_key','').strip())
		if ai_tersedia:mau_ai=popup_confirm('AI AUTO-FIX TERSEDIA',['Ada blok yang gagal ditemukan di file proyek.','Mau coba gunakan AI untuk mencari kode aslinya?'],[('y','Ya, Gunakan AI'),('n','Tidak, Lewati')])=='y'
		else:mau_ai=False;print(f"  [TIP] Aktifkan AI di menu [6] agar blok gagal diperbaiki otomatis.")
		if mau_ai:
			import threading,time
			for(fi,(fname,find_text,replace_text,ctx))in enumerate(failed_blocks,1):
				print(f"\n  [36m[Fallback 3: AI Semantic Fix][0m Menganalisis file untuk blok #{fi}...")
				if ctx:ai_filepath,ai_file_content=ctx
				elif fname!='__AUTO__':
					ai_filepath=os.path.join(SOURCE_ROOT,fname)
					if os.path.exists(ai_filepath):
						with open(ai_filepath,'r',encoding='utf-8')as f:ai_file_content=f.read()
					else:ai_file_content=''
				else:ai_filepath=None;ai_file_content=''
				if not ai_file_content:print(f"  [31m[AI GAGAL][0m Tidak ada konten file untuk dikirim ke AI. Blok #{fi} dilewati.");continue
				stop_ev_ai,t=_spinner_start('Menjalankan AI Semantic Matcher...',color='215');fixed_find,err=ai_fix_find(find_text,replace_text,ai_file_content,fname);_spinner_stop(stop_ev_ai,t)
				if err:print(f"  [31m[AI ERROR][0m {err}");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");continue
				if not fixed_find:print(f"  [31m[AI][0m AI mengembalikan respons kosong.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");log_fail_event(fi,'ai_fix_empty',fname);continue
				def extract_real_code(ai_ans,text_asli):
					import re;ai_norm=re.sub('\\s+','',ai_ans)
					if not ai_norm:return
					file_norm='';mapping=[]
					for(i,char)in enumerate(text_asli):
						if not char.isspace():file_norm+=char;mapping.append(i)
					idx=file_norm.find(ai_norm)
					if idx!=-1:start_orig=mapping[idx];end_orig=mapping[idx+len(ai_norm)-1]+1;return text_asli[start_orig:end_orig]
				real_fixed_find=extract_real_code(fixed_find,ai_file_content)
				if real_fixed_find:fixed_find=real_fixed_find
				else:
					_ai_match=fixed_find in ai_file_content or bool(find_in_content(fixed_find,ai_file_content))
					if not _ai_match:print(f"  [31m[AI GAGAL][0m AI tidak berhasil menemukan kecocokan yang valid di file.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");continue
				method_ai_lbl='\x1b[38;5;46m[Pure Character Match]\x1b[0m'if real_fixed_find else'\x1b[33m[AI Fuzzy Match]\x1b[0m';print(f"\n  [32m[AI MENEMUKAN][0m Blok #{fi} {method_ai_lbl} — cocok di file:\n");print(f"  [38;5;240m{"─"*_sa_sep_w}[0m")
				for ln in fixed_find.splitlines()[:10]:print(f"  [32m  {ln}[0m")
				if len(fixed_find.splitlines())>10:print(f"  [38;5;240m  ... (+{len(fixed_find.splitlines())-10} baris)[0m")
				print(f"  [38;5;240m{"─"*_sa_sep_w}[0m");pilihan_ai=popup_confirm('KONFIRMASI HASIL AI',['Gunakan hasil pencarian AI ini untuk mengganti kode?'],[('y','Ya, Gunakan'),('n','Tolak')])
				if pilihan_ai!='y':print(f"  [33m[LEWATI][0m Blok #{fi} ditolak dan tidak diterapkan.");continue
				result2=find_in_content(fixed_find,ai_file_content)
				if result2:
					st2,en2,mt2=result2;mode2='first'
					if mt2.startswith('head_tail')or mt2.startswith('auto_anchor'):lines_k=ai_file_content.splitlines(keepends=True);c_st2=sum(len(l)for l in lines_k[:st2]);c_en2=sum(len(l)for l in lines_k[:en2])
					else:c_st2,c_en2=st2,en2
					ai_fixed_pairs.append((ai_filepath,fixed_find,replace_text,mode2,ai_file_content));ai_fixed_indices.add(fi-1);plan.append((ai_filepath,fixed_find,replace_text,mode2,ai_file_content,mt2,c_st2,c_en2));rel_ai=os.path.relpath(ai_filepath,SOURCE_ROOT);print(f"  [32m[OK][0m Blok #{fi} → [1;36m{rel_ai}[0m [38;5;213m[AI Semantic Auto-Fix][0m siap diterapkan.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m")
				else:print(f"  [31m[GAGAL][0m Hasil AI tidak bisa dicocokkan ulang. Blok #{fi} dilewati.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m")
		masih_gagal=[b for(i,b)in enumerate(failed_blocks)if i not in ai_fixed_indices]
		if masih_gagal or failed_blocks and not mau_ai:
			sumber_gagal=masih_gagal if mau_ai else failed_blocks;print(f"\n  [35m[Fallback 4: Manual AI Prompt][0m Membuat prompt pintar untuk perbaikan manual...");prompt_lines=[];prompt_lines.append('Patch berikut gagal diterapkan karena blok :find tidak cocok dengan isi file saat ini.');prompt_lines.append('='*_sa_sep_w);prompt_lines.append('')
			for failed_block in sumber_gagal:filename,find_text,replace_text,context=failed_block;prompt_lines.append(f":file {filename}");prompt_lines.append(':find');prompt_lines.append(find_text if find_text else'[KOSONG]');prompt_lines.append(':end_find');prompt_lines.append(':replace');prompt_lines.append(replace_text if replace_text else'[KOSONG]');prompt_lines.append(':end_replace');prompt_lines.append('')
			prompt_lines.append('='*_sa_sep_w);prompt_lines.append('Instruksi: Perbaiki blok :find di atas agar cocok dengan kode yang ada di file. Kemudian test aplikasikan patch.');prompt='\n'.join(prompt_lines);copied=copy_to_clipboard(prompt)
			if copied:print('   \x1b[32m[OK]\x1b[0m Prompt perbaikan otomatis telah disalin ke clipboard.');print('        Tempelkan ke AI (ChatGPT/Claude) untuk mendapatkan blok :find yang benar.')
			else:print('   \x1b[33m[INFO]\x1b[0m Clipboard tidak tersedia. Salin teks berikut secara manual ke AI:\n')
			print('─'*_sa_sep_w);print(prompt);print('─'*_sa_sep_w)
	sisa_gagal=len(failed_blocks)-len(ai_fixed_indices)
	if sisa_gagal>0 and plan:
		pilih_lanjut=popup_confirm('⚠️ PATCH TIDAK SEMPURNA',[f"Masih ada [31m{sisa_gagal}[0m blok kode yang gagal ditemukan!",'Apakah Anda ingin melanjutkan patch hanya untuk','blok yang \x1b[32mBERHASIL\x1b[0m saja, atau \x1b[31mBATALKAN\x1b[0m semua?'],[('l','Lanjut (Sebagian)'),('b','Batal Semua')])
		if pilih_lanjut!='l':print('\n  \x1b[31m[BATAL]\x1b[0m Seluruh proses patch dibatalkan oleh pengguna.');input('\n  Tekan Enter untuk kembali ke menu...');return
	if not plan:
		if failed_blocks:print('\n  \x1b[31m[GAGAL]\x1b[0m Tidak ada blok yang berhasil. Membatalkan patch.')
		input('\n  Tekan Enter untuk kembali ke menu...');return
	scan_elapsed=time.time()-start_time;waktu_str=f"{scan_elapsed:.1f} detik"if scan_elapsed<60 else f"{int(scan_elapsed//60)}m {int(scan_elapsed%60)}s";print(f"\n  Pratinjau perubahan yang akan diterapkan [38;5;240m(Selesai dalam {waktu_str})[0m:\n");preview_map={};plan_by_file={}
	for item in plan:
		fp=item[0]
		if fp not in plan_by_file:plan_by_file[fp]=[]
		plan_by_file[fp].append(item)
	stop_ev_pv,t_pv=_spinner_start('Menyusun pratinjau perubahan (menerapkan blok ke memori)...')
	for(filepath,items)in plan_by_file.items():
		orig_content=items[0][4];preview_map[filepath]=[orig_content,orig_content];items_sorted=sorted(items,key=lambda x:x[6],reverse=True);working=orig_content
		for(_,find,replace,mode,_,mtype,c_start,c_end)in items_sorted:
			if mode=='all':new_content=working.replace(find,replace)
			else:
				nl_idx=working.rfind('\n',0,c_start);indent=''
				if nl_idx!=-1:
					for ch in working[nl_idx+1:c_start]:
						if ch in(' ','\t'):indent+=ch
						else:break
				else:
					for ch in working[:c_start]:
						if ch in(' ','\t'):indent+=ch
						else:break
				if mtype=='fuzzy_block':
					indented_replace=_reindent_relative(replace,indent)
					if replace.splitlines()or indented_replace:indented_replace+='\n'
					new_content=working[:c_start]+indented_replace+working[c_end:]
				elif mtype.startswith('head_tail')or mtype.startswith('auto_anchor')or mtype=='fuzzy':
					replace_lines=replace.splitlines();indented_replace='\n'.join(indent+l if l.strip()else l for l in replace_lines)
					if replace_lines or indented_replace:indented_replace+='\n'
					new_content=working[:c_start]+indented_replace+working[c_end:]
				elif mtype=='regex':
					replace_lines=replace.splitlines()
					if len(replace_lines)<=1 and'\n'not in working[c_start:c_end]:new_content=working[:c_start]+replace+working[c_end:]
					else:indented_replace='\n'.join(l if i==0 else indent+l if l.strip()else l for(i,l)in enumerate(replace_lines));new_content=working[:c_start]+indented_replace+working[c_end:]
				else:new_content=working[:c_start]+replace+working[c_end:]
			working=new_content
		preview_map[filepath][1]=working
	_spinner_stop(stop_ev_pv,t_pv)
	for(filepath,(lama,baru))in preview_map.items():rel=os.path.relpath(filepath,SOURCE_ROOT);print(f"  📄 {rel}");tampilkan_diff(lama,baru,filepath);print()
	print('─'*_sa_sep_w);cfg=load_ai_config()
	if cfg.get('api_key','').strip():
		cek_syn=popup_confirm('🛡️ CEK SYNTAX ERROR (AI)',['Periksa potensi Syntax Error fatal pada kode','yang baru diubah menggunakan AI?'],[('y','Ya, Periksa'),('n','Tidak, Lewati')])
		if cek_syn=='y':
			import threading,time;print()
			for(filepath,(_,baru))in preview_map.items():
				rel=os.path.relpath(filepath,SOURCE_ROOT);stop_ev_c,tc=_spinner_start(f"Menganalisis struktur syntax {rel}...",color='33');hasil_cek=cek_syntax_ai(baru,rel);_spinner_stop(stop_ev_c,tc)
				if hasil_cek=='SKIP':print(f"  [33m[SKIP][0m Pengecekan dilewati (API key belum diatur) untuk {rel}")
				elif hasil_cek.startswith('SKIP_ERR_HTTP:')or hasil_cek.startswith('SKIP_ERR_NET:'):_alasan=hasil_cek.split(':',1)[1].strip();print(f"  [33m[SKIP][0m Pengecekan dilewati untuk {rel} — gagal konek ke AI: {_alasan}")
				elif hasil_cek.upper().startswith('AMAN'):print(f"  [32m[AMAN][0m Struktur kode pada {rel} bebas dari error fatal.")
				else:print(f"  [31m[ERROR DETECTED][0m Peringatan pada {rel}:");print(f"         {hasil_cek}");print(f"         [33mSangat disarankan untuk membatalkan (Ketik 'n' di bawah) dan mengecek ulang kodenya.[0m")
				elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m")
			print('\n  '+'─'*_sa_sep_w)
	if dry_run:print();print('  \x1b[48;5;234m\x1b[1;38;5;45m  ⚠  MODE CEK SAJA (DRY-RUN)  ⚠\x1b[0m');print('  \x1b[38;5;244m');print(f"  Patch berhasil dianalisis untuk {len(preview_map)} file.");print(f"  Total blok yang akan diterapkan: {len(plan)} blok.");print(f"  Waktu pemrosesan: {waktu_str}");print();print(f"  [33mCATATAN: TIDAK ADA FILE YANG AKAN DIUBAH.[0m");print(f"  Ini hanya mode pratinjau untuk melihat diff perubahan.");print(f"  Untuk menerapkan patch, gunakan menu [1] Terapkan Patch.");print('  \x1b[0m');input('\n  Tekan Enter untuk kembali ke menu...');return
	file_count=len(preview_map);blok_total=len(plan);pilih_terapkan=popup_confirm('TERAPKAN PERUBAHAN',[f"{blok_total} blok patch siap untuk {file_count} file.",f"⏱ Waktu proses: [36m{waktu_str}[0m",'Apakah Anda yakin ingin menerapkan semua','perubahan kode ini ke file proyek Anda?'],[('y','Terapkan Patch'),('n','Batalkan')])
	if pilih_terapkan!='y':print('\n  \x1b[31m[BATAL]\x1b[0m Tidak ada perubahan yang diterapkan.');input('\n  Tekan Enter untuk kembali ke menu...');return
	session_files=[];_self_tool=_is_self_tool_root()
	if _self_tool:
		_ensure_rescue_script();_snap_dir=_snapshot_backup_self(preview_map)
		if _snap_dir:print(f"  [35m[BACKUP][0m Snapshot fisik dibuat: {os.path.relpath(_snap_dir,SOURCE_ROOT)}")
	_git_ensure_repo()
	for(filepath,(orig_content,new_content))in preview_map.items():
		rel=os.path.relpath(filepath,SOURCE_ROOT)
		if _self_tool:
			ok_syntax,syntax_err=_validate_python_syntax(filepath,new_content)
			if not ok_syntax:print(f"  [31m[DITOLAK][0m {rel} — {syntax_err}");print(f"         [33mFile TIDAK ditulis, isi lama dipertahankan supaya tool tidak rusak.[0m");continue
		if not _is_path_inside_root(filepath):print(f"  [31m[DITOLAK][0m {rel} — path di luar folder project, TIDAK ditulis.");continue
		is_new_file=not os.path.exists(filepath);os.makedirs(os.path.dirname(filepath)or SOURCE_ROOT,exist_ok=True)
		with open(filepath,'w',encoding='utf-8')as f:f.write(new_content)
		session_files.append({'rel':rel})
		if is_new_file:print(f"  [36m[OK][0m {rel} — file baru berhasil dibuat.")
		else:print(f"  [OK] {rel} — berhasil diperbarui.")
	if _confirm_amend_target():print(f"  [35m✎  Lanjut commit sama (amend) — pesan commit lama dipertahankan, judul baru diabaikan[0m");commit_hash,commit_err=_git_amend_session()
	else:
		if _AMEND_SESSION['head']:print(f"  [33m[INFO][0m Sesi lanjut-commit tidak berlaku lagi (tercatat: {_AMEND_SESSION["head"]}, HEAD sekarang: {_git_current_head()}) — dibuat commit baru.");_AMEND_SESSION['root']=None;_AMEND_SESSION['head']=None;_save_amend_session()
		if _patch_title:_custom_name=_patch_title;print(f"  [36m✎  Commit message: {_custom_name}[0m")
		else:
			_custom_name=_ask_commit_name()
			if not _custom_name:
				stop_ev_ai,t_ai=_spinner_start('AI sedang membuat pesan commit otomatis...',color='36');ai_msg=_generate_ai_commit_msg();_spinner_stop(stop_ev_ai,t_ai)
				if ai_msg:_custom_name=ai_msg;print(f"  [36m✎  AI Auto-Commit: {_custom_name}[0m")
		commit_hash,commit_err=_git_commit_session([e['rel']for e in session_files],custom_msg=_custom_name)
	file_count=len(session_files);ai_fixed_count=len(ai_fixed_pairs);total_blok=len(plan)+len(failed_blocks)-ai_fixed_count;blok_ok=len(plan);blok_gagal=len(failed_blocks)-ai_fixed_count;print();print('  ╔══════════════════════════════════╗');print('  ║         RINGKASAN SESI            ║');print('  ╚══════════════════════════════════╝');print(f"  [32m✔  Blok berhasil  : {blok_ok} / {total_blok}[0m")
	if blok_gagal:print(f"  [31m✘  Blok gagal     : {blok_gagal} / {total_blok}[0m")
	else:print(f"  [32m✔  Blok gagal     : 0 / {total_blok}[0m")
	print(f"  [36m✎  File diubah    : {file_count} file[0m")
	for entry in session_files:print(f"       • {entry["rel"]}")
	if commit_hash:print(f"  [33m⎘  Git commit      : {commit_hash}[0m")
	elif commit_err and commit_err!='tidak ada perubahan untuk di-commit':print(f"  [31m[GIT GAGAL][0m {commit_err}")
	print(f"  [38;5;244m⏱  Waktu total     : {waktu_str}[0m");print()
	if _tanya_lanjut_commit_sama(commit_hash):
		print(f"  [35m➜  Lanjut tempel patch berikutnya (masih nambal commit yang sama)...[0m");_next_patch=paste_patch(dry_run=dry_run)
		if _next_patch:scan_dan_apply(_next_patch,dry_run=dry_run);return
	if CAPROJ_MODE_ON:
		pilih_export=popup_confirm('💾 SIMPAN SEBAGAI .caproj?',['Mode compress .caproj aktif (toggle Ctrl+Q).','Compress & simpan project ini jadi .caproj','biar tinggal import ke CodeAssist?'],[('y','Simpan .caproj'),('n','Lewati')])
		if pilih_export=='y':
			stop_ev_zip,t_zip=_spinner_start('Membungkus project jadi .caproj...',color='36');ok_zip,zip_path,zip_err=_export_caproj(SOURCE_ROOT);_spinner_stop(stop_ev_zip,t_zip)
			if ok_zip:print(f"  [32m[OK][0m Tersimpan: {zip_path}")
			else:print(f"  [31m[GAGAL][0m {zip_err}")
	input('  Tekan Enter untuk kembali ke menu...')
def _git_dir():return os.path.join(SOURCE_ROOT,'.git')
def _git_run(args):
	try:
		r=subprocess.run(['git','-C',SOURCE_ROOT]+args,capture_output=True,text=True,errors='replace')
		if r.returncode!=0 and'dubious ownership'in r.stderr:subprocess.run(['git','config','--global','--add','safe.directory',SOURCE_ROOT],capture_output=True,text=True,errors='replace');r=subprocess.run(['git','-C',SOURCE_ROOT]+args,capture_output=True,text=True,errors='replace')
		return r.returncode,r.stdout.strip(),r.stderr.strip()
	except FileNotFoundError:return-1,'','git tidak ditemukan di sistem'
_GIT_AVAILABLE_CACHE=None
def _git_available():
	global _GIT_AVAILABLE_CACHE
	if _GIT_AVAILABLE_CACHE is None:code,_,_=_git_run(['--version']);_GIT_AVAILABLE_CACHE=code==0
	return _GIT_AVAILABLE_CACHE
_GIT_IDENTITY_APPLIED={}
def _git_ensure_repo():
	if not _git_available():return False,'git tidak terinstall. Jalankan: pkg install git (Termux) atau apt install git (Debian)'
	is_new=not os.path.isdir(_git_dir())
	if is_new:
		code,_,err=_git_run(['init'])
		if code!=0:return False,err or'gagal menjalankan git init'
	if is_new or _GIT_IDENTITY_APPLIED.get(SOURCE_ROOT)!=(GIT_USER_EMAIL,GIT_USER_NAME):_git_run(['config','user.email',GIT_USER_EMAIL]);_git_run(['config','user.name',GIT_USER_NAME]);_GIT_IDENTITY_APPLIED[SOURCE_ROOT]=GIT_USER_EMAIL,GIT_USER_NAME
	if is_new:
		gi_path=os.path.join(SOURCE_ROOT,'.gitignore')
		if not os.path.exists(gi_path):
			try:
				with open(gi_path,'w')as f:f.write('\n'.join(sorted(d+'/'for d in IGNORE_DIRS if d!='.git'))+'\n')
			except Exception:pass
		_git_run(['add','-A']);_git_run(['commit','-m','Initial commit (auto, sebelum FR Tool mulai patch)'])
	return True,None
def _git_commit_session(rels,custom_msg=None):
	ok,err=_git_ensure_repo()
	if not ok:return None,err
	_git_run(['add','-A']);code,out,_=_git_run(['status','--porcelain'])
	if code==0 and not out.strip():return None,'tidak ada perubahan untuk di-commit'
	try:_sess_tag=_fold_tag('commit',SOURCE_ROOT,len(rels))
	except RuntimeError:return None,'sesi kerja tidak lengkap, batal commit'
	if custom_msg:msg=custom_msg
	else:
		uniq=list(dict.fromkeys(rels))
		if len(uniq)==1:msg=f"Patch: {uniq[0]}"
		elif len(uniq)<=3:msg=f"Patch: {", ".join(uniq)}"
		else:msg=f"Patch: {uniq[0]} +{len(uniq)-1} file lain"
	msg=f"{msg}\n\nSess: {_sess_tag}";code,out,err=_git_run(['commit','-m',msg])
	if code!=0:return None,err or out
	code,out,_=_git_run(['rev-parse','--short','HEAD']);return out if code==0 else None,None
def _load_amend_session():
	if os.path.exists(AMEND_SESSION_PATH):
		try:
			with open(AMEND_SESSION_PATH,'r')as f:data=json.load(f)
			if isinstance(data,dict)and data.get('root')and data.get('head'):return{'root':data['root'],'head':data['head']}
		except Exception:pass
	return{'root':None,'head':None}
def _save_amend_session():
	try:
		if _AMEND_SESSION['root']and _AMEND_SESSION['head']:
			with open(AMEND_SESSION_PATH,'w')as f:json.dump(_AMEND_SESSION,f)
		elif os.path.exists(AMEND_SESSION_PATH):os.remove(AMEND_SESSION_PATH)
	except Exception:pass
_AMEND_SESSION=_load_amend_session()
def _amend_target_valid():
	if not _AMEND_SESSION['head']or _AMEND_SESSION['root']!=SOURCE_ROOT:return False
	return _git_current_head()==_AMEND_SESSION['head']
def _confirm_amend_target():
	if not _amend_target_valid():return False
	judul_lama=_git_head_subject()or'(tanpa pesan commit)';pilih=popup_confirm('TAMBAL KE COMMIT LAMA?',['Perubahan ini akan ditambal ke commit:',f'"{judul_lama}"','Yakin masih satu konteks, atau buat commit baru?'],[('y','Ya, Tambal (Amend)'),('n','Buat Commit Baru')],default=0)
	if pilih=='y':return True
	_AMEND_SESSION['root']=None;_AMEND_SESSION['head']=None;_save_amend_session();return False
def _git_amend_session():
	try:_fold_tag('amend',SOURCE_ROOT)
	except RuntimeError:return None,'sesi kerja tidak lengkap, batal commit'
	_git_run(['add','-A']);code,out,_=_git_run(['status','--porcelain'])
	if code==0 and not out.strip():return None,'tidak ada perubahan untuk di-commit'
	code,out,err=_git_run(['commit','--amend','--no-edit','--allow-empty'])
	if code!=0:return None,err or out
	code,out,_=_git_run(['rev-parse','--short','HEAD']);return out if code==0 else None,None
def _tanya_lanjut_commit_sama(commit_hash):
	if not commit_hash:return False
	lanjut=popup_confirm('LANJUT COMMIT INI?',['Kalau nanti ada patch susulan (mis. fix error),','mau ditambal ke commit yang barusan ini juga?'],[('y','Ya, Lanjut'),('n','Tidak, Commit Baru')],default=0)
	if lanjut=='y':_AMEND_SESSION['root']=SOURCE_ROOT;_AMEND_SESSION['head']=commit_hash
	else:_AMEND_SESSION['root']=None;_AMEND_SESSION['head']=None
	_save_amend_session();return lanjut=='y'
def _generate_ai_commit_msg():
	if not _rc_ok()or not _hb_sync():return
	ok,_=_git_ensure_repo()
	if not ok:return
	_git_run(['add','-A']);code,diff_text,_=_git_run(['diff','--staged'])
	if code!=0 or not diff_text.strip():return
	cfg=load_ai_config();api_keys=[k.strip()for k in cfg.get('api_key','').split(',')if k.strip()]
	if not api_keys:return
	if len(diff_text)>15000:diff_text=diff_text[:15000]+'\n...[diff dipotong karena terlalu panjang]...'
	prompt=f"""Kamu adalah asisten developer. Buatkan 1 baris pesan commit git singkat (Conventional Commits) berdasarkan hasil git diff berikut. Format: <type>: <deskripsi singkat>
Aturan:
1. JAWAB HANYA DENGAN PESAN COMMIT-NYA SAJA.
2. Jangan gunakan tanda kutip di awal/akhir, jangan gunakan format markdown (```).
3. Gunakan bahasa Indonesia yang baik.
4. Maksimal 70 karakter.

DIFF:
{diff_text}""";payload=json.dumps({'model':cfg.get('model','gpt-4o-mini'),'messages':[{'role':'user','content':prompt}],'max_tokens':60,'temperature':.2}).encode('utf-8');PROVIDER_URLS={'openai':'https://api.openai.com/v1/chat/completions','groq':'https://api.groq.com/openai/v1/chat/completions','openrouter':'https://openrouter.ai/api/v1/chat/completions','local':'http://127.0.0.1:4891/v1/chat/completions'};api_url=PROVIDER_URLS.get(cfg.get('provider','openai'),PROVIDER_URLS['openai'])
	if cfg.get('provider')=='local'and cfg.get('local_url','').strip():api_url=cfg['local_url'].strip()
	for current_key in api_keys:
		headers={'Content-Type':'application/json','Authorization':f"Bearer {current_key}",'User-Agent':'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'}
		if cfg.get('provider')=='openrouter':headers['HTTP-Referer']='https://github.com/frtool';headers['X-Title']='FR Patch Tool'
		req=urllib.request.Request(api_url,data=payload,headers=headers,method='POST')
		try:
			with urllib.request.urlopen(req,timeout=15)as resp:
				data=json.loads(resp.read().decode('utf-8'));msg=data['choices'][0]['message']['content'].strip();msg=msg.replace('```','').strip()
				if msg.startswith('"')and msg.endswith('"'):msg=msg[1:-1]
				if msg.startswith("'")and msg.endswith("'"):msg=msg[1:-1]
				return msg.strip()
		except:continue
def _ask_commit_name():
	print(f"  [36m✎  Nama versi ini (opsional, Enter = AI Auto-Commit):[0m ",end='')
	try:name=input().strip()
	except(EOFError,KeyboardInterrupt):name=''
	return name or None
def _git_log_entries(limit=300):
	fmt='%h\x1f%ad\x1f%s';code,out,_=_git_run(['reflog','show',f"-n{limit}",f"--pretty=format:{fmt}",'--date=format:%Y-%m-%d %H:%M'])
	if code!=0 or not out:return[]
	entries=[];seen=set()
	for line in out.split('\n'):
		parts=line.split('\x1f')
		if len(parts)!=3:continue
		h,date,msg=parts
		if h in seen:continue
		seen.add(h);entries.append({'hash':h,'date':date,'msg':msg})
	return entries
def _git_ancestry_hashes():
	code,out,_=_git_run(['log','--format=%h','HEAD'])
	if code!=0 or not out:return set()
	return set(out.split('\n'))
def _git_current_head():code,out,_=_git_run(['rev-parse','--short','HEAD']);return out if code==0 else None
def _git_head_subject():code,out,_=_git_run(['log','-1','--pretty=%s','HEAD']);return out.strip()if code==0 and out else None
def _git_reset_hard(commit_hash):code,out,err=_git_run(['reset','--hard',commit_hash]);return code==0,err or out
def _git_show_stat(commit_hash):code,out,_=_git_run(['show','--stat','--pretty=format:',commit_hash]);return out.strip()if code==0 else''
def _git_show_diff(commit_hash):code,out,_=_git_run(['show','--no-color','--pretty=format:',commit_hash]);return out.strip()if code==0 else''
def _git_changed_files(commit_hash):
	code,out,_=_git_run(['show','--name-only','--pretty=format:',commit_hash])
	if code!=0 or not out:return[]
	return[l for l in out.splitlines()if l.strip()]
def _git_file_at(rev,relpath):code,out,_=_git_run(['show',f"{rev}:{relpath}"]);return out if code==0 else''
def _git_all_files_in_history():
	code,out,_=_git_run(['log','--pretty=format:','--name-only'])
	if code!=0 or not out:return[]
	files=set()
	for line in out.splitlines():
		line=line.strip()
		if not line:continue
		if'"'in line or len(line)>200:continue
		files.add(line)
	return sorted(files)
def _git_current_tracked_files():
	code,out,_=_git_run(['ls-tree','-r','--name-only','HEAD'])
	if code!=0 or not out:return set()
	return set(l.strip()for l in out.splitlines()if l.strip())
def _build_file_tree(paths):
	root={'dirs':{},'files':[]}
	for p in paths:
		parts=[seg for seg in p.split('/')if seg]
		if not parts:continue
		node=root
		for seg in parts[:-1]:node=node['dirs'].setdefault(seg,{'dirs':{},'files':[]})
		node['files'].append((parts[-1],p))
	return root
def _git_log_entries_for_file(relpath,limit=300):
	fmt='%h\x1f%ad\x1f%s';code,out,_=_git_run(['log','--follow',f"-n{limit}",f"--pretty=format:{fmt}",'--date=format:%Y-%m-%d %H:%M','--',relpath])
	if code!=0 or not out:return[]
	entries=[]
	for line in out.split('\n'):
		parts=line.split('\x1f')
		if len(parts)!=3:continue
		h,date,msg=parts;entries.append({'hash':h,'date':date,'msg':msg})
	return entries
def _git_checkout_file_at(commit_hash,relpath):code,out,err=_git_run(['checkout',commit_hash,'--',relpath]);return code==0,err or out
_IMAGE_EXTS={'.png','.jpg','.jpeg','.gif','.bmp','.webp','.ico','.tiff'}
def _is_image_file(relpath):_,ext=os.path.splitext(relpath);return ext.lower()in _IMAGE_EXTS
def _git_show_binary(rev,relpath):
	try:r=subprocess.run(['git','-C',SOURCE_ROOT,'show',f"{rev}:{relpath}"],capture_output=True);return r.stdout if r.returncode==0 else None
	except FileNotFoundError:return
def _buka_gambar_commit(rev,relpath):
	data=_git_show_binary(rev,relpath)
	if not data:return False,'Gagal mengambil isi gambar dari commit ini (mungkin dihapus di revisi ini).'
	tmp_dir=os.path.join(SOURCE_ROOT,'.patch_backups','_preview_gambar')
	try:
		if os.path.isdir(tmp_dir):
			for fn in os.listdir(tmp_dir):
				try:os.remove(os.path.join(tmp_dir,fn))
				except OSError:pass
		else:os.makedirs(tmp_dir,exist_ok=True)
		tmp_path=os.path.join(tmp_dir,f"{rev}_{os.path.basename(relpath)}")
		with open(tmp_path,'wb')as f:f.write(data)
	except Exception as e:return False,f"Gagal menyimpan file sementara: {e}"
	try:
		r=subprocess.run(['termux-open',tmp_path],capture_output=True,text=True)
		if r.returncode!=0:err=(r.stderr or r.stdout or'').strip();return False,err or'termux-open gagal dijalankan. Install: pkg install termux-api'
	except FileNotFoundError:return False,'termux-open tidak ditemukan. Install dulu: pkg install termux-api'
	return True,f"Membuka {os.path.basename(relpath)} lewat aplikasi galeri..."
def _preview_diff_file(commit_hash,relpath,full_path,lama,baru):
	if _is_image_file(relpath):print(f"  [38;5;{C_DGRAY}m🖼  File gambar — preview teks tidak akan terbaca.[0m");ok,pesan=_buka_gambar_commit(commit_hash,relpath);warna='32'if ok else'31';print(f"  [{warna}m{pesan}[0m")
	else:tampilkan_diff(lama,baru,full_path)
def _marquee_text(text,width,speed=6.,gap='   •   '):
	import time
	if len(text)<=width:return text.ljust(width)
	loop=text+gap;offset=int(time.time()*speed)%len(loop);doubled=loop+loop;return doubled[offset:offset+width]
def _draw_pilih_list(sel_idx,items,judul,hint,item_render_fn,extra_top=None):
	term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines
	if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();return
	W=max(22,min(term_cols-2,int(term_cols*.95)));B=f"[38;5;{C_BORDER}m";R='\x1b[0m';BL=f"{B}│{R}";TL=f"  {B}┌{"─"*W}┐{R}";BT=f"  {B}└{"─"*W}┘{R}";buf=[''];buf.append(f"  [1;38;5;{C_CYAN}m{judul}[0m  [38;5;{C_DGRAY}m{hint}[0m")
	if extra_top:
		for l in extra_top:buf.append(f"  {l}")
	buf.append(TL)
	if not items:empty_raw='   (Tidak ada data)';buf.append(f"  {BL}[38;5;240m{empty_raw}{" "*max(0,W-len(empty_raw))}[0m{BL}")
	else:
		extra_n=len(extra_top)if extra_top else 0;max_view=max(4,min(14,term_lines-(10+extra_n)));start_i=max(0,sel_idx-max_view//2);start_i=min(start_i,max(0,len(items)-max_view));end_i=min(start_i+max_view,len(items))
		if start_i>0:s_raw=f"   ▲ scroll ke atas... ({start_i} disembunyikan)";buf.append(f"  {BL}[38;5;240m{s_raw}{" "*max(0,W-len(s_raw))}[0m{BL}")
		for i in range(start_i,end_i):
			is_sel=i==sel_idx;label_full=item_render_fn(i,items[i]);marker='❯'if is_sel else' ';avail=W-4
			if _SCROLL_SEP in label_full:
				prefix,scrollable=label_full.split(_SCROLL_SEP,1);msg_avail=max(0,avail-_vlen(prefix))
				if is_sel and _vlen(scrollable)>msg_avail:msg_t=_marquee_text(scrollable,msg_avail)
				elif _vlen(scrollable)<=msg_avail:msg_t=scrollable
				else:msg_t=scrollable[:max(0,msg_avail-1)]+'…'if msg_avail>0 else''
				label_t=f"{prefix}{msg_t}"
			elif _vlen(label_full)>avail:label_t=_marquee_text(label_full,avail)if is_sel else label_full[:max(0,avail-1)]+'…'if avail>0 else''
			else:label_t=label_full
			raw=f" {marker} {label_t}";pad=max(0,W-_vlen(raw))
			if _GRAY_SEP in label_t:pad+=1;label_t=label_t.replace(_GRAY_SEP,f"[38;5;{C_GRAY}m")
			if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {label_t}{" "*pad}[0m"
			else:row=f"   [38;5;{C_CYAN}m{label_t}[0m{" "*pad}"
			buf.append(f"  {BL}{row}{BL}")
		if end_i<len(items):s_raw=f"   ▼ scroll ke bawah... ({len(items)-end_i} lagi)";buf.append(f"  {BL}[38;5;240m{s_raw}{" "*max(0,W-len(s_raw))}[0m{BL}")
	buf.append(BT);buf.append('');_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
	if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
	out='\n'.join(line+'\x1b[K'for line in buf);sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+out+'\x1b[0J\x1b[?2026l');sys.stdout.flush()
def _pilih_file_dari_riwayat(active_items,deleted_items):
	tree=_build_file_tree(active_items);path_stack=[];node_stack=[tree];sel=0
	while True:
		node=node_stack[-1];is_root=not path_stack;dirnames=sorted(node['dirs'].keys(),key=str.lower);filenames=sorted(node['files'],key=lambda t:t[0].lower());entries=[('dir',d)for d in dirnames]+[('file',f)for f in filenames]
		if is_root and deleted_items:entries=[('trash',None)]+entries
		if not entries:
			if not path_stack:return
			node_stack.pop();path_stack.pop();sel=0;continue
		sel=min(sel,len(entries)-1);breadcrumb='/'+'/'.join(path_stack)if path_stack else'/ (root)';extra_top=[f"[38;5;{C_DGRAY}m{breadcrumb}[0m"]
		def _render(i,ent):
			kind,val=ent
			if kind=='trash':return f"🗑 Lihat file yang sudah dihapus ({len(deleted_items)})"
			if kind=='dir':return f"📁 {val}/"
			return f"📄 {val[0]}"
		hint='↑↓ Pilih  ·  Enter Buka  ·  Esc '+('Naik'if path_stack else'Kembali');_draw_pilih_list(sel,entries,'PILIH FILE',hint,_render,extra_top=extra_top);k=get_key()
		if k=='UP':sel=(sel-1)%len(entries)
		elif k=='DOWN':sel=(sel+1)%len(entries)
		elif k=='ENTER':
			kind,val=entries[sel]
			if kind=='trash':
				hasil=_pilih_file_terhapus(deleted_items)
				if hasil is not None:return hasil
				sel=0
			elif kind=='dir':node_stack.append(node['dirs'][val]);path_stack.append(val);sel=0
			else:return val[1]
		elif k in('ESC','q','Q','0'):
			if path_stack:node_stack.pop();path_stack.pop();sel=0
			else:return
def _pilih_file_terhapus(deleted_items):
	items=sorted(deleted_items,key=str.lower);sel=0
	while True:
		sel=min(sel,len(items)-1);extra_top=[f"[38;5;{C_DGRAY}m🗑 File terhapus/di-rename ({len(items)})[0m"];_draw_pilih_list(sel,items,'FILE SUDAH DIHAPUS','↑↓ Pilih  ·  Enter Lihat Riwayat  ·  Esc Kembali',lambda i,it:f"📄 {it}",extra_top=extra_top);k=get_key()
		if k=='UP':sel=(sel-1)%len(items)
		elif k=='DOWN':sel=(sel+1)%len(items)
		elif k=='ENTER':return items[sel]
		elif k in('ESC','q','Q','0'):return
def _riwayat_commit_untuk_file(relpath):
	entries=_git_log_entries_for_file(relpath);sel=0;msg=''
	while True:
		if not entries:clear();header(f"Riwayat: {relpath}");print('\n  \x1b[33m(Tidak ditemukan riwayat commit untuk file ini)\x1b[0m');input('\n  Tekan Enter untuk kembali...');return
		sel=min(sel,len(entries)-1);extra_top=[f"[38;5;{C_DGRAY}m📄 {relpath}[0m"]
		if msg:extra_top.append(msg)
		_draw_pilih_list(sel,entries,'RIWAYAT FILE INI','↑↓ Pilih  ·  Enter Pulihkan  ·  D Diff  ·  Esc Kembali',lambda i,e:f"{e["hash"]}  {e["date"]}  {_SCROLL_SEP}{e["msg"]}",extra_top=extra_top);msg='';k=get_key(animate=True)
		if k=='ANIMATE':continue
		if k=='UP':sel=(sel-1)%len(entries)
		elif k=='DOWN':sel=(sel+1)%len(entries)
		elif k in('d','D'):target=entries[sel];lama=_git_file_at(f"{target["hash"]}^",relpath);baru=_git_file_at(target['hash'],relpath);sys.stdout.write('\x1b[?1049l\x1b[?25h');sys.stdout.flush();clear();header(f"Diff {relpath} @ {target["hash"]}");print(f"\n  {target["msg"]}  [38;5;244m({target["date"]})[0m\n");_preview_diff_file(target['hash'],relpath,os.path.join(SOURCE_ROOT,relpath),lama,baru);input('\n\n  Tekan Enter untuk kembali...');sys.stdout.write('\x1b[?1049h\x1b[?25l');sys.stdout.flush()
		elif k=='ENTER':
			target=entries[sel];changed=_git_changed_files(target['hash']);other_files=[f for f in changed if f!=relpath];lanjut=True
			if other_files:
				daftar=other_files[:5];pesan=[f"Commit {target["hash"]} sebenarnya mengubah {len(changed)} file,",'bukan cuma file ini. File lain yang ikut berubah:']+[f"  • {f}"for f in daftar]
				if len(other_files)>len(daftar):pesan.append(f"  ... dan {len(other_files)-len(daftar)} file lain")
				pesan+=['','Memulihkan cuma file ini (tanpa file lain yang terkait)','berisiko bikin kode jadi tidak konsisten / error.','Tetap lanjutkan?']
				try:konfirm=popup_confirm('⚠ COMMIT INI MENGUBAH FILE LAIN JUGA',pesan,[('y','Ya, Lanjut'),('n','Batal')])
				except(EOFError,KeyboardInterrupt):konfirm='n'
				lanjut=konfirm=='y'
			if lanjut:
				lama=_git_file_at(f"{target["hash"]}^",relpath);baru=_git_file_at(target['hash'],relpath);sys.stdout.write('\x1b[?1049l\x1b[?25h');sys.stdout.flush();clear();header('Pulihkan File Ini');print(f"\n  Commit  : [1;38;5;117m{target["hash"]}[0m  ({target["date"]})");print(f"  Pesan   : {target["msg"]}");print(f"  File    : {relpath}\n");_preview_diff_file(target['hash'],relpath,os.path.join(SOURCE_ROOT,relpath),lama,baru)
				try:konfirm2=popup_confirm('PULIHKAN FILE INI',['\x1b[33m[PERINGATAN]\x1b[0m Isi file akan ditimpa dengan versi',f"pada commit {target["hash"]}. Perubahan yang belum di-commit",'pada file ini akan hilang. Lanjutkan?'],[('y','Ya, Pulihkan'),('n','Batal')])
				except(EOFError,KeyboardInterrupt):konfirm2='n'
				if konfirm2=='y':
					ok3,err3=_git_checkout_file_at(target['hash'],relpath)
					if ok3:_git_commit_session([relpath],custom_msg=f"Pulihkan {relpath} ke versi commit {target["hash"]}");print(f"\n  [32m[OK][0m {relpath} dipulihkan ke versi commit {target["hash"]}.");msg=f"[32m[OK][0m {relpath} dipulihkan ke {target["hash"]}.";entries=_git_log_entries_for_file(relpath)
					else:print(f"\n  [31m[GAGAL][0m {err3}");msg=f"[31m[GAGAL][0m {err3}"
					input('\n  Tekan Enter untuk lanjut...')
				sys.stdout.write('\x1b[?1049h\x1b[?25l');sys.stdout.flush()
		elif k in('ESC','q','Q','0'):return
def _restore_per_file():
	while True:
		semua_file=_git_all_files_in_history()
		if not semua_file:clear();header('Pulihkan Sesi — Per File');print('\n  \x1b[33m(Belum ada file yang tercatat di riwayat commit)\x1b[0m');input('\n  Tekan Enter untuk kembali ke menu...');return
		tracked=_git_current_tracked_files();file_aktif=[f for f in semua_file if f in tracked];file_hapus=[f for f in semua_file if f not in tracked];relpath=_pilih_file_dari_riwayat(file_aktif,file_hapus)
		if relpath is None:return
		_riwayat_commit_untuk_file(relpath)
def _list_py_files():
	hasil=[]
	for(dirpath,dirnames,filenames)in os.walk(SOURCE_ROOT):
		dirnames[:]=[d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.')]
		for fn in filenames:
			if fn.endswith('.py'):hasil.append(os.path.join(dirpath,fn))
	return sorted(hasil)
def cek_sintaks_menu():
	clear();M=header('Cek Sintaks Python');print();py_files=_list_py_files()
	if not py_files:print(f"{M}  [33m(Tidak ada file .py ditemukan di folder ini)[0m");input(f"\n{M}  Tekan Enter untuk kembali ke menu...");return
	self_path=os.path.abspath(sys.argv[0])if sys.argv and sys.argv[0].endswith('.py')else None;print(f"{M}  Pilih file yang mau dicek:\n")
	for(i,p)in enumerate(py_files):rel=os.path.relpath(p,SOURCE_ROOT);tag='  \x1b[38;5;244m← tool ini sendiri\x1b[0m'if self_path and os.path.abspath(p)==self_path else'';print(f"{M}    [{i}] {rel}{tag}")
	print()
	try:pilih=input(f"{M}  Nomor file (Enter = batal): ").strip()
	except(EOFError,KeyboardInterrupt):return
	if not pilih:return
	try:idx=int(pilih);target=py_files[idx]
	except(ValueError,IndexError):print(f"{M}  [31mNomor tidak valid.[0m");input(f"\n{M}  Tekan Enter untuk kembali ke menu...");return
	rel=os.path.relpath(target,SOURCE_ROOT)
	try:
		with open(target,'r',encoding='utf-8')as f:content=f.read()
	except Exception as e:print(f"{M}  [31m[GAGAL BACA][0m {e}");input(f"\n{M}  Tekan Enter untuk kembali ke menu...");return
	stop_ev,t=_spinner_start(f"Mengecek sintaks {rel}...")
	try:compile(content,target,'exec');err=None
	except SyntaxError as e:err=e
	_spinner_stop(stop_ev,t);print()
	if err is None:jml_baris=len(content.splitlines());print(f"{M}  [1;32m[AMAN][0m {rel} — tidak ada syntax error ({jml_baris} baris).");print(f"{M}  [38;5;244mFile ini sudah pasti bisa di-parse Python, aman untuk dipakai/restart.[0m")
	else:
		print(f"{M}  [1;31m[ADA ERROR][0m {rel} — SyntaxError baris {err.lineno}, kolom {err.offset or 1}");print(f"{M}  [31mPesan   : {err.msg}[0m")
		if err.text:
			cuplikan=err.text.rstrip('\n');print(f"\n{M}      [38;5;244m{err.lineno:>5} │[0m {cuplikan}")
			if err.offset:pointer=' '*(err.offset-1);print(f"{M}      [38;5;244m      │[0m [1;31m{pointer}^[0m")
		print(f"\n{M}  [33mJANGAN restart tool pakai file ini dulu — perbaiki errornya, cek ulang.[0m")
	print();input(f"{M}  Tekan Enter untuk kembali ke menu...")
def restore_backup():
	ok,err=_git_ensure_repo()
	if not ok:clear();header('Pulihkan Sesi (Git)');print(f"\n  [31m[GAGAL][0m {err}");input('\n  Tekan Enter untuk kembali ke menu...');return
	mode_items=[('f','Per File','Pilih 1 file, lihat & pulihkan riwayatnya sendiri'),('c','Semua Commit','Time machine seluruh project (reset --hard)')];_mode_w=max(len(it[1])for it in mode_items);sel=0
	while True:
		_draw_pilih_list(sel,mode_items,'PULIHKAN SESI','↑↓ Pilih  ·  Enter Lanjut  ·  Esc Batal',lambda i,it:f"{it[1]:<{_mode_w}}  {_GRAY_SEP}—  {it[2]}");k=get_key()
		if k=='UP':sel=(sel-1)%len(mode_items)
		elif k=='DOWN':sel=(sel+1)%len(mode_items)
		elif k=='ENTER':
			mode=mode_items[sel][0]
			if mode=='f':_restore_per_file()
			elif mode=='c':_restore_semua_commit()
		elif k in('ESC','q','Q','0'):return
def _restore_semua_commit():
	ok,err=_git_ensure_repo()
	if not ok:clear();header('Pulihkan Sesi (Git)');print(f"\n  [31m[GAGAL][0m {err}");input('\n  Tekan Enter untuk kembali ke menu...');return
	def _pad(col,raw,width):return col+' '*max(0,width-len(raw))
	_last_size=None;_first_draw=True
	def _draw(sel_idx,entries,head_hash,ancestry,msg=''):
		nonlocal _last_size,_first_draw;term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines;_last_size=term_cols,term_lines
		if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();return
		W=max(22,min(term_cols-2,int(term_cols*.95)));B=f"[38;5;{C_BORDER}m";R='\x1b[0m';BL=f"{B}│{R}";TL=f"  {B}┌{"─"*W}┐{R}";BT=f"  {B}└{"─"*W}┘{R}";SB=f"  {B}╔{"═"*W}╗{R}";SE=f"  {B}╚{"═"*W}╝{R}";SR_L=f"  {B}║{R}";SR_R=f"{B}║{R}";buf=[''];compact=term_lines<30
		if not compact:safe_logo=[l[:max(10,term_cols-2)]for l in LOGO_GIT];buf.extend(gradient_ascii_lines(safe_logo,RGB_FULL_DARK,RGB_FULL_LIGHT))
		else:buf.append(f"  [1;38;5;{C_VIOLET}mPULIHKAN SESI (GIT)[0m")
		buf.append('');buf.append(SB);raw_s=f"  HEAD saat ini: {head_hash or"-"}  |  {len(entries)} commit";col_s=f"  [38;5;{C_GRAY}mHEAD saat ini:[0m [1;38;5;{C_CYAN}m{head_hash or"-"}[0m[38;5;{C_DGRAY}m  |  [0m[38;5;{C_VIOLET}m{len(entries)} commit[0m";buf.append(f"{SR_L}{_pad(col_s,raw_s,W)}{SR_R}");buf.append(SE);buf.append('');hdr=f"  [1;38;5;{C_CYAN}mRIWAYAT COMMIT[0m  [38;5;{C_DGRAY}m↑↓ Pilih  ·  Enter Pulihkan  ·  D Diff  ·  Esc Keluar[0m";buf.append(hdr);buf.append(f"  [38;5;{C_DGRAY}mAbu-abu: commit yang telah digantikan oleh amend/reset — tidak disertakan saat push.[0m");buf.append(TL)
		if not entries:empty_raw='   (Belum ada commit)';buf.append(f"  {BL}[38;5;240m{empty_raw}{" "*max(0,W-len(empty_raw))}[0m{BL}")
		else:
			term_h=_term_size().lines;max_view=max(4,min(12,term_h-18));start_i=max(0,sel_idx-max_view//2);start_i=min(start_i,max(0,len(entries)-max_view));end_i=min(start_i+max_view,len(entries))
			if start_i>0:s_raw=f"   ▲ scroll ke atas... ({start_i} disembunyikan)";buf.append(f"  {BL}[38;5;240m{s_raw}{" "*max(0,W-len(s_raw))}[0m{BL}")
			for i in range(start_i,end_i):
				e=entries[i];is_sel=i==sel_idx;is_head=e['hash']==head_hash;is_stale=e['hash']not in ancestry if ancestry else False;marker='❯'if is_sel else' ';head_tag=' (HEAD)'if is_head else'';stale_tag='  · Digantikan'if is_stale else'';prefix=f"{e["hash"]}  {e["date"]}  ";msg_full=f"{e["msg"]}{head_tag}{stale_tag}";avail=W-4;msg_avail=max(0,avail-len(prefix))
				if is_sel and len(msg_full)>msg_avail:msg_t=_marquee_text(msg_full,msg_avail)
				elif len(msg_full)<=msg_avail:msg_t=msg_full
				else:msg_t=msg_full[:max(0,msg_avail-1)]+'…'if msg_avail>0 else''
				label_t=f"{prefix}{msg_t}";raw=f" {marker} {label_t}";pad=max(0,W-len(raw))
				if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {label_t}{" "*pad}[0m"
				else:hc=C_DGRAY if is_stale else'46'if is_head else C_CYAN;row=f"   [38;5;{hc}m{label_t}[0m{" "*pad}"
				buf.append(f"  {BL}{row}{BL}")
			if end_i<len(entries):s_raw=f"   ▼ scroll ke bawah... ({len(entries)-end_i} lagi)";buf.append(f"  {BL}[38;5;240m{s_raw}{" "*max(0,W-len(s_raw))}[0m{BL}")
		buf.append(BT);buf.append('')
		if msg:buf.append(f"  {msg}");buf.append('')
		_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
		if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
		out='\n'.join(line+'\x1b[K'for line in buf)
		if _first_draw:clear_seq='\x1b[?2026h\x1b[2J\x1b[3J\x1b[H';_first_draw=False
		else:clear_seq='\x1b[?2026h\x1b[H'
		sys.stdout.write(clear_seq+out+'\x1b[0J\x1b[?2026l');sys.stdout.flush()
	sel=0;msg='';entries=_git_log_entries();head_hash=_git_current_head();ancestry=_git_ancestry_hashes()
	while True:
		if entries:sel=min(sel,len(entries)-1)
		_draw(sel,entries,head_hash,ancestry,msg);msg='';k=get_key(animate=True)
		if k=='ANIMATE':continue
		if not entries:
			if k in('ESC','q','Q','0'):break
			continue
		if k=='UP':sel=(sel-1)%len(entries)
		elif k=='DOWN':sel=(sel+1)%len(entries)
		elif k in('d','D'):stat=_git_show_stat(entries[sel]['hash']);sys.stdout.write('\x1b[?1049l');sys.stdout.flush();sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();header(f"Diff commit {entries[sel]["hash"]}");print(f"\n  {entries[sel]["msg"]}  [38;5;244m({entries[sel]["date"]})[0m\n");print(stat if stat else'  (Tidak ada perubahan file / commit awal)');input('\n\n  Tekan Enter untuk kembali...');sys.stdout.write('\x1b[?1049h\x1b[?25l');sys.stdout.flush();_first_draw=True
		elif k=='ENTER':
			target=entries[sel];stat=_git_show_stat(target['hash']);changed_files=_git_changed_files(target['hash']);file_diffs=[]
			if changed_files:
				stop_ev_pv,t_pv=_spinner_start('Menyusun pratinjau perubahan...')
				for rel in changed_files:lama=_git_file_at(f"{target["hash"]}^",rel);baru=_git_file_at(target['hash'],rel);file_diffs.append((os.path.join(SOURCE_ROOT,rel),lama,baru))
				_spinner_stop(stop_ev_pv,t_pv)
			info_lines=['',f"  Commit  : [1;38;5;117m{target["hash"]}[0m  ({target["date"]})",f"  Pesan   : {target["msg"]}"]
			if stat:
				stat_lines=stat.splitlines()
				if stat_lines:info_lines.append(f"  [38;5;244m{stat_lines[-1]}[0m")
			sys.stdout.write('\x1b[?1049l');sys.stdout.flush();sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();header('Pulihkan ke Commit')
			for line in info_lines:print(line)
			print()
			if not file_diffs:print('  \x1b[38;5;244m(Tidak ada perubahan yang tercatat di riwayat ini)\x1b[0m\n')
			else:
				for(full_path,lama,baru)in file_diffs:rel=os.path.relpath(full_path,SOURCE_ROOT);print(f"  [1;38;5;{C_CYAN}m📄 {rel}[0m");_preview_diff_file(target['hash'],rel,full_path,lama,baru);print()
			try:konfirm=popup_confirm('PULIHKAN KE COMMIT INI',['\x1b[33m[PERINGATAN]\x1b[0m Semua perubahan setelah commit ini','akan hilang dari working directory (tetap ada di git history).','Lanjutkan?'],[('y','Ya, Pulihkan'),('n','Batal')])
			except(EOFError,KeyboardInterrupt):konfirm='n'
			if konfirm!='y':sys.stdout.write('\x1b[?1049h\x1b[?25l');sys.stdout.flush();_first_draw=True;continue
			ok2,err2=_git_reset_hard(target['hash'])
			if ok2:print(f"\n  [32m[OK][0m Berhasil dipulihkan ke commit {target["hash"]}.");msg=f"[32m[OK][0m Dipulihkan ke {target["hash"]}.";entries=_git_log_entries();head_hash=_git_current_head();ancestry=_git_ancestry_hashes()
			else:print(f"\n  [31m[GAGAL][0m {err2}");msg=f"[31m[GAGAL][0m {err2}"
			input('\n  Tekan Enter untuk lanjut...');sys.stdout.write('\x1b[?1049h\x1b[?25l');sys.stdout.flush();_first_draw=True
		elif k in('ESC','q','Q','0'):break
	sys.stdout.write('\x1b[?25h');sys.stdout.flush()
PROMPT_AI='Gunakan format Find & Replace untuk semua perubahan kode.\n\nPENTING:\n\n- Kirim SEMUA perubahan hanya dalam SATU BLOK KODE ("text ... ") agar bisa langsung saya copy sekali.\n- Jangan memecah menjadi beberapa blok kode.\n- Jangan mengirim seluruh file, hanya bagian yang perlu diubah.\n- Jika ada banyak file atau banyak perubahan, gabungkan semuanya di dalam blok kode yang sama.\n- Di baris PALING ATAS (sebelum ":file" pertama), tambahkan SATU baris ":title <judul singkat perubahan>" yang merangkum perubahan pada patch ini.\n\nFormat untuk MENGEDIT File (Wajib digunakan):\n\n:title Judul singkat perubahan (dipakai sebagai nama commit)\n\n:file path/ke/file.js\n:find\nkode lama yang ada di file (tulis persis seperti aslinya)\n:end_find\n:replace\nkode baru penggantinya\n:end_replace\n\nFormat untuk MEMBUAT File Baru (Gunakan :new_file):\n\n:file path/ke/NewFile.js\n:new_file\n:replace\nseluruh isi kode file baru\n:end_replace\n\nJika file benar-benar baru, gunakan ":new_file". Jangan mengisi ":find" dengan kode palsu, placeholder, atau potongan kode generik.\n\nAturan Tambahan:\n\n- Bagian ":find" harus berisi kode yang benar-benar ada di file.\n- Jika menambahkan kode baru di file yang sudah ada, gunakan ":find" pada bagian sebelum/sesudah lokasi penyisipan agar posisi penambahan jelas.\n- Pertahankan indentasi dan formatting asli file.\n- Jangan memberi penjelasan panjang di antara perubahan.\n\nJika blok ":find" terlalu panjang, gunakan format head...tail dengan penanda skip:\n\n:find\n5 baris pertama dari blok asli\n:skip\n5 baris terakhir dari blok asli\n:end_find\n:replace\nkode pengganti lengkap\n:end_replace\n\nWAJIB: baris ":skip" harus berdiri SENDIRI di baris tersendiri. Jangan gunakan "..." biasa.\n\nWAJIB DIPATUHI:\n- Seluruh output Find & Replace harus berada dalam SATU BLOK KODE.\n- Tidak boleh ada blok kode kedua.\n- Tidak boleh ada potongan Find & Replace di luar blok kode tersebut.'
def test_api_key_validity(provider,model,key,local_url_override=None):
	cfg=load_ai_config();local_url=cfg.get('local_url','').strip();PROVIDER_URLS={'openai':'https://api.openai.com/v1/chat/completions','groq':'https://api.groq.com/openai/v1/chat/completions','openrouter':'https://openrouter.ai/api/v1/chat/completions','local':local_url if local_url else'http://127.0.0.1:4891/v1/chat/completions'};api_url=PROVIDER_URLS.get(provider,PROVIDER_URLS['openai'])
	if provider=='local'and(local_url_override or'').strip():api_url=local_url_override.strip()
	elif provider=='local'and local_url:api_url=local_url
	if provider=='local':print(f"  [36m[DEBUG] Testing Local AI: {api_url}[0m")
	headers={'Content-Type':'application/json','Authorization':f"Bearer {key}",'User-Agent':'Mozilla/5.0 (Linux; Android 10)'}
	if provider=='openrouter':headers['HTTP-Referer']='https://github.com/frtool';headers['X-Title']='FR Patch Tool'
	target_model=model if model else'openrouter/auto';payload=json.dumps({'model':target_model,'messages':[{'role':'user','content':'hi'}],'max_tokens':1}).encode('utf-8');req=urllib.request.Request(api_url,data=payload,headers=headers,method='POST')
	try:
		with urllib.request.urlopen(req,timeout=10):return'\x1b[32m✅ AMAN (OK)\x1b[0m'
	except urllib.error.HTTPError as e:
		body=e.read().decode('utf-8',errors='ignore')
		try:msg=json.loads(body).get('error',{}).get('message',body[:40]).strip()
		except:msg=body[:40].strip()
		if e.code==401:return'\x1b[31m❌ INVALID (Key Salah/Tidak Aktif)\x1b[0m'
		if e.code==402:return'\x1b[33m⚠️ LIMIT (Saldo Kosong / Membutuhkan Credit)\x1b[0m'
		if e.code==429:return'\x1b[33m⚠️ LIMIT (Rate limit / Terlalu cepat)\x1b[0m'
		if e.code==403:return'\x1b[31m❌ BLOCKED (Akses ditolak)\x1b[0m'
		return f"[33m⚠️ ERROR {e.code}: {msg}[0m"
	except Exception as e:return f"[31m❌ GAGAL KONEKSI[0m"
def fetch_api_models(provider,api_key):
	import urllib.request,json;models=[];err_msg=''
	try:
		if provider=='openrouter':
			url='https://openrouter.ai/api/v1/models';req=urllib.request.Request(url,headers={'User-Agent':'FR-Tool'})
			with urllib.request.urlopen(req,timeout=10)as r:
				data=json.loads(r.read().decode())['data']
				for m in data:models.append((m['id'],m.get('name','')[:22]))
		elif provider in('groq','openai'):
			if not api_key:return[],'\x1b[33mAPI Key kosong! Isi dulu di Step 3.\x1b[0m'
			if provider=='groq':url='https://api.groq.com/openai/v1/models'
			else:url='https://api.openai.com/v1/models'
			headers={'Authorization':f"Bearer {api_key}",'User-Agent':'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36'};req=urllib.request.Request(url,headers=headers)
			with urllib.request.urlopen(req,timeout=10)as r:
				data=json.loads(r.read().decode())['data']
				for m in data:
					if'whisper'not in m['id']:models.append((m['id'],'Auto-fetched API'))
	except urllib.error.HTTPError as e:err_msg=f"[31mHTTP {e.code}: {e.reason}[0m"
	except Exception as e:err_msg=f"[31mError: {str(e)}[0m"
	return models,err_msg
def setup_ai():
	W=54;PROVIDERS=[('groq','Groq','Gratis & sangat cepat'),('openrouter','OpenRouter','Multi-model, ada yg gratis'),('openai','OpenAI','Berbayar, paling stabil'),('local','Local AI','App AI lokal di HP (offline)')];MODELS={'openai':[('gpt-4o-mini','Murah, disarankan'),('gpt-4o','Lebih pintar'),('gpt-3.5-turbo','Paling murah')],'groq':[('llama-3.3-70b-versatile','Disarankan'),('llama-3.1-8b-instant','Tercepat'),('mixtral-8x7b-32768','Konteks panjang')],'openrouter':[('google/gemini-2.0-flash-exp:free','Gratis & Sangat Pintar'),('qwen/qwen-2.5-coder-32b-instruct:free','Gratis & Ahli Koding'),('anthropic/claude-3-5-haiku','Super cepat (Berbayar)')],'local':[('local-model','Ganti manual sesuai model yg di-load di app')]}
	def _pad(content_colored,content_raw,width):return content_colored+' '*max(0,width-_vlen(content_raw))
	_last_setup_size=None
	def _draw(step,sel_idx,cfg,msg=''):
		nonlocal _last_setup_size;term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines;size_changed=_last_setup_size is not None and _last_setup_size!=(term_cols,term_lines);_last_setup_size=term_cols,term_lines
		if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_cols} kolom x {term_lines} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();return
		W2=max(22,min(term_cols-2,int(term_cols*.95)));aktif=bool(cfg.get('api_key',''));prov=cfg.get('provider','groq');model=cfg.get('model','');key=cfg.get('api_key','');key_list=[k.strip()for k in key.split(',')if k.strip()]
		if not key_list:masked='(kosong)'
		elif len(key_list)==1:masked=key_list[0][:5]+'...'+key_list[0][-4:]if len(key_list[0])>11 else key_list[0]
		else:masked=f"({len(key_list)} API Key) Multi-Key Aktif"
		B=f"[38;5;{C_BORDER}m";R='\x1b[0m';BL=f"{B}│{R}";TL=f"  {B}┌{"─"*W2}┐{R}";BT=f"  {B}└{"─"*W2}┘{R}";ML=f"  {B}├{"─"*W2}┤{R}";SB=f"  {B}╔{"═"*W2}╗{R}";SE=f"  {B}╚{"═"*W2}╝{R}";SR_L=f"  {B}║{R}";SR_R=f"{B}║{R}";buf=[];buf.append('');compact=term_lines<30
		if not compact:
			safe_logo=[l[:max(10,term_cols-2)]for l in LOGO_AI_SETUP]
			for line in gradient_ascii_lines(safe_logo,RGB_PATCH_DARK,RGB_PATCH_LIGHT):buf.append(line)
		else:buf.append(f"  [1;38;5;{C_VIOLET}mAI SETUP[0m")
		buf.append('');st_c='82'if aktif else'196';st_lbl='ON'if aktif else'OFF'if W2<42 else'Aktif'if aktif else'Belum setup';buf.append(SB)
		if W2<42:
			max_model_len=max(4,W2-16-len(prov[:6]));model_str=model or'-'
			if len(model_str)>max_model_len:model_str=model_str[:max_model_len-2]+'..'
			raw1=f"  {st_lbl} | {prov[:6]} | {model_str}";col1=f"  [1;38;5;{st_c}m{st_lbl}[0m[38;5;{C_DGRAY}m | [0m[38;5;{C_VIOLET}m{prov[:6]}[0m[38;5;{C_DGRAY}m | [0m[38;5;{C_CYAN}m{model_str}[0m"
		else:
			max_model_len=max(4,W2-32);model_str=model or'-'
			if len(model_str)>max_model_len:model_str=model_str[:max_model_len-2]+'..'
			raw1=f"  Status : {st_lbl}  |  {prov}  |  {model_str}";col1=f"  [38;5;{C_GRAY}mStatus :[0m [1;38;5;{st_c}m{st_lbl}[0m[38;5;{C_DGRAY}m  |  [0m[38;5;{C_VIOLET}m{prov}[0m[38;5;{C_DGRAY}m  |  [0m[38;5;{C_CYAN}m{model_str}[0m"
		buf.append(f"{SR_L}{_pad(col1,raw1,W2)}{SR_R}");max_k_len=max(4,W2-11)
		if len(masked)>max_k_len:masked=masked[:max_k_len-2]+'..'
		raw2=f"  Key    : {masked}";col2=f"  [38;5;{C_GRAY}mKey    :[0m [38;5;{C_DGRAY}m{masked}[0m";buf.append(f"{SR_L}{_pad(col2,raw2,W2)}{SR_R}");buf.append(SE);buf.append('')
		if step=='provider':
			hdr_raw=f"  STEP 1/3  PILIH PROVIDER";hdr_col=f"  [38;5;{C_DGRAY}mSTEP [0m[1;38;5;{C_VIOLET}m1/3[0m  [1;38;5;{C_CYAN}mPILIH PROVIDER[0m";buf.append(hdr_col);buf.append(TL)
			for(i,(pid,plabel,pdesc))in enumerate(PROVIDERS):
				is_sel=i==sel_idx;is_cur=pid==prov;marker='>'if is_sel else' ';cur_tag=' *'if is_cur else'  ';max_desc=max(0,W2-3-12-2);pdesc_t=pdesc[:max_desc];raw=f" {marker} {plabel:<12}{pdesc_t}{cur_tag}";pad_n=max(0,W2-len(raw))
				if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {plabel:<12}{pdesc_t}{cur_tag}{" "*pad_n}[0m"
				else:row=f"   [1;38;5;{C_VIOLET}m{plabel:<12}[0m[38;5;{C_GRAY}m{pdesc_t}[0m[38;5;82m{cur_tag}[0m{" "*pad_n}"
				buf.append(f"  {BL}{row}{BL}")
			buf.append(BT)
		elif step=='model':
			pure_models=[m for m in MODELS.get(prov,[])if not m[0].startswith('[')];hdr_raw=f"  STEP 2/3  PILIH MODEL  ({prov.upper()})";hdr_col=f"  [38;5;{C_DGRAY}mSTEP [0m[1;38;5;{C_VIOLET}m2/3[0m  [1;38;5;{C_CYAN}mPILIH MODEL[0m  [38;5;{C_DGRAY}m({prov.upper()})[0m";buf.append(hdr_col);buf.append(TL);is_sel_sync=0==sel_idx;m_sync='❯'if is_sel_sync else' ';raw_sync=f" {m_sync} [⟳] Sinkronisasi API";pad_sync=max(0,W2-len(raw_sync))
			if is_sel_sync:row_sync=f"[48;2;110;60;35m[1;38;2;230;210;255m {m_sync} [⟳] Sinkronisasi API{" "*pad_sync}[0m"
			else:row_sync=f"   [1;38;5;117m[⟳] Sinkronisasi API[0m{" "*pad_sync}"
			buf.append(f"  {BL}{row_sync}{BL}");is_sel_man=1==sel_idx;m_man='❯'if is_sel_man else' ';raw_man=f" {m_man} [+] Ketik Model Manual";pad_man=max(0,W2-len(raw_man))
			if is_sel_man:row_man=f"[48;2;110;60;35m[1;38;2;230;210;255m {m_man} [+] Ketik Model Manual{" "*pad_man}[0m"
			else:row_man=f"   [1;38;5;114m[+] Ketik Model Manual[0m{" "*pad_man}"
			buf.append(f"  {BL}{row_man}{BL}");buf.append(BT);buf.append('');buf.append(f"  [38;5;{C_DGRAY}m  Daftar Model Tersedia:[0m");buf.append(TL);term_h=_term_size().lines;max_view=max(4,min(15,term_h-27));list_sel_idx=max(0,sel_idx-2);start_i=max(0,list_sel_idx-max_view//2);start_i=min(start_i,max(0,len(pure_models)-max_view));end_i=min(start_i+max_view,len(pure_models))
			if start_i>0:s_raw=f"   ▲ scroll ke atas... ({start_i} disembunyikan)";s_pad=max(0,W2-len(s_raw));buf.append(f"  {BL}[38;5;240m{s_raw}{" "*s_pad}[0m{BL}")
			if not pure_models:empty_raw='   (Belum ada data model)';pad_e=max(0,W2-len(empty_raw));buf.append(f"  {BL}[38;5;240m{empty_raw}{" "*pad_e}[0m{BL}")
			else:
				for i in range(start_i,end_i):
					mid,mdesc=pure_models[i];actual_idx=i+2;is_sel=actual_idx==sel_idx;is_cur=mid==model;marker='❯'if is_sel else' ';cur_tag=' *'if is_cur else'  ';name_w=min(26,max(12,W2-10));name_s=mid if len(mid)<=name_w else mid[:name_w-1]+'~';max_desc=max(0,W2-3-name_w-2);mdesc_t=mdesc[:max_desc];raw=f" {marker} {name_s:<{name_w}}{mdesc_t}{cur_tag}";pad_n=max(0,W2-len(raw))
					if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {name_s:<{name_w}}{mdesc_t}{cur_tag}{" "*pad_n}[0m"
					else:row=f"   [38;5;{C_CYAN}m{name_s:<{name_w}}[0m[38;5;{C_GRAY}m{mdesc_t}[0m[38;5;82m{cur_tag}[0m{" "*pad_n}"
					buf.append(f"  {BL}{row}{BL}")
				if end_i<len(pure_models):s_raw=f"   ▼ scroll ke bawah... ({len(pure_models)-end_i} lagi)";s_pad=max(0,W2-len(s_raw));buf.append(f"  {BL}[38;5;240m{s_raw}{" "*s_pad}[0m{BL}")
			buf.append(BT)
		elif step=='apikey':
			hints={'groq':'Daftar gratis: console.groq.com','openrouter':'Daftar di: openrouter.ai/keys','openai':'Daftar di: platform.openai.com','local':'Tidak perlu daftar, isi bebas cth: local'};hint=hints.get(prov,'');hdr_raw=f"  STEP 3/3  API KEY  ({prov.upper()})";hdr_col=f"  [38;5;{C_DGRAY}mSTEP [0m[1;38;5;{C_VIOLET}m3/3[0m  [1;38;5;{C_CYAN}mAPI KEY[0m  [38;5;{C_DGRAY}m({prov.upper()})[0m";buf.append(hdr_col);buf.append(TL);raw_h=f"  {hint}";col_h=f"  [38;5;{C_DGRAY}m{hint}[0m";buf.append(f"  {BL}{_pad(col_h,raw_h,W2)}{BL}");buf.append(BT);buf.append('');key_str=cfg.get('api_key','');k_list=[k.strip()for k in key_str.split(',')if k.strip()];buf.append(f"  [38;5;{C_DGRAY}m  Daftar API Key Tersimpan:[0m");buf.append(TL)
			if not k_list:empty_raw='   (Belum ada API Key)';pad_e=max(0,W2-len(empty_raw));buf.append(f"  {BL}[38;5;240m{empty_raw}{" "*pad_e}[0m{BL}")
			else:
				for(i,k)in enumerate(k_list):
					is_sel=i==sel_idx;marker='❯'if is_sel else' ';k_mask=k[:6]+'...'+k[-4:]if len(k)>12 else k;raw_n=f" {marker} {i+1}. {k_mask}";pad_n=max(0,W2-len(raw_n))
					if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} {i+1}. {k_mask}{" "*pad_n}[0m"
					else:row=f"   [38;5;242m{i+1}.[0m [38;5;117m{k_mask}[0m{" "*pad_n}"
					buf.append(f"  {BL}{row}{BL}")
			buf.append(BT);buf.append('');buf.append(f"  [38;5;{C_DGRAY}m  Menu Aksi:[0m");buf.append(TL);idx_tambah=len(k_list);is_sel_t=idx_tambah==sel_idx;marker_t='❯'if is_sel_t else' ';raw_t=f" {marker_t} [+] Tambah API Key Baru";pad_t=max(0,W2-len(raw_t))
			if is_sel_t:row_t=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker_t} [+] Tambah API Key Baru{" "*pad_t}[0m"
			else:row_t=f"   [38;5;114m[+] Tambah API Key Baru[0m{" "*pad_t}"
			buf.append(f"  {BL}{row_t}{BL}");idx_test=len(k_list)+1;is_sel_test=idx_test==sel_idx;marker_test='❯'if is_sel_test else' ';raw_test=f" {marker_test} [?] Test Semua API Key";pad_test=max(0,W2-len(raw_test))
			if is_sel_test:row_test=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker_test} [?] Test Semua API Key{" "*pad_test}[0m"
			else:row_test=f"   [38;5;141m[?] Test Semua API Key[0m{" "*pad_test}"
			buf.append(f"  {BL}{row_test}{BL}");idx_selesai=len(k_list)+2;is_sel_s=idx_selesai==sel_idx;marker_s='❯'if is_sel_s else' ';raw_s=f" {marker_s} [v] Selesai & Simpan";pad_s=max(0,W2-len(raw_s))
			if is_sel_s:row_s=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker_s} [v] Selesai & Simpan{" "*pad_s}[0m"
			else:row_s=f"   [38;5;178m[v] Selesai & Simpan[0m{" "*pad_s}"
			buf.append(f"  {BL}{row_s}{BL}");idx_kembali=len(k_list)+3;is_sel_k=idx_kembali==sel_idx;marker_k='❯'if is_sel_k else' ';raw_k=f" {marker_k} [<] Kembali ke Step 2";pad_k=max(0,W2-len(raw_k))
			if is_sel_k:row_k=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker_k} [<] Kembali ke Step 2{" "*pad_k}[0m"
			else:row_k=f"   [38;5;167m[<] Kembali ke Step 2[0m{" "*pad_k}"
			buf.append(f"  {BL}{row_k}{BL}");buf.append(BT)
		buf.append('')
		if msg:buf.append(f"  {msg}");buf.append('')
		content_height=len(buf)
		if content_height<term_lines:available_v=term_lines-content_height;top_pad=available_v//3;buf=['']*top_pad+buf
		buf.append(f"  [38;5;{C_DGRAY}m> ↑↓ pilih   Enter eksekusi   ESC keluar[0m");buf.append('');_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
		if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
		if len(buf)>term_lines:buf=buf[:max(1,term_lines-1)]
		clear_prefix='\x1b[2J'if size_changed else'';sys.stdout.write('\x1b[?2026h'+clear_prefix+'\x1b[H'+'\n'.join(line+'\x1b[K'for line in buf)+'\x1b[0J\x1b[?2026l');sys.stdout.flush()
	cfg=load_ai_config();prov_ids=[p[0]for p in PROVIDERS];cur_prov=cfg.get('provider','groq');sel_prov=prov_ids.index(cur_prov)if cur_prov in prov_ids else 0
	if'api_key'in cfg and cfg['api_key']:
		if f"api_key_{cur_prov}"not in cfg:cfg[f"api_key_{cur_prov}"]=cfg['api_key']
	cfg['api_key']=cfg.get(f"api_key_{cur_prov}",'');sys.stdout.write('\x1b[?25l');sys.stdout.flush();msg=''
	while True:
		_draw('provider',sel_prov,cfg,msg);msg='';k=get_key()
		if k=='UP':sel_prov=(sel_prov-1)%len(PROVIDERS)
		elif k=='DOWN':sel_prov=(sel_prov+1)%len(PROVIDERS)
		elif k=='ENTER':
			prev=cfg.get('provider','groq');cfg['provider']=PROVIDERS[sel_prov][0]
			if cfg['provider']!=prev:cfg['model']=MODELS[cfg['provider']][0][0];cfg['api_key']=cfg.get(f"api_key_{cfg["provider"]}",'')
			break
		elif k in('ESC','q','Q','0'):sys.stdout.write('\x1b[?25h');sys.stdout.flush();return
	cur_prov=cfg['provider']
	def refresh_model_list():pure=[m for m in MODELS.get(cur_prov,[])if not m[0].startswith('[')];MODELS[cur_prov]=pure;return[('[⟳] Sinkronisasi API','Tarik model terbaru'),('[+] Ketik Model Manual','')]+pure
	full_list=refresh_model_list();model_ids=[m[0]for m in full_list];cur_model=cfg.get('model','');sel_model=model_ids.index(cur_model)if cur_model in model_ids else 2
	while True:
		_draw('model',sel_model,cfg,msg);msg='';k=get_key()
		if k=='UP':sel_model=(sel_model-1)%len(full_list)
		elif k=='DOWN':sel_model=(sel_model+1)%len(full_list)
		elif k=='ENTER':
			pilihan_id=model_ids[sel_model]
			if pilihan_id=='[⟳] Sinkronisasi API':
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();current_keys_raw=cfg.get(f"api_key_{cur_prov}",cfg.get('api_key',''));api_k=[k.strip()for k in current_keys_raw.split(',')if k.strip()];clear();print(f"\n  [36m[FETCH][0m Menarik daftar model dari server {cur_prov}...");fetched,err_msg=fetch_api_models(cur_prov,api_k[0]if api_k else'')
				if fetched:MODELS[cur_prov]=fetched;full_list=refresh_model_list();model_ids=[m[0]for m in full_list];sel_model=2;msg=f"[32m[OK] Berhasil menarik {len(fetched)} model![0m"
				else:msg=f"[31m[GAGAL][0m {err_msg if err_msg else"Tidak ada data dari server."}"
				clear();sys.stdout.write('\x1b[?25l');continue
			elif pilihan_id=='[+] Ketik Model Manual':
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();print(f"\n  [32m[MANUAL][0m Ketik ID Model (contoh: qwen/qwen-2.5-coder-32b-instruct)");print(f"  [38;5;240m(Kosongkan lalu Enter untuk batal)[0m");print(f"  > ",end='',flush=True)
				try:
					inp=input().strip()
					if inp:cfg['model']=inp;clear();break
				except:pass
				clear();sys.stdout.write('\x1b[?25l');continue
			else:cfg['model']=pilihan_id;break
		elif k=='ESC':sys.stdout.write('\x1b[?25h');sys.stdout.flush();setup_ai();return
		elif k in('q','Q','0'):sys.stdout.write('\x1b[?25h');sys.stdout.flush();return
	if cfg.get('provider')=='local':
		sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();cur_url=cfg.get('local_url','').strip();print(f"\n  [32m[LOCAL][0m Masukkan URL server AI lokal (OpenAI-compatible)");print(f"  [38;5;240mContoh: http://10.153.82.220:4891/v1/chat/completions[0m")
		if cur_url:print(f"  [38;5;240mSaat ini: {cur_url}[0m")
		print(f"  [38;5;240m(Kosongkan lalu Enter untuk pakai default 127.0.0.1:4891)[0m");print(f"  > ",end='',flush=True)
		try:
			inp=input().strip()
			if inp:cfg['local_url']=inp
		except(EOFError,KeyboardInterrupt):return
		clear();sys.stdout.write('\x1b[?25l');sys.stdout.flush()
	current_keys=[k.strip()for k in cfg.get('api_key','').split(',')if k.strip()];sel_key=0;sys.stdout.write('\x1b[?25l');sys.stdout.flush();msg=''
	while True:
		cfg['api_key']=','.join(current_keys);_draw('apikey',sel_key,cfg,msg);msg='';total_items=len(current_keys)+4;k=get_key()
		if k=='UP':sel_key=(sel_key-1)%total_items
		elif k=='DOWN':sel_key=(sel_key+1)%total_items
		elif k=='ENTER':
			if sel_key<len(current_keys):
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();print(f"\n  [36m[EDIT][0m Masukkan API Key pengganti");print(f"  [38;5;240m(Ketik 'hapus' untuk menghapus, atau kosongkan/Enter untuk BATAL)[0m");print(f"  > ",end='',flush=True)
				try:
					inp=input().strip()
					if inp==''or inp.lower()in('q','batal','0','exit'):msg='\x1b[33m[!] Edit dibatalkan.\x1b[0m'
					elif inp.lower()=='hapus':
						current_keys.pop(sel_key);msg='\x1b[31m[!] API Key dihapus.\x1b[0m'
						if sel_key>=len(current_keys):sel_key=len(current_keys)
					else:current_keys[sel_key]=inp;msg='\x1b[32m[OK] API Key berhasil diperbarui.\x1b[0m'
				except(EOFError,KeyboardInterrupt):return
				sys.stdout.write('\x1b[?25l')
			elif sel_key==len(current_keys):
				sys.stdout.write('\x1b[?25h');sys.stdout.flush();print(f"\n  [32m[TAMBAH][0m Tempel (Paste) API Key Baru:");print(f"  [38;5;240m(Kosongkan/Enter atau ketik 'q' untuk BATAL)[0m");print(f"  > ",end='',flush=True)
				try:
					inp=input().strip()
					if inp==''or inp.lower()in('q','batal','0','exit'):msg='\x1b[33m[!] Tambah API Key dibatalkan.\x1b[0m'
					elif inp not in current_keys:current_keys.append(inp);msg='\x1b[32m[OK] API Key berhasil ditambahkan.\x1b[0m'
					else:msg='\x1b[33m[!] API Key tersebut sudah ada di daftar.\x1b[0m'
				except(EOFError,KeyboardInterrupt):return
				sys.stdout.write('\x1b[?25l')
			elif sel_key==len(current_keys)+1:
				sys.stdout.write('\x1b[?25h');sys.stdout.flush()
				if not current_keys:msg='\x1b[33m[!] Tidak ada API Key untuk ditest.\x1b[0m'
				else:
					print(f"\n  [36m[TESTING][0m Menguji {len(current_keys)} API Key ({cfg["provider"]})...")
					for(idx_k,t_key)in enumerate(current_keys):k_mask=t_key[:6]+'...'+t_key[-4:]if len(t_key)>12 else t_key;sys.stdout.write(f"  [{idx_k+1}] {k_mask} ➜ ");sys.stdout.flush();status=test_api_key_validity(cfg['provider'],cfg.get('model',''),t_key,cfg.get('local_url','')if cfg.get('provider')=='local'else'');print(status)
					print(f"\n  Tekan Enter untuk kembali...",end='',flush=True)
					try:input()
					except:pass
					msg='\x1b[32m[OK] Proses test selesai.\x1b[0m'
				sys.stdout.write('\x1b[?25l')
			elif sel_key==len(current_keys)+2:break
			elif sel_key==len(current_keys)+3:sys.stdout.write('\x1b[?25h');sys.stdout.flush();setup_ai();return
		elif k=='ESC':sys.stdout.write('\x1b[?25h');sys.stdout.flush();setup_ai();return
		elif k in('q','Q','0'):sys.stdout.write('\x1b[?25h');sys.stdout.flush();return
	cfg['api_key']=','.join(current_keys);cfg[f"api_key_{cfg["provider"]}"]=cfg['api_key'];save_ai_config(cfg);sys.stdout.write('\x1b[?25l');sys.stdout.flush();ok_msg=f"[32m[OK] Tersimpan![0m  [38;5;{C_VIOLET}m{cfg["provider"]}[0m  [38;5;{C_CYAN}m{cfg.get("model","")}[0m";_draw('provider',sel_prov,cfg,ok_msg);sys.stdout.write('\x1b[?25h');sys.stdout.flush();print(f"\n  Tekan Enter untuk kembali...",end='',flush=True)
	try:input()
	except(EOFError,KeyboardInterrupt):pass
def setup_threshold():
	global AUTO_ANCHOR_TOLERANCE,AUTO_ANCHOR_MAX_GAP,PARTIAL_MIN_SCORE;sel_idx=0;msg=''
	while True:
		tsize=_term_size();term_cols,term_lines=tsize.columns,tsize.lines
		if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_cols} kolom x {term_lines} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();get_key();continue
		clear();M=header('Threshold Lanjutan');print(f"{M}  [1mPENGATURAN SAAT INI:[0m");print(f"{M}  1. Toleransi Auto-Anchor : [36m{AUTO_ANCHOR_TOLERANCE}[0m");print(f"{M}  2. Jarak Maksimal Anchor : [36m{AUTO_ANCHOR_MAX_GAP}[0m");print(f"{M}  3. Skor Partial Scan     : [36m{PARTIAL_MIN_SCORE}[0m");print()
		if msg:print(f"{M}  {msg}\n");msg=''
		print(f"{M}  [38;5;{C_VIOLET}mPilih nomor (1-3) untuk mengubah, atau 'Q' untuk kembali:[0m");sys.stdout.write(f"{M}  [1;32m❯ [0m");sys.stdout.flush();k=get_key()
		if k.lower()=='q'or k=='ESC':break
		elif k=='RESIZE':continue
		elif k=='1':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Baru [{AUTO_ANCHOR_TOLERANCE}]: ").strip()
			if val:
				try:AUTO_ANCHOR_TOLERANCE=int(val);save_thresholds();msg='\x1b[32m✅ Tersimpan\x1b[0m'
				except:msg='\x1b[31m❌ Input angka tidak valid\x1b[0m'
			sys.stdout.write('\x1b[?25l')
		elif k=='2':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Baru [{AUTO_ANCHOR_MAX_GAP}]: ").strip()
			if val:
				try:AUTO_ANCHOR_MAX_GAP=int(val);save_thresholds();msg='\x1b[32m✅ Tersimpan\x1b[0m'
				except:msg='\x1b[31m❌ Input angka tidak valid\x1b[0m'
			sys.stdout.write('\x1b[?25l')
		elif k=='3':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Baru [{PARTIAL_MIN_SCORE}]: ").strip()
			if val:
				try:PARTIAL_MIN_SCORE=float(val);save_thresholds();msg='\x1b[32m✅ Tersimpan\x1b[0m'
				except:msg='\x1b[31m❌ Input desimal tidak valid\x1b[0m'
			sys.stdout.write('\x1b[?25l')
	save_thresholds();print(f"\n{M}  [32m[OK][0m Threshold berhasil disimpan.");input(f"\n{M}  Tekan Enter untuk kembali ke menu...")
def copy_prompt_ai():
	import threading,time;clear();M=header('Salin Prompt untuk AI')
	if not _vf():input(f"\n{M}Tekan Enter untuk kembali ke menu...");return
	prompt_text=PROMPT_AI;_cp_term_cols=_term_size().columns;_cp_sep_w=max(20,min(_cp_term_cols-2,int(_cp_term_cols*.95)));stop_ev_cp,t=_spinner_start('Menyalin teks ke clipboard...');copied=copy_to_clipboard(prompt_text);_spinner_stop(stop_ev_cp,t)
	if copied:print(f"{M}  Prompt instruksi telah disalin ke clipboard.");print(f"{M}  Tempelkan ke sesi AI sebelum memberikan instruksi perubahan kode.")
	else:
		print(f"{M}  Clipboard tidak tersedia. Salin teks berikut secara manual:\n");print(f"{M}"+'─'*_cp_sep_w)
		for _line in prompt_text.splitlines():print(f"{M}{_line}")
		print(f"{M}"+'─'*_cp_sep_w)
	input(f"\n{M}Tekan Enter untuk kembali ke menu...")
VERSION='v5.2'
def header(title=''):
	term_cols=_term_size().columns;W=max(22,min(term_cols-2,int(term_cols*.95)));M=' '*max(0,(term_cols-(W+2))//2);print();print(f"{M}[38;5;{C_BORDER}m╔{"═"*W}╗[0m");name_raw=f"FR TOOL  {VERSION}";name_colored=f"[1;38;5;{C_VIOLET}mFR TOOL[0m  [38;5;{C_DGRAY}m{VERSION}[0m";pad=max(0,W-len(name_raw)-2);print(f"{M}[38;5;{C_BORDER}m║[0m  {name_colored}{" "*pad}[38;5;{C_BORDER}m║[0m")
	if title:
		print(f"{M}[38;5;{C_BORDER}m╠{"═"*W}╣[0m");tlabel=f"  ◆  {title.upper()}  "
		if len(tlabel)>W:tlabel=f"  ◆  {title.upper()[:max(0,W-8)]}...  "
		tpad=max(0,W-len(tlabel));print(f"{M}[38;5;{C_BORDER}m║[0m[1;38;5;{C_CYAN}m{tlabel}[0m{" "*tpad}[38;5;{C_BORDER}m║[0m")
	print(f"{M}[38;5;{C_BORDER}m╚{"═"*W}╝[0m");print();return M
def badge(text,color=240):return f"[38;5;{color}m{text}[0m"
def cari_dan_ganti_manual():
	sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();_cm_term_cols=_term_size().columns;sep_w=max(20,min(_cm_term_cols-2,int(_cm_term_cols*.95)));safe_logo=[l[:max(10,_cm_term_cols-2)]for l in LOGO];print_gradient_ascii_centered(safe_logo,RGB_TERRACOTTA_DARK,RGB_TERRACOTTA_LIGHT,_cm_term_cols);print();header('Cari & Ganti Manual')
	if not _rc_ok():print('\n  \x1b[31m[ERROR]\x1b[0m Inisialisasi runtime gagal.');input('\n  Tekan Enter untuk kembali ke menu...');return
	if _amend_target_valid():_cm_judul_amend=_git_head_subject()or'(tanpa pesan commit)';print(f'  [48;5;234m[1;97m ⚠  PERUBAHAN INI AKAN MENGGANTIKAN COMMIT:[0m[48;5;234m[1;38;5;{C_VIOLET}m "{_cm_judul_amend}" [0m');print()
	def _baca_blok(judul,hint_baris1,hint_baris2=''):
		print(f"  [1;38;5;{C_CYAN}m{judul}[0m");print(f"  [38;5;{C_DGRAY}m{hint_baris1}[0m")
		if hint_baris2:print(f"  [38;5;{C_GRAY}m{hint_baris2}[0m")
		print(f"  [1;38;5;46m  ✨ Ketik :clip untuk auto-paste dari clipboard[0m");print(f"  [38;5;240m{"─"*sep_w}[0m");lines=[];empty_streak=0
		while True:
			try:
				line=sys.stdin.readline()
				if not line:break
				line=line.strip('\n')
			except(EOFError,KeyboardInterrupt):return
			stripped=line.strip()
			if stripped==':clip':
				try:
					r=subprocess.run(['termux-clipboard-get'],capture_output=True,text=True,timeout=5)
					if r.returncode==0 and r.stdout:lines.extend(r.stdout.splitlines());print(f"  [32m[+] Berhasil mengambil {len(r.stdout.splitlines())} baris dari clipboard.[0m");empty_streak=0;continue
				except Exception:pass
				print('  \x1b[31m[!] Gagal membaca clipboard. Pastikan Termux:API terinstall.\x1b[0m');continue
			if stripped=='DONE':
				while lines and lines[-1].strip()=='':lines.pop()
				break
			if stripped.lower()in('exit','q','0','batal'):return
			if stripped.upper()=='HAPUS':return''
			if stripped=='':
				empty_streak+=1
				if empty_streak>=2:
					while lines and lines[-1].strip()=='':lines.pop()
					break
				lines.append(line)
			else:empty_streak=0;lines.append(line)
		return'\n'.join(lines).strip('\n')
	def _cari_kode(find_text):
		def _try_match(fp,content):
			stop_ev_m,t_m=_spinner_start(f"Mencocokkan di {os.path.relpath(fp,SOURCE_ROOT)}...",color='214');result=find_in_content(find_text,content,block_label='manual');_spinner_stop(stop_ev_m,t_m)
			if result and result[2]=='auto_anchor_confirm':
				h_idx,t_idx,_=result
				if _confirm_far_anchor(h_idx,t_idx,find_text.splitlines(),content.splitlines(),'manual'):result=h_idx,t_idx,'auto_anchor'
				else:result=None
			if result and result[2].startswith('head_tail'):
				if not _confirm_head_tail_skip(result,content,'manual'):result=None
			return result
		print();print(f"  [38;5;240m{"─"*sep_w}[0m");stop_ev,t=_spinner_start('Mencari di seluruh folder project...',color='214');matches=cari_file_berisi_kode(find_text);_spinner_stop(stop_ev,t);matched_file=matched_content=match_type=match_result=None
		if len(matches)==1:
			fp=os.path.join(SOURCE_ROOT,matches[0])
			try:
				with open(fp,'r',encoding='utf-8')as f:content=f.read()
				result=_try_match(fp,content)
				if result:matched_file,matched_content=fp,content;match_type,match_result=result[2],result
			except Exception:pass
		elif len(matches)>1:
			print(f"\n  [33m[PILIHAN][0m Kode ditemukan di [1m{len(matches)}[0m file berbeda:")
			for(j,m)in enumerate(matches,1):print(f"      [36m[{j}][0m {m}")
			print('      Masukkan nomor file yang dituju: ',end='')
			try:
				pilih=int(input().strip());fp=os.path.join(SOURCE_ROOT,matches[pilih-1])
				with open(fp,'r',encoding='utf-8',errors='replace')as f:content=f.read()
				result=_try_match(fp,content)
				if result:matched_file,matched_content=fp,content;match_type,match_result=result[2],result
			except Exception:print(f"  [31m[GAGAL][0m Pilihan tidak valid.")
		if matched_file is None:
			stop_ev_p,tp=_spinner_start('Fallback: Partial Token Scan...',color='129');partial_hits=cari_file_partial(find_text);_spinner_stop(stop_ev_p,tp)
			if partial_hits:
				best_fp,best_score,best_block,best_rel=partial_hits[0];print(f"  [35m[Fallback][0m Kandidat terdekat: [1;36m{best_rel}[0m [38;5;129m[{best_score:.0%}][0m")
				try:
					with open(best_fp,'r',encoding='utf-8')as f:content=f.read()
					result=_try_match(best_fp,content)
					if result:matched_file,matched_content=best_fp,content;match_type,match_result=result[2],result
				except Exception:pass
		return matched_file,matched_content,match_type,match_result
	_mt_map={'exact':'\x1b[38;5;46m[Exact]\x1b[0m','regex':'\x1b[38;5;39m[Regex]\x1b[0m','fuzzy':'\x1b[33m[Fuzzy]\x1b[0m','auto_anchor':'\x1b[38;5;208m[Auto-Anchor]\x1b[0m','fuzzy_block':'\x1b[38;5;214m[Fuzzy Block]\x1b[0m'};session_entries=[];blok_ke=0;file_cache={}
	while True:
		blok_ke+=1;print()
		if blok_ke>1:print(f"  [38;5;240m{"═"*sep_w}[0m")
		badge(f"BLOK #{blok_ke}",color='cyan');print();find_text=_baca_blok(f"BLOK #{blok_ke} — KETIK KODE YANG INGIN DICARI",'Ketik DONE lalu Enter untuk selesai  •  Q atau 0 = batal ke menu','Bisa satu baris atau beberapa baris — tidak perlu format :find/:replace')
		if find_text is None:
			if blok_ke==1:return
			break
		if not find_text.strip():print('\n  \x1b[33m[SKIP]\x1b[0m Teks pencarian kosong, blok diabaikan.');break
		import time;global _GLOBAL_TIMER_START;search_start=time.time();_GLOBAL_TIMER_START=search_start;matched_file,matched_content,match_type,match_result=_cari_kode(find_text);search_elapsed=time.time()-search_start
		if matched_file and matched_file in file_cache:
			matched_content=file_cache[matched_file];from types import SimpleNamespace;_saved=matched_content;matched_content=file_cache[matched_file];stop_ev_r,t_r=_spinner_start('Mencocokkan ulang di versi file terbaru...',color='214');result_r=find_in_content(find_text,matched_content,block_label='manual');_spinner_stop(stop_ev_r,t_r)
			if result_r:match_type=result_r[2];match_result=result_r
		if matched_file is None:
			print(f"\n  [31m[GAGAL][0m Kode tidak ditemukan di project manapun.");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");print(f"  [38;5;244mKetik [y] untuk coba blok find lain, atau Enter untuk kembali ke menu: [0m",end='')
			try:ans=input().strip().lower()
			except(EOFError,KeyboardInterrupt):break
			if ans=='y':blok_ke-=1;continue
			break
		rel=os.path.relpath(matched_file,SOURCE_ROOT);method_label=_mt_map.get(match_type,'')
		if not method_label:
			if match_type and match_type.startswith('head_tail'):method_label='\x1b[35m[Head...Tail]\x1b[0m'
			else:method_label=f"[38;5;244m[{match_type}][0m"
		r0,r1,rtype=match_result
		if rtype.startswith('head_tail'):found_lines=matched_content.splitlines()[r0:r1];found_text='\n'.join(found_lines);line_no=r0+1
		else:found_text=matched_content[r0:r1];line_no=matched_content[:r0].count('\n')+1
		print();print(f"  [32m[DITEMUKAN][0m → [1;36m{rel}[0m  [33m(baris {line_no})[0m  {method_label}");elapsed_now=time.time()-_GLOBAL_TIMER_START;print(f"      [38;5;244m↳ ⏱  {elapsed_now:.1f}s[0m");tampilkan_preview_pencarian(matched_content,matched_file,r0,r1,rtype,line_no);print(f"  [38;5;240m{"─"*sep_w}[0m");pilih_konfirm=popup_confirm(f"✅ KONFIRMASI HASIL — BLOK #{blok_ke}",[f"File  : {rel}",f"Baris : {line_no}",'Apakah ini kode yang ingin Anda ganti?'],[('y','Ya, Lanjutkan'),('n','Lewati Blok Ini'),('0','Batal ke Menu')],layout='vertical')
		if pilih_konfirm=='0':return
		if pilih_konfirm!='y':
			print(f"\n  [33m[SKIP][0m Blok #{blok_ke} dilewati.");print(f"  Ketik [y] untuk tambah blok baru, atau Enter untuk selesai: ",end='')
			try:ans=input().strip().lower()
			except(EOFError,KeyboardInterrupt):break
			if ans!='y':break
			blok_ke-=1;continue
		print();print(f"  [38;5;240m{"─"*sep_w}[0m");replace_text=_baca_blok(f"BLOK #{blok_ke} — KETIK KODE PENGGANTI",'Ketik DONE lalu Enter untuk selesai  •  Ketik HAPUS atau DONE (kosong) = hapus kode')
		if replace_text is None:return
		hapus_mode=replace_text=='';replace_text=replace_text if not hapus_mode else''
		if hapus_mode:print(f"\n  [33m[INFO][0m Mode HAPUS — kode yang ditemukan akan dihapus.")
		print();print(f"  [1;38;5;{C_CYAN}mPRATINJAU PERUBAHAN — BLOK #{blok_ke}[0m");print();effective_mode=match_type if match_type=='fuzzy_block'else'first';new_content,cnt=replace_in_content(matched_content,find_text,replace_text,effective_mode)
		if cnt==0:new_content,cnt=replace_in_content(matched_content,found_text,replace_text,'first')
		if cnt==0:
			print(f"  [31m[GAGAL][0m Penggantian tidak bisa dilakukan (kode berubah sejak pencarian).");print(f"  Ketik [y] untuk tambah blok baru, atau Enter untuk selesai: ",end='')
			try:ans=input().strip().lower()
			except(EOFError,KeyboardInterrupt):break
			if ans=='y':blok_ke-=1;continue
			break
		tampilkan_diff(matched_content,new_content,matched_file);print();print(f"  [38;5;240m{"─"*sep_w}[0m");pilih_apply=popup_confirm(f"TERAPKAN — BLOK #{blok_ke}",[f"Terapkan perubahan ke: {rel}?",'Backup otomatis dibuat. Semua blok sesi ini bisa di-undo sekaligus.'],[('y','Terapkan'),('l','Terapkan + Tambah Blok Lagi'),('n','Lewati')],layout='vertical')
		if pilih_apply in('y','l'):
			if not any(e.get('rel')==rel for e in session_entries):session_entries.append({'rel':rel})
			with open(matched_file,'w',encoding='utf-8')as f:f.write(new_content)
			file_cache[matched_file]=new_content;print(f"\n  [32m✔[0m Blok #{blok_ke} diterapkan ke [1;36m{rel}[0m")
			if pilih_apply=='l':continue
		else:print(f"\n  [33m[SKIP][0m Blok #{blok_ke} tidak diterapkan.")
		print();print(f"  [38;5;240m{"─"*sep_w}[0m");print(f"  Tambah blok find/replace lagi? [36m[y][0m Ya  [36m[n / Enter][0m Selesai: ",end='')
		try:ans=input().strip().lower()
		except(EOFError,KeyboardInterrupt):break
		if ans!='y':break
	if session_entries:
		if _confirm_amend_target():print(f"  [35m✎  Lanjut commit sama (amend) — pesan commit lama dipertahankan, judul baru diabaikan[0m");commit_hash,commit_err=_git_amend_session()
		else:
			if _AMEND_SESSION['head']:print(f"  [33m[INFO][0m Sesi lanjut-commit tidak berlaku lagi (tercatat: {_AMEND_SESSION["head"]}, HEAD sekarang: {_git_current_head()}) — dibuat commit baru.");_AMEND_SESSION['root']=None;_AMEND_SESSION['head']=None;_save_amend_session()
			_custom_name=_ask_commit_name()
			if not _custom_name:
				stop_ev_ai,t_ai=_spinner_start('AI sedang membuat pesan commit otomatis...',color='36');ai_msg=_generate_ai_commit_msg();_spinner_stop(stop_ev_ai,t_ai)
				if ai_msg:_custom_name=ai_msg;print(f"  [36m✎  AI Auto-Commit: {_custom_name}[0m")
			commit_hash,commit_err=_git_commit_session([e['rel']for e in session_entries],custom_msg=_custom_name)
		n_files=len({e['rel']for e in session_entries});print();print('  ╔══════════════════════════════════════╗');print(f"  ║   SESI SELESAI: {blok_ke} blok, {n_files} file diubah   ║");print('  ╚══════════════════════════════════════╝')
		if commit_hash:print(f"  [33m⎘  Git commit: {commit_hash}[0m")
		elif commit_err and commit_err!='tidak ada perubahan untuk di-commit':print(f"  [31m[GIT GAGAL][0m {commit_err}")
		print(f"  [38;5;244m   (Gunakan menu [4] Pulihkan Sesi untuk undo)[0m")
		if _tanya_lanjut_commit_sama(commit_hash):print(f"  [35m➜  Lanjut cari & ganti lagi (masih nambal commit yang sama)...[0m");cari_dan_ganti_manual();return
	else:print();print('  \x1b[33m[INFO]\x1b[0m Tidak ada perubahan yang diterapkan dalam sesi ini.')
	input('\n  Tekan Enter untuk kembali ke menu...')
def setup_git_identity():
	global GIT_USER_EMAIL,GIT_USER_NAME;msg=''
	while True:
		tsize=_term_size();term_cols,term_lines=tsize.columns,tsize.lines
		if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_cols} kolom x {term_lines} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();get_key();continue
		clear();M=header('Identitas Git');print(f"{M}  [1mPENGATURAN SAAT INI:[0m");print(f"{M}  1. Email commit : [36m{GIT_USER_EMAIL}[0m");print(f"{M}  2. Nama commit  : [36m{GIT_USER_NAME}[0m");print()
		if msg:print(f"{M}  {msg}\n");msg=''
		print(f"{M}  [38;5;{C_VIOLET}mPilih nomor (1-2) untuk mengubah, atau 'Q' untuk kembali:[0m");sys.stdout.write(f"{M}  [1;32m❯ [0m");sys.stdout.flush();k=get_key()
		if k.lower()=='q'or k=='ESC':break
		elif k=='RESIZE':continue
		elif k=='1':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Email baru [{GIT_USER_EMAIL}]: ").strip()
			if val:GIT_USER_EMAIL=val;save_git_identity();msg='\x1b[32m✅ Tersimpan\x1b[0m'
			sys.stdout.write('\x1b[?25l')
		elif k=='2':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Nama baru [{GIT_USER_NAME}]: ").strip()
			if val:GIT_USER_NAME=val;save_git_identity();msg='\x1b[32m✅ Tersimpan\x1b[0m'
			sys.stdout.write('\x1b[?25l')
	save_git_identity();print(f"\n{M}  [32m[OK][0m Identitas git berhasil disimpan.");input(f"\n{M}  Tekan Enter untuk kembali ke menu...")
def kelola_folder_exclude():
	msg=''
	while True:
		tsize=_term_size();term_cols,term_lines=tsize.columns,tsize.lines
		if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_cols} kolom x {term_lines} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();get_key();continue
		clear();M=header('Kelola Exclude');entries=_read_frignore_raw();print(f"{M}  [1mBAWAAN TOOL (selalu di-skip, tidak bisa dihapus):[0m");print(f"{M}  [38;5;{C_GRAY}m{", ".join(sorted(BASE_IGNORE_DIRS))}[0m");print();print(f"{M}  [1mTAMBAHAN KAMU (disimpan di .frignore):[0m")
		if entries:
			for(i,e)in enumerate(entries,1):jenis='ekstensi'if e.startswith('*.')else'folder';print(f"{M}  {i}. [36m{e}[0m [38;5;{C_DGRAY}m({jenis})[0m")
		else:print(f"{M}  [38;5;{C_DGRAY}m(belum ada folder/ekstensi tambahan)[0m")
		print()
		if msg:print(f"{M}  {msg}\n");msg=''
		print(f"{M}  [38;5;{C_VIOLET}m[A] Tambah   [D] Hapus   [Q] Kembali[0m");sys.stdout.write(f"{M}  [1;32m❯ [0m");sys.stdout.flush();k=get_key()
		if k.lower()=='q'or k=='ESC':break
		elif k=='RESIZE':continue
		elif k.lower()=='a':
			sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Nama folder (mis. auth_info) atau ekstensi (mis. *.bak): ").strip();sys.stdout.write('\x1b[?25l')
			if val:
				norm=val if val.startswith('*.')else val.strip('/')
				if norm in entries:msg='\x1b[33m⚠ Sudah ada di daftar\x1b[0m'
				else:entries.append(norm);_write_frignore_raw(entries);load_frignore();msg=f"[32m✅ '{norm}' ditambahkan ke daftar exclude[0m"
		elif k.lower()=='d':
			if not entries:msg='\x1b[33m⚠ Belum ada yang bisa dihapus\x1b[0m'
			else:
				sys.stdout.write('\x1b[?25h');val=input(f"\r{M}  Nomor yang mau dihapus (1-{len(entries)}): ").strip();sys.stdout.write('\x1b[?25l')
				if val.isdigit()and 1<=int(val)<=len(entries):removed=entries.pop(int(val)-1);_write_frignore_raw(entries);load_frignore();msg=f"[32m✅ '{removed}' dihapus dari daftar exclude[0m"
				else:msg='\x1b[31m✗ Nomor tidak valid\x1b[0m'
	input(f"\n{M}  Tekan Enter untuk kembali ke menu...")
MENU_SECTIONS=[('OPERASI PATCH',[('1','Terapkan Patch','Eksekusi patch dari blok :find/:replace ke file target'),('2','Cari & Ganti','Cari cuplikan kode secara manual, lalu ganti isinya'),('3','Cek Saja','Simulasikan patch tanpa mengubah file (dry-run)')]),('MANAJEMEN',[('4','Pulihkan Sesi','Kembalikan 1 file atau seluruh commit git'),('5','Cek Sintaks','Validasi sintaks file .py sebelum diterapkan'),('6','Ubah Direktori','Pindahkan direktori kerja aktif ke folder lain'),('e','Kelola Exclude','Tambah/hapus folder atau ekstensi yang di-skip saat patch')]),('UTILITAS',[('7','Prompt AI','Salin instruksi format patch untuk asisten AI'),('8','AI Setup','Atur kredensial API key OpenAI'),('9','Threshold','Atur ambang toleransi pencocokan auto-anchor & partial scan'),('g','Identitas Git','Kelola nama & email penulis commit git'),('0','Keluar','Keluar dari aplikasi FR Tool')])]
def get_key(animate=False):
	global _resize_pending;fd=sys.stdin.fileno();old_settings=termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		while True:
			if _resize_pending:_resize_pending=False;return'RESIZE'
			ready,_,_=select.select([fd],[],[],.08 if animate else .15)
			if ready:break
			elif animate:return'ANIMATE'
		ch=sys.stdin.read(1)
		if ch=='\x1b':
			ch2=sys.stdin.read(1)
			if ch2=='[':
				ch3=sys.stdin.read(1)
				if ch3=='A':return'UP'
				elif ch3=='B':return'DOWN'
				elif ch3=='C':return'RIGHT'
				elif ch3=='D':return'LEFT'
			return'ESC'
		elif ch in('\r','\n'):return'ENTER'
		elif ch=='\x03':raise KeyboardInterrupt
		else:return ch
	finally:termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
def _animated_dir_text(text):
	import time,math;t=time.time()*3.5;out=[]
	for(i,char)in enumerate(text):wave=(math.sin(t-i*.2)+1)/2;r=int(91+105*wave);g=int(33+131*wave);b=int(182+73*wave);out.append(f"[1;38;2;{r};{g};{b}m{char}")
	out.append('\x1b[0m');return''.join(out)
_HEADER_TIPS=[('Tempel blok patch AI, lalu tekan [1]','untuk menerapkannya otomatis ke file'),('Pastikan isi :find sama persis dengan','kode asli di file, termasuk indentasi'),('Coba [3] Cek Saja dulu untuk pratinjau','sebelum patch diterapkan permanen'),('Gunakan [4] Pulihkan Sesi bila hasil','patch meleset dari yang diharapkan'),('Jalankan [5] Cek Sintaks setelah patch','untuk memastikan file tetap valid'),('Naikkan [9] Threshold jika pencocokan','gagal karena teks sedikit berbeda'),('Sertakan baris unik di :find agar','posisi penyisipan tidak ambigu'),('Satu blok patch bisa mencakup','beberapa file sekaligus dalam 1 :file')]
_HEADER_TIP_INTERVAL=180
def _get_dynamic_tip():window=int(time.time()//_HEADER_TIP_INTERVAL);idx=window*2654435761%len(_HEADER_TIPS);return _HEADER_TIPS[idx]
_HEADER_ACTIVITY_CACHE={'text':None,'ts':.0}
_HEADER_ACTIVITY_TTL=5.
def _get_recent_activity():
	now=time.time();cached=_HEADER_ACTIVITY_CACHE
	if cached['text']is not None and now-cached['ts']<_HEADER_ACTIVITY_TTL:return cached['text']
	text='Belum ada aktivitas tercatat'
	try:
		r=subprocess.run(['git','-C',SOURCE_ROOT,'log','-1','--format=%s|%cr'],capture_output=True,text=True,timeout=1.5)
		if r.returncode==0 and r.stdout.strip():subj,_,rel=r.stdout.strip().partition('|');subj=subj.strip();text=f"{subj} ({rel.strip()})"if rel.strip()else subj
	except Exception:pass
	if text=='Belum ada aktivitas tercatat':
		try:
			log_path=os.path.join(SOURCE_ROOT,'.patch_backups','fail_log.json')
			if os.path.exists(log_path):
				with open(log_path,'r')as f:logs=json.load(f)
				if logs:text=f"Percobaan patch: {logs[-1].get("timestamp","-")}"
		except Exception:pass
	cached['text']=text;cached['ts']=now;return text
def draw_menu(selected_idx):
	global _last_draw_size;term_size=_term_size();term_cols=term_size.columns;term_lines=term_size.lines;size_changed=_last_draw_size is not None and _last_draw_size!=(term_cols,term_lines);_last_draw_size=term_cols,term_lines
	if term_cols<MIN_TERM_COLS or term_lines<MIN_TERM_LINES:warn=['','  \x1b[1;38;5;196m⚠  Layar terlalu kecil / zoom terlalu dalam\x1b[0m',f"  [38;5;{C_GRAY}mMinimal {MIN_TERM_COLS} kolom x {MIN_TERM_LINES} baris[0m",f"  [38;5;{C_GRAY}mSaat ini   : {term_cols} kolom x {term_lines} baris[0m",'',f"  [38;5;{C_DGRAY}mPerbesar (zoom out) tampilan terminal, lalu tekan tombol apa saja...[0m",''];sys.stdout.write('\x1b[?2026h\x1b[2J\x1b[3J\x1b[H'+'\n'.join(line+'\x1b[K'for line in warn)+'\x1b[0J\x1b[?2026l');sys.stdout.flush();return
	compact=term_lines<30;_zoom_factor=term_cols/8e1;W=max(24,min(term_cols-2,int(term_cols*.95)));div_w=W-2;max_path_len=max(5,div_w-15);root_short=SOURCE_ROOT if len(SOURCE_ROOT)<=max_path_len else'…'+SOURCE_ROOT[-(max_path_len-1):];buf=[];buf.append('');two_col=div_w>=56;left_w=max(18,int(div_w*.4))if two_col else div_w;right_w=div_w-left_w-3 if two_col else 0
	if two_col and right_w<16:two_col=False;left_w,right_w=div_w,0
	mascot_lines=_render_mascot_frame(_get_mascot_frame(),RGB_TERRACOTTA_DARK,RGB_TERRACOTTA_LIGHT,RGB_DELTA_LIGHT);left_cells=[_pad_cell(l,left_w,center=True)for l in mascot_lines];left_cells.append(_pad_cell('',left_w));_lp_len=max(6,left_w-10);_dir_disp=root_short if len(root_short)<=_lp_len else'…'+root_short[-(_lp_len-1):];left_cells.append(_pad_cell(f"[38;5;{C_DGRAY}m{VERSION} · By Reza[0m",left_w,center=True));left_cells.append(_pad_cell(f"[38;5;{C_GRAY}mDIR [0m{_animated_dir_text(_dir_disp)}",left_w,center=True));_caproj_label=f"[1;38;5;46m📦 .caproj: ON[0m"if CAPROJ_MODE_ON else f"[38;5;{C_DGRAY}m📦 .caproj: OFF · Ctrl+Q[0m";left_cells.append(_pad_cell(_caproj_label,left_w,center=True))
	if two_col:
		_tip_l1,_tip_l2=_get_dynamic_tip();_tip_l1=_tip_l1 if len(_tip_l1)<=right_w else _tip_l1[:max(0,right_w-1)]+'…';_tip_l2=_tip_l2 if len(_tip_l2)<=right_w else _tip_l2[:max(0,right_w-1)]+'…';right_cells=[_pad_cell(f"[1;38;5;{C_BORDER}mTips[0m",right_w),_pad_cell(f"[38;5;{C_GRAY}m{_tip_l1}[0m",right_w),_pad_cell(f"[38;5;{C_GRAY}m{_tip_l2}[0m",right_w),_pad_cell(f"[38;5;{C_DGRAY}m{"─"*right_w}[0m",right_w),_pad_cell(f"[1;38;5;{C_BORDER}mCommit Terakhir[0m",right_w)];_act=_get_recent_activity()
		for _act_line in _wrap_plain_text(_act,right_w):right_cells.append(_pad_cell(f"[38;5;{C_GRAY}m{_act_line}[0m",right_w))
		while len(right_cells)<len(left_cells):right_cells.append(_pad_cell('',right_w))
		while len(left_cells)<len(right_cells):left_cells.append(_pad_cell('',left_w))
		_div=f"[38;5;{C_DGRAY}m │ [0m";header_rows=[l+_div+r for(l,r)in zip(left_cells,right_cells)]
	else:header_rows=left_cells
	_title=f" FR TOOL {VERSION} "
	if len(_title)>div_w-2:_title=_title[:max(0,div_w-2)]
	_dash_r=max(0,div_w-2-len(_title));buf.append(f"  [38;5;{C_BORDER}m╭──[0m[1;38;5;{C_BORDER}m{_title}[0m[38;5;{C_BORDER}m{"─"*_dash_r}╮[0m")
	for row in header_rows:buf.append(f"  [38;5;{C_BORDER}m│[0m{row}[38;5;{C_BORDER}m│[0m")
	buf.append(f"  [38;5;{C_BORDER}m╰{"─"*div_w}╯[0m");buf.append('');buf.append(f"  [38;5;{C_BORDER}m╭{"─"*div_w}╮[0m");flat_idx=0
	for(s_i,(sec_title,items))in enumerate(MENU_SECTIONS):
		if s_i>0:buf.append(f"  [38;5;{C_BORDER}m├{"─"*div_w}┤[0m")
		sec_label=f"  {sec_title} "
		if len(sec_label)>div_w:sec_label=sec_label[:div_w]
		line_len=max(0,div_w-len(sec_label));buf.append(f"  [38;5;{C_BORDER}m│[0m[1;38;5;{C_VIOLET}m{sec_label}[0m[38;5;{C_DGRAY}m{"─"*line_len}[0m[38;5;{C_BORDER}m│[0m")
		for(key,label,desc)in items:
			is_sel=flat_idx==selected_idx;k_color=C_DGRAY if key=='0'else C_CYAN;marker='❯'if is_sel else' ';base_len=8;lbl_len=max(12,min(30,div_w//3))
			if base_len+lbl_len>div_w:lbl_len=max(0,div_w-base_len)
			label_padded=label[:lbl_len].ljust(lbl_len);max_desc=div_w-base_len-lbl_len;desc_t=desc[:max_desc]if max_desc>0 else'';row_raw=f" {marker} [{key}]  {label_padded}{desc_t}";pad=max(0,div_w-len(row_raw))
			if is_sel:row=f"[48;2;110;60;35m[1;38;2;230;210;255m {marker} [{key}]  {label_padded}{desc_t}{" "*pad}[0m"
			else:row=f"   [38;5;{C_BORDER}m[[0m[1;38;5;{k_color}m{key}[38;5;{C_BORDER}m][0m  [1;38;5;{C_WHITE}m{label_padded}[0m[38;5;{C_GRAY}m{desc_t}[0m{" "*pad}"
			buf.append(f"  [38;5;{C_BORDER}m│[0m{row}[38;5;{C_BORDER}m│[0m");flat_idx+=1
	buf.append(f"  [38;5;{C_BORDER}m╰{"─"*div_w}╯[0m");content_height=len(buf)
	if content_height<term_lines:available_v=term_lines-content_height;top_pad=available_v//3;bottom_pad=available_v-top_pad-1;buf=['']*top_pad+buf
	hint='↑↓ pilih   Enter konfirmasi   atau ketik nomor langsung'
	if len(hint)>term_cols-4:hint='↑↓ pilih   Enter eksekusi'
	if len(hint)>term_cols-4:hint='Navigasi ↑↓'
	buf.append(f"  [38;5;{C_DGRAY}m{hint}[0m");buf.append('');_content_w=max((_vlen(l)for l in buf if l),default=0);_extra_margin=max(0,(term_cols-_content_w)//2)
	if _extra_margin:buf=[' '*_extra_margin+l if l else l for l in buf]
	if len(buf)>term_lines:buf=buf[:max(1,term_lines-1)]
	clear_prefix='\x1b[2J'if size_changed else'';sys.stdout.write('\x1b[?2026h'+clear_prefix+'\x1b[H'+'\n'.join(line+'\x1b[K'for line in buf)+'\x1b[0J\x1b[?2026l');sys.stdout.flush()
def _sys_auth():
	import subprocess,urllib.request,urllib.error,urllib.parse,json,sys,time,os,uuid,hashlib;FIREBASE_URL='https://frtools-users-default-rtdb.asia-southeast1.firebasedatabase.app/users';ADMIN_WA='584161220741';sys.stdout.write('\x1b[?25l');fast_clear();print('\n  \x1b[36m[System]\x1b[0m Memeriksa konfigurasi perangkat...');hwid='';_INVALID_ANDROID_ID_VALUES={'null','none','unknown','nan','0','00000000','0000000000000000','undefined','n/a',''}
	try:
		out=subprocess.getoutput('settings get secure android_id').strip();out_clean=out.strip().strip('"').strip("'")
		if out_clean and'Failure'not in out and'not found'not in out.lower()and len(out_clean)<=20 and out_clean.lower()not in _INVALID_ANDROID_ID_VALUES:hwid=out_clean
	except:pass
	if not hwid:
		try:model=subprocess.getoutput('getprop ro.product.model').strip();uid=subprocess.getoutput('id -u').strip();board=subprocess.getoutput('getprop ro.board.platform').strip();serial=subprocess.getoutput('getprop ro.serialno').strip()
		except:model=uid=board=serial=''
		id_file=os.path.expanduser('~/.frtool_hwid');install_salt=''
		if os.path.exists(id_file):
			try:
				with open(id_file,'r')as f:content=f.read().strip()
				if content.count('|')==2:
					saved_id,saved_fp,saved_salt=content.split('|',2);install_salt=saved_salt;check_fp=hashlib.md5(f"{model}_{uid}_{board}_{serial}_{saved_salt}".encode()).hexdigest()
					if saved_fp==check_fp:hwid=saved_id
				elif content.count('|')==1:saved_id,_old_fp=content.split('|',1);hwid=saved_id
				elif len(content)==13 and content.startswith('FR-'):hwid=content
			except:pass
		if not hwid:hwid='FR-'+uuid.uuid4().hex[:10].upper()
		if not install_salt:install_salt=uuid.uuid4().hex
		try:
			current_fp=hashlib.md5(f"{model}_{uid}_{board}_{serial}_{install_salt}".encode()).hexdigest()
			with open(id_file,'w')as f:f.write(f"{hwid}|{current_fp}|{install_salt}")
		except:pass
	print(f"  [38;5;244mID Lisensi: {hwid}[0m");safe_hwid=urllib.parse.quote(hwid);check_url=f"{FIREBASE_URL}/{safe_hwid}.json"
	try:_fp_model=subprocess.getoutput('getprop ro.product.model').strip();_fp_board=subprocess.getoutput('getprop ro.board.platform').strip();_fp_serial=subprocess.getoutput('getprop ro.serialno').strip()
	except Exception:_fp_model=_fp_board=_fp_serial=''
	device_fp=hashlib.md5(f"{_fp_model}_{_fp_board}_{_fp_serial}".encode()).hexdigest()
	try:
		req=urllib.request.Request(check_url,headers={'User-Agent':'Mozilla/5.0'})
		with urllib.request.urlopen(req,timeout=10)as response:data=json.loads(response.read().decode('utf-8'))
		expired_at=data.get('expired_at','')if isinstance(data,dict)else'';is_expired=False;sisa_hari=None
		if expired_at:
			try:
				exp_date=datetime.strptime(expired_at,'%Y-%m-%d');now_date=datetime.now()
				if now_date>exp_date.replace(hour=23,minute=59,second=59):is_expired=True
				else:sisa_hari=(exp_date-now_date).days
			except Exception:pass
		try:
			import hmac as _hm,hashlib as _hs;_sudah_terdaftar=isinstance(data,dict)and bool(data)
			if _sudah_terdaftar:
				_sig_rcv=data.get('sig','');_status=data.get('status','');_exp=data.get('expired_at','');_sig_exp=_hm.new(bytes.fromhex(_vkey),f"{hwid}|{_status}|{_exp}".encode(),_hs.sha256).hexdigest()
				if not _hm.compare_digest(_sig_exp,_sig_rcv):fast_clear();print('\n  \x1b[31m[ERROR]\x1b[0m Konfigurasi tidak valid.');sys.stdout.write('\x1b[?25h');sys.exit(0)
		except Exception:pass
		if not data or not isinstance(data,dict)or data.get('status')!='active'or is_expired:
			print('\n  \x1b[31m[AKSES DITOLAK]\x1b[0m Lisensi Premium tidak ditemukan, belum aktif, atau sudah kedaluwarsa!')
			if data and isinstance(data,dict)and data.get('status')=='banned':print('  \x1b[1;31m[!] ID PERANGKAT INI TELAH DIBLOKIR.\x1b[0m')
			elif is_expired:print(f"  [1;31m[!] MASA AKTIF LISENSI SUDAH HABIS PADA {expired_at}.[0m")
			else:print('  ID Perangkat kamu belum terdaftar di database.')
			print('\n  \x1b[33mMengarahkan ke WhatsApp Admin dalam 3 detik...\x1b[0m');time.sleep(3);wa_text=f"Halo Admin, saya mau beli/perpanjang lisensi premium. Ini ID saya: {hwid}";wa_url=f"https://wa.me/{ADMIN_WA}?text={urllib.parse.quote(wa_text)}"
			try:subprocess.run(['termux-open-url',wa_url],check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
			except:
				try:subprocess.run(['am','start','-a','android.intent.action.VIEW','-d',wa_url],check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
				except:print(f"\n  [36mSilakan salin dan buka link ini manual:[0m\n  {wa_url}")
			sys.stdout.write('\x1b[?25h');sys.exit(0)
		else:
			_saved_fp=data.get('device_fp','')if isinstance(data,dict)else''
			if _saved_fp and _saved_fp!=device_fp:
				fast_clear();print('\n  \x1b[31m[AKSES DITOLAK]\x1b[0m ID Lisensi ini terdeteksi dipakai di perangkat lain.');print('  \x1b[1;31m[!] Satu ID Lisensi hanya untuk SATU perangkat.\x1b[0m');print('\n  \x1b[33mMengarahkan ke WhatsApp Admin dalam 3 detik...\x1b[0m');time.sleep(3);wa_text=f"Halo Admin, ID Lisensi saya ({hwid}) terdeteksi dipakai di perangkat lain. Mohon dibantu.";wa_url=f"https://wa.me/{ADMIN_WA}?text={urllib.parse.quote(wa_text)}"
				try:subprocess.run(['termux-open-url',wa_url],check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
				except:
					try:subprocess.run(['am','start','-a','android.intent.action.VIEW','-d',wa_url],check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
					except:print(f"\n  [36mSilakan salin dan buka link ini manual:[0m\n  {wa_url}")
				sys.stdout.write('\x1b[?25h');sys.exit(0)
			if _saved_fp!=device_fp:
				try:_patch_req=urllib.request.Request(check_url,data=json.dumps({'device_fp':device_fp}).encode(),headers={'User-Agent':'Mozilla/5.0','Content-Type':'application/json'},method='PATCH');urllib.request.urlopen(_patch_req,timeout=10)
				except Exception:pass
			print('  \x1b[32m[OK]\x1b[0m Konfigurasi valid.')
			if sisa_hari is not None:
				if sisa_hari<=3:print(f"  [33m[PERINGATAN][0m Aktif hingga {expired_at} ({sisa_hari} hari lagi).")
				else:print(f"  [38;5;244mAktif hingga: {expired_at}  ({sisa_hari} hari lagi)[0m")
			time.sleep(1);fast_clear();_rc_map['_v']=True;_rc_map['_t']=int(time.time());_rc_map['_k']=_hm.new(bytes.fromhex(_vkey),f"{hwid}|{_status}|{_exp}".encode(),_hs.sha256).digest();_rc_map['_hb']=int(time.time());_rc_map['_id']=hwid
	except Exception as e:fast_clear();print(f"\n  [31m[TIDAK ADA KONEKSI][0m Gagal terhubung ke internet.");print(f"  [38;5;244mPastikan internet menyala, lalu coba jalankan ulang tool.[0m");sys.stdout.write('\x1b[?25h');sys.exit(1)
def _find_git_root(start_dir,max_up=6):
	cur=os.path.abspath(start_dir)
	for _ in range(max_up+1):
		if os.path.isdir(os.path.join(cur,'.git')):return cur
		parent=os.path.dirname(cur)
		if parent==cur:break
		cur=parent
LOCAL_BUILD_VERSION=1
FIREBASE_CONFIG_URL='https://frtools-users-default-rtdb.asia-southeast1.firebasedatabase.app/app_config.json'
def _find_git_root(start_dir,max_up=6):
	cur=os.path.abspath(start_dir)
	for _ in range(max_up+1):
		if os.path.isdir(os.path.join(cur,'.git')):return cur
		parent=os.path.dirname(cur)
		if parent==cur:break
		cur=parent
def _do_git_pull_and_restart():
	exe_dir=os.path.dirname(os.path.abspath(sys.executable));git_root=_find_git_root(exe_dir)
	if not git_root:return False,"Folder tool ini bukan hasil 'git clone' (tidak ketemu .git)."
	try:
		fetch=subprocess.run(['git','-C',git_root,'fetch','--quiet'],timeout=30,capture_output=True)
		if fetch.returncode!=0:return False,'Gagal fetch dari GitHub (kemungkinan tidak ada internet).'
	except Exception as e:return False,f"Gagal menjalankan git fetch: {e}"
	try:stop_ev_u,t_u=_spinner_start('Menarik pembaruan dari GitHub (git pull)...',color='36');pull=subprocess.run(['git','-C',git_root,'pull','--ff-only','--quiet'],timeout=120,capture_output=True,text=True);_spinner_stop(stop_ev_u,t_u)
	except Exception as e:return False,f"Gagal menjalankan git pull: {e}"
	if pull.returncode!=0:
		detail=pull.stderr.strip()[:200]if pull.stderr else'';msg=f"git pull gagal (kemungkinan ada perubahan lokal yang bentrok)."
		if detail:msg+=f" Detail: {detail}"
		msg+=f" Jalankan manual: git -C {git_root} pull";return False,msg
	try:os.chmod(sys.executable,os.stat(sys.executable).st_mode|73)
	except Exception:pass
	print(f"\n  [32m[OK][0m Berhasil diperbarui ke versi terbaru. Merestart tool...");time.sleep(1.2);sys.stdout.write('\x1b[?25h\x1b[?1049l');sys.stdout.flush();os.execv(sys.executable,sys.argv);return True,None
def firebase_update_check():
	try:
		req=urllib.request.Request(FIREBASE_CONFIG_URL,headers={'User-Agent':'Mozilla/5.0'})
		with urllib.request.urlopen(req,timeout=10)as resp:cfg=json.loads(resp.read().decode('utf-8'))
	except Exception:return
	if not cfg or not isinstance(cfg,dict):return
	latest_version=int(cfg.get('latest_version',LOCAL_BUILD_VERSION));min_required=int(cfg.get('min_required_version',0));force_update=bool(cfg.get('force_update',False));changelog=str(cfg.get('changelog','')).strip()
	if LOCAL_BUILD_VERSION>=latest_version:return
	is_mandatory=force_update or LOCAL_BUILD_VERSION<min_required;clear();print(f"\n  [1;38;5;{C_CYAN}m[UPDATE TERSEDIA][0m Versi baru terdeteksi (via Firebase).");print(f"  [38;5;244mVersi lokal  : {LOCAL_BUILD_VERSION}[0m");print(f"  [38;5;244mVersi terbaru: {latest_version}[0m")
	if changelog:
		print(f"\n  [1mPerubahan:[0m")
		for line in changelog.splitlines()[:8]:print(f"    • {line}")
	print()
	if is_mandatory:
		print('  \x1b[31m[WAJIB]\x1b[0m Update ini WAJIB dipasang sebelum tool bisa dipakai.')
		while True:
			pilih=popup_confirm('UPDATE WAJIB',['Versi yang kamu pakai sudah tidak didukung lagi.','Update HARUS dipasang untuk melanjutkan.'],[('y','Update Sekarang (git pull)'),('q','Keluar')])
			if pilih!='y':sys.stdout.write('\x1b[?25h');sys.stdout.flush();sys.exit(0)
			ok,err=_do_git_pull_and_restart()
			if not ok:
				print(f"\n  [31m[GAGAL][0m {err}");lagi=popup_confirm('UPDATE GAGAL',['Pembaruan wajib gagal dipasang lewat git pull.','Coba lagi, atau keluar dan update manual nanti?'],[('y','Coba Lagi'),('q','Keluar')])
				if lagi!='y':sys.stdout.write('\x1b[?25h');sys.stdout.flush();sys.exit(0)
	else:
		pilih=popup_confirm('UPDATE TERSEDIA',['Ada pembaruan baru untuk tool ini di GitHub.','Perbarui sekarang via git pull? (tool akan restart otomatis)'],[('y','Ya, Perbarui'),('n','Lewati Dulu')])
		if pilih!='y':return
		ok,err=_do_git_pull_and_restart()
		if not ok:print(f"\n  [31m[GAGAL UPDATE][0m {err}");input('\n  Tekan Enter untuk lanjut memakai versi saat ini...')
def main():
	_init_blk();firebase_update_check();_sys_auth();load_thresholds();load_frignore();load_git_identity();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
	try:signal.signal(signal.SIGWINCH,_on_resize)
	except(AttributeError,ValueError):pass
	show_welcome();flat_keys=[key for(_,items)in MENU_SECTIONS for(key,_,_)in items];selected_idx=0;clear();sys.stdout.write('\x1b[?25l');sys.stdout.flush()
	try:
		while True:
			draw_menu(selected_idx);tombol=get_key(animate=True)
			if tombol=='ANIMATE':continue
			elif tombol=='UP':selected_idx=(selected_idx-1)%len(flat_keys);continue
			elif tombol=='DOWN':selected_idx=(selected_idx+1)%len(flat_keys);continue
			elif tombol=='ENTER':pilihan=flat_keys[selected_idx]
			elif tombol in flat_keys:pilihan=tombol;selected_idx=flat_keys.index(tombol)
			elif tombol=='\x11':global CAPROJ_MODE_ON;CAPROJ_MODE_ON=not CAPROJ_MODE_ON;continue
			else:continue
			global _GLOBAL_TIMER_START;_GLOBAL_TIMER_START=.0
			if pilihan=='0':sys.stdout.write('\x1b[?25h');sys.stdout.flush();clear();break
			elif pilihan=='1':
				sys.stdout.write('\x1b[?1049l');sys.stdout.flush();patch_text=paste_patch(dry_run=False)
				if patch_text:scan_dan_apply(patch_text)
				sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='2':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();cari_dan_ganti_manual();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='3':
				sys.stdout.write('\x1b[?1049l');sys.stdout.flush();patch_text=paste_patch(dry_run=True)
				if patch_text:scan_dan_apply(patch_text,dry_run=True)
				sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='4':restore_backup()
			elif pilihan=='5':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();cek_sintaks_menu();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='6':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();pilih_folder();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='e':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();kelola_folder_exclude();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='7':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();copy_prompt_ai();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='8':setup_ai()
			elif pilihan=='9':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();setup_threshold();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			elif pilihan=='g':sys.stdout.write('\x1b[?1049l');sys.stdout.flush();setup_git_identity();sys.stdout.write('\x1b[?1049h');sys.stdout.flush()
			sys.stdout.write('\x1b[?25l');sys.stdout.flush();clear()
	finally:sys.stdout.write('\x1b[?25h\x1b[?1049l');sys.stdout.flush()
if __name__=='__main__':main()