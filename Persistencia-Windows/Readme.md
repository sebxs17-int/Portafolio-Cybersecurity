# Persistencia en Windows — Laboratorio

**Resumen:**  
Laboratorio que demuestra técnicas de persistencia en Windows mediante **Scheduled Task** (tarea programada) y, opcionalmente, **Run Key** en el Registro. Incluye artefactos benignos, evidencias y recomendaciones de detección/mitigación.

---

## Objetivo
Aprender a implementar mecanismos de persistencia post-explotación en Windows, documentar los artefactos que generan y entender cómo defenderse de ellos.  
**Este proyecto es con fines educativos y éticos. No me hago responsable de usos indebidos.**

---

## Técnicas implementadas

### 1) Scheduled Task
- Script benigno: `C:\Users\Public\lab_persist.ps1` → agrega una línea con timestamp a `lab_persist.log`.
- Tarea creada: `LabPersist` que corre como **SYSTEM** al arrancar.
- Comando de registro (PowerShell Admin):
```powershell
$scriptPath = 'C:\Users\Public\lab_persist.ps1'
$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName 'LabPersist' -Action $action -Trigger $trigger -Principal $principal
```
# Detección y mitigación

## Detección:

- Revisar C:\Windows\System32\Tasks\ y el canal Microsoft-Windows-TaskScheduler/Operational.

- Monitorizar cambios en claves HKLM\...\Run.

- Habilitar logging avanzado de PowerShell y Sysmon (eventos de ProcessCreate, Registry).

## Mitigación:

- Principio de privilegios mínimos: limitar quién puede crear tareas programadas.

- Políticas AppLocker/WDAC para restringir ejecución de scripts no autorizados.

- Revisiones periódicas con Autoruns (Sysinternals).