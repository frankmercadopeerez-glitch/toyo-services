"""Apply only approved branding to public pages; preserve unrelated content edits."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from site_ui import apply_branding

parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
parser.add_argument('--backup',action='store_true')
args=parser.parse_args()
root=args.root.resolve()
public={'blog','servicios','modelos','nosotros','legal','privacidad','metodologia','preguntas-frecuentes','creditos-imagenes','cotizar','repuestos'}
files=list(root.glob('*.html'))
for directory in sorted(public):
    files.extend((root/directory).rglob('*.html'))
changed=[]
for file in sorted(files):
    old=file.read_text(encoding='utf-8')
    if 'class="brand"' not in old and 'styles.min.css' not in old:
        continue
    new=apply_branding(old)
    assert apply_branding(new)==new, f'Non-idempotent branding: {file}'
    if old!=new:
        if args.backup:
            dest=root/'output/brand-before-2026-11-04'/file.relative_to(root)
            if not dest.exists():
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(file,dest)
        file.write_text(new,encoding='utf-8')
        changed.append(file.relative_to(root).as_posix())
print(json.dumps({'root':str(root),'public_pages':len(files),'changed':len(changed),'paths':changed},ensure_ascii=False))
