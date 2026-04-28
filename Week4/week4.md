# Competency 4 — APIs and Data Aquisition (Week 4)

**Course definition:** *“Pulling structured data from a web page API using Python. Reading API documentation to understand what endpoints exist, what parameters they take, and what the response looks like. Handling API keys safely- not committing them to a public repo.”*

## Claim
I called the College Scorecard API, hosted by the U.S. Department of Education, which required a key. The endpoint returns a list of the largest 50 colleges in Washington state based on their enrollment size. I filtered for colleges in Washington state and sorted by enrollment size, then added a max cap of 50 entries for the output. My week4.md explains further in depth the intent, endpoints, parameters, and how the key was maintained.

As someone who has been doing some local resource allocation for some recent volunteer work, I wanted to use this project as an opportunity to see how data could be used and structured for local governances to make decisions on resource allocation. This led me to choosing the Department of Education's API that contains lists of colleges in the US and their enrollment sizes, which represents impact, something that plays a major role in determining allocation. Overall, this script is meant to use an API from the U.S. Department of Education to create a CSV report of the top 50 colleges in Washington state based on their enrollment size, with the intent of this report to inform those interested on where the investment of educational resources may have the most widespread impact.

Endpoint: I used the Base URL (Line 13) provided by the U.S. Department of Education: https://api.data.gov/ed/collegescorecard/v1/schools. This served as my endpoint, which can be modified to include later set parameters in my code. The endpoint returns JSON with a list of records to return in the form of results, with items within the results that contain school metadata (as defined in parameters). In short, the endpoint provides a small report about the schools in the API using a set of parameters defined in the script.

Parameters: To add parameters, I modified the base URL endpoint to search for 
specific types of information amongst the data the U.S. Department of Education
provides. This occurs in lines 37-42, where parameters such as school.state were used to parse the data for schools only in Washington state. Overall, parameters were set to create a report that would capture the top 50 colleges in Washington state in terms of enrollment size, which required using the following parameters to pull data: school.state, fields (id, school name, school.city latest.student.size), and sort. Each school in the report would contain the school name, their school id, enrollment size, city, and state. 

Key meaning: The key in my code (held in key.env) was used to access the API and its associated data. This was accessed through a variable name set called DATA_GOV_API_KEY, which hosted the key after it was read from load_key_env_file() in line 46. This was all done to ensure that my personal key would not be published to my script code and github, ensuring it stays local only to my files and use. 

