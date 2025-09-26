# Persistencia en Linux - Laboratorio

**Resumen:**  
Laboratorio didactico que demuestra tecnicas de persistencia en Linux (systemd, cron),

---

## Objetivo  

Implementar persistencia basica en Linux para entender: 
- Los mecanismos del sistema que permiten ejecucion automatica (systemd, cron),
- Los artefactos que dichas tecnicas generan,
- Como detectarlos y mitigarlos.

---

## Contenido 
- Evidencias - Archivos generados en el laboratorio (script, unidad systemd, log, crontrab, ZIP) 
- Screenshots - Capturas de pantalla de las comprobaciones clave

---
## Tecnicas implementadas   

### 1 ) Systemd service
- **Que hice:** cree ´/usr/local/bin/lab_persist.sh´ y la unidad ´/etc/systemd/system/lab_persist.service´ para ejecutarel script de arranque.
- **Comando principal (ejecutando en el laboratorio):** 

```bash
sudo tee /usr/local/bin/lab_persist.sh <<'EOF'
#!/bin/bash
echo "lab_ok $(date --iso-8601=seconds)" >> /var/log/lab_persist.log
EOF
sudo chmod +x /usr/local/bin/lab_persist.sh

sudo tee /etc/systemd/system/lab_persist.service <<'EOF'
[Unit]
Description=Lab persist service
Type=oneshot
ExecStart=/usr/local/bin/lab_persist.sh
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now lab_persist.service 

```
### 2) Cron @reboot
- Que hice: añdi una entrada @reboot en el crontab del usuario para ejecutar el mismo script en cada reinicio.
```bash
(crontab -l 2>/dev/null; echo "@reboot /usr/local/bin/lab_persist.sh") | crontab - 

```


### 3) Mitigacion y Deteccion 

## Detección y Mitigación

**Resumen:** además de mostrar cómo implementar persistencia, este laboratorio documenta cómo detectarla y mitigarla en entornos reales.

### Detección recomendada (qué monitorizar)
- Cambios en unidades `systemd`: vigilar `/etc/systemd/system/` y llamadas a `systemctl daemon-reload` / `systemctl enable`.
- Cambios en crontabs de usuarios y en `/var/spool/cron` o `/etc/cron.*`.
- Creación/modificación de archivos ejecutables en rutas típicas (`/usr/local/bin`, `/opt`, `/tmp`).
- Nuevas tareas programadas en Windows (canal `Microsoft-Windows-TaskScheduler/Operational`) y cambios en `HKLM\...\Run`.
- Ejecuciones de PowerShell con argumentos sospechosos (`-EncodedCommand`, `-ExecutionPolicy Bypass`) o procesos hijos con padres inusuales.

### Controles preventivos
- Principio de privilegios mínimos: restringir quién puede escribir en `/etc/systemd/system` y `/usr/local/bin`.
- Control de integridad de archivos (AIDE, OSSEC, Tripwire) sobre rutas críticas.
- Configurar AppLocker o WDAC (Windows) y políticas de ejecución de scripts controladas.
- Habilitar registro avanzado: Sysmon (Windows) y auditd (Linux) para capturar ProcessCreate / execve / registry changes.
- Revisiones de crontab y cambios en la configuración de arranque realizadas por un proceso de cambio controlado (change control).

### Respuesta y remediación (pasos rápidos)
1. **Detectar** — recopilar logs, identificar timestamp y usuario/proceso creador.  
2. **Contener** — deshabilitar the artifact (`systemctl disable --now <unit>`, `schtasks /Delete …`), aislar host si hay indicios de movimiento lateral.  
3. **Erradicar** — eliminar archivos maliciosos, revertir Run keys, restaurar desde snapshot limpio si procede.  
4. **Recuperar** — reinstalar service/paquetes legítimos si fue alterado; aplicar parches.  
5. **Aprender** — guardar evidencia, actualizar reglas SIEM y documentar lecciones aprendidas.

### Recomendaciones operativas
- Implementar alertas que correlacionen creación de nuevas unidades/tareas con ejecución de PowerShell o conexiones de red.  
- Revisar semanalmente la salida de herramientas como `autoruns` (Windows) y listas de unidades no documentadas en Linux.  
- Mantener un repositorio de "artefactos permitidos" (whitelist) y auditar las excepciones.













