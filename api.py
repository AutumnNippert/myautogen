from openai import OpenAI
import os
from dotenv import load_dotenv
from timeout_decorator import timeout

DEBUG = True

# Set your API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class System:
    def run_command(string):
        import subprocess

        # print("$ " + string)
        cmd = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE)
        output = cmd.stdout.read()
        return "Successfully run command\n" + output.decode('utf-8')

class OpenAI:
    # Define function to generate response
    @timeout(30, timeout_exception=TimeoutError)
    def generate_response(model="gpt-3.5-turbo", history=[], personality=None):
        # is_truncated = False
        try:
            # add {} to the top of history
            if personality:
                history.insert(0, {"role": "system", "content": personality})
            
            response = client.chat.completions.create(model=model,messages=history)
            response = response.choices[0].message.content

            # remove the personality from the history, saving space
            if personality:
                history.pop(0)
                
            return response 
        except Exception as e:
            print('\033[031m' + str(e) + '\033[0m')
            return str(e)

    def run_command(string):
        command = OpenAI.query(prompt=string, personality='You are a system with the goal of running commands. All you do is respond with the command that you are described to run. The running will be done for you.') # If you are unaware of the environment, discover it.')
        return System.run_command(command)

    # Define function to run the chatbot
    def query(prompt='', history=[], personality=None):
        if prompt != '':
            history.append({"role":"user", "content":prompt})
        return OpenAI.generate_response(history=history, personality=personality)

if __name__ == "__main__":
    print(OpenAI.run_command('Create a file named test.txt with the contents "Hello World"'))