Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & WScript.ScriptFullName & "\..\remote_control.bat" & chr(34), 0
Set WshShell = Nothing
