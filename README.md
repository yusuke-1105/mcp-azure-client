日本語版は[こちら](README-ja.md)をご覧ください。

# MCP Azure Client

A Python-based Model Context Protocol (MCP) client specifically designed to interact with Azure. This application provides a convenient way to connect to [Azure MCP servers](https://github.com/Azure/azure-mcp) and call available tools through an interactive command-line interface.

## Features

- Connects to Azure MCP servers using the MCP protocol
- Lists available tools with their descriptions and required parameters
- Allows interactive execution of tools with parameter input
- Packaged in Docker for consistent deployment across environments

## Requirements

- Python 3.12+
- Required Python packages:
  - `mcp`: Model Context Protocol library
  - `uv`: Dependency management
- Docker (for containerized execution)
- Node.js & npm (for Azure MCP server connection)

## Usage

### Docker Compose (Recommended)

The application is containerized for ease of use and is best run using Docker Compose, which manages all dependencies and environment setup automatically.

1. From the project directory, start the service:
   ```bash
   docker compose up -d
   ```
   
   After the service starts for the first time, enter the container and log in with Azure CLI:
   ```bash
   docker compose exec mcp-client az login
   ```

2. This will build the container, start the application, and show the logs directly in your terminal.

   ```bash
   docker compose exec mcp-client python3 mcp-client.py
   ```

3. When the application starts, it will automatically connect to the Azure MCP server and show the client interface.

4. To stop the service, press `Ctrl+C` and then run:
   ```bash
   docker compose down
   ```

### Local Installation

If you prefer to run the application locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure npm is installed on your system

3. Run the client:
   ```bash
   python mcp-client.py
   ```

## How It Works

1. The application initializes and connects to an Azure MCP server using npx to run the `@azure/mcp` package
2. Once connected, you can:
   - List all available tools (option 1)
   - Call a specific tool by number (option 2)
   - Exit the application (option 3)
3. When calling a tool, you'll be prompted to input required and optional parameters

## Code Overview

The `mcp-client.py` file contains:

- `MCPClient` class: Handles server connection logic
- `list_and_call_tools` function: Manages the interactive CLI interface
- Helper functions for unpacking tool definitions and displaying them
- Main function that orchestrates the application flow

## Project Structure

```plaintext
.
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker Compose configuration
├── mcp-client.py         # Main application code
└── requirements.txt      # Python dependencies
```