
import os
import sys

def get_current_path():
    print("current work path : " + os.getcwd())
    paths = sys.path
    current_file = os.path.basename(__file__)
    for path in paths:
        try:
            if current_file in os.listdir(path):
                current_path = path
                os.chdir(current_path)
                print("after change dir, current work path : " + os.getcwd())

                break
        except (FileExistsError,FileNotFoundError) as e:
            print(e)

if __name__ == '__main__':
    get_current_path()