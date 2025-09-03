from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from controller_v1 import route_query_stream, route_query
import uuid
import time
import re
import os
# from prettytable import PrettyTable
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

## Added 05-08
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials = True,
    allow_methods =['*'],
    allow_headers = ['*'],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# ────────────────────────────────────────────────────────────────────────────────
# Glossary Abbreviation Expanded
# ────────────────────────────────────────────────────────────────────────────────
def expand_abbreviations(text):
    glossary_path = "data/glossary_final.md"
    if not os.path.exists(glossary_path):
        return text

    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary = f.read()

    glossary_pairs = re.findall(r"\*\*(.*?)\*\* — (.*)", glossary)
    abbreviation_map = {abbr.strip(): desc.strip() for abbr, desc in glossary_pairs}

    for abbr, full in abbreviation_map.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        replacement = f"{abbr} ({full})"
        text = re.sub(pattern, replacement, text)

    return text

# ────────────────────────────────────────────────────────────────────────────────
# Format NADRA Center Output (location agent only)
# ────────────────────────────────────────────────────────────────────────────────
# def format_location_response(response):
#     table = PrettyTable()
#     table.field_names = ["Address", "Location", "Phone"]
#     for row in response.get("locations", []):
#         table.add_row([row["address"], row["location"], row["phone"]])
#     return table.get_string()

def format_locations(raw_text):
    # Split based on location index pattern (e.g., "1. ", "2. ", etc.)
    entries = re.split(r'(?=\d+\.\s)', raw_text)
    locations = []

    for entry in entries:
        if not entry.strip():
            continue
        
        # Extract index and label
        match = re.match(r'(\d+)\.\s+([^\n]+?)\s+Address:', entry)
        if not match:
            continue
        
        index = int(match.group(1))
        name = match.group(2).strip()

        # Extract Address
        address_match = re.search(r'Address:\s*(.+?)\s+Phone:', entry)
        address = address_match.group(1).strip() if address_match else ""

        # Extract Phone
        phone_match = re.search(r'Phone:\s*([^\s]+)', entry)
        phone = phone_match.group(1).strip() if phone_match else ""

        # Extract City
        city_match = re.search(r'City:\s*([^\s]+)', entry)
        city = city_match.group(1).strip() if city_match else ""

        locations.append({
            # "id": index,
            "Center Name": name,
            "Center Address": address,
            "Center Phone": phone,
            # "city": city
        })

    return locations

def format_location_response(response):
    raw_locations = format_locations(response.get("answer", ""))
    
    if not raw_locations:
        return "No locations found."

    formatted = ["Locations are:\n"]
    for loc in raw_locations:
        formatted.append(
            f"Center Name   : {loc['Center Name']}\n"
            f"Center Address: {loc['Center Address']}\n"
            f"Center Phone  : {loc['Center Phone']}\n"
        )

    return "\n".join(formatted)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ────────────────────────────────────────────────────────────────────────────────
# Sync API – used by frontend widgets or web dashboard
# ────────────────────────────────────────────────────────────────────────────────
@app.post("/ask")
async def ask(request: Request):
    start = time.time()
    data = await request.json()
    question = data.get("question", "").strip()
    request_id = str(uuid.uuid4())

    if not question:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "answer": "No question provided.",
                "request_id": request_id,
                "response_time": f"{(time.time() - start):.3f}s"
            }
        )

    try:
        response = await route_query(question)
        agent = response.get("agent", "agent_default")
        answer = response.get("answer", "No response.")

        if agent not in ["agent_location", "agent_documents", "agent_default"]:
            answer = expand_abbreviations(answer)
        elif "Locations" in response['answer']:
            answer = format_location_response(response)

        status = "success"

    except Exception as e:
        agent = "agent_default"
        answer = f"Exception: {str(e)}"
        status = "error"

    print(f"[LOG] {question} | Agent: {agent} | ReqID: {request_id} | Time: {(time.time() - start):.2f}s")

    return {
        "status": status,
        "answer": answer,
        # "request_id": request_id,
        "response_time": f"{(time.time() - start):.3f}s",
        # "agent": agent
    }

# ────────────────────────────────────────────────────────────────────────────────
# Streaming API – Real-time token output
# ────────────────────────────────────────────────────────────────────────────────
# @app.post("/stream")
# async def stream(request: Request):
#     data = await request.json()
#     question = data.get("question", "").strip()
#     request_id = str(uuid.uuid4())

#     if not question:
#         return JSONResponse(
#             status_code=400,
#             content={"error": "No question provided", "request_id": request_id}
#         )

#     async def streamer():
#         async for chunk in route_query_stream(question):
#             yield chunk

#     return StreamingResponse(streamer(), media_type="text/plain")

# ---------------------------------------------------------------------

@app.post("/stream")
async def stream(request: Request):
    try:
        data = await request.json()
    except json.JSONDecodeError as e:
        print("Invalid JSON data:", await request.body)
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    question = data.get("question", "").strip()
    request_id = str(uuid.uuid4())

    if not question:
        return JSONResponse(
            status_code=400,
            content={"error": "No question provided", "request_id": request_id}
        )

    async def streamer():
        try:
            full_answer = ""
            async for chunk in route_query_stream(question):
                full_answer += chunk
                yield chunk  # stream each token/word as it comes

            # After all tokens streamed, check if it's a location answer
            if "Locations for" in full_answer or re.search(r"\d+\.\s+.+Address:", full_answer):
                formatted = format_location_response({"answer": full_answer})
                yield formatted

        except Exception as e:
            print("Error during streaming:", str(e))
            yield f"\n\nError: {str(e)}"

    return StreamingResponse(streamer(), media_type="text/plain")



# async def stream(request: Request):
#     data = await request.json()
#     question = data.get("question", "").strip()
#     request_id = str(uuid.uuid4())

#     if not question:
#         return JSONResponse(
#             status_code=400,
#             content={"error": "No question provided", "request_id": request_id}
#         )

#     async def streamer():
#         try:
#             full_answer = ""
#             async for chunk in route_query_stream(question):
#                 full_answer += chunk
#                 yield chunk  # stream each token/word as it comes

#             # After all tokens streamed, check if it's a location answer
#             if "Locations for" in full_answer or re.search(r"\d+\.\s+.+Address:", full_answer):
#                 formatted = format_location_response({"answer": full_answer})
#                 yield formatted

#         except Exception as e:
#             yield f"\n\nError: {str(e)}"

#     return StreamingResponse(streamer(), media_type="text/plain")

# -----# --------------------------------------------------




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)


# ----------------------------------- Working Version 1.1 --------------------------------------------------------------

