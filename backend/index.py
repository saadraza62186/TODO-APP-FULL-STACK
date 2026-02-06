from mangum import Mangum
from main import app

# Vercel serverless function handler using Mangum
handler = Mangum(app, lifespan="off")
