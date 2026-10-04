"""Create a fresh GitHub repository and push the reviewed project and release tag.

Uses the standard authenticated GitHub CLI. Never requests or prints tokens.
"""
from pathlib import Path
import argparse
import subprocess
import shutil
import json
import datetime

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--public',action='store_true',help='Create a public repository; default is private.')
parser.add_argument('--name',default='Aygo-E85-Blend')
args=parser.parse_args()
if not shutil.which('gh'):raise SystemExit('GitHub CLI (gh) est requis pour cette commande de publication.')
def run(*cmd,capture=False,check=True):
    return subprocess.run(cmd,cwd=ROOT,check=check,text=True,capture_output=capture)
login=run('gh','api','user','--jq','.login',capture=True).stdout.strip()
if not login:raise SystemExit('Compte GitHub authentifié introuvable.')
if run('git','branch','--show-current',capture=True).stdout.strip()!='main':raise SystemExit('La branche revue doit être main.')
if run('git','status','--porcelain',capture=True).stdout.strip():raise SystemExit('Créer le commit de la version revue avant publication.')
run('git','rev-parse','HEAD',capture=True)
if run('git','remote',capture=True).stdout.strip():raise SystemExit('Ce script attend un projet neuf sans remote pour éviter une destination ambiguë.')
name=args.name
candidate=f'{login}/{name}'
existing=run('gh','repo','view',candidate,'--json','nameWithOwner',capture=True,check=False)
if existing.returncode==0:
    name=name+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
    candidate=f'{login}/{name}'
description='Calculateur E85/SP98 pour Toyota Aygo : rapport sourcé, simulations avec incertitudes et prototypes natifs Kotlin/Compose et Swift/SwiftUI.'
run('gh','repo','create',candidate,'--public' if args.public else '--private','--description',description,
    '--source',str(ROOT),'--remote','origin','--push')
run('gh','repo','edit',candidate,'--default-branch','main','--enable-issues=true','--enable-wiki=false',
    '--delete-branch-on-merge','--add-topic','toyota-aygo,ethanol,fuel-calculator,kotlin,swift')
run('git','tag','-a','v0.1.0','-F','RELEASE_NOTES.md')
run('git','push','origin','v0.1.0')
info=json.loads(run('gh','repo','view',candidate,'--json','nameWithOwner,url,isPrivate',capture=True).stdout)
print(json.dumps(dict(repository=info,release='CI publiera la préversion après réussite des jobs.'),ensure_ascii=False))
