from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_database_session
from app.models.recipe import RecipeModel, IngredientModel
from app.schemas.recipe import RecipeCreate, RecipeResponse

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_new_recipe(recipe_payload: RecipeCreate, db_session: Session = Depends(get_database_session)):
    # Se extraen los ingredientes del payload validado antes de crear el modelo principal
    ingredients_payload = recipe_payload.ingredients
    
    # Se instancia el modelo ORM de la receta omitiendo la lista de ingredientes
    recipe_attributes = recipe_payload.model_dump(exclude={"ingredients"})
    new_recipe = RecipeModel(**recipe_attributes)
    
    db_session.add(new_recipe)
    db_session.flush() # flush asigna un ID a new_recipe sin cerrar la transaccion
    
    # Se construyen y asocian los ingredientes utilizando el ID generado
    for ingredient_item in ingredients_payload:
        new_ingredient = IngredientModel(
            **ingredient_item.model_dump(),
            recipe_id=new_recipe.id
        )
        db_session.add(new_ingredient)
        
    db_session.commit()
    db_session.refresh(new_recipe)
    
    return new_recipe

@router.get("/", response_model=List[RecipeResponse])
def get_all_recipes(db_session: Session = Depends(get_database_session)):
    recipes_collection = db_session.query(RecipeModel).all()
    return recipes_collection

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(recipe_id: int, db_session: Session = Depends(get_database_session)):
    target_recipe = db_session.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    
    if not target_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La receta solicitada no existe en la base de datos."
        )
        
    return target_recipe