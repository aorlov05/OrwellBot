import subprocess
import os
import random


def call_smalltalk_is_http(message):
    """
    Checks if a message is a link using the Smalltalk programming language

    Parameters:
    message: The content of a user message

    Returns:
    If the message is a link starting with http, https, or www, returns True.
    This also returns silently returns False if GNU Smalltalk is not installed on the OS.
    """
    # Open the Smalltalk file to read the existing content
    with open("hello.st", "r") as file:
        file_content = file.read()
    # Add small talk code to initialize MessageDetector object and call 'isHttp'
    modified_content = file_content.rstrip() + f"\n| message_detector |\nmessage_detector := MessageDetector new: '{message}'.\nmessage_detector isHttp.\n"
    # Generate random file name for running Smalltalk to avoid race condition
    random_file_name = f"check_link_{random.randint(1, 1000)}.st"
    # Write the modified content back to the file (replacing the old content)
    with open(random_file_name, "w") as file:
        file.write(modified_content)
    # Run the Smalltalk code using GNU Smalltalk
    try:
        result = subprocess.run(['gst', random_file_name], capture_output=True, text=True)
    except FileNotFoundError:
        # Could not compile the Smalltalk program
        return False
    finally:
        # Cleanup temp file
        if os.path.exists(random_file_name):
            os.remove(random_file_name)
    # If stdout=False, url was not found, therwise url pattern matched.
    return "False" not in str(result)


def check_profanity(mongo_client, message):
    """
    Returns a list of all profane words in a message with their corresponding severities
    :param mongo_client: A PyMongo MongoClient object to access the database
    :param message: The message to check
    :return: A list containing all profane words and their severities in a list
    """
    db = mongo_client["filter"]
    profanity = db["profanity"]

    detected_profanity = []
    # Fetch all profane words with rating and description
    for doc in profanity.find({}, {"text": 1, "severity_rating": 1, "severity_description": 1}):
        profanity_word = doc.get("text", "")
        # Check for profanity in the message
        if profanity_word.lower() in message.lower():
            # Add to list which contains the word and severity
            detected_profanity.append({
                "word": profanity_word,
                "severity_rating": doc["severity_rating"],
                "severity_description": doc["severity_description"]
            })
    return detected_profanity
