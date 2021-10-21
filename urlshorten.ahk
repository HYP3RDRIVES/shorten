; AutoHotkey Version: 1.x
; Language: English
; Platform: Win9x/NT ; Author: A.N.Other ;
; #NoEnv
; Recommended for performance and compatibility with future AutoHotkey releases.
; Spaghetti Code that somehow works

SendMode Input
SetWorkingDir %A_ScriptDir%
^+b::
Send ^c
sleep,200
locationnn = %clipboard%
URL := "https://s.hypr.ax/shorten/" locationnn
HttpObj := ComObjCreate("WinHttp.WinHttpRequest.5.1")
HttpObj.Open("POST", URL, 0)
HttpObj.SetRequestHeader("Authorization", "YOUR_AUTH_TOKEN_HERE")
HttpObj.Send()
Result := HttpObj.ResponseText
Status := HttpObj.Status
if (HttpObj.ResponseText = "Invalid URL"){
        MsgBox Invalid URL
        return
}
else if (HttpObj.Status == 200){
        Clipboard := "" ; Empty the clipboard
        Clipboard := Result
        sleep,200
        msgbox %clipboard%`n`n Shortened URL Copied to clipboard
}
return
