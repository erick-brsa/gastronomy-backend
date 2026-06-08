from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_database_session
from app.models.recipe import RecipeModel, IngredientModel
from app.schemas.recipe import RecipeCreate, RecipeResponse

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_new_recipe(recipe_payload: RecipeCreate, db_session: AsyncSession = Depends(get_database_session)):
    # Se extraen los ingredientes del payload validado antes de crear el modelo principal
    ingredients_payload = recipe_payload.ingredients
    
    # Se instancia el modelo ORM de la receta omitiendo la lista de ingredientes
    recipe_attributes = recipe_payload.model_dump(exclude={"ingredients"})
    new_recipe = RecipeModel(**recipe_attributes)
    
    db_session.add(new_recipe)
    await db_session.flush() # flush asigna un ID a new_recipe sin cerrar la transaccion
    
    created_ingredients = []
    
    # Se construyen y asocian los ingredientes utilizando el ID generado
    for ingredient_item in ingredients_payload:
        new_ingredient = IngredientModel(
            **ingredient_item.model_dump(),
            recipe_id=new_recipe.id
        )
        db_session.add(new_ingredient)
        created_ingredients.append(new_ingredient)
        
    await db_session.commit()
    
    query_recipe = select(RecipeModel).options(selectinload(RecipeModel.ingredients)).filter(RecipeModel.id == new_recipe.id)
    query_result = await db_session.execute(query_recipe)
    populated_recipe = query_result.scalars().first()
    
    return populated_recipe

@router.get("/", response_model=List[RecipeResponse])
async def get_all_recipes(db_session: AsyncSession = Depends(get_database_session)):
    query = select(RecipeModel).options(selectinload(RecipeModel.ingredients))
    result = await db_session.execute(query)
    recipes_collection = result.scalars().all()
    return recipes_collection

@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe_by_id(recipe_id: int, db_session: AsyncSession = Depends(get_database_session)):
    query = select(RecipeModel).options(selectinload(RecipeModel.ingredients)).filter(RecipeModel.id == recipe_id)
    result = await db_session.execute(query)
    target_recipe = result.scalars().first()
    
    if not target_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La receta solicitada no existe en la base de datos."
        )
        
    return target_recipe