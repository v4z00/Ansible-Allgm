BESCHREIBUNGEN FUER MENSCH UND MANAGEMENT-JUMP-HOST - FORMAT 1.1.0
Stand: 18.11.2026
commands/: bestehende Control-Befehle, Rollen-/Playbook-/Konfigurationsreferenzen
unter roles/, playbooks/ und configurations/. Alle .md-Dateien koennen ohne
Add-on mit einem Texteditor gelesen werden. Der JSON-Codeblock beschreibt
Parameter fuer die TUI. Nur eine Pflegequelle; keine parallele JSON-Beschreibung.
Befehlsname, Kurzbeschreibung, Aliase und Feature bleiben in bin/control.d.
Die Beschreibungen ergaenzen diese Registry. Quellhashs sperren veraltete Formulare.
Nur belegte Optionen sind als Formular markiert; unvollstaendig dokumentierte
Befehle bleiben im vorhandenen Terminalablauf benutzbar.
Keine Standortsettings, Secrets oder aktiven Feature-Schalter durch Uebernahme
aendern. Beschreibungen allein installieren/aktivieren keine fachliche Funktion.
Quelle von Allgemein/Homelab: passende neutrale Vorlage. NXTS3-Pflegequelle:
05_Metadaten/NXTS3/Quelle, weil der aktuelle NXTS3-Code als getrennte Paketfolge
vorliegt. Im installierten Ansible-Projekt liegen nur dessen Beschreibungsdateien;
das Add-on liest ausschliesslich diese, nie die lokalen Auslieferungspakete.
Versionierte Pakete sind daraus erstellte Auslieferungen, nicht separat zu pflegen.
Fachliche Ausfuehrung und bestehende Rueckfragen bleiben in Control/Ansible.
