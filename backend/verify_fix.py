import urllib.request
import urllib.parse
import json
import uuid

# Define the boundary for multipart upload
boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
data = []
data.append(f'--{boundary}')
data.append('Content-Disposition: form-data; name="file"; filename="test_upload.txt"')
data.append('Content-Type: text/plain')
data.append('')
data.append('This is a test file content for verify_fix.py')
data.append(f'--{boundary}--')
data.append('')

body = '\r\n'.join(data).encode('utf-8')
headers = {
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Content-Length': len(body)
}

req = urllib.request.Request('http://localhost:8001/upload', data=body, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Response:", result)
        if 'project_id' in result:
            print("SUCCESS: project_id found in response.")
        else:
            print("FAILURE: project_id NOT found in response.")
except Exception as e:
    print(f"Error: {e}")
