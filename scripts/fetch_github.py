"""Refresh public GitHub facts. Failed requests never replace the last snapshot."""
from datetime import datetime,timezone
import json,os,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]

def get(endpoint):
    headers={'User-Agent':'ashifrza-profile','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    token=os.environ.get('GH_TOKEN')
    if token:headers['Authorization']='Bearer '+token
    for attempt in range(3):
        try:
            with urlopen(Request('https://api.github.com/'+endpoint,headers=headers),timeout=30) as r:return json.load(r)
        except (OSError,HTTPError):
            if attempt==2:raise
            time.sleep(2**attempt)

def main():
    user=get('users/ashifrza');repos=[];page=1
    while True:
        batch=get(f'users/ashifrza/repos?type=owner&sort=pushed&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch)<100:break
        page+=1
    languages={}
    selected=[]
    fields=['name','description','html_url','homepage','language','stargazers_count','forks_count','fork','archived','pushed_at']
    for repo in repos:
        selected.append({k:repo[k] for k in fields})
        if not repo['fork'] and repo['name'].lower()!='ashifrza':
            for language,count in get(f"repos/ashifrza/{repo['name']}/languages").items():
                languages[language]=languages.get(language,0)+count
    data={'as_of':datetime.now(timezone.utc).date().isoformat(),'username':user['login'],'bio':user['bio'],'followers':user['followers'],'following':user['following'],'public_repos':len(repos),'stars':sum(r['stargazers_count'] for r in repos),'forks':sum(r['forks_count'] for r in repos),'repos':selected,'language_bytes':dict(sorted(languages.items(),key=lambda pair:-pair[1]))}
    out=ROOT/'data/github.json';tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');tmp.replace(out)
    print(f"Fetched {len(repos)} public repositories and {len(languages)} languages")

if __name__=='__main__':main()
