import os
import subprocess
import socket
from datetime import datetime
import shutil


def build_exe_from_spec(spec_file, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Building exe for {spec_file}...")

    # Define the output executable name with version
    exe_name = f"LLM_Chat"
    try:
        # Run pyinstaller with the new spec file
        subprocess.run([
            'pyinstaller',
            '--distpath', output_directory,
            '--workpath', os.path.join(output_directory, 'build'),
            spec_file
        ])
        print(f"Finished building {exe_name}.exe")
    finally:
        # 삭제할 폴더 목록
        temp_folders = [
            os.path.join(output_directory, 'build'),
        ]
        
        for folder in temp_folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)


if __name__ == "__main__":
    if socket.gethostname() == "BigMacServer":
        output_directory = "C:/GitHub/BIGMACLAB/MANAGER/source"

    # Spec file path
    spec_file = os.path.join(os.path.dirname(__file__), 'LLM_Chat.spec')

    same_version = os.path.join(output_directory, "LLM_Chat.exe")
    if os.path.exists(same_version):
        os.remove(same_version)

    build_exe_from_spec(spec_file, output_directory)

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    print(f"{current_time} LLM_Chat built successfully\n")