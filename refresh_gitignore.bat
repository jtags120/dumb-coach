@echo off
echo Refreshing .gitignore tracking...

gim rm -r --cached .
git add .
git commit -m "Refresh gitignore"

echo Done!
pause