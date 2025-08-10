"""
Calculator MCP Server using FastMCP SDK

This MCP server provides basic arithmetic operations for AI agents, allowing them to:
- Perform addition of two numbers
- Perform subtraction of two numbers  
- Perform multiplication of two numbers
- Perform division of two numbers (with error handling for division by zero)

The server follows the same patterns as the note-taking and weather servers.
"""

from mcp.server.fastmcp import FastMCP

# Create the MCP server instance with a descriptive name
mcp = FastMCP("Calculator Server")


@mcp.tool()
def add(a: float, b: float) -> dict[str, str | float]:
    """
    Add two numbers together.
    
    Args:
        a (float): The first number
        b (float): The second number
        
    Returns:
        dict: Dictionary containing the operation, operands, and result
    """
    try:
        result = a + b
        return {
            "operation": "addition",
            "operand_1": a,
            "operand_2": b,
            "result": result,
            "expression": f"{a} + {b} = {result}"
        }
    except Exception as e:
        return {
            "operation": "addition",
            "operand_1": a,
            "operand_2": b,
            "error": f"Error performing addition: {str(e)}",
            "result": "N/A"
        }


@mcp.tool()
def subtract(a: float, b: float) -> dict[str, str | float]:
    """
    Subtract the second number from the first number.
    
    Args:
        a (float): The number to subtract from (minuend)
        b (float): The number to subtract (subtrahend)
        
    Returns:
        dict: Dictionary containing the operation, operands, and result
    """
    try:
        result = a - b
        return {
            "operation": "subtraction",
            "operand_1": a,
            "operand_2": b,
            "result": result,
            "expression": f"{a} - {b} = {result}"
        }
    except Exception as e:
        return {
            "operation": "subtraction",
            "operand_1": a,
            "operand_2": b,
            "error": f"Error performing subtraction: {str(e)}",
            "result": "N/A"
        }


@mcp.tool()
def multiply(a: float, b: float) -> dict[str, str | float]:
    """
    Multiply two numbers together.
    
    Args:
        a (float): The first number (multiplicand)
        b (float): The second number (multiplier)
        
    Returns:
        dict: Dictionary containing the operation, operands, and result
    """
    try:
        result = a * b
        return {
            "operation": "multiplication",
            "operand_1": a,
            "operand_2": b,
            "result": result,
            "expression": f"{a} × {b} = {result}"
        }
    except Exception as e:
        return {
            "operation": "multiplication",
            "operand_1": a,
            "operand_2": b,
            "error": f"Error performing multiplication: {str(e)}",
            "result": "N/A"
        }


@mcp.tool()
def divide(a: float, b: float) -> dict[str, str | float]:
    """
    Divide the first number by the second number.
    
    Args:
        a (float): The dividend (number to be divided)
        b (float): The divisor (number to divide by)
        
    Returns:
        dict: Dictionary containing the operation, operands, and result
    """
    try:
        # Check for division by zero
        if b == 0:
            return {
                "operation": "division",
                "operand_1": a,
                "operand_2": b,
                "error": "Division by zero is not allowed",
                "result": "undefined"
            }
        
        result = a / b
        return {
            "operation": "division",
            "operand_1": a,
            "operand_2": b,
            "result": result,
            "expression": f"{a} ÷ {b} = {result}"
        }
    except Exception as e:
        return {
            "operation": "division",
            "operand_1": a,
            "operand_2": b,
            "error": f"Error performing division: {str(e)}",
            "result": "N/A"
        }


@mcp.resource("calculator://operations")
def get_available_operations() -> str:
    """
    Get information about all available calculator operations.
    
    This resource provides documentation about the calculator's capabilities,
    which can be useful for AI agents to understand what operations are available.
    
    Returns:
        str: Documentation of available operations
    """
    operations_info = """
    CALCULATOR OPERATIONS AVAILABLE:

    1. ADDITION (add)
       - Adds two numbers together
       - Usage: add(a, b)
       - Example: add(5, 3) = 8

    2. SUBTRACTION (subtract)  
       - Subtracts second number from first
       - Usage: subtract(a, b)
       - Example: subtract(10, 4) = 6

    3. MULTIPLICATION (multiply)
       - Multiplies two numbers together
       - Usage: multiply(a, b)
       - Example: multiply(6, 7) = 42

    4. DIVISION (divide)
       - Divides first number by second number
       - Usage: divide(a, b)
       - Example: divide(15, 3) = 5
       - Note: Division by zero returns an error

    All operations accept floating-point numbers and return detailed result objects.
    """
    
    return operations_info


@mcp.prompt("calculate-expression")
def calculation_prompt() -> str:
    """
    Provide a prompt template for performing calculations.
    
    This prompt helps AI agents structure their approach to mathematical
    problems and provides guidance on using the calculator tools effectively.
    
    Returns:
        str: A prompt template for calculation assistance
    """
    prompt_template = """
    You are a mathematical calculation assistant with access to basic arithmetic operations.

    AVAILABLE OPERATIONS:
    - add(a, b): Addition
    - subtract(a, b): Subtraction  
    - multiply(a, b): Multiplication
    - divide(a, b): Division

    CALCULATION GUIDELINES:
    1. Break down complex expressions into individual operations
    2. Perform operations step by step in the correct order
    3. Use parentheses to clarify operation precedence
    4. Handle division by zero gracefully
    5. Provide clear explanations of each calculation step

    RESPONSE FORMAT:
    - Show the mathematical expression
    - Explain the calculation process
    - Present the final result clearly
    - Include any relevant mathematical context

    Please help the user with their calculation needs using the available tools.
    """
    
    return prompt_template


def main():
    """
    Entry point for running the calculator MCP server.
    
    This function starts the FastMCP server, which will listen for
    connections from AI agents and provide the defined arithmetic tools,
    resources, and prompts.
    """
    print("🧮 Starting Calculator MCP Server...")
    print("🔧 Available tools: add, subtract, multiply, divide")
    print("📊 Available resources: get_available_operations")  
    print("📋 Available prompts: calculation_prompt")
    print("🚀 Server ready for AI agent connections!")
    
    # Start the MCP server
    mcp.run()


# Run the server if this script is executed directly
if __name__ == "__main__":
    main()
