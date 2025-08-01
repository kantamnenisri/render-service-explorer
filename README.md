# Render Service Explorer

A centralized dashboard to view all your Render services, including Web Services, Static Sites, Cron Jobs, Private Services, and Background Workers.

## Features
- **Unified View**: See all service types in one place.
- **Filtering**: Easily filter by service type (Web, Static, Cron, etc.).
- **Live Status**: Real-time status indicators (Live, Suspended, Not Deployed).
- **Direct Links**: Quick access to service URLs, Repositories, and the Render Dashboard.
- **FastAPI Backend**: Efficiently handles Render API requests.

## Setup

### Prerequisites
1. **Render API Key**: Generate one from your [Render Account Settings](https://dashboard.render.com/u/settings#api-keys).

### Local Running
1. Create a `.env` file:
   ```env
   RENDER_API_KEY=your_api_key_here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker
```bash
docker build -t render-explorer .
docker run -p 8000:8000 -e RENDER_API_KEY=your_key render-explorer
```

## Deployment
This app is ready for deployment on Render using the included `render.yaml` and `Dockerfile`.
1. Push to GitHub.
2. Connect to Render.
3. Add your `RENDER_API_KEY` to the environment variables.


## 💡 Inspiration
This project is a reference implementation exploring concepts related to 
multi-cloud reliability engineering. The author holds USPTO patent 
applications in this domain (US 19/325,718 and US 19/344,864).

## Health Check
- Added /ping endpoint for automated health monitoring.
