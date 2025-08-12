#!/usr/bin/env python3
"""
Philips WiZ Bulb Controller
A Python library for controlling Philips WiZ bulbs via UDP local control protocol.
"""

from typing import Dict, Any, Optional
import socket
import json
import time


class WizBulbController:
    """Controller for Philips WiZ bulbs using UDP protocol on port 38899."""
    
    def __init__(self, bulb_ip: str, port: int = 38899, timeout: float = 2.0):
        """
        Initialize the WiZ bulb controller.
        
        Args:
            bulb_ip: IP address of the WiZ bulb
            port: UDP port (default: 38899)
            timeout: Socket timeout in seconds
        """
        self.bulb_ip = bulb_ip
        self.port = port
        self.timeout = timeout
        self.socket = None
    
    def _send_command(self, command: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a UDP command to the bulb and return the response.
        
        Args:
            command: JSON command dictionary
            
        Returns:
            Response dictionary or None if failed
        """
        try:
            # Create socket for each command to ensure clean state
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Send command
            message = json.dumps(command).encode('utf-8')
            sock.sendto(message, (self.bulb_ip, self.port))
            
            # Receive response
            data, _ = sock.recvfrom(2048)
            response = json.loads(data.decode('utf-8'))
            
            sock.close()
            return response
            
        except socket.timeout:
            print(f"Timeout: No response from bulb at {self.bulb_ip}")
            return None
        except Exception as e:
            print(f"Error communicating with bulb: {e}")
            return None
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """Get the current status of the bulb."""
        command = {"method": "getPilot"}
        return self._send_command(command)
    
    def turn_on(self) -> bool:
        """Turn the bulb on."""
        command = {
            "method": "setPilot",
            "params": {"state": True}
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def turn_off(self) -> bool:
        """Turn the bulb off."""
        command = {
            "method": "setPilot",
            "params": {"state": False}
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def set_brightness(self, brightness: int) -> bool:
        """
        Set bulb brightness.
        
        Args:
            brightness: Brightness level (10-100)
        """
        if not 10 <= brightness <= 100:
            raise ValueError("Brightness must be between 10 and 100")
        
        command = {
            "method": "setPilot",
            "params": {
                "state": True,
                "dimming": brightness
            }
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def set_rgb_color(self, r: int, g: int, b: int, brightness: int = 100) -> bool:
        """
        Set RGB color.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            brightness: Brightness level (10-100)
        """
        if not all(0 <= val <= 255 for val in [r, g, b]):
            raise ValueError("RGB values must be between 0 and 255")
        if not 10 <= brightness <= 100:
            raise ValueError("Brightness must be between 10 and 100")
        
        command = {
            "method": "setPilot",
            "params": {
                "state": True,
                "r": r,
                "g": g,
                "b": b,
                "dimming": brightness
            }
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def set_color_temperature(self, temp: int, brightness: int = 100) -> bool:
        """
        Set color temperature (warm/cool white).
        
        Args:
            temp: Color temperature in Kelvin (2200-6500)
            brightness: Brightness level (10-100)
        """
        if not 2200 <= temp <= 6500:
            raise ValueError("Color temperature must be between 2200K and 6500K")
        if not 10 <= brightness <= 100:
            raise ValueError("Brightness must be between 10 and 100")
        
        command = {
            "method": "setPilot",
            "params": {
                "state": True,
                "temp": temp,
                "dimming": brightness
            }
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def set_scene(self, scene_id: int) -> bool:
        """
        Set a predefined scene.
        
        Common scene IDs:
        1: Ocean, 2: Romance, 3: Sunset, 4: Party, 5: Fireplace,
        6: Cozy, 7: Forest, 8: Pastel Colors, 9: Wake up, 10: Bedtime,
        11: Warm White, 12: Daylight, 13: Cool white, 14: Night light,
        15: Focus, 16: Relax, 17: True colors, 18: TV time, 19: Plantgrowth,
        20: Spring, 21: Summer, 22: Fall, 23: Deepdive, 24: Jungle,
        25: Mojito, 26: Club, 27: Christmas, 28: Halloween, 29: Candlelight,
        30: Golden white, 31: Pulse, 32: Steampunk
        """
        command = {
            "method": "setPilot",
            "params": {
                "state": True,
                "sceneId": scene_id
            }
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def set_speed(self, speed: int) -> bool:
        """
        Set animation speed for dynamic scenes.
        
        Args:
            speed: Speed value (10-200, where 200 is fastest)
        """
        if not 10 <= speed <= 200:
            raise ValueError("Speed must be between 10 and 200")
        
        command = {
            "method": "setPilot",
            "params": {"speed": speed}
        }
        response = self._send_command(command)
        return response is not None and response.get("result", {}).get("success", False)
    
    def is_online(self) -> bool:
        """Check if the bulb is online and responding."""
        status = self.get_status()
        return status is not None


def discover_bulbs(network_range: str = "192.168.1.0/24") -> list:
    """
    Discover WiZ bulbs on the network using nmap.
    
    Args:
        network_range: Network range to scan (e.g., "192.168.1.0/24")
        
    Returns:
        List of potential bulb IP addresses
    """
    import subprocess
    import re
    
    try:
        # Run nmap to discover devices
        result = subprocess.run(
            ["nmap", "-sn", network_range],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Extract IP addresses from nmap output
        ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', result.stdout)
        
        # Test each IP to see if it's a WiZ bulb
        bulb_ips = []
        for ip in ips:
            controller = WizBulbController(ip, timeout=1.0)
            if controller.is_online():
                bulb_ips.append(ip)
                print(f"Found WiZ bulb at: {ip}")
        
        return bulb_ips
        
    except subprocess.TimeoutExpired:
        print("Network scan timed out")
        return []
    except FileNotFoundError:
        print("nmap not found. Please install nmap to use bulb discovery.")
        return []
    except Exception as e:
        print(f"Error during discovery: {e}")
        return []


def main():
    """Example usage of the WiZ bulb controller."""
    
    # Discover WiZ bulbs on the network
    print("🔍 Discovering WiZ bulbs on the network...")
    bulb_ips = discover_bulbs()
    
    if not bulb_ips:
        print("❌ No WiZ bulbs found on the network.")
        print("Make sure:")
        print("  1. Your bulbs are powered on and connected to WiFi")
        print("  2. You're on the same network as the bulbs")
        print("  3. nmap is installed (brew install nmap on macOS)")
        print("\nYou can also manually specify an IP address by editing BULB_IP variable.")
        return
    
    # Use the first discovered bulb
    BULB_IP = bulb_ips[0]
    print(f"✅ Using bulb at {BULB_IP}")
    
    if len(bulb_ips) > 1:
        print(f"📝 Note: Found {len(bulb_ips)} bulbs. Using the first one.")
        print(f"   All discovered bulbs: {', '.join(bulb_ips)}")
    
    print(f"\n🔮 Connecting to WiZ bulb at {BULB_IP}...")
    bulb = WizBulbController(BULB_IP)
    
    # Check if bulb is online
    if not bulb.is_online():
        print("Bulb is not responding. Check IP address and network connection.")
        return
    
    print("Bulb is online!")
    
    # Get current status
    status = bulb.get_status()
    if status:
        print(f"Current status: {json.dumps(status, indent=2)}")
    
    # Demo sequence
    print("\n--- Demo Sequence ---")
    
    # Turn on
    print("Turning bulb on...")
    bulb.turn_on()
    time.sleep(1)
    
    # Set to bright white
    print("Setting to bright white...")
    bulb.set_color_temperature(4000, 100)
    time.sleep(2)
    
    # Set to red
    print("Setting to red...")
    bulb.set_rgb_color(255, 0, 0, 80)
    time.sleep(2)
    
    # Set to blue
    print("Setting to blue...")
    bulb.set_rgb_color(0, 0, 255, 80)
    time.sleep(2)
    
    # Set to green
    print("Setting to green...")
    bulb.set_rgb_color(0, 255, 0, 80)
    time.sleep(2)
    
    # Set romantic scene
    print("Setting romantic scene...")
    bulb.set_scene(2)  # Romance scene
    time.sleep(3)
    
    # Dim to 30%
    print("Dimming to 30%...")
    bulb.set_brightness(30)
    time.sleep(2)
    
    # Turn off
    print("Turning bulb off...")
    bulb.turn_off()
    
    print("Demo complete!")


if __name__ == "__main__":
    main()
