import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المتصفح الخفي</title>
        <style>
            body { font-family: sans-serif; background: #1a1a1a; color: white; margin: 0; display: flex; flex-direction: column; height: 100vh; }
            .bar { background: #333; padding: 10px; display: flex; gap: 10px; }
            input { flex: 1; padding: 10px; border-radius: 5px; border: none; font-size: 16px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            iframe { flex: 1; border: none; background: white; width: 100%; height: 100%; }
        </style>
    </head>
    <body>
        <div class="bar">
            <input type="text" id="urlInput" placeholder="اكتب الرابط..." onkeypress="handleKey(event)">
            <button onclick="go()">فتح</button>
        </div>
        <iframe id="frame" src="about:blank"></iframe>
        <script>
            function go() {
                let url = document.getElementById('urlInput').value;
                if (!url.startsWith('http')) url = 'https://' + url;
                document.getElementById('frame').src = '/proxy?url=' + encodeURIComponent(url);
            }
            function handleKey(e) { if (e.key === 'Enter') go(); }
        </script>
    </body>
    </html>
    """

@app.get("/proxy")
async def proxy(url: str):
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            content_type = resp.headers.get("content-type", "text/html")
            return Response(content=resp.content, media_type=content_type, status_code=resp.status_code)
    except Exception as e:
        return HTMLResponse(content=f"<h1>خطأ</h1><p>{e}</p>", status_code=500)
