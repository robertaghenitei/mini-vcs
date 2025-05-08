import hashlib
import os
import pickle
from pprint import pprint
import sys

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

    current_files = set()
    for (root, dir, files) in os.walk(".", topdown=True):
        if any(skip_dir in root for skip_dir in ['.my_git', '.git']):
            continue  # ignores files in .my_Git or .git directories

        for file in files:
            current_files.add(os.path.join(root, file))
    snapshot_files = set(snapshot_data['file_list'])
    files_to_delete = current_files - snapshot_files
    for file_path in files_to_delete:
        os.remove(file_path)
        print(f"Removed {file_path}")
    print(f'We reverted to snapshot {hash_digest}')
    
def main():
    directory = os.getcwd() # This is the current directory



if __name__ == "__main__":
    main()