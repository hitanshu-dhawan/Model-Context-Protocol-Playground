"""
Smart Bulb MCP Server using FastMCP SDK

This MCP server provides smart bulb control capabilities for AI agents, allowing them to:
- Turn the bulb on/off
- Set brightness levels
- Change RGB colors
- Set color temperature
- Apply predefined scenes
- Check bulb status

The server uses the WizBulbController to communicate with Philips WiZ bulbs.
"""

from mcp.server.fastmcp import FastMCP
from wiz_bulb_controller import WizBulbController

# Create the MCP server instance with a descriptive name
mcp = FastMCP("Smart Bulb Server")

# Configure the bulb IP address
BULB_IP = "192.168.1.8"

# Initialize the bulb controller
bulb = WizBulbController(BULB_IP)


@mcp.tool()
def get_bulb_status() -> dict:
    """
    Get the current status of the smart bulb.
    
    Returns:
        dict: Dictionary containing the bulb's current state and properties
    """
    try:
        status = bulb.get_status()
        if status is None:
            return {
                "error": f"Failed to get status from bulb at {BULB_IP}",
                "bulb_ip": BULB_IP,
                "status": "offline"
            }
        
        # Extract useful information from the status
        result = {
            "bulb_ip": BULB_IP,
            "status": "online",
            "state": "on" if status.get("result", {}).get("state", False) else "off"
        }
        
        # Add brightness if available
        if "dimming" in status.get("result", {}):
            result["brightness"] = f"{status['result']['dimming']}%"
        
        # Add color information if available
        pilot_data = status.get("result", {})
        if "r" in pilot_data and "g" in pilot_data and "b" in pilot_data:
            result["color"] = f"RGB({pilot_data['r']}, {pilot_data['g']}, {pilot_data['b']})"
        elif "temp" in pilot_data:
            result["color_temperature"] = f"{pilot_data['temp']}K"
        
        # Add scene if available
        if "sceneId" in pilot_data:
            result["scene_id"] = pilot_data["sceneId"]
        
        return result
        
    except Exception as e:
        return {
            "error": f"Error getting bulb status: {str(e)}",
            "bulb_ip": BULB_IP,
            "status": "error"
        }


@mcp.tool()
def turn_bulb_on() -> dict:
    """
    Turn the smart bulb on.
    
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        success = bulb.turn_on()
        return {
            "operation": "turn_on",
            "bulb_ip": BULB_IP,
            "success": success,
            "message": "Bulb turned on successfully" if success else "Failed to turn on bulb"
        }
    except Exception as e:
        return {
            "operation": "turn_on",
            "bulb_ip": BULB_IP,
            "success": False,
            "error": f"Error turning on bulb: {str(e)}"
        }


@mcp.tool()
def turn_bulb_off() -> dict:
    """
    Turn the smart bulb off.
    
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        success = bulb.turn_off()
        return {
            "operation": "turn_off",
            "bulb_ip": BULB_IP,
            "success": success,
            "message": "Bulb turned off successfully" if success else "Failed to turn off bulb"
        }
    except Exception as e:
        return {
            "operation": "turn_off",
            "bulb_ip": BULB_IP,
            "success": False,
            "error": f"Error turning off bulb: {str(e)}"
        }


@mcp.tool()
def set_bulb_brightness(brightness: int) -> dict:
    """
    Set the brightness level of the smart bulb.
    
    Args:
        brightness (int): Brightness level between 10 and 100
        
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        if not 10 <= brightness <= 100:
            return {
                "operation": "set_brightness",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "Brightness must be between 10 and 100",
                "requested_brightness": brightness
            }
        
        success = bulb.set_brightness(brightness)
        return {
            "operation": "set_brightness",
            "bulb_ip": BULB_IP,
            "success": success,
            "brightness": brightness,
            "message": f"Brightness set to {brightness}%" if success else f"Failed to set brightness to {brightness}%"
        }
    except Exception as e:
        return {
            "operation": "set_brightness",
            "bulb_ip": BULB_IP,
            "success": False,
            "brightness": brightness,
            "error": f"Error setting brightness: {str(e)}"
        }


@mcp.tool()
def set_bulb_rgb_color(r: int, g: int, b: int, brightness: int = 100) -> dict:
    """
    Set the RGB color of the smart bulb.
    
    Args:
        r (int): Red value (0-255)
        g (int): Green value (0-255) 
        b (int): Blue value (0-255)
        brightness (int): Brightness level (10-100, default: 100)
        
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        if not all(0 <= val <= 255 for val in [r, g, b]):
            return {
                "operation": "set_rgb_color",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "RGB values must be between 0 and 255",
                "requested_color": f"RGB({r}, {g}, {b})"
            }
        
        if not 10 <= brightness <= 100:
            return {
                "operation": "set_rgb_color",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "Brightness must be between 10 and 100",
                "requested_brightness": brightness
            }
        
        success = bulb.set_rgb_color(r, g, b, brightness)
        return {
            "operation": "set_rgb_color",
            "bulb_ip": BULB_IP,
            "success": success,
            "color": f"RGB({r}, {g}, {b})",
            "brightness": brightness,
            "message": f"Color set to RGB({r}, {g}, {b}) at {brightness}% brightness" if success else "Failed to set RGB color"
        }
    except Exception as e:
        return {
            "operation": "set_rgb_color",
            "bulb_ip": BULB_IP,
            "success": False,
            "color": f"RGB({r}, {g}, {b})",
            "brightness": brightness,
            "error": f"Error setting RGB color: {str(e)}"
        }


@mcp.tool()
def set_bulb_color_temperature(temperature: int, brightness: int = 100) -> dict:
    """
    Set the color temperature of the smart bulb (warm/cool white).
    
    Args:
        temperature (int): Color temperature in Kelvin (2200-6500)
        brightness (int): Brightness level (10-100, default: 100)
        
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        if not 2200 <= temperature <= 6500:
            return {
                "operation": "set_color_temperature",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "Color temperature must be between 2200K and 6500K",
                "requested_temperature": f"{temperature}K"
            }
        
        if not 10 <= brightness <= 100:
            return {
                "operation": "set_color_temperature",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "Brightness must be between 10 and 100",
                "requested_brightness": brightness
            }
        
        success = bulb.set_color_temperature(temperature, brightness)
        return {
            "operation": "set_color_temperature",
            "bulb_ip": BULB_IP,
            "success": success,
            "temperature": f"{temperature}K",
            "brightness": brightness,
            "message": f"Color temperature set to {temperature}K at {brightness}% brightness" if success else "Failed to set color temperature"
        }
    except Exception as e:
        return {
            "operation": "set_color_temperature",
            "bulb_ip": BULB_IP,
            "success": False,
            "temperature": f"{temperature}K",
            "brightness": brightness,
            "error": f"Error setting color temperature: {str(e)}"
        }


@mcp.tool()
def set_bulb_scene(scene_id: int) -> dict:
    """
    Set a predefined scene on the smart bulb.
    
    Args:
        scene_id (int): Scene ID (1-32). Common scenes:
                       1=Ocean, 2=Romance, 3=Sunset, 4=Party, 5=Fireplace,
                       6=Cozy, 7=Forest, 11=Warm White, 12=Daylight, etc.
        
    Returns:
        dict: Dictionary containing the operation result
    """
    try:
        # Scene names for reference
        scene_names = {
            1: "Ocean", 2: "Romance", 3: "Sunset", 4: "Party", 5: "Fireplace",
            6: "Cozy", 7: "Forest", 8: "Pastel Colors", 9: "Wake up", 10: "Bedtime",
            11: "Warm White", 12: "Daylight", 13: "Cool white", 14: "Night light",
            15: "Focus", 16: "Relax", 17: "True colors", 18: "TV time", 19: "Plantgrowth",
            20: "Spring", 21: "Summer", 22: "Fall", 23: "Deepdive", 24: "Jungle",
            25: "Mojito", 26: "Club", 27: "Christmas", 28: "Halloween", 29: "Candlelight",
            30: "Golden white", 31: "Pulse", 32: "Steampunk"
        }
        
        if not 1 <= scene_id <= 32:
            return {
                "operation": "set_scene",
                "bulb_ip": BULB_IP,
                "success": False,
                "error": "Scene ID must be between 1 and 32",
                "requested_scene_id": scene_id
            }
        
        success = bulb.set_scene(scene_id)
        scene_name = scene_names.get(scene_id, f"Scene {scene_id}")
        
        return {
            "operation": "set_scene",
            "bulb_ip": BULB_IP,
            "success": success,
            "scene_id": scene_id,
            "scene_name": scene_name,
            "message": f"Scene set to '{scene_name}' (ID: {scene_id})" if success else f"Failed to set scene '{scene_name}'"
        }
    except Exception as e:
        return {
            "operation": "set_scene",
            "bulb_ip": BULB_IP,
            "success": False,
            "scene_id": scene_id,
            "error": f"Error setting scene: {str(e)}"
        }


@mcp.tool()
def check_bulb_connection() -> dict:
    """
    Check if the smart bulb is online and responding.
    
    Returns:
        dict: Dictionary containing the connection status
    """
    try:
        is_online = bulb.is_online()
        return {
            "operation": "check_connection",
            "bulb_ip": BULB_IP,
            "online": is_online,
            "status": "connected" if is_online else "disconnected",
            "message": f"Bulb at {BULB_IP} is {'online' if is_online else 'offline'}"
        }
    except Exception as e:
        return {
            "operation": "check_connection",
            "bulb_ip": BULB_IP,
            "online": False,
            "status": "error",
            "error": f"Error checking connection: {str(e)}"
        }


@mcp.resource("smartbulb://capabilities")
def get_bulb_capabilities() -> str:
    """
    Get information about all available smart bulb capabilities.
    
    This resource provides documentation about the bulb's capabilities,
    which can be useful for AI agents to understand what operations are available.
    
    Returns:
        str: Documentation of available bulb operations
    """
    capabilities_info = """
    SMART BULB CAPABILITIES AVAILABLE:

    1. POWER CONTROL
       - turn_bulb_on(): Turn the bulb on
       - turn_bulb_off(): Turn the bulb off

    2. BRIGHTNESS CONTROL
       - set_bulb_brightness(brightness): Set brightness (10-100%)

    3. COLOR CONTROL
       - set_bulb_rgb_color(r, g, b, brightness): Set RGB color (0-255 each)
       - set_bulb_color_temperature(temp, brightness): Set white temperature (2200-6500K)

    4. SCENE CONTROL
       - set_bulb_scene(scene_id): Apply predefined scenes (1-32)
         Popular scenes: 1=Ocean, 2=Romance, 3=Sunset, 4=Party, 11=Warm White, 12=Daylight

    5. STATUS & MONITORING
       - get_bulb_status(): Get current bulb state and properties
       - check_bulb_connection(): Test if bulb is online

    CURRENT CONFIGURATION:
    - Bulb IP Address: {BULB_IP}
    - Protocol: UDP (Port 38899)
    - Bulb Type: Philips WiZ Compatible

    All operations return detailed status information including success/failure and error messages.
    """.format(BULB_IP=BULB_IP)
    
    return capabilities_info


@mcp.prompt("control-smart-bulb")
def bulb_control_prompt() -> str:
    """
    Provide a prompt template for controlling the smart bulb.
    
    This prompt helps AI agents structure their approach to smart bulb control
    and provides guidance on using the bulb control tools effectively.
    
    Returns:
        str: A prompt template for smart bulb control assistance
    """
    prompt_template = f"""
    You are a smart home lighting assistant with access to control a Philips WiZ smart bulb.

    CURRENT BULB CONFIGURATION:
    - IP Address: {BULB_IP}
    - Connection: UDP Protocol (Port 38899)

    AVAILABLE OPERATIONS:
    - Power: turn_bulb_on(), turn_bulb_off()
    - Brightness: set_bulb_brightness(10-100)
    - RGB Colors: set_bulb_rgb_color(r, g, b, brightness)
    - White Temperature: set_bulb_color_temperature(2200-6500K, brightness)
    - Scenes: set_bulb_scene(1-32) - Romance, Party, Cozy, etc.
    - Status: get_bulb_status(), check_bulb_connection()

    BEST PRACTICES:
    1. Always check bulb connection before performing operations
    2. Provide clear feedback about operation success/failure
    3. Suggest appropriate brightness levels for different scenarios
    4. Recommend suitable color temperatures (warm: 2700K, cool: 5000K+)
    5. Explain scene options when user asks for ambiance

    RESPONSE GUIDELINES:
    - Confirm each action taken with the bulb
    - Explain any errors in user-friendly terms
    - Suggest alternatives if an operation fails
    - Provide context for color and brightness recommendations

    Please help the user control their smart bulb effectively and create the perfect lighting ambiance.
    """
    
    return prompt_template


def main():
    """
    Entry point for running the smart bulb MCP server.
    
    This function starts the FastMCP server, which will listen for
    connections from AI agents and provide the defined smart bulb control tools,
    resources, and prompts.
    """
    print("💡 Starting Smart Bulb MCP Server...")
    print(f"🔗 Connected to bulb at IP: {BULB_IP}")
    print("🔧 Available tools: get_bulb_status, turn_bulb_on, turn_bulb_off,")
    print("    set_bulb_brightness, set_bulb_rgb_color, set_bulb_color_temperature,")
    print("    set_bulb_scene, check_bulb_connection")
    print("📊 Available resources: get_bulb_capabilities")  
    print("📋 Available prompts: bulb_control_prompt")
    print("🚀 Server ready for AI agent connections!")
    
    # Test bulb connection on startup
    print(f"\n🔍 Testing connection to bulb at {BULB_IP}...")
    if bulb.is_online():
        print("✅ Bulb is online and ready!")
    else:
        print("⚠️  Warning: Cannot connect to bulb. Please check:")
        print("   1. Bulb is powered on and connected to WiFi")
        print("   2. IP address is correct")
        print("   3. You're on the same network as the bulb")
    
    # Start the MCP server
    mcp.run()


# Run the server if this script is executed directly
if __name__ == "__main__":
    main()