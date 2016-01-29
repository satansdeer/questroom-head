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
Local $url_with_id[$NUM_ID]
Local $browsersPidsp[$NUM_ID]
Local $winHandlers[$NUM_ID]
Local $titles[$NUM_ID]

For $index=1 To 4
    $url_with_ids[$index - 1] = $URL_ADDRESS & String($index)
    $titles[$index - 1] = $TITLE & String($index)

    $browserPid[$index - 1] = Run($BROWSER_EXE & $BROWSER_ARGS & $url_with_ids[$index - 1])
    $winHandlers[$index - 1] = WinWait($titles[$index - 1], "", 10)
Next

Sleep(5000)

For $index=1 To 4
   Run($MONITOR_TOOL_EXE & " /MoveWindow " & String($index) & " Title " & titles[$index - 1])
   Sleep(2000)
   WinActivate($winHandlers[$index - 1])
   WinWaitActive($winHandlers[$index - 1], "", 5)
   ;WinSetState($winHandlers[$index - 1], "", @SW_MAXIMIZE)
   Send("{F11}")
   Sleep(1000)
   ; try to deactivate window
   WinActivate("Program Manager");
Next

