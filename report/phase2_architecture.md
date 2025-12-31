You are a senior software architect designing a Smart Agriculture Decision Support System.

CONTEXT:
- Target users: Farmers with basic technical knowledge
- Data sources: IoT sensors (soil moisture, temperature, humidity)
- Primary goal: Provide actionable irrigation and fertilization recommendations
- Scale: Small to medium farms (100-1000 sensors)

FUNCTIONAL REQUIREMENTS:
1. Ingest sensor data in real-time
2. Store historical data for analysis
3. Generate irrigation recommendations based on soil moisture and temperature
4. Generate fertilization suggestions
5. Provide alerts (drought risk, overwatering)
6. Display data via web dashboard

NON-FUNCTIONAL REQUIREMENTS:
- Modularity: Clear separation of concerns
- Explainability: Users must understand why recommendations are made
- Extensibility: Easy to add new sensor types or crops
- Security: Basic authentication and input validation
- Maintainability: Clean code, well-documented
- Performance: Response time < 2 seconds for recommendations

TECHNICAL CONSTRAINTS:
- Backend: Python + FastAPI
- Frontend: Streamlit
- Database: SQLite (for prototype)
- Deployment: Initially local, future cloud migration possible

EXPECTED OUTPUT:
Please provide:
1. A layered architecture diagram (describe in text with ASCII art or mermaid syntax)
2. List of major components with responsibilities
3. Data flow description
4. API contract (main endpoints)
5. Justification of key architectural decisions
6. Identified risks and mitigation strategies

Focus on a pragmatic, production-ready architecture that balances simplicity with professional quality.

