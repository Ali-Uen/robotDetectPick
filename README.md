# robotDetectPick – Objekterkennungsbasiertes Greifsystem (Bachelorarbeit)

Dieses Repository enthält die begleitende Implementierung zur Bachelorarbeit **„Entwicklung und Implementierung eines objekterkennungsbasierten Greifsystems für einen Roboterarm“**. Ziel ist es, Objekte auf einem laufenden Förderband mit YOLOv5 zu erkennen, ihre Greifpositionen mithilfe von Kamera­kalibrierung & SolvePnP in Welt- und Roboterkoordinaten zu bestimmen und sie anschließend mit einem **Niryo Ned2** zu greifen.

---

## ✨ Kernfunktionen
- **Objektdetektion** mit YOLOv5 (Webcam/Stream)
- **Kamerakalibrierung** (Schachbrett) & **Pose-Schätzung** via `solvePnP`
- **Weltkoordinatensystem** (Landmarken an den Förderband‑Ecken) & Koordinaten­transformation in das Roboter­koordinatensystem
- **Pick&Place** auf einem **Niryo Ned2** inkl. Greifersteuerung & Förderband
- **Echtzeit‑Geschwindigkeitsabschätzung** von Objekten für dynamisches Greifen
- **Evaluation** (Excel‑Export) von Zeiten, Erfolgsraten und Stabilität

---

## 📁 Projektstruktur

```
robotDetectPick/
├─ parallelProcess.py            # Startet Detektion, SolvePnP und Roboter als Threads
├─ frame1.jpg                    # Beispielbild
├─ yolov5/                       # Upstream YOLOv5 (detect.py, train.py, val.py, ... + *.pt)
├─ solvepnp/
│  ├─ camera.py                  # Kamera-Kalibrierung (Schachbrett)
│  └─ SolvePNP.py                # Pixel→Welt: SolvePnP + Geschwindigkeit
├─ robot/
│  ├─ robotAndDetect.py          # Hauptlogik Robotersteuerung + Detektions-Integration
│  ├─ pickAndPlace.py            # High-Level Bewegungsabläufe
│  ├─ workspace.py               # Workspace (4 Ecken) am Ned2 anlernen
│  ├─ coordinates.py, converter.py, color.py, sound.py
│  ├─ robotcoordinates/*.txt     # Referenzpunkte Roboter-KS
│  └─ sounds/*.mp3               # Sprachhinweise (gTTS)
├─ evaluation/
│  ├─ evaluation.py              # Excel-Schreiber (Ergebnisse)
│  └─ ergebnisse.xlsx            # Ergebnisdatei (wird angelegt/fortgeschrieben)
└─ weights/                      # Platz für eigene/feinjustierte Gewichte (optional)
```

> Hinweis: `parallelProcess.py` enthält teils absolute Pfade aus dem Entwicklungssetup. Bitte im Abschnitt **Konfiguration** anpassen.

---

## 🧰 Voraussetzungen

**Hardware**
- Niryo **Ned2** mit Greifer (oder Vakuumpumpe) und **Niryo Conveyor Belt**
- 2D‑Webcam (z. B. Logitech) auf das Förderband ausgerichtet
- Rechner mit Python (getestet mit 3.8–3.11) und ggf. NVIDIA‑GPU (optional für schnellere YOLO‑Inference)
- Netzwerkverbindung zum Ned2 (LAN/WLAN)

**Software / Python‑Pakete**
- PyTorch + Abhängigkeiten aus `yolov5/requirements.txt`
- Zusätzlich: `pyniryo`, `gTTS`, `openpyxl`, `pandas`

Beispiel (innerhalb eines frischen venv):
```bash
pip install -r yolov5/requirements.txt
pip install pyniryo gTTS openpyxl pandas
```

---

## ⚙️ Konfiguration

1) **Repository‑Pfad**
   - Empfohlen: in das Home‑Verzeichnis klonen/entpacken als `~/robotDetectPick`.
   - In `parallelProcess.py` ggf. absolute `sys.path.append(...)`-Einträge anpassen oder durch relative Pfade ersetzen.

2) **Robot‑IP & Workspace‑Name**
   - In `robot/robotAndDetect.py` und `robot/stopConveyor.py` die Variable `robot_ip_address` auf die IP deines Ned2 setzen.
   - Den gewünschten `workspace_name` eintragen (siehe Workspace‑Anlernen).

3) **YOLO‑Gewichte**
   - Standardgewichte (`yolov5s.pt`, `yolov5m.pt`) liegen unter `yolov5/`.
   - Eigene/feinjustierte Gewichte (z. B. `best.pt`) ablegen (z. B. in `weights/`) und den Pfad in den Skripten/Parametern angeben.

4) **Kamera‑Index / Quelle**
   - In der Regel Webcam = `--source 0` (siehe Startvarianten unten).

---

## 🎯 Weltkoordinatensystem & Landmarken

- Bringe an den **vier Ecken** des Förderbands Landmarken (markante Marker) an.
- Definiere das Weltkoordinatensystem mit Ursprung **oben links**; **y‑Achse ~30 cm**, **x‑Achse ~14,5 cm**.
- `SolvePNP.py` erwartet **4 korrespondierende 3D‑Weltpunkte** und **4 2D‑Pixelpunkte** (Landmarken) aus der Detektion.
- Die Transformation Pixel→Welt→Roboter erfolgt anschließend automatisch in der Pipeline.

> Tipp: Die Kameraperspektive sollte möglichst orthogonal/ohne starke Schräglage montiert sein. Nutze die Schachbrett‑Kalibrierung (s. unten) vorab.

---

## 🎥 Kamera­kalibrierung (einmalig pro Aufbau)

1) Drucke ein **Schachbrettmuster** und nimm mehrere Bilder aus unterschiedlichen Winkeln auf.
2) Lege die Bilder in den von `solvepnp/camera.py` erwarteten Ordner und führe aus:
   ```bash
   python solvepnp/camera.py
   ```
3) Die Skripte berechnen **Kameramatrix** und **Verzerrungen**; diese werden in der SolvePnP‑Schätzung verwendet.

---

## 🚀 Startvarianten

### Variante A: Alles aus einem Skript (Thread‑basiert)
```bash
python parallelProcess.py
```
Startet drei Threads:
- **Detektion** (YOLOv5 Webcam‑Stream)
- **SolvePnP + Geschwindigkeit** (Pixel→Welt, Tracking)
- **Robotersteuerung** (Ned2: Greifen/Platzieren, Conveyor Control)

> Prüfe vorab die Pfade in `parallelProcess.py` und die `robot_ip_address`.

### Variante B: Manuell in separaten Terminals
1) **Detektion** (YOLOv5 Webcam):
   ```bash
   cd yolov5
   python detect.py --weights yolov5m.pt --source 0 --conf-thres 0.5
   ```
2) **SolvePnP & Geschwindigkeit**:
   ```bash
   python solvepnp/SolvePNP.py
   ```
3) **Robotersteuerung**:
   ```bash
   python robot/robotAndDetect.py
   ```

---

## 📝 Training (optional)

- Datensatz (YOLO‑Format) z. B. via Roboflow exportieren.
- Training mit YOLOv5:
  ```bash
  cd yolov5
  python train.py --img 640 --batch 16 --epochs 150 --data data.yaml --weights yolov5m.pt
  ```
- Die resultierenden Gewichte `best.pt` anschließend in der Detektion verwenden.

---

## 📊 Evaluation

- Während der Laufzeit werden Messwerte (Zeiten, Koordinaten, Erfolgsraten/Stabilität) nach `evaluation/ergebnisse.xlsx` geschrieben.
- Das Format wird in `evaluation/evaluation.py` definiert. Zum reinen Stoppen des Förderbands existiert `robot/stopConveyor.py`.

---

## 🛡️ Sicherheit & Hinweise

- Not‑Aus am Ned2 bekannt machen; Greiferhöhe richtig konfigurieren (Kollisionsgefahr!).
- Förderband zunächst langsam testen und Greifpunkte validieren.
- Kamera und Landmarken fixieren, sonst driften Koordinaten.
- Rote Objekte (falls so gelabelt) ggf. in der Logik ausschließen/ignorieren.

---

## ❗️Typische Stolpersteine

- **Keine Verbindung**: Prüfe `robot_ip_address`, Netzwerk und Kalibrierungsstatus des Ned2.
- **Detektion findet nichts**: `--source`/Kamera‑Index prüfen, Gewichtsdatei korrekt?
- **Koordinaten falsch**: Kamerakalibrierung wiederholen, Landmarken‑Reihenfolge in SolvePnP beachten, Workspace am Roboter neu anlernen.
- **Pfadprobleme**: `parallelProcess.py` auf relative Pfade umstellen oder Repo in `~/robotDetectPick` ablegen.

---

## 📄 Lizenz & Danksagung

- Teile dieses Repos verwenden **YOLOv5** (Ultralytics) – **GPL‑3.0**. Beachte die Lizenzdateien im `yolov5/`‑Ordner.
- Hardware/SDK: **Niryo Ned2**, **PyNiryo**, **Niryo Conveyor**.
- Dieses Projekt entstand im Rahmen einer Bachelorarbeit an der TH Köln.

---

## 👤 Autor & Kontakt

- Autor: Ali Ünal
- Projekt: Bachelorarbeit – Objekterkennungsbasiertes Greifsystem (TH Köln)

