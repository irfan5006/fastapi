from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")

def hello():
    return {"Message": "Patient Management System API"}

@app.get("/about")

def about():
    return {"Message":"This is a fully Functional API to manage your patient records."}


@app.get("/view")

def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")

def view_patient(patient_id: str = Path (..., description="ID of the Patient in DB"
                                        , example= "P001")):

    ### load data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient ID is not found.")

@app.get("/sort")

def sort_patient(sort_by: str = Query(..., 
                            description="sort on the basis of weight, height or bmi"),
                order: str = Query("Asc", 
                            description="Sort on the basis of ASC or DESC")):
    
    valid_fields = ["height","weight","bmi"]
    if sort_by  not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    
    if order  not in ["ASC","DESC"]:
        raise HTTPException(status_code=400, detail=f"Invalid Order select between ASC or DESC")
    

    data = load_data()
    sort_order = True if order=="DESC" else False
    sort_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sort_data