
# Dental Clinic Appointment Booking Assistant

This project implements an AI-powered conversational assistant for booking dental clinic appointments. 
It utilizes LangChain with OpenAI's GPT models and stores user appointment details in a JSON file for persistent data management. 
The assistant ensures continuity in conversations and validates input for proper scheduling.

---

## Table of Contents

1. [Installation Requirements](#installation-requirements)
2. [How the Internal Process Works](#how-the-internal-process-works)
3. [Video Demonstration Link](#video-demonstration-link)

---

## Installation Requirements

### Prerequisites
1. **Python**: Ensure Python 3.7 or later is installed.
2. **Pip**: Install pip (Python's package manager).
3. **OpenAI API Key**: Obtain your API key from the [OpenAI website](https://platform.openai.com/).

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-link>
   cd <repository-folder>
   ```

2. **Set Up Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On macOS/Linux
   venv\Scripts\activate       # On Windows
   ```

3. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project directory.
   - Add your OpenAI API key to the file:
     ```env
     OPENAI_API_KEY=your-api-key
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

---

## How the Internal Process Works

### Overview
The assistant is built to manage user interactions efficiently and provide a seamless booking experience.

1. **User Data Management**:
   - The assistant checks if the user exists in the database (stored in a JSON file).
   - If the user already has an appointment, it retrieves and displays the details.
   - If not, it proceeds to book a new appointment.

2. **LangChain Setup**:
   - Uses OpenAI’s GPT-3.5 model for conversation.
   - A **ConversationBufferMemory** ensures context is retained across interactions.
   - A custom **PromptTemplate** tailors the AI’s behavior for booking appointments.

3. **Appointment Booking Flow**:
   - The user provides their name and unique ID.
   - If no appointment exists:
     - The assistant prompts the user for a **date** and **time**.
     - Validates the date and time formats.
     - Saves the booking details in the JSON file.
     - Confirms the booking and provides the cost.
   - If an appointment already exists:
     - The assistant notifies the user and displays the appointment details.

4. **Persistence**:
   - User data is saved in a `user_data.json` file.
   - The JSON file is updated dynamically with each new appointment.

5. **Error Handling**:
   - Ensures invalid date or time inputs are corrected through prompts.
   - Provides clear messages if the API key or required configurations are missing.

---

## Video Demonstration Link

Watch the demonstration of the assistant's functionality [here](https://drive.google.com/file/d/18g_xob1IjoZHooPHeajIaHnAPihxJeJ1/view?usp=sharing).

---