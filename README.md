# Website-displayer-docker-

## Docker

```
 docker pull ghcr.io/glitchyyz/htmlhost:latest
```
 change /app/html to any host path containing html files

## Local Development (Without Docker)

1. **Run the server:**
   ```bash
   python3 server.py
   ```

2. **Access it:**
   - Open http://localhost:8000 in your browser
   - The server will serve files from the `html/` directory
   - `index.html` will be served as the default page

3. **Add HTML files:**
   - Create `html/` directory if it doesn't exist
   - Place your HTML files there
   - Access them at `http://localhost:8000/filename.html`
