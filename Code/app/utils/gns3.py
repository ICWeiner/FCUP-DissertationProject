import os
import uuid
import json
import zipfile
import re
import unicodedata

def generate_unique_filename(filename):
    filename = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode("utf-8")
    filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)

    secured_name = filename.strip("._")

    if not secured_name:
        secured_name = "default"

    unique_suffix = uuid.uuid4().hex

    name, ext = os.path.splitext(secured_name)
    unique_name = f"{name}_{unique_suffix}{ext.lower()}"

    return unique_name

def extract_node_names(uploaded_file):
    data = None
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        gns3_filename = [name for name in zip_ref.namelist() if name.endswith('.gns3')][0]
        
        with zip_ref.open(gns3_filename) as file:
            data = json.load(file)

    node_names = [item['name'] for item in data['topology']['nodes'] if 'name' in item]

    return node_names