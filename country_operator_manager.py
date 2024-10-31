from fastapi import HTTPException, Depends
from routes import APIRouter
from pydantic import BaseModel
import os
from auth import get_current_user

countryApp = APIRouter()
PROGRAMS_DIR = './TestingPrograms'


class Program(BaseModel):
    filename: str
    content: str


@countryApp.post("/program", dependencies=[Depends(get_current_user)])
def create_program(program: Program):
    file_path = os.path.join(PROGRAMS_DIR, program.filename)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="File already exists")

    with open(file_path, 'w') as f:
        f.write(program.content)
    return {"message": "File created successfully"}


@countryApp.get("/program/{filename}", dependencies=[Depends(get_current_user)])
def read_program(filename: str):
    file_path = os.path.join(PROGRAMS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, 'r') as f:
        content = f.read()
    return {"filename": filename, "content": content}


@countryApp.put("/program/{filename}", dependencies=[Depends(get_current_user)])
def update_program(filename: str, program: Program):
    file_path = os.path.join(PROGRAMS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, 'w') as f:
        f.write(program.content)
    return {"message": "File updated successfully"}


@countryApp.delete("/program/{filename}", dependencies=[Depends(get_current_user)])
def delete_program(filename: str):
    file_path = os.path.join(PROGRAMS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted successfully"}


@countryApp.get("/programs", dependencies=[Depends(get_current_user)])
def list_programs():
    programs = os.listdir(PROGRAMS_DIR)
    return {"programs": programs}