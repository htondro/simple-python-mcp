"""
Model Context Protocol (MCP) Server Implementation

This module implements a server for the Model Context Protocol (MCP), which handles
tool execution requests from AI models. It provides a JSON-RPC interface for
receiving tool calls and returning their results.

The server currently implements a simple get_current_time tool as an example,
but can be extended to support additional tools as needed.
"""

import json
import sys
import datetime

def get_current_time():
    """
    Get the current date and time in a standardized format.
    
    Returns:
        str: Current date and time in the format "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_request(request):
    """
    Handle incoming JSON-RPC requests from the MCP client.
    
    This function processes different types of requests:
    - initialize: Protocol initialization
    - tools/list: List available tools
    - tools/call: Execute a specific tool
    
    Args:
        request (dict): The JSON-RPC request to process
        
    Returns:
        dict: The JSON-RPC response containing either the result or an error
    """
    method = request.get('method')
    
    if method == 'initialize':
        # Return protocol version and capabilities
        return {"result": {"protocolVersion": "2025-03-26", "capabilities": {}}}
    elif method == 'tools/list':
        # Define available tools and their schemas
        tools = [
            {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "input_schema": {"type": "object", "properties": {}}
            }
        ]
        return {"result": {"tools": tools}}
    elif method == 'tools/call':
        # Extract tool name and parameters
        params = request.get('params', {})
        tool_name = params.get('name')
        
        # Execute the requested tool
        if tool_name == 'get_current_time':
            result = get_current_time()
            return {"result": result}
        else:
            return {"error": {"code": -32601, "message": "Method not found"}}
    else:
        return {"error": {"code": -32601, "message": "Method not found"}}

def main():
    """
    Main entry point for the MCP server.
    
    This function:
    1. Reads JSON-RPC requests from stdin
    2. Processes each request using handle_request
    3. Writes responses to stdout
    4. Handles errors gracefully
    """
    while True:
        # Read a line from stdin
        line = sys.stdin.readline()
        if not line:
            break
            
        try:
            # Parse and process the request
            request = json.loads(line)
            response = handle_request(request)
            
            # Add request ID to response
            response['id'] = request.get('id')
            
            # Send response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            # Handle invalid JSON input
            pass
        except Exception as e:
            # Handle other errors
            error_response = {
                "jsonrpc": "2.0", 
                "id": request.get('id'),
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == '__main__':
    main()