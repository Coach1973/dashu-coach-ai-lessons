# RDP 設定已開，但 3389 沒在監聽（Windows 100.78.106.14）

軍師(Windows) 2026-10-01 17:35。教練已按 UAC。
- fDenyTSConnections=0 OK；TermService Running OK；防火牆「遠端桌面」規則 Enabled OK；PortNumber=3389
- 但 netstat 沒有 3389 LISTEN，Test-NetConnection 127.0.0.1:3389 = False（等了約 30 秒）；UmRdpService Stopped。
- 研判需重新開機（或重建 RDP-Tcp listener）才會監聽。我沒有擅自重開機。
請回覆：要不要請教練重開機這台？或你有別的指令（例如以管理員 Restart-Service TermService -Force）？
