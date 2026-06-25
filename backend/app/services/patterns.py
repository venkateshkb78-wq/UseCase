import json
from typing import List, Optional, Dict
from pathlib import Path
from app.models import ArchitecturePattern

class PatternCatalog:
    """Manages architecture pattern catalog"""
    
    def __init__(self):
        """Initialize pattern catalog from JSON file"""
        self.patterns: Dict[str, dict] = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, dict]:
        """Load patterns from JSON file"""
        patterns_file = Path(__file__).parent.parent.parent / "data" / "patterns.json"
        
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                data = json.load(f)
                return {p['id']: p for p in data.get('patterns', [])}
        
        return {}
    
    def get_all_patterns(self) -> List[dict]:
        """Get all patterns"""
        return list(self.patterns.values())
    
    def get_pattern(self, pattern_id: str) -> Optional[dict]:
        """Get a specific pattern by ID"""
        return self.patterns.get(pattern_id)
    
    def search_patterns(self, keyword: str) -> List[dict]:
        """Search patterns by keyword"""
        keyword_lower = keyword.lower()
        results = []
        
        for pattern in self.patterns.values():
            if (keyword_lower in pattern.get('name', '').lower() or 
                keyword_lower in pattern.get('description', '').lower()):
                results.append(pattern)
        
        return results
    
    def get_patterns_for_team_size(self, team_size: int) -> List[dict]:
        """Get patterns suitable for team size"""
        suitable = []
        
        for pattern in self.patterns.values():
            team_fit = pattern.get('team_size_fit', 'medium')
            if self._matches_team_size(team_size, team_fit):
                suitable.append(pattern)
        
        return suitable
    
    def _matches_team_size(self, size: int, fit: str) -> bool:
        """Check if team size matches pattern fit"""
        if fit == 'small':
            return size <= 10
        elif fit == 'medium':
            return 5 <= size <= 50
        elif fit == 'large':
            return size >= 20
        return True
