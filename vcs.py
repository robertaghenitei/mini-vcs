import hashlib
import os
import pickle
from pprint import pprint

def init_vcs():
    os.makedirs(".my_git", exist_ok=True)
    with open('.my_git/index', 'wb') as f:
        pickle.dump({}, f)
    print('VCS initialized.')


# print(cwd)  
def stage(arg):
    if not os.path.exists('.my_git/index'):
        print("Repository not initialized.")
        return

    with open(".my_git/index", "rb") as f:
        index = pickle.load(f)

    if arg == ".":
        for (root, dir , files) in os.walk(".", topdown=True):
            for file in files:
                if any(skip_dir in os.path.join(root, file) for skip_dir in ['.my_git', '.git']):
                    continue  # ignores files in .my_Git or .git directories
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                file_path = os.path.normpath(os.path.join(root, file))
                index[file_path] = 1
                print(f"Staged {file_path}")
    elif os.path.exists(arg):
        file_path = os.path.normpath(arg)
        index[file_path] = 1
        print(f"Staged {file_path}")
    else:
        print(f"File not found: {arg}")
        return

    with open(".my_git/index", "wb") as f:
         pickle.dump(index, f)


def commit():
    snapshot_hash = hashlib.sha256()
    snapshot_data = {"files": {}}

    if not os.path.exists('.my_git/index'):
        print("Repository not initialized.")
        return
    else: 
        with open(".my_git/index", "rb") as f:
            index = pickle.load(f)

        for file_path in index:
            try: 
                with open(file_path, "rb") as f:
                    content = f.read()
            
            except FileNotFoundError:
                print(f"Warning: File {file_path} not found, skipping.")
                continue

            snapshot_hash.update(content)
            snapshot_data['files'][file_path] = content

    hash_digest = snapshot_hash.hexdigest()
    snapshot_path = f'.my_git/{hash_digest}'
    if os.path.exists(snapshot_path):
        print(f'No changes detected from the snapshot -  {hash_digest}')
        return
    snapshot_data['file_list'] = list(snapshot_data['files'].keys())

    with open(f'.my_git/{hash_digest}', 'wb') as f:
        pickle.dump(snapshot_data, f)
    
    print(f'Snapshot created with hash {hash_digest}')


def revert_to_snapshot(hash_digest):
    snapshot_path = f'.my_git/{hash_digest}'
    if not os.path.exists(snapshot_path):
        print("Snapshot does not exist")
        return
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
        if not file_path.startswith('.') and os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed {file_path}")

    print(f'We reverted to snapshot {hash_digest}')

 
def log():
    pass

