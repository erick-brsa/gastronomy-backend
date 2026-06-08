from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class IngredientBase(BaseModel):
    ingredient_name: str = Field(..., min_length=2, max_length=100)
    measurement_quantity: float = Field(..., gt=0.0)
    measurement_unit: str = Field(..., min_length=1, max_length=50)

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int
    recipe_id: int
    
    model_config = ConfigDict(from_attributes=True)

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    instructions: str = Field(..., min_length=10)
    prep_time_minutes: int = Field(..., gt=0)

class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate]

class RecipeResponse(RecipeBase):
    id: int
    ingredients: List[IngredientResponse]

    model_config = ConfigDict(from_attributes=True)