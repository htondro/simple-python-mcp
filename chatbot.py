"""
A chatbot implementation using Anthropic's Claude API with a custom MCP (Model Context Protocol) server.
This module provides functionality to interact with Claude and execute various tools through an MCP server.
"""

import subprocess
import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv

class MCPClient:
    """
    A client for interacting with the MCP (Model Context Protocol) server.
    Handles JSON-RPC communication with the server for tool execution and initialization.
    """

    def __init__(self, server_command):
        """
        Initialize the MCP client with a server command.

        Args:
            server_command (str): Command to start the MCP server
        """
        self.process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            shell=True
        )
        self.request_id = 0

    def send_request(self, method, params=None):
        """
        Send a JSON-RPC request to the MCP server.

        Args:
            method (str): The RPC method name to call
            params (dict, optional): Parameters for the RPC method. Defaults to None.

        Returns:
            dict: The result from the server

        Raises:
            Exception: If the server returns an error
        """
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        self.process.stdin.write(json.dumps(request) + '\n')
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        response = json.loads(response_line)
        if 'error' in response:
            raise Exception(response['error']['message'])
        return response['result']

    def initialize(self):
        """Initialize the connection with the MCP server."""
        return self.send_request('initialize')

    def list_tools(self):
        """Retrieve the list of available tools from the server."""
        return self.send_request('tools/list')

    def call_tool(self, name, input_data):
        """
        Call a specific tool on the MCP server.

        Args:
            name (str): Name of the tool to call
            input_data (dict): Input parameters for the tool

        Returns:
            dict: The result from the tool execution
        """
        return self.send_request('tools/call', {"name": name, "input": input_data})

def main():
    """
    Main function to run the chatbot application.
    Sets up the environment, initializes clients, and handles the chat loop.
    """
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        return

    # Initialize Anthropic client for Claude API
    client = Anthropic(api_key=api_key)

    # Initialize MCP client and get available tools
    mcp_client = MCPClient("python mcp_server.py")
    mcp_client.initialize()
    tools_response = mcp_client.list_tools()
    tools = tools_response['tools']
    print(f"Available tools: {[tool['name'] for tool in tools]}")

    # Main chat loop
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        # Initialize conversation with user's input
        messages = [{"role": "user", "content": user_input}]
        
        # Continue getting responses until we have a complete interaction
        while True:
            try:
                # Get initial response from Claude
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1024,
                    messages=messages,
                    tools=tools
                )
                
                # Process any tool calls in the response
                has_tool_calls = False
                tool_calls = []
                
                # Extract tool calls from response blocks
                for block in response.content:
                    if block.type == 'tool_use':
                        has_tool_calls = True
                        tool_calls.append({
                            "name": block.name,
                            "input": block.input,
                            "id": block.id
                        })
                
                if has_tool_calls:
                    print(f"Found {len(tool_calls)} tool calls")
                    # Add Claude's response with tool calls to conversation
                    messages.append({"role": "assistant", "content": response.content})
                    
                    # Execute each tool call and add results to conversation
                    for tool_call in tool_calls:
                        try:
                            # Execute the tool
                            tool_result = mcp_client.call_tool(tool_call["name"], tool_call["input"])
                            print(f"Tool {tool_call['name']} result: {tool_result}")
                            
                            # Add tool result to conversation
                            tool_result_message = {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_call["id"],
                                        "content": tool_result
                                    }
                                ]
                            }
                            
                            messages.append(tool_result_message)
                        except Exception as e:
                            # Handle tool execution errors
                            print(f"Error processing tool call {tool_call['name']}: {e}")
                            error_message = {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_call["id"],
                                        "content": f"Error: {str(e)}",
                                        "is_error": True
                                    }
                                ]
                            }
                            messages.append(error_message)
                    
                    # Get final response after tool execution
                    try:
                        final_response = client.messages.create(
                            model="claude-3-7-sonnet-20250219",
                            max_tokens=1024,
                            messages=messages
                        )
                        
                        # Extract and print text from final response
                        response_text = ""
                        for block in final_response.content:
                            if block.type == "text":
                                response_text += block.text
                        print("Assistant:", response_text)
                    except Exception as e:
                        print(f"Error: {e}")
                        print("Failed to process the tool results. Please try again.")
                    
                    break
                else:
                    # Handle responses without tool calls
                    response_text = ""
                    for block in response.content:
                        if block.type == "text":
                            response_text += block.text
                    print("Assistant:", response_text)
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                print("Failed to process the response. Please try again.")
                break

if __name__ == '__main__':
    main()