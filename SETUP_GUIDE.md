# 🛡️ QR Phishing Awareness Demo — Kali Linux Setup Guide

## Educational Use Only
> This demo is designed for cybersecurity awareness workshops.
> It demonstrates what data a malicious QR code can collect, and teaches participants to be cautious.

---

## 📋 Prerequisites

- **Kali Linux** (VM or bare metal)
- Participants' phones connected to the **same network** as your Kali machine
- Python 3 (pre-installed on Kali)

---

## 🚀 Step-by-Step Setup

### Step 1 — Install Dependencies

```bash
sudo apt update
pip3 install flask qrcode[pil]
```

### Step 2 — Transfer Files to Kali

Copy the `demo_server.py` file to your Kali machine (USB, SCP, shared folder, etc.):

```bash
# Example via SCP from Windows
scp demo_server.py kali@<kali-ip>:/home/kali/phishing_demo/
```

### Step 3 — Connect to the Same Network

Make sure your Kali machine and participants' phones are on the **same Wi-Fi / LAN**.

Check your Kali IP:
```bash
ip addr show          # Find your IP (e.g., 192.168.1.105)
# or
hostname -I
```

### Step 4 — Start the Server

```bash
cd /home/kali/phishing_demo/
python3 demo_server.py --port 8080
```

If you need to specify a network interface:
```bash
python3 demo_server.py --port 8080 --interface wlan0
```

You'll see:
```
╔══════════════════════════════════════════════════╗
║   🛡️  QR PHISHING AWARENESS DEMO  🛡️            ║
╠══════════════════════════════════════════════════╣
║   Victim page :  http://192.168.1.105:8080      ║
║   Dashboard   :  http://192.168.1.105:8080/dashboard ║
║   QR Image    :  http://192.168.1.105:8080/qr   ║
╚══════════════════════════════════════════════════╝
```

### Step 5 — Display the QR Code

**Option A** — Open the QR in your browser:
```
http://192.168.1.105:8080/qr
```
Project this on the workshop screen.

**Option B** — Open the saved image:
```bash
xdg-open demo_qr.png
```

**Option C** — Print it and place it on tables (for a more realistic scenario).

### Step 6 — Open Your Dashboard

On your laptop (NOT projected to audience), open:
```
http://192.168.1.105:8080/dashboard
```
This shows all scans in real-time (auto-refreshes every 5 seconds).

---

## 🎬 Workshop Flow

### Before the Session
1. Set up Kali and start the server
2. Print or display the QR code
3. DON'T tell participants what it does

### During the Session

| Time | Action |
|------|--------|
| 0:00 | Ask participants: "I have free Wi-Fi for everyone. Scan this QR code to connect." |
| 0:02 | Wait for participants to scan and tap "Connect Now" |
| 0:03 | Watch their reactions as the REVEAL page appears |
| 0:05 | Switch to the **dashboard** — show everyone's data on the projector |
| 0:08 | Ask: "Did anyone tap Allow on the location/camera prompts?" |
| 0:10 | Discuss what a real attacker would do with this data |
| 0:15 | Walk through the defense tips shown on the reveal page |

### Key Talking Points

1. **"I didn't enter anything!"** — Emphasize that no input was needed; just opening the link was enough
2. **IP → Location** — Show how an IP reveals approximate city/ISP
3. **Device fingerprinting** — The combination of OS + browser + screen + language creates a nearly unique fingerprint
4. **Permissions** — Discuss why reflexively tapping "Allow" is dangerous
5. **Physical QR codes** — Mention that attackers paste fake QR stickers over real ones (parking meters, restaurant menus)

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Phones can't reach the server | Make sure they're on the same network. Check `sudo ufw status` and allow port 8080: `sudo ufw allow 8080` |
| QR code not generating | Install Pillow: `pip3 install Pillow` |
| Server shows 0.0.0.0 as IP | Use `--interface wlan0` or `--interface eth0` |
| HTTPS warnings on phones | This demo runs on HTTP intentionally (real phishing often does too). If needed, use `ngrok` for HTTPS. |

---

## 🌐 Advanced: Using ngrok for Remote Access

If participants are NOT on the same network (e.g., remote workshop):

```bash
# Install ngrok
sudo apt install ngrok   # or download from ngrok.com

# Start tunnel
ngrok http 8080
```

Use the ngrok HTTPS URL for your QR code. This also gives a more realistic scenario.

---

## ⚠️ Legal & Ethical Reminders

- ✅ Only use in **controlled workshop environments**
- ✅ Always **reveal it's a demo** immediately after
- ✅ **No data is stored permanently** (memory only, lost on server restart)
- ✅ Get **written consent** if required by your organization
- ❌ Never use this outside an authorized educational setting
- ❌ Never target anyone who hasn't consented to participate

---

## 📁 File Structure

```
phishing_demo/
├── demo_server.py      ← Main server (run this)
├── demo_qr.png         ← Auto-generated QR code
└── SETUP_GUIDE.md      ← This file
```
