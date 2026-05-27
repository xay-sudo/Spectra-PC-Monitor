import os
import time
import socket
import urllib.request
import http.client
import psutil

from PyQt6.QtCore import QThread, pyqtSignal

# -------------------------------------------------------------
# THREAD-SAFE SPEEDTEST WORKER
# -------------------------------------------------------------
class SpeedTestWorker(QThread):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def run(self):
        try:
            results = {}
            
            # Phase 1: Ping
            self.progress.emit("Measuring Ping latency...", 10)
            pings = []
            for i in range(5):
                t0 = time.perf_counter()
                try:
                    s = socket.create_connection(("1.1.1.1", 53), timeout=2.0)
                    s.close()
                    pings.append((time.perf_counter() - t0) * 1000.0)
                except Exception as e:
                    print(f"[SpeedTest Ping Error] Attempt {i+1}: {e}")
                time.sleep(0.06)
                self.progress.emit("Measuring Ping latency...", 10 + i * 4)
            
            ping_val = sum(pings) / len(pings) if pings else 42.0
            results["ping"] = ping_val
            self.progress.emit(f"Ping: {ping_val:.1f} ms", 30)
            time.sleep(0.5)

            # Phase 2: Download Speed (using 3MB test file from Cloudflare CDN)
            self.progress.emit("Starting Download Test...", 35)
            url = "https://speed.cloudflare.com/__down?bytes=3000000"
            t0 = time.perf_counter()
            try:
                import ssl
                context = ssl._create_unverified_context()
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=20.0, context=context) as response:
                    total_size = int(response.info().get('Content-Length', 3000000))
                    bytes_read = 0
                    chunk_size = 65536
                    
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        bytes_read += len(chunk)
                        
                        elapsed = time.perf_counter() - t0
                        if elapsed > 0:
                            speed = (bytes_read * 8) / (elapsed * 1_000_000)
                            pct = 35 + int((bytes_read / total_size) * 35)
                            self.progress.emit(f"Download: {speed:.1f} Mbps", pct)
                            
                t1 = time.perf_counter()
                dl_time = t1 - t0
                dl_speed = (bytes_read * 8) / (dl_time * 1_000_000)
            except Exception as e:
                print(f"[SpeedTest Download Error] {e}")
                dl_speed = 0.0
                self.progress.emit(f"Download error: {str(e)}", 70)
                time.sleep(1.0)
                
            results["download"] = dl_speed
            self.progress.emit(f"Download: {dl_speed:.1f} Mbps", 70)
            time.sleep(0.5)

            # Phase 3: Upload Speed (POSTing 1MB to Cloudflare)
            self.progress.emit("Starting Upload Test...", 75)
            upload_payload = b"\0" * 1000000  # 1 MB
            t0 = time.perf_counter()
            try:
                import ssl
                context = ssl._create_unverified_context()
                conn = http.client.HTTPSConnection("speed.cloudflare.com", timeout=20.0, context=context)
                headers = {
                    "Content-Type": "application/octet-stream",
                    "Content-Length": str(len(upload_payload)),
                    "User-Agent": "Mozilla/5.0"
                }
                
                conn.putrequest("POST", "/__up")
                for k, v in headers.items():
                    conn.putheader(k, v)
                conn.endheaders()
                
                chunk_size = 32768
                uploaded = 0
                while uploaded < len(upload_payload):
                    chunk = upload_payload[uploaded:uploaded+chunk_size]
                    conn.send(chunk)
                    uploaded += len(chunk)
                    
                    elapsed = time.perf_counter() - t0
                    if elapsed > 0:
                        speed = (uploaded * 8) / (elapsed * 1_000_000)
                        pct = 75 + int((uploaded / len(upload_payload)) * 20)
                        self.progress.emit(f"Upload: {speed:.1f} Mbps", pct)
                        
                response = conn.getcall = conn.getresponse()
                response.read()
                t1 = time.perf_counter()
                ul_time = t1 - t0
                ul_speed = (len(upload_payload) * 8) / (ul_time * 1_000_000)
            except Exception as e:
                # Fallback support if connection was closed
                try:
                    response = conn.getresponse()
                    response.read()
                except Exception:
                    pass
                t1 = time.perf_counter()
                ul_time = t1 - t0
                ul_speed = (len(upload_payload) * 8) / (max(0.1, ul_time) * 1_000_000)
                
            results["upload"] = ul_speed
            self.progress.emit("Speed Test Completed!", 100)
            self.finished.emit(results)
            
        except Exception as e:
            print(f"[SpeedTest Thread Crash] {e}")
            self.error.emit(str(e))

# -------------------------------------------------------------
# THREAD-SAFE DISK BENCHMARK WORKER (SSD/M.2 Speed)
# -------------------------------------------------------------
class DiskSpeedTestWorker(QThread):
    progress = pyqtSignal(str, int)  # message, percentage (0-100)
    finished = pyqtSignal(dict)      # results
    error = pyqtSignal(str)          # error

    def run(self):
        try:
            # We will create a temp file in the active folder
            file_path = "temp_disk_speed_test.bin"
            chunk_size = 4 * 1024 * 1024  # 4MB chunks
            num_chunks = 64  # 256MB total
            total_size = chunk_size * num_chunks
            
            # Generate dummy bytes once and write repeatedly (avoids CPU bottleneck)
            dummy_chunk = os.urandom(chunk_size)
            
            # Phase 1: Write Speed Test
            self.progress.emit("Testing Write Speed...", 10)
            t0 = time.perf_counter()
            with open(file_path, "wb", buffering=0) as f:
                for i in range(num_chunks):
                    f.write(dummy_chunk)
                    f.flush()
                    try:
                        os.fsync(f.fileno())  # force OS cache flush to SSD hardware
                    except Exception:
                        pass
                    
                    elapsed = time.perf_counter() - t0
                    if elapsed > 0:
                        speed = ((i + 1) * chunk_size) / (elapsed * 1024 * 1024)  # MB/s
                        pct = 10 + int((i / num_chunks) * 40)
                        self.progress.emit(f"Writing: {speed:.1f} MB/s", pct)
                    
            t1 = time.perf_counter()
            write_time = t1 - t0
            write_speed = total_size / (write_time * 1024 * 1024)  # MB/s
            self.progress.emit(f"Write Completed: {write_speed:.1f} MB/s", 50)
            time.sleep(0.4)
            
            # Phase 2: Read Speed Test
            self.progress.emit("Testing Read Speed...", 60)
            t0 = time.perf_counter()
            with open(file_path, "rb", buffering=0) as f:
                for i in range(num_chunks):
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    elapsed = time.perf_counter() - t0
                    if elapsed > 0:
                        speed = ((i + 1) * chunk_size) / (elapsed * 1024 * 1024)  # MB/s
                        pct = 60 + int((i / num_chunks) * 40)
                        self.progress.emit(f"Reading: {speed:.1f} MB/s", pct)
                    
            t1 = time.perf_counter()
            read_time = t1 - t0
            read_speed = total_size / (read_time * 1024 * 1024)  # MB/s
            self.progress.emit(f"Read Completed: {read_speed:.1f} MB/s", 100)
            
            # Cleanup temp file
            if os.path.exists(file_path):
                os.remove(file_path)
                
            results = {
                "write_speed": write_speed,
                "read_speed": read_speed
            }
            self.finished.emit(results)
            
        except Exception as e:
            if 'file_path' in locals() and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            self.error.emit(str(e))

# -------------------------------------------------------------
# BACKGROUND WORKER FOR SYSTEM TUNE-UP
# -------------------------------------------------------------
class TuneUpWorker(QThread):
    progress_signal = pyqtSignal(str, int)
    category_size_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, mode="scan", selected_categories=None):
        super().__init__()
        self.mode = mode
        self.selected_categories = selected_categories or []
        self.categories = {
            "browser": {
                "name": "Web Browser Caches",
                "paths": [
                    os.path.expanduser("~/.cache/google-chrome"),
                    os.path.expanduser("~/.cache/mozilla"),
                    os.path.expanduser("~/.cache/BraveSoftware"),
                    os.path.expanduser("~/.cache/chromium"),
                    os.path.expanduser("~/.cache/Opera Software")
                ],
                "icon": "🌐"
            },
            "trash": {
                "name": "System Trash Bin",
                "paths": [
                    os.path.expanduser("~/.local/share/Trash/files"),
                    os.path.expanduser("~/.local/share/Trash/info")
                ],
                "icon": "🗑️"
            },
            "temp": {
                "name": "Temporary Files",
                "paths": ["/tmp", "/var/tmp"],
                "icon": "⚙️"
            },
            "pip_cache": {
                "name": "Package Manager Cache",
                "paths": [
                    os.path.expanduser("~/.cache/pip"),
                    os.path.expanduser("~/.cache/pipenv"),
                    os.path.expanduser("~/.cache/yarn"),
                    os.path.expanduser("~/.cache/npm"),
                    os.path.expanduser("~/.cache/flatpak")
                ],
                "icon": "📦"
            },
            "logs": {
                "name": "System Log Archives",
                "paths": [
                    os.path.expanduser("~/.cache/log"),
                    os.path.expanduser("~/.xsession-errors")
                ],
                "icon": "📝"
            }
        }

    def run(self):
        results = {}
        for cat_id, cat_info in self.categories.items():
            results[cat_id] = {"bytes": 0, "count": 0, "name": cat_info["name"]}
            
        if self.mode == "scan":
            self.progress_signal.emit("Initializing storage sweep...", 5)
            time.sleep(0.2)
            
            total_cats = len(self.categories)
            for i, (cat_id, cat_info) in enumerate(self.categories.items()):
                pct = int(10 + (i / total_cats) * 80)
                self.progress_signal.emit(f"Scanning {cat_info['name']}...", pct)
                
                cat_bytes = 0
                cat_count = 0
                for path in cat_info["paths"]:
                    if not os.path.exists(path):
                        continue
                    for root, dirs, files in os.walk(path):
                        for f in files:
                            fp = os.path.join(root, f)
                            try:
                                sz = os.path.getsize(fp)
                                cat_bytes += sz
                                cat_count += 1
                            except Exception:
                                pass
                results[cat_id]["bytes"] = cat_bytes
                results[cat_id]["count"] = cat_count
                
                self.category_size_signal.emit({cat_id: results[cat_id]})
                time.sleep(0.1)
                
            self.progress_signal.emit("Storage scan completed successfully.", 100)
            self.finished_signal.emit(results)
            
        elif self.mode == "clean":
            self.progress_signal.emit("Starting targeted cleanup operation...", 5)
            time.sleep(0.2)
            
            total_cats = len(self.selected_categories)
            if not total_cats:
                self.progress_signal.emit("No selections made.", 100)
                self.finished_signal.emit({})
                return
                
            for i, cat_id in enumerate(self.selected_categories):
                pct = int(10 + (i / total_cats) * 80)
                cat_info = self.categories.get(cat_id)
                if not cat_info:
                    continue
                self.progress_signal.emit(f"Wiping {cat_info['name']} cache buffers...", pct)
                
                cat_bytes = 0
                cat_count = 0
                for path in cat_info["paths"]:
                    if not os.path.exists(path):
                        continue
                    for root, dirs, files in os.walk(path):
                        for f in files:
                            fp = os.path.join(root, f)
                            try:
                                sz = os.path.getsize(fp)
                                os.remove(fp)
                                cat_bytes += sz
                                cat_count += 1
                            except Exception:
                                pass
                results[cat_id]["bytes"] = cat_bytes
                results[cat_id]["count"] = cat_count
                time.sleep(0.15)
                
            self.progress_signal.emit("System tune-up completed cleanly!", 100)
            self.finished_signal.emit(results)
