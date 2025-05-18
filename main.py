from vcs import init_vcs, stage, commit, revert_to_snapshot, log
import sys


def main():
    if len(sys.argv) < 2:
        print("Use these commands")
        print("python main.py init")
        print("python main.py add <.|file>")
        print("python main.py commit <messsage optional>")
        print("python main.py revert <hash>")
        return
    command = sys.argv[1]
    if command == 'init':
        init_vcs()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: python main.py add <.|file>")
            return
        stage(sys.argv[2])
    elif command == "commit":
        if len(sys.argv) > 2:
            commit(sys.argv[2])
        else:
            commit()
    elif command == "revert":
        revert_to_snapshot(sys.argv[2])
    elif command == "log":
        log()
    else: 
        print("Unknown command:", command)

if __name__ == "__main__":
    main()