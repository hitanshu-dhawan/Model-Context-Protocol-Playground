"""
AI Sticky Notes MCP Server

This MCP server provides note-taking functionality for AI agents, allowing them to:
- Add new notes to a persistent storage file
- Read all existing notes
- Get the latest note as a resource
- Use a prompt template for note summarization

Based on the tutorial from: https://www.youtube.com/watch?v=-8k9lGpGQ6g
Source code reference: https://github.com/techwithtim/PythonMCPServer
"""

import os
from mcp.server.fastmcp import FastMCP

# Create the MCP server instance with a descriptive name
mcp = FastMCP("AI Sticky Notes")

# Configuration - Define the file where notes will be stored
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")


def ensure_file() -> None:
    """
    Ensure the notes file exists before performing any operations.
    
    This function checks if the notes.txt file exists, and if not,
    creates it with an empty state. This prevents file not found errors
    when trying to read or append to the file.
    """
    if not os.path.exists(NOTES_FILE):
        # Create the file in write mode (this will create a new file)
        with open(NOTES_FILE, "w") as f:
            # Write an empty string to initialize the file
            f.write("")


@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky notes file.
    
    This tool allows AI agents to add new notes to persistent storage.
    Each note is appended to a new line in the notes.txt file.
    
    Args:
        message (str): The note content to be added
        
    Returns:
        str: Confirmation message indicating the note was saved
    """
    # Ensure the notes file exists before writing to it
    ensure_file()
    
    # Open the file in append mode to add content without overwriting
    with open(NOTES_FILE, "a") as f:
        # Write the message followed by a newline character
        f.write(message + "\n")
    
    # Return a confirmation message to the AI agent
    return "Note saved!"


@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky notes file.
    
    This tool retrieves all previously saved notes and returns them
    as a single string. If no notes exist, returns a helpful message.
    
    Returns:
        str: All notes content or a message if no notes exist
    """
    # Ensure the file exists before trying to read it
    ensure_file()
    
    try:
        # Open the file in read mode
        with open(NOTES_FILE, "r") as f:
            # Read all content from the file
            content = f.read()
        
        # Check if the file is empty or contains only whitespace
        if not content.strip():
            return "No notes yet."
        
        return content
    
    except Exception as e:
        # Handle any unexpected errors when reading the file
        return f"Error reading notes: {str(e)}"


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the most recent note from the sticky notes file.
    
    This resource provides access to just the latest note, which can be
    useful for AI agents that need to reference the most recent entry
    without loading all notes.
    
    Resources are like GET endpoints - they provide data/context to AI agents.
    The URI 'notes://latest' identifies this resource uniquely.
    
    Returns:
        str: The latest note content or a message if no notes exist
    """
    # Ensure the file exists before reading
    ensure_file()
    
    try:
        # Open and read the file
        with open(NOTES_FILE, "r") as f:
            lines = f.readlines()
        
        # Check if there are any notes
        if not lines:
            return "No notes available."
        
        # Get the last line (most recent note) and strip whitespace
        latest_note = lines[-1].strip()
        
        # Return the latest note or a message if it's empty
        return latest_note if latest_note else "No notes available."
    
    except Exception as e:
        # Handle any errors that occur while reading the file
        return f"Error retrieving latest note: {str(e)}"


@mcp.prompt("note-summary")
def note_summary_prompt() -> str:
    """
    Provide a reusable prompt template for summarizing notes.
    
    This prompt gives AI agents a structured template for analyzing
    and summarizing the contents of the notes file. Prompts are
    reusable templates that help maintain consistency in AI interactions.
    
    The prompt name 'note-summary' identifies this template uniquely.
    
    Returns:
        str: A prompt template for note summarization
    """
    # Read the current notes to include in the prompt
    current_notes = read_notes()
    
    # Create a comprehensive prompt template
    prompt_template = f"""
        Please analyze and summarize the following notes:

        NOTES CONTENT:
        {current_notes}

        SUMMARIZATION INSTRUCTIONS:
        1. Provide a concise overview of the main topics covered
        2. Identify any recurring themes or patterns
        3. Highlight the most important or actionable items
        4. Organize the summary in a clear, structured format
        5. If there are many notes, group related topics together

        Please create a well-organized summary that captures the key information from these notes.
        """
    
    return prompt_template


def main():
    """
    Entry point for running the note-taking MCP server.
    
    This function starts the FastMCP server, which will listen for
    connections from AI agents and provide the defined tools, resources,
    and prompts.
    """
    print("🗒️  Starting AI Sticky Notes MCP Server...")
    print(f"📝 Notes will be stored in: {os.path.abspath(NOTES_FILE)}")
    print("🔧 Available tools: add_note, read_notes")
    print("📊 Available resources: get_latest_note")  
    print("📋 Available prompts: note_summary_prompt")
    print("🚀 Server ready for AI agent connections!")
    
    # Start the MCP server
    mcp.run()


# Run the server if this script is executed directly
if __name__ == "__main__":
    main()
