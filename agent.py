import api

goal = input("Set the goal >>> ")
goal = "GOAL: " + goal
history = []

"""
Until the goal is reached, run the agent
"""
while True:
    # Generate the response
    response = api.OpenAI.query(prompt=goal, history=history, personality="""
                                You are a system that has a task to complete.
                                If you want to run a command, write only RUN_COMMAND: <command>.
                                The commands after "QUERY_COMMAND:" can be interpreted by the command runner, so plain english works.
                                If you want to ask the user for input, write only ASK_USER: <prompt>.
                                don't forget you can do things like ls, mkdir, etc. to navigate the filesystem.
                                You CANNOT use the cd command though!
                                After you think you have completed the goal, write GOAL_REACHED.
                                If you think you can't complete the goal, write FAILED.""")
    # If the response is an error, print it and exit
    if response.startswith('\033[031m'):
        print(response)
        exit()

    # Print the response
    print(response)

    # Add the response to the history

    for line in response.splitlines():
        if line.startswith('GOAL_REACHED') or line.startswith('FAILED'):
            exit()
        if line.startswith('RUN_COMMAND: '):
            command = line.replace('RUN_COMMAND: ', '')
            history.append({"role":"system", "content":response})
            output = api.System.run_command(command)
            print(output)
            history.append({"role":"user", "content":"OUTPUT: " + output})
        elif line.startswith('ASK_USER: '):
            command = line.replace('ASK_USER: ', '')
            history.append({"role":"system", "content":response})
            output = input('>>> ' + command)
            print(output)
            history.append({"role":"user", "content":"USER_INPUT: " + output})
        elif line.startswith('QUERY_COMMAND: '):
            command = line.replace('QUERY_COMMAND: ', '')
            history.append({"role":"system", "content":response})
            output = api.OpenAI.run_command(command)
            print(output)
            history.append({"role":"user", "content":"OUTPUT: " + output})
        # print(history)