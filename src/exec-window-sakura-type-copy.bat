call %USERPROFILE%\venvs\base\Scripts\activate.bat
python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --noconsole ^
    --icon resources\sakura-type-copy.ico ^
    --version-file resources\file_version_info.txt ^
    sakura-type-copy.py
