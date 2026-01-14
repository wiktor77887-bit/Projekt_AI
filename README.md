
**SYSTEM WYKRYWANIA SENNOSCI KIEROWCY (Driver Drowsiness Detection)**


**Termin oddania:** 29.01.2026 r. 
**Autor:** [Wiktor Cemel, Wojciech Frontczak]

**1. OPIS PROJEKTU**
System monitoruje stan kierowcy w czasie rzeczywistym, wykrywajac oznaki zmeczenia. Wykorzystuje model MediaPipe Face Mesh do obliczania wskaznika EAR (Eye Aspect Ratio). Alarm aktywuje sie, gdy EAR spadnie ponizej progu 0.22 na minimum 15 klatek.

**2. WYMAGANIA I INSTALACJA**

* Wymagany Python 3.11+ oraz srodowisko wirtualne (.venv).


* Instalacja bibliotek:
pip install mediapipe==0.10.11 opencv-python<4.10 numpy<2.0.0

**3. URUCHAMIANIE**
Glowny skrypt: main.py 
Mozliwosc zmiany trybu w kodzie (zmienna MODE):

* "CAMERA" - obraz z kamery na zywo.


* "DATASET" - automatyczne testowanie na plikach ze zbioru YawDD.



**4. STEROWANIE (Podczas dzialania programu)**

* 'n' - Przejdz do nastepnego filmu (tryb DATASET).


* 'r' - Nagraj 10-sekundowe demo do pliku 'demo_projektu.mp4'.
* 'q' - Wyjdz z programu.



**5. ZBIOR DANYCH (YawDD)**
Pelny zbior danych YawDD (4.94 GB) zostal wykorzystany do walidacji. Ze wzgledu na limity GitHub (100 MB na plik), w repozytorium znajduje sie jedynie reprezentatywna probka nagran. Pelne dzialanie algorytmu udokumentowano w zalaczonym pliku wideo 'demo_projektu.mp4'.

**6. PLIKI W REPOZYTORIUM**

* main.py - glowny kod zrodlowy.


* AI_Projekt.pdf - pelna dokumentacja teoretyczna.


* requirements.txt - lista zaleznosci.


* demo_projektu.mp4 - nagranie prezentujace skutecznosc systemu.

---