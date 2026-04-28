# Competency 2 — Code Literacy and Documentation (Week 4)

**Course definition:** *“Code Literacy and Documentation. Reading code well enough to explain what it does, change it when needed, and document it so someone else -- or future you -- can follow it. This icludes inine comments, docstrings, commit messages, and README content.”*

## Claim
For this assignment, I added several inline comments throughout the code to
explain what the endpoint returned, what parameters I used, and what the key
meant in my code. Overall, this script is meant to use an API from the U.S. Department of Education to create a CSV report of the top 50 colleges in Washington state based on their enrollment size. 

Endpoint: I used the Base URL (Line 13) provided by the U.S. Department of Education: https://api.data.gov/ed/collegescorecard/v1/schools. This served as my endpoint, which can be modified to include later set parameters in my code. The endpoint returns JSON with a list of records to return in the form of results, with items within the results that contain school metadata (as defined in parameters). In short, the endpoint provides a small report about the schools in the API using a set of parameters defined in the script.

Parameters: To add parameters, I modified the base URL endpoint to search for 
specific types of information amongst the data the U.S. Department of Education
provides. This occurs in lines 37-42, where parameters such as school.state were used to parse the data for schools only in Washington state. Overall, parameters were set to create a report that would capture the top 50 colleges in Washington state in terms of enrollment size, which required using the following parameters to pull data: school.state, fields (id, school name, school.city latest.student.size), and sort. Each school in the report would contain the school name, their school id, enrollment size, city, and state. 

Key meaning: The key in my code (held in key.env) was used to access the API and its associated data. This was accessed through a variable name set called DATA_GOV_API_KEY, which hosted the key after it was read from load_key_env_file() in line 46. 

