"""
Shared data contracts (Pydantic models) between Team 5 and Team 3.
These define the exact shape of data going in and out of the AI engine.
Team 3 should use these same models on their side to avoid mismatches.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ---------- CATALOG ----------

class CatalogRequest(BaseModel):
    raw_text: str = Field(..., description="Artisan's spoken description, transcribed to text")
    image_tags: Optional[list[str]] = Field(default=None, description="Tags detected from product image, if available")


class CatalogResult(BaseModel):
    title_en: str
    title_hi: str
    description_en: str
    description_hi: str
    category: str
    tags: list[str]
    catalog_ai_available: bool


# ---------- PRICING ----------

class PricingRequest(BaseModel):
    material_cost: float = Field(..., ge=0, description="Cost of raw materials in rupees")
    complexity: str = Field(..., description="One of: simple, medium, complex, very_complex")
    category: str = Field(..., description="Must be one of the valid categories from pricing rules")
    artisan_entered_labor_cost: Optional[float] = Field(default=None, ge=0, description="Artisan's own labor cost estimate, if provided")
    product_description: Optional[str] = Field(default=None, description="Used for AI price adjustment context")


class PricingResult(BaseModel):
    material_cost: float
    labor_cost: float
    base_cost: float
    complexity_multiplier: float
    category_margin: float
    final_price: float
    ai_adjusted_price: float
    ai_explanation: str
    ai_available: bool


# ---------- TRANSLATION ----------

class TranslationRequest(BaseModel):
    text: str
    target_language: str = Field(default="English")


class TranslationResult(BaseModel):
    translated_text: str
    target_language: str
    translation_available: bool


class LanguageDetectionResult(BaseModel):
    language_code: str
    language_name: str
    confidence: str
    detection_available: bool