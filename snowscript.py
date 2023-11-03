import requests 
import json 
# Replace with your ServiceNow instance URL and API credentials 
url = 'https://dev142790.service-now.com/api/now/table/sc_req_item' 
username = 'admin' 
password = os.environ.get('PASSWORD')
# Define your query to filter by approved RITMs 
query = 'approval=approved' 
# Make an API request to ServiceNow to retrieve approved RITMs 
response = requests.get(url, verify=False, auth=(username, password), params={'sysparm_query': query}) 
if response.status_code == 200: # Parse the JSON response 
    data = response.json() # Define your substitution variables 
    
    substitution_variables = { 
                              "short_description": "junk", 
                              "variable2": "replacement2", 
                              # Add more variables as needed 
                              } 
    # Function to perform variable substitution 
    def substitute_variables(data, variables): 
        if isinstance(data, dict): 
            for key, value in data.items(): 
                if isinstance(value, str): 
                    for var, replacement in variables.items(): 
                        value = value.replace(var, replacement) 
                        print(value)
                    data[key] = value 
                elif isinstance(value, (dict, list)): 
                    substitute_variables(value, variables) 
        elif isinstance(data, list): 
            for item in data: 
                substitute_variables(item, variables) 
    
    # Perform variable substitution for each RITM 
    for ritm in data.get('result', []): 
        #print("RIMT DATA OUT")
        #print(ritm)
        substitute_variables(ritm, substitution_variables) 
    # Now 'data' contains the substituted values for approved RITMs 
    print(json.dumps(data, indent=2)) 
else: print(f"Failed to retrieve data. Status code: {response.status_code}")
