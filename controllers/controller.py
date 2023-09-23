from fastapi import HTTPException
from fastapi import APIRouter, HTTPException
from MongoDB.mongo_connection import db
from models.model import Employee

router = APIRouter()


@router.post("/create_employee/")
async def create_item(employee: Employee):
    """
    Create a new employee.

    Args:
        employee (Employee): The employee details to be created.

    Returns:
        dict: A JSON response with a message indicating the creation status.
    """

    # Check if the email already exists in the database
    existing_employee = db.items.find_one({"email": employee.email})
    if existing_employee:
        raise HTTPException(
            status_code=400, detail="Email Address already exists")

    # If the email doesn't exist, insert the new employee
    result = db.items.insert_one(employee.dict())
    inserted_employee = db.items.find_one({"email": employee.email})
    print(inserted_employee)
    inserted_email = str(inserted_employee['email'])
    return {"message": f"Employee with email {inserted_email} has been created."}


@router.get("/get_all_employees/")
async def get_all_employees():
    """
    Get a list of all employees.

    Returns:
        list: A list of employee records as JSON objects.
    """

    # Query the database to retrieve all employees
    employees = list(db.items.find({}))

    # If no employees are found, return an empty list
    if not employees:
        return []

    # Convert ObjectId to string for serialization (if needed)
    for employee in employees:
        employee["_id"] = str(employee["_id"])

    return employees


@router.get("/get_employee_by_email/")
async def get_employee_by_email(email: str):
    """
    Get an employee by email.

    Args:
        email (str): The email address of the employee to retrieve.

    Returns:
        dict: The employee record as a JSON object.
    """

    # Query the database to retrieve an employee by email
    employee = db.items.find_one({"email": email})

    # If no employee is found, return a 404 Not Found response
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Convert ObjectId to string for serialization (if needed)
    employee["_id"] = str(employee["_id"])

    return employee


@router.put("/update_employee_by_email/")
async def update_employee_by_email(email: str, updated_employee: Employee):
    """
    Update an employee by email.

    Args:
        email (str): The email address of the employee to update.
        updated_employee (Employee): The updated employee details.

    Returns:
        dict: A JSON response with a message indicating the update status.
    """

    # Check if the email exists in the database
    existing_employee = db.items.find_one({"email": email})
    if not existing_employee:
        raise HTTPException(
            status_code=404, detail="Employee not found")

    # Ensure that the updated_employee's email is the same as the existing email
    if updated_employee.email != email:
        raise HTTPException(
            status_code=400, detail="Email cannot be changed")

    # # Convert the ObjectId to a string if it exists
    existing_employee_id = existing_employee.get('_id')
    if existing_employee_id:
        existing_employee_id = str(existing_employee_id)

    # # Remove the _id field from the updated_employee dictionary
    updated_employee_dict = updated_employee.dict()
    updated_employee_dict.pop('_id', None)

    # # Update the employee with the provided email
    db.items.update_one(
        {"email": email},
        {"$set": updated_employee_dict}
    )

    # # Retrieve the updated employee from the database (optional)
    updated_employee_doc = db.items.find_one({"email": email})
    updated_employee_doc.pop('_id', None)
    print(updated_employee_doc)

    return {"message": f"Employee with email {email} has been updated.", "updated_employee": updated_employee_doc}


@router.delete("/delete_employee_by_email/")
async def delete_employee_by_email(email: str):
    """
    Delete an employee by email.

    Args:
        email (str): The email address of the employee to delete.

    Returns:
        dict: A JSON response with a message indicating the deletion status.
    """

    # Check if the email exists in the database
    existing_employee = db.items.find_one({"email": email})
    if not existing_employee:
        raise HTTPException(
            status_code=404, detail="Employee not found")

    # If the email exists, delete the employee
    db.items.delete_one({"email": email})

    return {"message": f"Employee with email {email} has been deleted."}
