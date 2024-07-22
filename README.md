README for Running the Chatbot Code


Prerequisites


Ensure you have the following installed on your system:

• Python 3.7 or higher

• pip (Python package installer)


Required Python Packages


Install the necessary packages by running the following command:

bash

pip install sentence-transformers scikit-learn numpy pymupdf tk pyttsx3


Project Directory Structure

Your project directory should look like this:

chatbot_project/

│
├── chatbot.py

├── Sample Question Answers.json

├── corpus.pdf

•

chatbot.py: The main Python file containing the chatbot code.

•Sample Question Answers.json: A JSON file with sample questions and answers.

•corpus.pdf: A PDF file containing additional text for the chatbot to use.


JSON File Structure


The Sample Question Answers.json file should have the following structure:

json

Copy code
[

{

"question": "What is your question?",

"answer": "This is the answer."


},

{
"question": "Another question?",

"answer": "Another answer."

}
]


Running the Code
1.Place all the required files (chatbot.py, Sample Question Answers.json, corpus.pdf) in the same directory.

2.Open a terminal or command prompt.

3.
Navigate to the project directory:

bash
cd path/to/chatbot_project

5.
Run the chatbot application:

bash

python chatbot.py
'

Using the Chatbot


•
Once the application starts, a GUI window will open.

•
You can type your questions into the text entry box at the bottom and press the "Send" button or press Enter to send the message.
•

The chatbot will respond in the chat window, and you will also hear the responses through text-to-speech.
Note
•
Ensure your corpus.pdf and Sample Question Answers.json files are formatted correctly and are placed in the correct directory.
•
If you encounter any issues, check the terminal for error messages and ensure all dependencies are installed correctly.
Enjoy using your chatbot!
