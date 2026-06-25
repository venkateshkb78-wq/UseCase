from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectRequirements(BaseModel):
    """Project requirements for pattern recommendation"""
    project_description: str = Field(..., description="Detailed description of the project")
    team_size: int = Field(..., description="Number of team members", ge=1, le=500)
    time_to_market: str = Field(..., description="Time constraint (e.g., '6 months', '3 weeks')")
    scalability_needs: str = Field(..., description="Scalability requirement: 'low', 'medium', or 'high'")
    budget_constraints: str = Field(..., description="Budget constraint: 'tight', 'medium', or 'flexible'")
    data_volume: Optional[str] = Field(None, description="Expected data volume")
    concurrency_level: Optional[str] = Field(None, description="Concurrency requirement")
    compliance_requirements: Optional[str] = Field(None, description="Compliance or regulatory requirements")

class ArchitecturePattern(BaseModel):
    """Architecture pattern information"""
    id: str
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    best_for: List[str]
    avoid_when: List[str]
    implementation_effort: str  # low, medium, high
    learning_curve: str  # low, medium, high
    scalability: str  # low, medium, high
    maintainability: str  # low, medium, high
    team_size_fit: str  # small, medium, large
    cost: str  # low, medium, high

class Recommendation(BaseModel):
    """Pattern recommendation with rationale"""
    pattern: ArchitecturePattern
    score: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    alignment_details: dict

class RecommendationResponse(BaseModel):
    """Response containing recommendations"""
    recommendations: List[Recommendation]
    processing_time_ms: float
    explanation: str

class FeedbackRequest(BaseModel):
    """User feedback on recommendations"""
    recommendation_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = None
    helpful: bool = Field(..., description="Whether the recommendation was helpful")
