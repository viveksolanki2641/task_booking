import os
import json
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# File to store user data persistently
USER_DATA_FILE = "user_data.json"

def load_user_data():
    """
    Loads user data from a JSON file.
    Returns an empty dictionary if the file does not exist.
    """
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_data(data):
    """
    Saves user data to a JSON file.
    Overwrites the existing data in the file with the updated dictionary.
    """
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load existing user data into memory
user_database = load_user_data()

def setup_langchain():
    """
    Sets up a LangChain conversation agent with a custom prompt and memory.
    Ensures the OpenAI API key is available and configures the agent's behavior.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

    # Define the chat model to be used (OpenAI's GPT-3.5 Turbo)
    chat_model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # Initialize memory to retain conversational context
    memory = ConversationBufferMemory()

    # Define a custom prompt template for the AI assistant
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template="""
        You are a helpful AI assistant for booking dental clinic appointments. 
        Clinic timing is morning 9 AM to 1 PM, and evening 4 PM to 8 PM.  
        Maintain a polite and professional tone. Use the conversation history to ensure continuity. 
        Check if the user already has an appointment and update details if necessary.

        Conversation History:
        {history}

        New Message:
        {input}

        Your response:
        """
    )

    # Create and return a conversation chain using the chat model, memory, and prompt
    return ConversationChain(llm=chat_model, memory=memory, prompt=prompt)

def simulate_booking():
    """
    Simulates the conversation flow for booking a dental clinic appointment.
    Handles user identification, checks for existing appointments, and books new ones.
    """
    agent = setup_langchain()

    # Greet the user
    print("Welcome to our dental clinic!")

    # Collect user's name and unique identifier
    user_name = input("Please provide your name: ").strip()
    user_id = input("Please provide your user ID: ").strip()

    # Check if the user already has an appointment
    if user_id in user_database:
        print(f"AI Assistant: Hello {user_name}, it looks like you already have an appointment booked!")
        print(f"Details: {user_database[user_id]['appointment']}")
        return  # Exit if an appointment already exists

    # Start a conversation with the user
    print("AI Assistant: Hi! How can I assist you today?")
    user_input = input("Patient: ")

    while True:
        # Generate the assistant's response using the LangChain agent
        response = agent.run(input=user_input)
        print(f"AI Assistant: {response}")

        # Check for date and time in the response to proceed with booking
        if "date" in response.lower() and "time" in response.lower():
            # Collect and confirm date and time from the user
            date = input("Patient: Please confirm the date (e.g., August 10th): ").strip()
            time = input("Patient: Please confirm the time (e.g., 10 AM): ").strip()

            # Save appointment details to the user database
            appointment_details = f"{date} at {time}"
            user_database[user_id] = {"name": user_name, "appointment": appointment_details}
            save_user_data(user_database)  # Persist the data to the JSON file

            # Confirm the booking with the user
            print(f"AI Assistant: Booking your appointment for {appointment_details}... Done!")
            print(f"AI Assistant: Your appointment is confirmed. The cost is $50. Thank you!")
            break

        # End the conversation if the user says goodbye
        elif "goodbye" in response.lower():
            print("AI Assistant: Thank you for choosing our clinic. Goodbye!")
            break

        # Prompt the user for further input
        user_input = input("Patient: ")

# Run the script when executed directly
if __name__ == "__main__":
    simulate_booking()
