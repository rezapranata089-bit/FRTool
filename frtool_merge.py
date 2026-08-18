#!/usr/bin/env python3
"""
frtool_merge.py — Plugin OPSIONAL untuk FR Tool.

Fitur "Gabung Kode": scan semua file kode di sebuah folder project,
gabungkan isinya jadi satu teks dengan format jelas (path file, nama,
pembatas antar file), lalu otomatis disalin ke clipboard.

Modul ini SENGAJA berdiri sendiri (tidak import frtool.py) supaya:
  - frtool.py bisa mengimpornya secara opsional (try/except) tanpa risiko
    circular import atau menjalankan ulang kode inti frtool.py.
  - Kalau file ini dihapus/rusak, frtool.py tetap berjalan normal dan
    menu terkait otomatis hilang.

Entry point yang dipanggil dari frtool.py: run_menu(default_root=None)
"""

import os
import sys
import json
import subprocess
from datetime import datetime

HISTORY_PATH = os.path.expanduser("~/.frtool_merge_history.json")

DEFAULT_EXTS = ['kt', 'xml', 'json', 'js', 'css', 'kts', 'pro', 'gradle', 'toml', 'java']

JSON_MAX_SIZE = 50 * 1024  # 50 KB — file .json di atas ini dilewati

IGNORE_DIRS = {
    '.git', '.gradle', '.idea', 'build', '.kotlin', 'captures', '.cxx',
    'node_modules', '__pycache__', '.venv', 'venv', '.next', 'dist',
    '.vercel', '.cache', '.turbo', '.patch_backups',
}

SEP_WIDTH = 80


def _clear():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()


def _load_history():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_history(path):
    if not path or not os.path.isdir(path):
        return
    hist = _load_history()
    if path in hist:
        hist.remove(path)
    hist.insert(0, path)
    hist = hist[:5]
    try:
        with open(HISTORY_PATH, 'w') as f:
            json.dump(hist, f, indent=2)
    except Exception:
        pass


def _copy_to_clipboard(text):
    """Salin teks ke clipboard. Mendukung Termux, xclip, xsel, Windows, macOS."""
    cmds = [
        ['termux-clipboard-set'],
        ['xclip', '-selection', 'clipboard'],
        ['xsel', '--clipboard', '--input'],
        ['clip.exe'],
        ['pbcopy'],
    ]
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, input=text.encode('utf-8'), timeout=5,
                                capture_output=True)
            if r.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def _ask_folder(default_root):
    history = [p for p in _load_history() if p != default_root]

    print("  \033[1mPilih folder project yang mau di-scan:\033[0m\n")
    options = []
    if default_root:
        print(f"    [0] Direktori aktif saat ini: {default_root}")
        options.append(default_root)
    for i, p in enumerate(history, start=1):
        print(f"    [{i}] {p}")
        options.append(p)
    print(f"    [m] Ketik path baru")
    print(f"    [q] Batal\n")

    try:
        pilih = input("  Pilihan: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if pilih == '' and default_root:
        return default_root
    if pilih.lower() in ('q', 'batal'):
        return None
    if pilih.lower() == 'm':
        try:
            path = input("  Masukkan path folder: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if not path:
            return None
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            print(f"\n  \033[31m[GAGAL]\033[0m Folder tidak ditemukan: {path}")
            input("\n  Tekan Enter untuk kembali...")
            return None
        return path
    if pilih.isdigit():
        idx = int(pilih)
        if idx == 0 and default_root:
            return default_root
        if 1 <= idx <= len(history):
            return history[idx - 1]
    print("\n  \033[31m[GAGAL]\033[0m Pilihan tidak dikenal.")
    input("\n  Tekan Enter untuk kembali...")
    return None


def _ask_extensions():
    default_str = ','.join(DEFAULT_EXTS)
    print(f"\n  \033[1mEkstensi file yang disertakan\033[0m (pisah koma)")
    print(f"  Kosongkan lalu Enter untuk pakai default: {default_str}")
    try:
        raw = input("  Ekstensi: ").strip()
    except (EOFError, KeyboardInterrupt):
        raw = ''
    if not raw:
        return list(DEFAULT_EXTS)
    exts = [e.strip().lower().lstrip('.') for e in raw.split(',') if e.strip()]
    return exts or list(DEFAULT_EXTS)


def _scan_files(root, exts):
    ext_set = {e.lower() for e in exts}
    matched = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS and not d.startswith('.'))
        for fname in sorted(filenames):
            ext = fname.rsplit('.', 1)[-1].lower() if '.' in fname else ''
            if ext in ext_set:
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, root)
                matched.append((rel, full))
    matched.sort(key=lambda x: x[0])
    return matched


def _build_merged_text(files):
    parts = []
    skipped = []
    for rel, full in files:
        ext = rel.rsplit('.', 1)[-1].lower() if '.' in rel else ''
        if ext == 'json':
            try:
                size = os.path.getsize(full)
            except Exception as e:
                skipped.append((rel, str(e)))
                continue
            if size > JSON_MAX_SIZE:
                skipped.append((rel, f"json > {JSON_MAX_SIZE // 1024}KB, dilewati"))
                continue
        try:
            with open(full, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            skipped.append((rel, str(e)))
            continue
        parts.append(f"### FILE: {rel}\n{content}")
    return "\n\n".join(parts), skipped


def _build_file_tree(files, root):
    """Bangun representasi tree sederhana dari daftar file (path relatif)."""
    tree = {}
    for rel, _ in files:
        parts = rel.split(os.sep)
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault(parts[-1], None)

    root_name = os.path.basename(root.rstrip(os.sep)) or root
    lines = [root_name]

    def _render(node, prefix=""):
        entries = sorted(node.items(), key=lambda kv: (kv[1] is None, kv[0].lower()))
        count = len(entries)
        for i, (name, child) in enumerate(entries):
            is_last = (i == count - 1)
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + name)
            if child is not None:
                extension = "    " if is_last else "│   "
                _render(child, prefix + extension)

    _render(tree)
    return "\n".join(lines)


def run_menu(default_root=None):
    _clear()
    print("  \033[1;38;5;213m╔══════════════════════════════════════╗\033[0m")
    print("  \033[1;38;5;213m║           GABUNG KODE PROJECT          ║\033[0m")
    print("  \033[1;38;5;213m╚══════════════════════════════════════╝\033[0m\n")

    root = _ask_folder(default_root)
    if not root:
        return

    _save_history(root)

    exts = _ask_extensions()

    print(f"\n  Memindai folder: {root}")
    print(f"  Ekstensi: {', '.join(exts)}\n")

    files = _scan_files(root, exts)
    if not files:
        print("  \033[33m[INFO]\033[0m Tidak ada file yang cocok dengan ekstensi tersebut.")
        input("\n  Tekan Enter untuk kembali ke menu...")
        return

    tree_text = _build_file_tree(files, root)

    merged_text, skipped = _build_merged_text(files)
    merged_text = f"### PROJECT STRUCTURE\n{tree_text}\n\n{merged_text}"

    total_files = len(files) - len(skipped)
    total_chars = len(merged_text)
    total_lines = merged_text.count('\n') + 1

    print(f"  \033[32m[OK]\033[0m {total_files} file digabungkan "
          f"({total_lines} baris, {total_chars:,} karakter).")
    if skipped:
        print(f"  \033[33m[SKIP]\033[0m {len(skipped)} file dilewati:")
        for rel, err in skipped[:5]:
            print(f"         - {rel} ({err})")
        if len(skipped) > 5:
            print(f"         ... dan {len(skipped) - 5} lainnya")

    copied = _copy_to_clipboard(merged_text)
    if copied:
        print("\n  \033[32m[OK]\033[0m Hasil gabungan telah disalin ke clipboard.")
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback_path = os.path.join(root, f"frtool_merge_{ts}.txt")
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(merged_text)
            print(f"\n  \033[33m[INFO]\033[0m Clipboard tidak tersedia.")
            print(f"  Hasil gabungan disimpan ke file:\n    {fallback_path}")
        except Exception as e:
            print(f"\n  \033[31m[GAGAL]\033[0m Clipboard tidak tersedia dan gagal menyimpan file: {e}")

    input("\n  Tekan Enter untuk kembali ke menu...")


if __name__ == "__main__":
    run_menu(default_root=os.getcwd())