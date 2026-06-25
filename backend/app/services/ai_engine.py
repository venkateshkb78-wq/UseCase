import json
from typing import Tuple, Dict
from app.models import ProjectRequirements
from app.config import settings
import openai

class AIEngine:
    """AI-powered evaluation engine using OpenAI"""
    
    def __init__(self):
        """Initialize AI engine"""
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    async def evaluate_pattern(
        self,
        requirements: ProjectRequirements,
        pattern: dict
    ) -> Tuple[float, str, Dict]:
        """
        Evaluate how well a pattern matches requirements using AI.
        
        Args:
            requirements: Project requirements
            pattern: Architecture pattern
            
        Returns:
            Tuple of (score, rationale, alignment_details)
        """
        try:
            prompt = self._build_evaluation_prompt(requirements, pattern)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert software architect evaluating how well an architecture pattern matches project requirements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            # Parse the AI response
            score, rationale, details = self._parse_ai_response(result_text)
            
            return score, rationale, details
            
        except Exception as e:
            print(f"AI evaluation error: {str(e)}")
            # Fallback to basic scoring
            score = 0.5
            rationale = f"Pattern: {pattern.get('name', 'Unknown')} may be suitable for your requirements."
            details = {"evaluation_method": "fallback", "error": str(e)}
            return score, rationale, details
    
    def _build_evaluation_prompt(self, requirements: ProjectRequirements, pattern: dict) -> str:
        """
        Build prompt for AI evaluation.
        
        Args:
            requirements: Project requirements
            pattern: Architecture pattern
            
        Returns:
            Evaluation prompt
        """
        prompt = f"""
Evaluate how well the following architecture pattern matches the project requirements.

PROJECT REQUIREMENTS:
- Description: {requirements.project_description}
- Team Size: {requirements.team_size} members
- Time to Market: {requirements.time_to_market}
- Scalability Needs: {requirements.scalability_needs}
- Budget Constraints: {requirements.budget_constraints}
- Data Volume: {requirements.data_volume or 'Not specified'}
- Concurrency Level: {requirements.concurrency_level or 'Not specified'}
- Compliance Requirements: {requirements.compliance_requirements or 'None'}

ARCHITECTURE PATTERN:
- Name: {pattern.get('name')}
- Description: {pattern.get('description')}
- Implementation Effort: {pattern.get('implementation_effort')}
- Learning Curve: {pattern.get('learning_curve')}
- Scalability: {pattern.get('scalability')}
- Maintainability: {pattern.get('maintainability')}
- Team Size Fit: {pattern.get('team_size_fit')}
- Cost: {pattern.get('cost')}
- Best For: {', '.join(pattern.get('best_for', []))}
- Avoid When: {', '.join(pattern.get('avoid_when', []))}

Provide your evaluation in the following JSON format:
{{
  "score": <float between 0 and 1>,
  "rationale": "<brief explanation of why this pattern is or isn't suitable>",
  "alignment_details": {{
    "scalability_match": "<assessment>",
    "team_capability_match": "<assessment>",
    "timeline_feasibility": "<assessment>",
    "budget_alignment": "<assessment>"
  }}
}}

Be concise and focus on key alignment points.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Tuple[float, str, Dict]:
        """
        Parse AI response into score, rationale, and details.
        
        Args:
            response_text: Raw AI response
            
        Returns:
            Tuple of (score, rationale, details)
        """
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                data = json.loads(json_str)
                
                score = float(data.get('score', 0.5))
                rationale = str(data.get('rationale', 'Pattern evaluation complete.'))
                details = data.get('alignment_details', {})
                
                return min(max(score, 0.0), 1.0), rationale, details
        except Exception as e:
            print(f"Error parsing AI response: {str(e)}")
        
        # Fallback
        return 0.5, "Pattern evaluation complete.", {}
