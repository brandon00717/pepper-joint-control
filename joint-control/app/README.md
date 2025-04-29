# Joint-Control App

Control Pepper’s arm and head joints to match a target pose displayed on the tablet.

## Prerequisites

- Pepper must be connected to the **CSHRI_ASUS** Wi-Fi network.  
- An SSH client (OpenSSH, PuTTY, etc.) installed on your computer.

---

## 1. SSH into Pepper

Open a terminal and run:

```bash
ssh nao@192.168.137.48
# password: cruJe7ra
```

---

## 2. Start the Python service

```bash
cd /data/home/nao/.local/share/PackageManager/apps/joint-control/scripts
python2 joint.py
```

> **Leave this terminal open** — the NAOqi service must keep running while you use the tablet UI.

---

## 3. Launch the tablet app

1. On Pepper’s tablet screen, tap the **⋮** (three-dots) menu icon in the bottom-right corner.  
2. Scroll to **joint-control** in the list.  
3. Tap **joint-control** to open the app.

You will see:

- **Top Section**: Controls for each joint (inputs + Set buttons).  
- **Bottom Section**: An image showing the target pose.

---

## 4. Using the UI

- **Set a single joint**  
  1. Enter an angle (in degrees) into the input field for that joint.  
  2. Tap **Set Angle**.  
  Pepper will move and hold that joint at the specified angle.

- **Reset All**  
  Tap **Reset All** to return every joint to its neutral position.

- **Exit App**  
  1. Tap **Exit App** to start the closing process
  2. Put your hands over peppers forehead until you hear a bubble pop sound, then release your hand

---

## 5. Stop the service

In the SSH terminal where `joint.py` is running, press:

<kbd>Ctrl</kbd> + <kbd>C</kbd>

This will:

- Reset joints to neutral  
- Terminate the Python process

---

## Troubleshooting

- **“Service Joint not found”**  
  - Ensure `joint.py` is still running without errors.  
  - Stop service and run again using steps **5** and **2**


---

Enjoy matching Pepper’s joints to your target poses!
