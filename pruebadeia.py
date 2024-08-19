from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import google.generativeai as genai
import requests
from urllib3.exceptions import InsecureRequestWarning
from supabase import create_client, Client
import uvicorn

app = FastAPI()

API_KEY = "AIzaSyA_ByC3rvWhv8zCECdmxiZPIrCMZfqTdeY"
genai.configure(api_key=API_KEY)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url: str = "https://segwpauegxdqyfolvqrd.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNlZ3dwYXVlZ3hkcXlmb2x2cXJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyMjQxMzQsImV4cCI6MjAzMTgwMDEzNH0.8V-VAfb2983I8RkqEPHc5t7YyxbbBFbbjZb2eCnEGRE"
supabase: Client = create_client(url, key)

@app.post('/process')
async def process_content(request: Request):
    content = await request.json()
    url = content.get('url')
    
    def get_html_from_url(url):
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                return f"Error al obtener HTML: {response.status_code}"
        except Exception as e:
            return f"Error al obtener HTML: {e}"
    
    html_content = get_html_from_url(url)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(["Knowing the HTML i provide you, can you give me the classname of the SIGN IN clickable? ONLY GIVE ME THE CLASSNAME, NOTHING ELSE", html_content])
    content_classname = response.text.strip()
    
    def check_value_exists(content: str) -> bool:
        response = supabase.table("content").select("*").eq("content", content).execute()
        return bool(response.data)
    
    check = check_value_exists(content_classname)
    if not check:
        cont = supabase.table("content").insert({"content": content_classname}).execute()
        return JSONResponse(content={"status": "inserted", "data": cont.data}, status_code=200)
    else:
        cont = supabase.table("content").select("*").eq("content", content_classname).execute()
        return JSONResponse(content={"status": "exists", "data": cont.data}, status_code=200)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=10000)
