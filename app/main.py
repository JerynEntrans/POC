import datetime
import os

# NOTE: Used to make SQL model enums to behave like SQLAlchemy enums
# import app.patch_sql_model_enums as SQLModelEnumPatcher  # noqa F401

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import markdown2

from fastapi.responses import RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.services.scheduler.sync import start_scheduler, run_sync_job

from dotenv import load_dotenv
load_dotenv()


# ⬇️ Routers import
from app.api.routes import sync  # noqa: E402
from app.api.routes import providers  # noqa: E402
from app.api.routes import employees  # noqa: E402


app = FastAPI(
    title="Talonify DB Services APIs",
    version="0.1.1",
    openapi_url="/documentation.json",
    description="""
For detailed workflow steps, refer to the full documentation:
[View Workflow Summary](/readme)
""",
    docs_url=None,  # disable default /docs
)

# 🗃️ Serve static files (like favicon.ico) from the 'static' folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# 🗃️ Templates include
templates = Jinja2Templates(directory="app/templates")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    excluded_routes = {
        ("/documentation", None),
        # ("/health", None),
        ("/readme", None),
        ("/", None)
    }

    def should_include_route(route):
        if isinstance(route, APIRoute):
            for method in route.methods:
                if (route.path, method) in excluded_routes or (route.path, None) in excluded_routes:
                    return False
        else:
            if (getattr(route, "path", None), None) in excluded_routes:
                return False
        return True

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=[route for route in app.routes if should_include_route(route)]
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# ✅ Routers include
app.include_router(sync.router)
app.include_router(providers.router)
app.include_router(employees.router)


# Serve custom docs with favicon
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css",
        # swagger_favicon_url="/static/favicon.ico"
    )


@app.get("/", summary="About Talonify DB Services API")
def read_root(request: Request):
    about_info = {
        "version": "v1",
        "company": "Talonify",
        "app": "Talonify DB Services API"
    }
    return templates.TemplateResponse(request, "index.html", {"info": about_info})


@app.get("/documentation")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    # TODO: Add distinct health checks that are relevant to the service ,e.g. API connectivity, etc...
    return {
        "company": "Talonify",
        "api_health_status": "OK",
        "version": os.getenv("GITHASH", "not set"),
        "timestamp": datetime.datetime.now().timestamp()
    }


# @app.on_event("startup")
# def startup_event():
#     run_sync_job()
#     start_scheduler()


@app.get("/readme", response_class=HTMLResponse, summary="Brief html documentation")
async def render_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        md_content = f.read()
        html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks"])
        return f"""
<html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: auto; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            code {{ font-family: monospace; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
</html>"""
