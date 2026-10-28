import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = """You are a customer service assistant for Kamau Stores,
a wholesale distributor in Nairobi.

Your rules:
- Only answer questions about orders, pricing, and delivery
- All prices are in KES. Never mention USD.
- Delivery covers Nairobi, Mombasa, Kisumu, and Nakuru only
- If a question is outside your scope, say: "Please call our office on 0712 345 678 for that."
- Always be polite and professional. End with "Asante kwa kuwasiliana."
"""
system_prompt = """You classify customer messages as: ORDER, COMPLAINT, or INQUIRY.

Examples:
User: "I need 50 bags of maize flour"
Answer: ORDER

User: "My delivery was 2 days late and items were damaged"
Answer: COMPLAINT

User: "Do you stock Pembe flour?"
Answer: INQUIRY

Reply with only the category. No explanation."""
# Tell Claude to return JSON so your code can parse it
system_prompt = """Extract the order details from the customer message.
Return ONLY valid JSON in this format:
{"product": "...", "quantity": ..., "urgency": "normal" or "urgent"}
No explanation. No markdown. Just the JSON."""

user_message = "I need 30 bags of rice urgently for tomorrow's event"

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    system=system_prompt,
    messages=[{"role": "user", "content": user_message}]
)
print(message.content[0].text)