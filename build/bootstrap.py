from pathlib import Path
import tempfile,subprocess,shutil,base64
root=Path.cwd()
commit='a7f2260203befb7e9c70b585219f0f0b5ca57703'
with tempfile.TemporaryDirectory(prefix='khavaran-upstream-') as td:
 source=Path(td)/'source';source.mkdir()
 def git(*args):subprocess.run(['git',*args],cwd=source,check=True)
 git('init');git('config','core.autocrlf','false');git('remote','add','origin','https://github.com/rustdesk/rustdesk.git')
 git('fetch','--depth','1','origin',commit);git('checkout','--detach','FETCH_HEAD')
 git('-c','core.autocrlf=false','submodule','update','--init','--depth','1')
 for p in source.iterdir():
  if p.name=='.git':continue
  if p.name=='.github':
   for child in p.iterdir():
    if child.name=='workflows':continue
    target=root/'.github'/child.name
    if child.is_dir():shutil.copytree(child,target,dirs_exist_ok=True)
    else:shutil.copy2(child,target)
  elif p.is_dir():
   shutil.copytree(p,root/p.name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git'))
  else:shutil.copy2(p,root/p.name)
 subprocess.run(['git','apply','--check','build/khavaran.patch'],cwd=root,check=True)
 subprocess.run(['git','apply','build/khavaran.patch'],cwd=root,check=True)
 subprocess.run(['git','apply','--directory=libs/hbb_common','build/identity.patch'],cwd=root,check=True)
 (root/'flutter/assets').mkdir(exist_ok=True)
 (root/'flutter/assets/icon.png').write_bytes(base64.b64decode((root/'build/icon.b64').read_text()))
print('Loaded pinned RustDesk source with Khavaran Desk changes')
