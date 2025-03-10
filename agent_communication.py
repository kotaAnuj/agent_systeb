"""
agent_communication.py

This module provides enhanced inter-agent communication protocols.
It defines methods for sending messages between multiple agents, allowing for
sophisticated inter-agent interactions.
"""

from typing import Dict, Any

class InterAgentCommunicator:
    def __init__(self):
        self.message_queue = []

    def send_message(self, agent_id: str, message: Dict[str, Any]) -> None:
        """
        Send a message to another agent.
        """
        self.message_queue.append((agent_id, message))
        print(f"Sent message to agent {agent_id}: {message}")

    def receive_messages(self) -> list:
        """
        Retrieve messages from the communication queue.
        """
        messages = self.message_queue[:]
        self.message_queue.clear()
        return messages
