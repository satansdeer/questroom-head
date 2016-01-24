#include <Constants.au3>

; Run the calculator
Local $BROWSER_EXE="C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
Local $URL_ADDRESS="http://localhost:8888/?id="
Local $BROWSER_ARGS=" -new-window "
Local $TITLE="cb_"

Local $MONITOR_TOOL_EXE="C:\Users\dementr.DESKTOP-27EDVKQ.000\MonitorEXE\MultiMonitorTool.exe"

Local $NUM_ID=4
Sleep(5000)
Local $chindex = 1
Local $url_with_id = 1
For $index=1 To 4
   if $index = 4 Then
	  Local $url_with_id = $URL_ADDRESS & String(2)
	  $chindex = 2
   ElseIf $index = 2 Then
	  $url_with_id = $URL_ADDRESS & String(3)
	  $chindex = 3
   ElseIf $index = 3 Then
	  $url_with_id = $URL_ADDRESS & String(4)
	  $chindex = 4
   Else
	  $url_with_id = $URL_ADDRESS & String(1)
	  $chindex = 1
   EndIf

   Local $url_with_id = $URL_ADDRESS & String($chindex)
   Local $browserPid = Run($BROWSER_EXE & $BROWSER_ARGS & $url_with_id)

   Local $hWnd = WinWait($TITLE & String($chindex), "", 10)
   Run( $MONITOR_TOOL_EXE & " /MoveWindow " & String($chindex) & " Title " & $TITLE & String($chindex))
   Sleep(1000)
   WinActivate($hWnd)
   WinWaitActive($hWnd, "", 5)
   Send("{F11}")
   Sleep(500)
Next
#CS ;Run("C:\Program Files (x86)\Mozilla Firefox\firefox.exe -new-window http://localhost:8888/?id=1")
### Run("C:\Program Files (x86)\Mozilla Firefox\firefox.exe -new-window http://google.com")
###
### ; Wait for the calculator to become active. The classname "CalcFrame" is monitored instead of the window title
### WinWaitActive("[CLASS:MozillaWindowClass]", "", 5)
###
### ; Now that the calculator window is active type the values 2 x 4 x 8 x 16
### ; Use AutoItSetOption to slow down the typing speed so we can see it
###
### Sleep(2000)
###
### Run("C:\Users\dementr.DESKTOP-27EDVKQ.000\MonitorEXE\MultiMonitorTool.exe /MoveWindow 1 Title google")
### Sleep(2000)
### AutoItSetOption("SendKeyDelay", 400)
### Send("{F11}")
### Sleep(2000)
###
###
### Run("C:\Program Files (x86)\Mozilla Firefox\firefox.exe -new-window http://google.com")
###
### ; Wait for the calculator to become active. The classname "CalcFrame" is monitored instead of the window title
### WinWaitActive("[CLASS:MozillaWindowClass]", "", 5)
###
### ; Now that the calculator window is active type the values 2 x 4 x 8 x 16
### ; Use AutoItSetOption to slow down the typing speed so we can see it
###
### Sleep(2000)
###
### Run("C:\Users\dementr.DESKTOP-27EDVKQ.000\MonitorEXE\MultiMonitorTool.exe /MoveWindow 2 Title google")
### Sleep(2000)
### AutoItSetOption("SendKeyDelay", 400)
### Send("{F11}")
### Sleep(2000)
 #CE
; Now quit by sending a "close" request to the calculator window using the classname
;WinClose("[CLASS:MozillaWindowClass]")

; Now wait for the calculator to close before continuing
;WinWaitClose("[CLASS:MozillaWindowClass]")

; Finished!
