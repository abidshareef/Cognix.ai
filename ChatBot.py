from groq import Groq #Importing the Groq Tibrary to use its API.
from json import load, dump, decoder    #Importing functions to read and write JSON files.
import datetime    #Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values    #Importing dotenv values to read environment variables from a .env file.

#Load environment variables from the .env file.
env_vars=dotenv_values(#path to your env)  

#Retrieve specific environment variables for username, assistant hame, and API key.
  #**env shouls and must include!!!**
Username=env_vars.get("Username") #Multiple usernames/ users
Assistantname=env_vars.get("Assistantname") #COGNIX
GroqAPIkey=env_vars.get("GroqAPIkey")

if not GroqAPIkey:
    raise ValueError("GroqAPIkey not found in .env file or is empty!")

#Initialize the Groq client using the provided API key.
client=Groq(api_key=GroqAPIkey)

#Initialize an empty list to store chat messages.
messages = []

#Define a system message that provides context to the Al chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi URDU, reply in English.***
*** YOU ARE SPECIFICALLY DESIGNED TO HELP STUDENTS EXCEL IN THEIR STUDIES YOU FIND THEM PLANS ROUTES AND ANALYTICS ACCORDING TO THEIR EACH UNDERSTANDING LEVELS STEADY SLOW BUT EFFICIENT.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""


# A list of system instructions that define the behavior and capabilities of the AI assistant.
SystemChatBot= [
    {"role": "system", "content": System}
]

# Attempt to load the chat history from a JSON file.
try:
    with open("ChatHistory.json", "r") as file:
        ChatHistory = load(file)
except (FileNotFoundError, decoder.JSONDecodeError):
    # If the file is not found or is invalid/empty, initialize an empty chat history.
    with open("ChatHistory.json", "w") as file:
        dump([], file)
    ChatHistory = []

#Funtion to get real time date and time in

def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # Get the current date and time.   
    day = current_date_time.strftime("%A")  # Get the current day of the week.  
    date = current_date_time.strftime("%d")  # Get the current day of the month.
    month = current_date_time.strftime("%B")  # Get the current month.
    year = current_date_time.strftime("%Y")  # Get the current year.  
    hour = current_date_time.strftime("%I")  # Get the current hour in 12-hour format.
    minute = current_date_time.strftime("%M")  # Get the current minute.    
    second = current_date_time.strftime("%S")  # Get the current second.

    # format the information into a string.
    data = f"Please use this real time information in your query:,\n"
    data += f"Day: {day}, Date: {date}, Month: {month}, Year: {year}, Hour: {hour}, Minute: {minute}, Second: {second}.\n"  
    return data  # Return the formatted string.

#Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split("\n")  # Split the answer into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = "\n".join(non_empty_lines)  # Join the non-empty lines back together.
    return modified_answer  # Return the modified answer.  

# mAIN CHATBOT FUNCTION TO HANDLE USER QUERIES.
def ChatBot(Query):
    try:
        # Load chat history
        with open("ChatHistory.json", "r") as file:
            ChatHistory = load(file)

        # Add user message to chat history
        ChatHistory.append({"role": "user", "content": Query})

        # Limit chat history to the last N messages to avoid token overflow
        MAX_HISTORY = 20  # Adjust as needed
        trimmed_history = ChatHistory[-MAX_HISTORY:]

        # Send request to Groq API
        completion = client.chat.completions.create(
            stream=False,
            model="llama3-70b-8192",
            messages=SystemChatBot + trimmed_history,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        Answer = completion.choices[0].message.content

        # Add assistant response to chat history
        ChatHistory.append({"role": "assistant", "content": Answer})

        # Save updated chat history
        with open("ChatHistory.json", "w") as file:
            dump(ChatHistory, file)
        return AnswerModifier(Answer)
    except Exception as e:
        print(f"Error: {e}")  # Show the real error in your terminal
        return "An error occurred while processing your request."

if __name__ == "__main__":
    while True:
        user_input = input("Ask me something>>  ")
        if user_input.lower() == "exit":
            break
        response = ChatBot(user_input)
        print(response)
