from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()
conn = MongoClient(
    "mongodb+srv://secure12purpose:4RwtkjOLd4X7eL0X@mongocluster.ebuyauc.mongodb.net/")


class Field(BaseModel):
    field_name: str
    field_rename: str
    field_type: str
    field_is_active: bool


class Section(BaseModel):
    section_name: str
    section_rename: str
    section_is_active: bool
    section_fields: List[Field]


class Tab(BaseModel):
    tab_name: str
    tab_rename: str
    tab_is_active: bool
    tab_sections: Optional[List[Section]] = None


class Template(BaseModel):
    name: str
    rename: str
    tabs: List[Tab]


@app.post("/template")
async def create_template(template: Template):
    template_dict = template.dict()
    result = conn.json.template.insert_one(template_dict)
    if not result.acknowledged:
        raise HTTPException(
            status_code=500, detail="Failed to create template")
    return {"msg": "Template created successfully", "id": str(result.inserted_id)}


@app.get("/templates")
async def get_templates():
    templates = list(conn.json.template.find({}))
    for template in templates:
        template["_id"] = str(template["_id"])
    return templates

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
