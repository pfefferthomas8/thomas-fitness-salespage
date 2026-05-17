import json, urllib.request, os, subprocess, sys

try:
    commits = subprocess.check_output(['git', 'log', '--oneline', '-10'], text=True).strip()
except Exception:
    commits = ''

try:
    changed = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~1'], text=True).strip()
except Exception:
    changed = ''

payload = json.dumps({
    'project':      os.environ.get('PROJECT_NAME', 'Unknown'),
    'repo':         os.environ.get('GITHUB_REPOSITORY', ''),
    'description':  os.environ.get('PROJECT_DESCRIPTION', ''),
    'commits':      commits,
    'changedFiles': changed,
}).encode()

req = urllib.request.Request(
    'https://brain-voice-worker.pfeffer-thomas8.workers.dev/sync-project',
    data=payload,
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ.get('BRAIN_SYNC_SECRET', ''),
    },
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=30) as res:
        print(res.read().decode())
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP Error {e.code}: {e.reason} - {body}')
    sys.exit(1)
