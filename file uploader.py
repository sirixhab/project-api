import requests


def upload_file(filepath):
    with open(filepath, 'rb') as f:
        files = {'file': f}                                                        # GET  → asking for data  
        r = requests.post("https://tmpfiles.org/api/v1/upload", files=files)       # POST → sending data/files 

    r.raise_for_status()
    data = r.json()
    return data['data']['url']   # only return the useful field — the download URL


result = upload_file("notes.txt")                                 #for raw data:
print(f"required file{result}")                                  #result = create_repo("my-test-repo")
                                                                 #print(json.dumps(result, indent=2))





# NOTE:
# Basic form   →  quick uploads, filename/type don't matter
# Tuple form   →  when you need to:
#                   rename the file the server sees
#                   specify exact content type
#                   send generated data without a real file
#                   add custom part headers