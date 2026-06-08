from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    prep_time_minutes = Column(Integer, nullable=False)

    ingredients = relationship(
        "IngredientModel", 
        back_populates="recipe_reference", 
        cascade="all, delete-orphan"
    )

class IngredientModel(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(100), nullable=False, index=True)
    measurement_quantity = Column(Float, nullable=False)
    measurement_unit = Column(String(50), nullable=False)
    
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe_reference = relationship("RecipeModel", back_populates="ingredients")