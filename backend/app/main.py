from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from app.config import settings
from app.models import ProjectRequirements, RecommendationResponse
from app.services.recommender import RecommendationService
from app.services.patterns import PatternCatalog

# Initialize FastAPI app
app = FastAPI(
    title="Architecture Pattern Recommendation Tool",
    description="AI-powered tool for recommending architecture patterns based on project requirements",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pattern_catalog = PatternCatalog()
recommender_service = RecommendationService(pattern_catalog)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Architecture Pattern Recommendation Tool",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/patterns")
async def get_all_patterns():
    """Get all available architecture patterns"""
    return {"patterns": pattern_catalog.get_all_patterns()}

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(requirements: ProjectRequirements) -> RecommendationResponse:
    """
    Get architecture pattern recommendations based on project requirements.
    
    Args:
        requirements: Project requirements details
        
    Returns:
        Recommendations with scores and rationale
    """
    start_time = time.time()
    
    # Get recommendations from service
    recommendations = await recommender_service.recommend(requirements)
    
    processing_time_ms = (time.time() - start_time) * 1000
    
    # Create response
    return RecommendationResponse(
        recommendations=recommendations,
        processing_time_ms=processing_time_ms,
        explanation="Recommendations ranked by relevance to your project requirements"
    )

@app.get("/api/pattern/{pattern_id}")
async def get_pattern_details(pattern_id: str):
    """Get detailed information about a specific pattern"""
    pattern = pattern_catalog.get_pattern(pattern_id)
    if not pattern:
        return {"error": "Pattern not found"}, 404
    return pattern

@app.post("/api/compare")
async def compare_patterns(pattern_ids: list):
    """Compare multiple architecture patterns"""
    patterns = [pattern_catalog.get_pattern(pid) for pid in pattern_ids]
    return {"comparison": patterns}

@app.on_event("startup")
async def startup_event():
    """Initialize on app startup"""
    print(f"🚀 Application starting on {settings.HOST}:{settings.PORT}")
    print(f"📚 Loaded {len(pattern_catalog.get_all_patterns())} architecture patterns")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
