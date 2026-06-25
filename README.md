# Architecture Pattern Recommendation Tool

An AI-powered assistant that recommends suitable software architecture patterns based on project requirements, helping IT teams make consistent design choices and reduce decision time.

## Problem Statement

IT project teams struggle to select appropriate architecture patterns that align with business and technical requirements. The diversity of patterns and lack of centralized guidance leads to:
- Inconsistent design choices
- Scalability or maintainability issues
- Extended decision-making cycles
- Difficulty comparing trade-offs

## Solution Overview

This tool provides:
- **AI-Powered Recommendations**: Uses GenAI to analyze project descriptions and suggest relevant patterns
- **Structured Pattern Catalog**: 20-30+ well-documented architecture patterns with trade-offs
- **Interactive UI**: Simple interface for project input and recommendation display
- **Rationale Explanations**: Clear reasoning for each recommendation
- **Performance Target**: Response time under 10 seconds

## Project Structure

```
.
├── backend/              # FastAPI backend server
│   ├── app/
│   │   ├── main.py      # Application entry point
│   │   ├── api/         # API routes
│   │   ├── models/      # Data models and schemas
│   │   ├── services/    # Business logic
│   │   └── config.py    # Configuration
│   ├── data/
│   │   ├── patterns.json        # Architecture pattern catalog
│   │   └── sample_projects.json # Sample project requirements
│   ├── requirements.txt
│   └── .env.example
├── frontend/            # React web interface
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API service layer
│   │   ├── App.jsx      # Main app component
│   │   └── index.css    # Styling
│   ├── package.json
│   └── .env.example
├── docs/                # Documentation
│   ├── ARCHITECTURE.md  # System design
│   ├── API.md           # API reference
│   ├── PATTERNS.md      # Pattern catalog details
│   └── SETUP.md         # Setup instructions
├── scripts/             # Utility scripts
│   └── seed_data.py     # Initialize sample data
├── docker-compose.yml   # Local development setup
├── .gitignore
└── LICENSE
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key (or compatible GenAI service)
- Docker (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The application will be available at `http://localhost:3000`

## API Endpoints

### POST /api/recommend
Submit project requirements and receive architecture pattern recommendations.

**Request:**
```json
{
  "project_description": "E-commerce platform...",
  "team_size": 8,
  "time_to_market": "6 months",
  "scalability_needs": "high",
  "budget_constraints": "medium"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "pattern": "Microservices",
      "score": 0.92,
      "rationale": "...",
      "pros": [...],
      "cons": [...],
      "implementation_effort": "high"
    }
  ]
}
```

## Features

- ✅ Natural language project input
- ✅ AI-powered pattern matching
- ✅ Ranked recommendations with confidence scores
- ✅ Detailed rationale for each suggestion
- ✅ Pattern comparison tools
- ✅ Feedback collection for continuous improvement
- ✅ Response time < 10 seconds

## Pattern Catalog

Current patterns include:
- Monolithic Architecture
- Microservices
- Event-Driven Architecture
- CQRS (Command Query Responsibility Segregation)
- Serverless/Lambda
- API Gateway Pattern
- Layered Architecture
- Hexagonal (Ports & Adapters)
- And more...

## Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Pydantic (Data validation)
- OpenAI API (GenAI integration)
- SQLite (Local data storage)

**Frontend:**
- React 18
- Tailwind CSS (Styling)
- Axios (HTTP client)

## Success Metrics

1. **Relevance**: Architect feedback indicates >80% recommendation accuracy
2. **Performance**: Average response time < 10 seconds
3. **Adoption**: Tool used in decision-making for new projects
4. **Consistency**: Reduced pattern selection conflicts across teams

## Development Roadmap

- [ ] Phase 1: Core recommendation engine
- [ ] Phase 2: Interactive UI
- [ ] Phase 3: Feedback loop & refinement
- [ ] Phase 4: Multi-user support & history tracking
- [ ] Phase 5: Integration with project management tools

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with documentation

## License

MIT License - see LICENSE file for details

## Support

For questions or issues, please open a GitHub issue or contact the maintainers.
