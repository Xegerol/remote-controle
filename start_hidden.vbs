Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & WScript.ScriptFullName & "\..\start_bot.bat" & chr(34), 0
Set WshShell = Nothing
