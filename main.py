# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
import uvicorn
from routes import router as process_router
from process_manager import process_manager_app
from country_operator_manager import countryApp


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


app = FastAPI()
app.include_router(process_router)
app.include_router(process_manager_app)
app.include_router(countryApp)


@app.get("/")
def read_root():
    return {"message": "Welcome to sms management system!"}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=7000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/