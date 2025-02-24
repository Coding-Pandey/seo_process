import pandas as pd
import json

def flatten_seo_data(json_data):
    # Initialize lists to store flattened data
    flattened_data = []
    
    for page in json_data:
        # Get the base page information
        page_title = page['Page Title']
        intent = page['Intent']
        url = page['Suggested URL Structure']
        
        # For each keyword in the page
        for keyword in page['Keywords']:
            # Get the monthly search volume for this keyword
            search_volume = page['Monthly Search Volume'].get(keyword, 0)
            
            # Create a row for this keyword
            row = {
                'page_title': page_title,
                'keyword': keyword,
                'monthly_search_volume': search_volume,
                'intent': intent,
                'url_structure': url
            }
            
            flattened_data.append(row)
    
    # return pd.DataFrame(flattened_data)
    return flattened_data



def extract_first_json_object(text):
    """
    Extracts the first complete JSON object from `{` to `}` found in the input text.

    Args:
        text (str): The input text containing JSON data.

    Returns:
        dict: The extracted JSON object as a dictionary, or None if no valid JSON is found.
    """
    brace_count = 0
    json_str = ""
    start_index = None

    for i, char in enumerate(text):
        if char == "{":
            if brace_count == 0:
                start_index = i  # Mark the beginning of the JSON object
            brace_count += 1
        elif char == "}":
            brace_count -= 1
        
        if brace_count > 0 or (brace_count == 0 and start_index is not None):
            json_str += char
        
        if brace_count == 0 and start_index is not None:
            break  # Stop when the first valid JSON object is found

    if json_str:
        try:
            return json.loads(json_str)  # Convert to dictionary
        except json.JSONDecodeError:
            return None  # Return None if JSON parsing fails

    return None  # Return None if no valid JSON object is found