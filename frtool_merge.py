#!/usr/bin/env python3
import os,sys,json,subprocess
from datetime import datetime
HISTORY_PATH=os.path.expanduser('~/.frtool_merge_history.json')
DEFAULT_EXTS=['kt','xml','json','js','css','kts','pro','gradle','toml','java']
EXT_TEMPLATES={'1':('Kotlin / Android',['kt','kts','java','xml','gradle','properties','pro','toml','json','yml','yaml','aidl','proto','cpp','c','h','cmake','md','txt']),'2':('Flutter / Dart',['dart','yaml','yml','json','gradle','kts','xml','plist','kt','java','swift','properties','pro','frag','vert','arb','toml','cfg','md','txt']),'3':('HTML / Web',['html','htm','css','scss','sass','less','js','mjs','cjs','json','ts','jsx','tsx','vue','svelte','svg','yml','yaml','env','md']),'4':('Python',['py','pyi','json','toml','cfg','ini','txt','yml','yaml','env','sh','md','sql']),'5':('Node / JS Backend',['js','mjs','cjs','ts','json','env','yml','yaml','sql','prisma','graphql','sh','md']),'6':('Java / Spring / Maven',['java','kt','xml','gradle','kts','properties','yml','yaml','json','sql','sh','md']),'7':('CI / DevOps / Config',['yml','yaml','json','toml','ini','cfg','conf','properties','env','sh','bat','tf','dockerfile','md','txt'])}
JSON_MAX_SIZE=51200
IGNORE_DIRS={'.git','.gradle','.idea','build','.kotlin','captures','.cxx','node_modules','__pycache__','.venv','venv','.next','dist','.vercel','.cache','.turbo','.patch_backups'}
SEP_WIDTH=80
CLIPBOARD_DIR='/storage/emulated/0/ClipBoard'
CLIPBOARD_MAX_CHARS=900000
def _save_to_clipboard_folder(text,root):
	B=os.path.basename(root.rstrip(os.sep))or'project';B=''.join(A if A.isalnum()or A in'-_.'else'_'for A in B);I=datetime.now().strftime('%Y%m%d_%H%M%S');C=CLIPBOARD_DIR
	if not os.path.isdir(os.path.dirname(CLIPBOARD_DIR)):C=os.path.expanduser('~/ClipBoard');print(f"  [33m[PERINGATAN][0m Storage Android tidak terbaca, simpan ke {C}")
	try:
		A=os.path.join(C,B);os.makedirs(A,exist_ok=True);D=os.path.join(A,'merge.txt')
		for E in os.listdir(A):
			if E.startswith('merge_')and E.endswith('.txt'):
				try:os.remove(os.path.join(A,E))
				except OSError:pass
		F=D+'.tmp'
		with open(F,'w',encoding='utf-8')as G:G.write(text)
		os.replace(F,D);return D,None
	except Exception as H:return None,str(H)
def _clear():sys.stdout.write('\x1b[2J\x1b[H');sys.stdout.flush()
def _load_history():
	if os.path.exists(HISTORY_PATH):
		try:
			with open(HISTORY_PATH,'r')as A:return json.load(A)
		except Exception:pass
	return[]
def _save_history(path):
	B=path
	if not B or not os.path.isdir(B):return
	A=_load_history()
	if B in A:A.remove(B)
	A.insert(0,B);A=A[:5]
	try:
		with open(HISTORY_PATH,'w')as C:json.dump(A,C,indent=2)
	except Exception:pass
def _copy_to_clipboard(text):
	A=[['termux-clipboard-set'],['xclip','-selection','clipboard'],['xsel','--clipboard','--input'],['clip.exe'],['pbcopy']]
	for B in A:
		try:
			C=subprocess.run(B,input=text.encode('utf-8'),timeout=5,capture_output=True)
			if C.returncode==0:return True
		except(FileNotFoundError,subprocess.TimeoutExpired,OSError):continue
	return False
def _ask_folder(default_root):
	A=default_root;D=[B for B in _load_history()if B!=A];print('  \x1b[1mPilih folder project yang mau di-scan:\x1b[0m\n');F=[]
	if A:print(f"    [0] Direktori aktif saat ini: {A}");F.append(A)
	for(H,G)in enumerate(D,start=1):print(f"    [{H}] {G}");F.append(G)
	print(f"    [m] Ketik path baru");print(f"    [q] Batal\n")
	try:C=input('  Pilihan: ').strip()
	except(EOFError,KeyboardInterrupt):return
	if C==''and A:return A
	if C.lower()in('q','batal'):return
	if C.lower()=='m':
		try:B=input('  Masukkan path folder: ').strip()
		except(EOFError,KeyboardInterrupt):return
		if not B:return
		B=os.path.abspath(os.path.expanduser(B))
		if not os.path.isdir(B):print(f"\n  [31m[GAGAL][0m Folder tidak ditemukan: {B}");input('\n  Tekan Enter untuk kembali...');return
		return B
	if C.isdigit():
		E=int(C)
		if E==0 and A:return A
		if 1<=E<=len(D):return D[E-1]
	print('\n  \x1b[31m[GAGAL]\x1b[0m Pilihan tidak dikenal.');input('\n  Tekan Enter untuk kembali...')
def _ask_extensions():
	D=','.join(DEFAULT_EXTS);print(f"\n  [1mPilih template ekstensi[0m")
	for E in sorted(EXT_TEMPLATES.keys()):F,B=EXT_TEMPLATES[E];print(f"    [{E}] {F} ({", ".join(B)})")
	print(f"    [d] Default lama ({D})");print(f"    [c] Ketik manual (pisah koma)");print(f"  Kosongkan lalu Enter untuk pakai default: {D}")
	try:A=input('  Pilihan: ').strip()
	except(EOFError,KeyboardInterrupt):A=''
	if not A or A.lower()=='d':return list(DEFAULT_EXTS)
	if A in EXT_TEMPLATES:return list(EXT_TEMPLATES[A][1])
	if A.lower()=='c':
		try:C=input('  Ekstensi: ').strip()
		except(EOFError,KeyboardInterrupt):C=''
		if not C:return list(DEFAULT_EXTS)
		B=[A.strip().lower().lstrip('.')for A in C.split(',')if A.strip()];return B or list(DEFAULT_EXTS)
	B=[A.strip().lower().lstrip('.')for A in A.split(',')if A.strip()];return B or list(DEFAULT_EXTS)
def _scan_all_entries(root):
	A=[]
	for(D,B,E)in os.walk(root):
		B[:]=sorted(A for A in B if A not in IGNORE_DIRS)
		for F in sorted(E):C=os.path.join(D,F);G=os.path.relpath(C,root);A.append((G,C))
	A.sort(key=lambda x:x[0]);return A
def _scan_files(root,exts):
	E={A.lower()for A in exts};A=[]
	for(F,C,G)in os.walk(root):
		C[:]=sorted(A for A in C if A not in IGNORE_DIRS)
		for B in sorted(G):
			H=B.rsplit('.',1)[-1].lower()if'.'in B else''
			if H in E:D=os.path.join(F,B);I=os.path.relpath(D,root);A.append((I,D))
	A.sort(key=lambda x:x[0]);return A
def _build_merged_text(files):
	D=[];B=[]
	for(A,E)in files:
		F=A.rsplit('.',1)[-1].lower()if'.'in A else''
		if F=='json':
			try:G=os.path.getsize(E)
			except Exception as C:B.append((A,str(C)));continue
			if G>JSON_MAX_SIZE:B.append((A,f"json > {JSON_MAX_SIZE//1024}KB, dilewati"));continue
		try:
			with open(E,'r',encoding='utf-8',errors='replace')as H:I=H.read()
		except Exception as C:B.append((A,str(C)));continue
		D.append(f"### FILE: {A}\n{I}")
	return'\n\n'.join(D),B
def _build_file_tree(files,root):
	B={}
	for(F,I)in files:
		C=F.split(os.sep);A=B
		for G in C[:-1]:A=A.setdefault(G,{})
		A.setdefault(C[-1],None)
	H=os.path.basename(root.rstrip(os.sep))or root;D=[H]
	def E(node,prefix=''):
		A=prefix;B=sorted(node.items(),key=lambda kv:(kv[1]is None,kv[0].lower()));G=len(B)
		for(H,(I,C))in enumerate(B):
			F=H==G-1;J='└── 'if F else'├── ';D.append(A+J+I)
			if C is not None:K='    'if F else'│   ';E(C,A+K)
	E(B);return'\n'.join(D)
def run_menu(default_root=None):
	_clear();print('  \x1b[1;38;5;213m╔══════════════════════════════════════╗\x1b[0m');print('  \x1b[1;38;5;213m║           GABUNG KODE PROJECT          ║\x1b[0m');print('  \x1b[1;38;5;213m╚══════════════════════════════════════╝\x1b[0m\n');A=_ask_folder(default_root)
	if not A:return
	_save_history(A);E=_ask_extensions();print(f"\n  Memindai folder: {A}");print(f"  Ekstensi: {", ".join(E)}\n");D=_scan_files(A,E)
	if not D:print('  \x1b[33m[INFO]\x1b[0m Tidak ada file yang cocok dengan ekstensi tersebut.');input('\n  Tekan Enter untuk kembali ke menu...');return
	I=_scan_all_entries(A);J=_build_file_tree(I,A);B,C=_build_merged_text(D);B=f"### PROJECT STRUCTURE\n{J}\n\n{B}";K=len(D)-len(C);F=len(B);L=B.count('\n')+1;print(f"  [32m[OK][0m {K} file digabungkan ({L} baris, {F:,} karakter).")
	if C:
		print(f"  [33m[SKIP][0m {len(C)} file dilewati:")
		for(M,N)in C[:5]:print(f"         - {M} ({N})")
		if len(C)>5:print(f"         ... dan {len(C)-5} lainnya")
	G=len(B)>=CLIPBOARD_MAX_CHARS;O=False if G else _copy_to_clipboard(B)
	if O:print('\n  \x1b[32m[OK]\x1b[0m Hasil gabungan telah disalin ke clipboard.')
	else:
		H,P=_save_to_clipboard_folder(B,A)
		if H:Q=f"Hasil terlalu besar untuk clipboard ({F:,} karakter)."if G else'Clipboard tidak tersedia.';print(f"\n  [33m[INFO][0m {Q}");print(f"  Hasil gabungan disimpan ke file:\n    {H}")
		else:print(f"\n  [31m[GAGAL][0m Gagal menyimpan file: {P}")
	input('\n  Tekan Enter untuk kembali ke menu...')
if __name__=='__main__':run_menu(default_root=os.getcwd())