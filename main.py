import hashlib
import os
import pickle

def init_vcs():
    os.makedirs(".my_Git", exist_ok=True)
    print('VCS initialized.')

# cwd = os.getcwd() // This is the current directory
# print(cwd)  


def snapshot(directory):
    snapshot_hash = hashlib.sha256()
    snapshot_data = {"files": {}}

    for (root, dir, files) in os.walk(directory, topdown=True):
        for file in files:
            if '.my_Git' in os.path.join(root, file):
                continue # ignores the files already in .my_Git (previous snapshots)
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                content = f.read()
                snapshot_hash.update(content)
                snapshot_data['files'][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())