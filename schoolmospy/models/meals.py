from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MealEntry(BaseModel):
    id: int
    code: str
    name: str
    price: int
    ingredients: str | None = None
    calories: float | None = None
    weight: str | None = None
    protein: float | None = None
    fat: float | None = None
    carbohydrates: float | None = None


class MealComplex(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    price: int
    kind: int
    payment_type: int = Field(alias="paymentType")
    preorder_allowed: bool = Field(alias="preorderAllowed")
    allow_select_items: bool = Field(alias="allowSelectItems")
    items: list[MealEntry]


class MealComplexes(BaseModel):
    items: list[MealComplex]
