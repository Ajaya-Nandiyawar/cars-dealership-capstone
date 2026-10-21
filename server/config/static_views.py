import mimetypes
from pathlib import Path
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings


def serve_about(request):
    """Serves server/frontend/static/About.html"""
    path = settings.BASE_DIR / "server" / "frontend" / "static" / "About.html"
    if path.exists():
        return HttpResponse(path.read_text(encoding="utf-8"), content_type="text/html")
    raise Http404("About.html not found")


def serve_contact(request):
    """Serves server/frontend/static/Contact.html"""
    path = settings.BASE_DIR / "server" / "frontend" / "static" / "Contact.html"
    if path.exists():
        return HttpResponse(path.read_text(encoding="utf-8"), content_type="text/html")
    raise Http404("Contact.html not found")


def serve_static_css(request):
    """Serves server/frontend/static/style.css"""
    path = settings.BASE_DIR / "server" / "frontend" / "static" / "style.css"
    if path.exists():
        return HttpResponse(path.read_text(encoding="utf-8"), content_type="text/css")
    raise Http404("style.css not found")


def serve_frontend_asset(request, path):
    """Serves built React assets from frontend/dist/assets/<path>"""
    file_path = settings.BASE_DIR / "frontend" / "dist" / "assets" / path
    if file_path.exists() and file_path.is_file():
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(open(file_path, "rb"), content_type=mime_type or "application/octet-stream")
    raise Http404(f"Asset {path} not found")


def serve_frontend_app(request):
    """Serves built React frontend index.html if available, or a clean fallback."""
    dist_index = settings.BASE_DIR / "frontend" / "dist" / "index.html"
    if dist_index.exists():
        return HttpResponse(dist_index.read_text(encoding="utf-8"), content_type="text/html")
    
    # Clean fallback if frontend is not yet built
    return HttpResponse(
        """<!DOCTYPE html>
<html>
<head><title>Cars Dealership API Server</title></head>
<body style="font-family:sans-serif;padding:40px;background:#0f172a;color:#f8fafc;">
    <h1>Cars Dealership Backend Server Running</h1>
    <p>API endpoints are active at <code>/api/</code>.</p>
    <ul>
        <li><a style="color:#38bdf8;" href="/api/dealers/">/api/dealers/</a></li>
        <li><a style="color:#38bdf8;" href="/api/car-makes/">/api/car-makes/</a></li>
        <li><a style="color:#38bdf8;" href="/about/">About Us (/about/)</a></li>
        <li><a style="color:#38bdf8;" href="/contact/">Contact Us (/contact/)</a></li>
        <li><a style="color:#38bdf8;" href="/admin/">Django Admin (/admin/)</a></li>
    </ul>
</body>
</html>""",
        content_type="text/html",
    )
