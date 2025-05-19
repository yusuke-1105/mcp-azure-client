from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

from typing import Optional, Tuple, Any
from types import SimpleNamespace
import asyncio

class MCPClient:
    def __init__(self) -> None:
        """Initialize the Azure-specific MCP client"""
    
    # Connect to Azure MCP server ----------------------------
    async def connect_to_server(self) -> Optional[Tuple[Any, Any]]:
        """
        Establish a connection to the Azure MCP Server
        
        This method sets up the server parameters, initializes the stdio client context,
        establishes communication streams, and creates a client session.
        
        Returns:
            tuple: A tuple containing (session, stdio_cm) if successful, None otherwise
        """
        # Set up server parameters
        server_params = StdioServerParameters(command="npx", args=["-y", "@azure/mcp@latest", "server", "start"])

        try:
            print("Connecting to Azure MCP Server...")
            # Connect to the server (maintain stdio client context)
            stdio_cm = stdio_client(server_params)
            read_stream, write_stream = await stdio_cm.__aenter__()
            
            # Create client session
            session = ClientSession(read_stream, write_stream)
            await session.__aenter__()
            
            # Initialize session
            await session.initialize()
            
            print("Successfully connected to Azure MCP Server")
            return session, stdio_cm
        except Exception as e:
            print(f"Error: Failed to connect to Azure MCP Server - {e}")
            return None

# List and call tools ----------------------------
async def list_and_call_tools(session: ClientSession) -> None:
    """
    Main function to manage tool listing and execution
    
    This function provides an interactive interface for users to:
    1. View available tools
    2. Call tools with the required arguments
    3. Exit the tool management interface
    
    Args:
        session: The active MCP client session
    """
    def unpack_tool(tool: Any) -> Tuple[str, str, Any]:
        """
        Extract name, description, and arguments from a tool object
        
        This helper function handles different tool object formats:
        - Direct arguments attribute
        - JSON schema format
        - Tuple/list format
        - String fallback format
        
        Args:
            tool: Tool object in any supported format
            
        Returns:
            tuple: (name, description, arguments)
        """
        # Existing argument descriptors take precedence
        if hasattr(tool, 'arguments') and getattr(tool, 'arguments'):
            return tool.name, getattr(tool, 'description', ''), tool.arguments
        # Parse JSON schema if available
        if hasattr(tool, 'inputSchema') and tool.inputSchema:
            schema = tool.inputSchema or {}
            props = schema.get('properties', {})
            required_list = schema.get('required', []) or []
            args_list = []
            for arg_name, info in props.items():
                desc = info.get('description', '')
                is_req = arg_name in required_list
                args_list.append(SimpleNamespace(name=arg_name, description=desc, required=is_req))
            return tool.name, getattr(tool, 'description', ''), args_list
        # tuple or list fallback
        if isinstance(tool, (tuple, list)):
            name = tool[0] if len(tool) > 0 else ''
            description = tool[1] if len(tool) > 1 else ''
            arguments = tool[2] if len(tool) > 2 else []
            return name, description, arguments
        # fallback to string
        return str(tool), '', []
    
    # Helper function to display available tools -----------------
    async def show_available_tools(session: ClientSession) -> None:
        """
        Display all available tools with their descriptions and arguments
        
        This function retrieves all tools from the session, formats them
        in a user-friendly manner, and displays them with their arguments.
        
        Args:
            session: The active MCP client session
        """
        result = await session.list_tools()
        tools = getattr(result, 'tools', result)
        if not tools:
            print("No tools available")
            return

        print("\nAvailable tools:")
        for idx, tool in enumerate(tools):
            name, description, arguments = unpack_tool(tool)
            print(f"{idx + 1}. {name}: {description}")
            print("   Arguments:")
            for arg in arguments:
                required = "(Required)" if arg.required else "(Optional)"
                print(f"   - {arg.name}: {arg.description} {required}")
            print()
    
    # Helper function to call tools interactively ----------------------------
    async def call_tool_interactive(session: ClientSession) -> None:
        """
        Interactive function to select and call a tool
        
        This function:
        1. Lists all available tools
        2. Prompts the user to select a tool by number
        3. Collects required and optional arguments from the user
        4. Calls the selected tool with the provided arguments
        5. Displays the results
        
        Args:
            session: The active MCP client session
        """
        result = await session.list_tools()
        tools = getattr(result, 'tools', result)
        if not tools:
            print("No tools available")
            return

        print("\nAvailable tools:")
        for idx, tool in enumerate(tools):
            name, description, _ = unpack_tool(tool)
            print(f"{idx + 1}. {name}: {description}")

        try:
            tool_idx = int(input("\nEnter the tool number you want to use: ")) - 1
            if tool_idx < 0 or tool_idx >= len(tools):
                print("Invalid tool number")
                return

            selected_tool = tools[tool_idx]
            name, _, arguments = unpack_tool(selected_tool)

            print(f"\nArguments for '{name}' tool:")
            args = {}
            for arg in arguments:
                required = "(Required)" if arg.required else "(Optional)"
                value = input(f"{arg.name} {required}: ")
                if value or arg.required:
                    args[arg.name] = value

            result = await session.call_tool(name, args)
            if result:
                print("\nResults:")
                content = result.content
                if isinstance(content, list):
                    for item in content:
                        text = getattr(item, 'text', None)
                        print(text if text is not None else item)
                else:
                    text = getattr(content, 'text', None)
                    print(text if text is not None else content)
        except ValueError:
            print("Please enter a number")
    
    """
    Main interaction loop for the tool interface
    
    Provides a menu system for:
    1. Viewing available tools
    2. Calling tools interactively
    3. Exiting the application
    
    This loop continues until the user chooses to exit.
    """
    while True:
        print("\nSelect an operation:")
        print("1. Display available tools")
        print("2. Call a tool")
        print("3. Exit")
        
        choice = input("\nChoice (1-3): ")
        
        if choice == "1":
            await show_available_tools(session)
            continue
        
        elif choice == "2":
            await call_tool_interactive(session)
            continue
        
        elif choice == "3":
            break
        
        else:
            print("Invalid selection. Please enter 1, 2, or 3.")

async def main() -> None:
    """
    Main entry point for the MCP Azure client application
    
    This function performs the following steps:
    1. Creates an MCP client instance
    2. Connects to the Azure MCP server
    3. Handles tool listing and calling through the interactive interface
    4. Properly cleans up resources on exit
    """
    # Create MCP client
    client = MCPClient()

    # Connect to Azure server
    result = await client.connect_to_server()
    if not result:
        return
    session, stdio_cm = result

    # List and call tools through interactive interface
    await list_and_call_tools(session)

    # Clean up session and stdio client context
    await session.__aexit__(None, None, None)
    await stdio_cm.__aexit__(None, None, None)

if __name__ == "__main__":
    """
    Script entry point
    
    When this script is run directly (not imported as a module),
    execute the main async function with proper asyncio handling.
    """
    asyncio.run(main())
