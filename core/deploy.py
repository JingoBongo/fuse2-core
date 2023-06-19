import os

from utils import os_utils

# so here's the idea. deploy will
# 1 check that there is properly name .git file, in not create from existing file
# 2 move that git init in core folder, in core folder have gittignored everything outside core folder
# 3 add executables to update or push core folder ? no. but I need that

fuse_core_git_name = '.fuse_core_git'
root_dir = os.path.dirname(os.path.abspath(__file__)).replace('/core', '')
is_windows_running = os_utils.is_windows_running()


def recreate_git_files():
    if not os.path.isdir(f"{root_dir}/core/{fuse_core_git_name}"):
        # first, if .git doesnt exist this is unexpected and should be caught
        if not os.path.isdir(f"{root_dir}/.git"):
            print(
                f"Fuse deploy can't properly function, root folder has no .git file, therefore this repo wasn't cloned"
                f" and can't be updated from fuse2-core repo")
            return 13
        #     here we need to move git file, git init from root and stuff
        rename_pref = 'ren' if is_windows_running else 'mv'
        move_pref = 'move' if is_windows_running else 'mv'
        #   execute rename + move
        os_utils.start_system_barrel_process([f"cd {root_dir}", f"{rename_pref} .git {fuse_core_git_name}",
                               f"{move_pref} {fuse_core_git_name} core/{fuse_core_git_name}"],
                                             wait_for_result=True)
        os_utils.start_system_barrel_process([f"cd {root_dir}", f"echo core/ >> ../.gitignore"], wait_for_result=True)
        os_utils.start_system_barrel_process([f"cd {root_dir}", 'git init'])
        print('git recreation completed')
    else:
        print('git file recreation omitted')

# TODO: master remastering: entire repo folder is our core folder. therefore move everything 1 level upper, create
# runnable folder as separate thing

if __name__ == "__main__":
    recreate_git_files()
