pyinstaller.exe --onefile --noconsole --paths=.\Lib\site-packages --icon=airdrop.ico .\diy-airdrop.py
copy dist\diy-airdrop.exe diy-airdrop.exe
rmdir /S /Q build
rmdir /S /Q dist
del diy-airdrop.spec