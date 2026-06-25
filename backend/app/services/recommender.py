import asyncio
from typing import List
from app.models import ProjectRequirements, Recommendation, ArchitecturePattern
from app.services.patterns import PatternCatalog
from app.services.ai_engine import AIEngine

class RecommendationService:
    """Handles architecture pattern recommendations"""
    
    def __init__(self, pattern_catalog: PatternCatalog):
        """Initialize recommendation service"""
        self.pattern_catalog = pattern_catalog
        self.ai_engine = AIEngine()
    
    async def recommend(self, requirements: ProjectRequirements) -> List[Recommendation]:
        """
        Generate architecture pattern recommendations.
        
        Args:
            requirements: Project requirements
            
        Returns:
            List of recommendations sorted by relevance score
        """
        # Get all patterns
        all_patterns = self.pattern_catalog.get_all_patterns()
        
        # Score each pattern
        recommendations = []
        for pattern in all_patterns:
            score, rationale, details = await self.ai_engine.evaluate_pattern(
                requirements, pattern
            )
            
            # Only include patterns with meaningful scores
            if score >= 0.3:
                rec = Recommendation(
                    pattern=ArchitecturePattern(**pattern),
                    score=score,
                    rationale=rationale,
                    alignment_details=details
                )
                recommendations.append(rec)
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        # Return top 5 recommendations
        return recommendations[:5]
    
    def _calculate_basic_score(self, requirements: ProjectRequirements, pattern: dict) -> float:
        """
        Calculate a basic relevance score (fallback if AI fails).
        
        Args:
            requirements: Project requirements
            pattern: Architecture pattern
            
        Returns:
            Score between 0 and 1
        """
        score = 0.5  # Base score
        
        # Scalability alignment
        if requirements.scalability_needs.lower() == 'high':
            if pattern.get('scalability') in ['high', 'medium']:
                score += 0.15
        
        # Team size alignment
        if self.pattern_catalog._matches_team_size(
            requirements.team_size,
            pattern.get('team_size_fit', 'medium')
        ):
            score += 0.15
        
        # Budget constraints
        if requirements.budget_constraints.lower() == 'tight':
            if pattern.get('cost') in ['low', 'medium']:
                score += 0.1
        
        return min(score, 1.0)
