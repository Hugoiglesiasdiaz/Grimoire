import os
import json
import uuid
import datetime

folder = 'testfiles'
skip = {'mock_data.json'}

for f in os.listdir(folder):
    if f in skip or f.endswith('.metadata.json'):
        continue
    filepath = os.path.join(folder, f)
    if not os.path.isfile(filepath):
        continue
    meta_path = filepath + '.metadata.json'
    if os.path.exists(meta_path):
        print(f'SKIP (already has metadata): {f}')
        continue
    ext = os.path.splitext(f)[1].lower().replace('.', '') or 'unknown'
    meta = {
        'id': str(uuid.uuid4()),
        'fileName': f,
        'originalFileName': f,
        'fileType': ext,
        'fileSize': os.path.getsize(filepath),
        'uploadDate': datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
        'filePath': filepath,
        'extractedText': '',
        'textLength': 0,
        'summary': '',
        'category': 'Uncategorized',
        'tags': '[]',
        'aiProcessed': False,
        'aiProcessedDate': None
    }
    with open(meta_path, 'w', encoding='utf-8') as mf:
        json.dump(meta, mf, indent=4)
    print(f'OK: {f}')

print('\nDone!')
