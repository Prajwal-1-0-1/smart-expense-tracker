from fastapi import APIRouter, Depends, UploadFile, File,HTTPException
from app.database import engine,SessionLocal
from app.models import Base,Expense, User
from app.auth import get_current_user, oauth2_scheme
from app.services.gemini_service import parse_receipt
from app.services.normalize import normalize_merchant, normalize_category
from app.schemas import ExpenseCreate, ExpenseUpdate
import os



router = APIRouter(prefix="/crud", tags=["crud"])
os.makedirs("uploads", exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...),current_user: User = Depends(get_current_user),db: SessionLocal = Depends(get_db)):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())



    try:
        receipt_data = parse_receipt(filepath)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
    

    if not receipt_data["merchant"] or not receipt_data["amount"]:
        raise HTTPException(400,"Receipt invalid")
    
    if not receipt_data["category"] or not receipt_data["purchase_date"]:
        raise HTTPException(400,"Receipt invalid")
    
    receipt_data["merchant"] = normalize_merchant(db, receipt_data["merchant"], current_user.id)
    receipt_data["category"] = normalize_category(db, receipt_data["category"], current_user.id)
    
    expense = Expense(
    merchant=receipt_data["merchant"],
    amount=receipt_data["amount"],
    category=receipt_data["category"],
    purchase_date=receipt_data["purchase_date"],
    user_id=current_user.id
    )

    

    db.add(expense)
    db.commit()
    db.refresh(expense)
 
    return {"message" : "Receipt uploaded successfully", "expense" : expense}





@router.post("/add-expense")
def add_expense(expense_data: ExpenseCreate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    merchant = normalize_merchant(db, expense_data.merchant, current_user.id)
    category = normalize_category(db, expense_data.category, current_user.id)

    expense = Expense(
        merchant=merchant,
        amount=expense_data.amount,
        category=category,
        purchase_date=expense_data.purchase_date,
        user_id=current_user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {"message": "Expense added successfully", "expense": expense}


@router.get("/get_expenses")
def get_expenses(current_user: User = Depends(get_current_user),db: SessionLocal = Depends(get_db)):

    

    expenses = db.query(Expense).filter(
               Expense.user_id == current_user.id,
               ).all()
    

    return expenses




@router.get("/get_expense/{id}")
def get_expense(id: int, current_user: User = Depends(get_current_user),db: SessionLocal = Depends(get_db)):

    expense = db.query(Expense).filter(
            Expense.id == id,
            Expense.user_id == current_user.id
            ).first()
    


    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return expense





@router.delete("/delete_expenses/{id}")
def delete_expense(id: int,current_user: User = Depends(get_current_user),db: SessionLocal = Depends(get_db)):

    expense = db.query(Expense).filter(
                Expense.id == id,
                Expense.user_id == current_user.id
            ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()


    return {"message": "Expense deleted successfully"}




@router.put("/update_expense/{id}")
def update_expense(id: int,expense: ExpenseUpdate,current_user: User = Depends(get_current_user),db: SessionLocal = Depends(get_db)):
    exp = db.query(Expense).filter(
        Expense.id == id,
        Expense.user_id == current_user.id
    ).first()

    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")

    exp.merchant = expense.merchant
    exp.amount = expense.amount
    exp.category = expense.category
    exp.purchase_date = expense.purchase_date

    db.commit()
    db.refresh(exp)

    return {"message": "Expense updated successfully","expense": exp}
    

