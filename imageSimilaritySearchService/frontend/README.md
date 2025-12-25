# Frontend for Image Similarity Search

This frontend is a small React app built with Vite. It expects a backend running and reachable at the environment variable `VITE_BACKEND_URL` (defaults to `http://localhost:8000`).

Dev:

1. Install dependencies

```bash
cd frontend
npm install
npm run dev
```

Build / Docker (production):

```bash
# Set backend url for build (optional)
VITE_BACKEND_URL=http://your-backend:8000 npm run build
# Serve `dist` with nginx (the provided `Dockerfile` builds and serves the app)
```