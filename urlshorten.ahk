; AutoHotkey Version: 1.x
; Language: English
; Platform: Win9x/NT ; Author: A.N.Other ;
; #NoEnv
; Recommended for performance and compatibility with future AutoHotkey releases.
; Spaghetti Code that somehow works
json_fromobj( obj ) {

        If IsObject( obj )
        {
                isarray := 0 ; an empty object could be an array... but it ain't, says I
                for key in obj
                        if ( key != ++isarray )
                        {
                                isarray := 0
                                Break
                        }

                for key, val in obj
                        str .= ( A_Index = 1 ? "" : "," ) ( isarray ? "" : json_fromObj( key ) ":" ) json_fromObj( val )

                return isarray ? "[" str "]" : "{" str "}"
        }
        else if obj IS NUMBER
                return obj
;       else if obj IN null,true,false ; AutoHotkey does not natively distinguish these
;               return obj

        ; Encode control characters, starting with backslash.
        StringReplace, obj, obj, \, \\, A
        StringReplace, obj, obj, % Chr(08), \b, A
        StringReplace, obj, obj, % A_Tab, \t, A
        StringReplace, obj, obj, `n, \n, A
        StringReplace, obj, obj, % Chr(12), \f, A
        StringReplace, obj, obj, `r, \r, A
        StringReplace, obj, obj, ", \", A
        StringReplace, obj, obj, /, \/, A
        While RegexMatch( obj, "[^\x20-\x7e]", key )
        {
                str := Asc( key )
                val := "\u" . Chr( ( ( str >> 12 ) & 15 ) + ( ( ( str >> 12 ) & 15 ) < 10 ? 48 : 55 ) )
                                . Chr( ( ( str >> 8 ) & 15 ) + ( ( ( str >> 8 ) & 15 ) < 10 ? 48 : 55 ) )
                                . Chr( ( ( str >> 4 ) & 15 ) + ( ( ( str >> 4 ) & 15 ) < 10 ? 48 : 55 ) )
                                . Chr( ( str & 15 ) + ( ( str & 15 ) < 10 ? 48 : 55 ) )
                StringReplace, obj, obj, % key, % val, A
        }
        return """" obj """"
} ; json_fromobj( obj )
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
