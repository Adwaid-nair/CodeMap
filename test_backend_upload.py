
import urllib.request
import urllib.error
import os

def test_upload():
    url = "http://localhost:8000/upload"
    file_path = "c:\\AntiGravity L\\CodeMap\\test_upload_file.py"
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("print('test')")

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
        body.append(f.read().decode('utf-8')) # Assuming text file
    
    body.append('--' + boundary + '--')
    body.append('')
    
    data = '\r\n'.join(body).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            print("Success:", response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print("Failed:", e)

if __name__ == "__main__":
    test_upload()
