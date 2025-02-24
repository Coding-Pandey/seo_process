# from chatbot import PROMPT, query_llm, prompt_keyword_suggestion, query_keyword_suggestion
import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from clustering_pipeline.k_mean import ClusteringConfig, Cluster 
import json
from Agents.Keyword_agent import query_keyword_suggestion,query_keywords_description
from Agents.clusterURL_keyword import url_agent
from prompts.keywords_prompt import prompt_keyword,prompt_keyword_suggestion
from collections import defaultdict
from utiles import flatten_seo_data , extract_first_json_object
app = FastAPI()

def extract_keywords(json_string):
    """Validate JSON and extract 'keywords' list if present."""
    try:
        parsed_json = json.loads(json_string)  # Try parsing JSON
        if "keywords" in parsed_json and isinstance(parsed_json["keywords"], list):
            return True, parsed_json["keywords"]  #  Return keywords if valid
        else:
            return False, "'keywords' field is missing or not a list."
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"  #  Return JSON parsing error

# Define tool function for getting current time
def Seo_keyword_search(keywords: list ) -> str:
    # Lod CSV file
    csv_file = r"C:\Users\nickc\OneDrive\Desktop\SEO\data\input test 2 - input test 2.csv"  # Replace with your file path
    df = pd.read_csv(csv_file)
    # Convert DataFrame to JSON
    json_data = df.to_json(orient="records", indent=4)
    return json_data    


#  Define input model with at least one required field
class KeywordRequest(BaseModel):
    keywords: Optional[str] = None
    description: Optional[str] = None

    def validate(self):
        if not self.keywords and not self.description:
            raise ValueError("At least one of 'keywords' or 'description' must be provided")
        


@app.post("/generate_keywords")
def generate_keywords(request: KeywordRequest):
    try:
        request.validate()
        keyword_json = query_keywords_description(prompt_keyword, request.keywords, request.description)
        # print(result)
        keyword = extract_keywords(str(keyword_json))
       
        if keyword:
            result = Seo_keyword_search(keywords=keyword)
            return result
        else:
            return keyword
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing request")
    

@app.post("/keyword_suggestion")
def keyword_suggestion(request: KeywordRequest):
    try:
        request.validate()
        keyword_json = query_keyword_suggestion(prompt_keyword_suggestion, request.keywords, request.description)
        print(keyword_json)
        # print(result)
        keyword = extract_keywords(keyword_json)
        if keyword:
            return keyword
        else:
            return "Could you retry"
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing request")    
    

@app.post("/keyword_clustering")
def keyword_clustering(file: UploadFile = File(...)):
    try:

        # file_contents = file.file.read()
        # print("File contents:", file_contents)  
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension == "csv":
            df = pd.read_csv(file.file)
        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV or Excel file.")
        
        data = df.to_dict(orient="records")

        # try:
        #     data = json.loads(data.decode("utf-8"))
        # except json.JSONDecodeError as e:
        #     raise HTTPException(status_code=400, detail="Invalid JSON file format")

        # # Validate the structure of the data
        # if not isinstance(data, list):
        #     raise HTTPException(status_code=400, detail="JSON must contain a list of records")

        print("Parsed data:", data)  

        config = ClusteringConfig(min_clusters=4, max_clusters=20, random_state=42)
        clusterer = Cluster(config)
        metadata_column = "Keyword"
  
        results, optimal_cluter = clusterer.process_clustering(data, metadata_column)
        # print(results)
        print(optimal_cluter)
        results = json.loads(results)

        clusters = defaultdict(list)

        for item in results:
            if "cluster" in item:  
                cluster_id = item["cluster"]
                clusters[cluster_id].append(item)

            else:
                return HTTPException(status_code=500, detail="cluster not found")    
        
        structured_data = []

        for cluster_id, items in clusters.items():
            structure = url_agent(items=items)
            json_data = extract_first_json_object(str(structure))
            print(json_data)
            structured_data.append(json_data)
        
        print(structured_data)
        # structure_json = json.loads(structured_data)
        final_data = flatten_seo_data(structured_data)
        print(final_data)

        return final_data


    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing request")   