import api

goal = input("Set the goal >>> ")
history = []

"""
Until the goal is reached, run the agent
"""
while True:
    # Generate the response
    response = api.OpenAI.query(prompt=goal, history=history, personality='You are a system that has a task to complete. You have another instance of ChatGPT to query and run commands to be able to accomplish your task. If your goal has been reached, write only GOAL_REACHED. If you want to run a command, write only RUN_COMMAND: <command>. The commands after "RUN_COMMAND:" can also be interpreted by the command runner, so plain english works as well.')
    # If the response is an error, print it and exit
    if response.startswith('\033[031m'):
        print(response)
        exit()

    # Print the response
    print(response)

    # Add the response to the history
    history.append({"role":"system", "content":response})

    # If the goal is reached, exit
    if response == 'GOAL_REACHED':
        exit()

    if response.startswith('RUN_COMMAND: '):
        command = response.replace('RUN_COMMAND: ', '')
        output = api.OpenAI.run_command(command)
        print(output)
        history.append({"role":"system", "content":output})