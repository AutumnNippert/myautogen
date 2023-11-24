import api

goal = input("Set the goal >>> ")
history = []

"""
Until the goal is reached, run the agent
"""
while True:
    # Generate the response
    response = api.OpenAI.query(prompt=goal, history=history, personality="""
                                You are a system that has a task to complete.
                                You have another instance of ChatGPT to query and run commands to be able to accomplish your task.
                                If your goal has been reached, write only GOAL_REACHED.
                                If you want to run a command, write only RUN_COMMAND: <command>.
                                The commands after "QUERY_COMMAND:" can be interpreted by the command runner, so plain english works.
                                don't forget you can do things like ls, mkdir, etc. to navigate the filesystem.
                                You CANNOT use the cd command though
                                Finally, write only GOAL_REACHED or FAILED to end the conversation, when you think you can't do anything else.""")
    # If the response is an error, print it and exit
    if response.startswith('\033[031m'):
        print(response)
        exit()

    # Print the response
    print(response)

    # Add the response to the history
    history.append({"role":"system", "content":response})

    for line in response.splitlines():
        if response == 'GOAL_REACHED' or response == 'FAILED':
            exit()
        if line.startswith('RUN_COMMAND: '):
            command = line.replace('RUN_COMMAND: ', '')
            output = api.System.run_command(command)
            print(output)
            history.append({"role":"system", "content":"OUTPUT: " + output})
        elif line.startswith('QUERY_COMMAND: '):
            command = line.replace('QUERY_COMMAND: ', '')
            output = api.OpenAI.run_command(command)
            print(output)
            history.append({"role":"system", "content":"OUTPUT: " + output})