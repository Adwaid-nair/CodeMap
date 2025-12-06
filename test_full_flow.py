
import urllib.request
import urllib.error
import json
import os

def test_flow():
    base_url = "http://localhost:8000"
    upload_url = f"{base_url}/upload"
    file_path = "c:\\AntiGravity L\\CodeMap\\test_upload_file.py"
    
    # Ensure dummy file
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("def foo():\n    pass\n")

    # 1. Upload
    boundary = '---BOUNDARY'
    headers = {
        'Content-Type': 'multipart/form-data; boundary=' + boundary,
        'User-Agent': 'Python-urllib/3.x'
    }

    body = []
    body.append('--' + boundary)
    body.append('Content-Disposition: form-data; name="file"; filename="test_upload_file.py"')
    body.append('Content-Type: text/x-python')
    body.append('')
    
    with open(file_path, 'rb') as f:
        body.append(f.read().decode('utf-8'))
    
    body.append('--' + boundary + '--')
    body.append('')
    
    data = '\r\n'.join(body).encode('utf-8')

    req = urllib.request.Request(upload_url, data=data, headers=headers, method='POST')
    
    project_id = None
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            print("Upload Success:", resp_data)
            project_id = resp_data.get("project_id")
    except urllib.error.URLError as e:
        print("Upload Failed:", e)
        return

    if not project_id:
        print("No project_id returned")
        return

    # 2. Get Analysis
    analyze_url = f"{base_url}/api/analyze/python/{project_id}"
    print(f"Fetching analysis from {analyze_url}...")
    
    try:
        with urllib.request.urlopen(analyze_url) as response:
            analysis = json.loads(response.read().decode('utf-8'))
            print("Analysis Result Keys:", analysis.keys())
            # Check if metrics exist
            if 'complexity' in analysis and 'file_metrics' in analysis['complexity']:
                print("Complexity Metrics Found:", analysis['complexity']['file_metrics'])
            else:
                print("Warning: Complexity metrics missing or empty.")
    except urllib.error.URLError as e:
        print("Analysis Fetch Failed:", e)

if __name__ == "__main__":
    test_flow()
