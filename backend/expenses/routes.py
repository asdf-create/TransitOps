from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List

from database.connection import get_session
from expenses.models import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseCategory
from expenses.service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate, 
    session: Session = Depends(get_session)
):
    service = ExpenseService(session)
    try:
        return service.create_expense(expense_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    vehicle_id: Optional[int] = None,
    trip_id: Optional[int] = None,
    category: Optional[ExpenseCategory] = None,
    session: Session = Depends(get_session)
):
    service = ExpenseService(session)
    return service.get_expenses(skip, limit, vehicle_id, trip_id, category)

@router.get("/vehicle/{vehicle_id}/cost")
def get_vehicle_operational_cost(vehicle_id: int, session: Session = Depends(get_session)):
    service = ExpenseService(session)
    return service.get_vehicle_operational_cost(vehicle_id)

@router.get("/fleet/cost")
def get_fleet_operational_cost(session: Session = Depends(get_session)):
    service = ExpenseService(session)
    return service.get_fleet_operational_cost()

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, session: Session = Depends(get_session)):
    service = ExpenseService(session)
    expense = service.get_expense(expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    session: Session = Depends(get_session)
):
    service = ExpenseService(session)
    expense = service.update_expense(expense_id, expense_data)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, session: Session = Depends(get_session)):
    service = ExpenseService(session)
    if not service.delete_expense(expense_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return {"message": "Expense deleted successfully"}
