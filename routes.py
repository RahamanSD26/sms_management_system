from fastapi import APIRouter, HTTPException, status, Depends, Request
from process_manager import stop_process, restart_process
from models import Token, authenticate_user, create_access_token, User,pwd_context, user_collection, LoginRequest
from datetime import timedelta
from config.mongoConfig import ACCESS_TOKEN_EXPIRE_MINUTES
from auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def index_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )


@router.post("/stop/{program_name}/{country_operator}", dependencies=[Depends(get_current_user)])
def stop_sms_program(program_name: str, country_operator: str):
    result = stop_process(program_name)
    # Check if there was an error in stopping the program
    if "error" in result:  # This checks if the result contains an error key
        raise HTTPException(status_code=400, detail=result["error"])  # Use the error message from the result
    return result


@router.post("/restart/{program_name}/{country_operator}", dependencies=[Depends(get_current_user)])
def restart_sms_program(program_name: str, country_operator: str):
    result = restart_process(program_name)
    if "error" in result:  # This checks if the result contains an error key
        raise HTTPException(status_code=400, detail=result["error"])  # Use the error message from the result
    return result


# @router.post("/login", response_model=Token)
# async def login_for_access_token(username: str, password: str):
#     user = authenticate_user(username, password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_for_access_token(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected", response_model=User)
async def protected_route(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token")
async def login():
    # Authenticate the user and return a token
    return {"access_token": Token.access_token, Token.token_type: "bearer"}


@router.post("/register", response_model=User)
async def register_user(username: str, password: str, full_name: str | None = None):
    hashed_password = pwd_context.hash(password)
    user = {
        "username": username,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "disabled": False
    }
    user_collection.insert_one(user)
    return User(**user)



#
# @router.post("/program", response_model=Program)
# async def create_program(program: ProgramCreate):
#     if programs_collection.find_one({"filename": program.filename}):
#         raise HTTPException(status_code=409, detail="File already exists.")
#
#     program_data = {
#         "filename": program.filename,
#         "content": program.content,
#     }
#
#     result = programs_collection.insert_one(program_data)
#     program_data["_id"] = str(result.inserted_id)
#     return program_data
#
#
# @router.get("/program/{filename}", response_model=Program)
# async def read_program(filename: str):
#     program = programs_collection.find_one({"filename": filename})
#
#     if not program:
#         raise HTTPException(status_code=404, detail="File not found.")
#
#     program["id"] = str(program["_id"])
#     return program
#
#
# @router.put("/program/{filename}", response_model=Program)
# async def update_program(filename: str, program_update: ProgramCreate):
#     result = programs_collection.update_one(
#         {"filename": filename},
#         {
#             "$set": {
#                 "content": program_update.content,
#             }
#         }
#     )
#
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="File not found.")
#
#     updated_program = programs_collection.find_one({"filename": filename})
#     updated_program["id"] = str(updated_program["_id"])
#     return updated_program
#
#
# @router.delete("/program/{filename}")
# async def delete_program(filename: str):
#     result = programs_collection.delete_one({"filename": filename})
#
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="File not found.")
#
#     return {"message": "File deleted successfully."}
#
#
# @router.get("/programs", response_model=List[Program])
# async def list_programs():
#     programs = programs_collection.find()
#     program_list = [
#         {
#             "id": str(program["_id"]),
#             "filename": program["filename"],
#             "content": program["content"],
#             "created_at": program["created_at"],
#             "updated_at": program["updated_at"]
#         }
#         for program in programs
#     ]
#     return program_list




