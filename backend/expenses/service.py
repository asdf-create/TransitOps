from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, timezone

from database.models import Expense, Vehicle, Trip
from expenses.models import ExpenseCreate, ExpenseUpdate, ExpenseCategory

class ExpenseService:
    def __init__(self, session: Session):
        self.session = session

    def create_expense(self, expense_data: ExpenseCreate) -> Expense:
        # Validate vehicle if provided
        if expense_data.vehicle_id:
            vehicle = self.session.get(Vehicle, expense_data.vehicle_id)
            if not vehicle:
                raise ValueError("Vehicle not found")
        
        # Validate trip if provided
        if expense_data.trip_id:
            trip = self.session.get(Trip, expense_data.trip_id)
            if not trip:
                raise ValueError("Trip not found")
        
        db_expense = Expense.model_validate(expense_data)
        if not db_expense.expense_date:
            db_expense.expense_date = datetime.now(timezone.utc)
        
        self.session.add(db_expense)
        self.session.commit()
        self.session.refresh(db_expense)
        return db_expense

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        return self.session.get(Expense, expense_id)

    def get_expenses(
        self, 
        skip: int = 0, 
        limit: int = 100,
        vehicle_id: Optional[int] = None,
        trip_id: Optional[int] = None,
        category: Optional[ExpenseCategory] = None
    ) -> List[Expense]:
        query = select(Expense)
        
        if vehicle_id:
            query = query.where(Expense.vehicle_id == vehicle_id)
        if trip_id:
            query = query.where(Expense.trip_id == trip_id)
        if category:
            query = query.where(Expense.category == category)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update_expense(self, expense_id: int, expense_data: ExpenseUpdate) -> Optional[Expense]:
        db_expense = self.get_expense(expense_id)
        if not db_expense:
            return None
        
        expense_data_dict = expense_data.model_dump(exclude_unset=True)
        for key, value in expense_data_dict.items():
            setattr(db_expense, key, value)
        
        self.session.add(db_expense)
        self.session.commit()
        self.session.refresh(db_expense)
        return db_expense

    def delete_expense(self, expense_id: int) -> bool:
        db_expense = self.get_expense(expense_id)
        if not db_expense:
            return False
        
        self.session.delete(db_expense)
        self.session.commit()
        return True

    def get_vehicle_operational_cost(self, vehicle_id: int) -> dict:
        expenses = self.session.exec(
            select(Expense).where(Expense.vehicle_id == vehicle_id)
        ).all()
        
        if not expenses:
            return {"total_cost": 0, "by_category": {}}
        
        total_cost = sum(exp.amount for exp in expenses)
        by_category = {}
        
        for category in ExpenseCategory:
            category_expenses = [exp for exp in expenses if exp.category == category]
            by_category[category.value] = sum(exp.amount for exp in category_expenses)
        
        return {
            "total_cost": total_cost,
            "by_category": by_category
        }

    def get_fleet_operational_cost(self) -> dict:
        expenses = self.session.exec(select(Expense)).all()
        
        if not expenses:
            return {"total_cost": 0, "by_category": {}}
        
        total_cost = sum(exp.amount for exp in expenses)
        by_category = {}
        
        for category in ExpenseCategory:
            category_expenses = [exp for exp in expenses if exp.category == category]
            by_category[category.value] = sum(exp.amount for exp in category_expenses)
        
        return {
            "total_cost": total_cost,
            "by_category": by_category
        }
