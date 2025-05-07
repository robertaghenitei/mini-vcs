import hashlib
import os
import pickle
from pprint import pprint

directory = os.getcwd() # This is the current directory

def init_vcs():
    os.makedirs(".my_git", exist_ok=True)
    print('VCS initialized.')


# print(cwd)  


def snapshot(directory):
    snapshot_hash = hashlib.sha256()
    snapshot_data = {"files": {}}

    for (root, dir, files) in os.walk(directory, topdown=True):
        for file in files:
            if any(skip_dir in os.path.join(root, file) for skip_dir in ['.my_git', '.git']):
                continue  # ignores files in .my_Git or .git directories
        
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                content = f.read()
                snapshot_hash.update(content)
                snapshot_data['files'][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())

    with open(f'.my_git/{hash_digest}', 'wb') as f:
        pickle.dump(snapshot_data, f)
    
    pprint(f'Snapshot created with hash {hash_digest}')


def revert_to_snapshot(hash_digest):
    snapshot_path = f'.my_git/{hash_digest}'
    if not os.path.exists(snapshot_path):
        print("Snapshot does not exist")

    with open(snapshot_path, 'rb') as f:
        snapshot_data = pickle.load(f)
    for file_path, content in snapshot_data['files'].items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
    
init_vcs()

snapshot(directory)

revert_to_snapshot("1d43da4cd518d87c99a2f0b6b00cf130575e18efd641c2780f3d66d51852db27")