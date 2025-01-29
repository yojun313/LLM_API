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

    # Run pyinstaller with the new spec file
    subprocess.run([
        'pyinstaller',
        '--distpath', output_directory,
        '--workpath', os.path.join(output_directory, 'build'),
        spec_file
    ])
    print(f"Finished building {exe_name}.exe")

    # 삭제할 폴더 목록 정의
    temp_folders = [
        os.path.join(output_directory, 'build'),  # 빌드 폴더
        os.path.join(os.path.dirname(spec_file), 'build'),  # 빌드 폴더 (추가 확인)
        os.path.join(os.path.dirname(spec_file), 'dist'),  # PyInstaller dist 폴더
        os.path.join(os.path.dirname(spec_file), '__pycache__'),  # __pycache__ 폴더
    ]

    # 삭제할 파일 목록 정의
    temp_files = [
        os.path.join(os.path.dirname(spec_file), f"{os.path.splitext(os.path.basename(spec_file))[0]}.spec")
    ]

    # 불필요한 폴더 삭제
    for folder in temp_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    # 불필요한 파일 삭제
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    if socket.gethostname() == "BigMacServer":
        output_directory = "C:/GitHub/BIGMACLAB/MANAGER/source"

    # Spec file path
    spec_file = os.path.join(os.path.dirname(__file__), 'LLM_Chat.spec')

    same_version = os.path.join(output_directory, "LLM_Chat.exe")
    if os.path.exists(same_version):
        shutil.rmtree(same_version)

    build_exe_from_spec(spec_file, output_directory)
    os.system("cls")

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    print(f"{current_time} LLM_Chat built successfully\n")