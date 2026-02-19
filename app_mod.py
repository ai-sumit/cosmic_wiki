import os
import sys
import wikipedia
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# -------------------- DJANGO SETTINGS --------------------

BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=False,  # Production ready
    SECRET_KEY=os.environ.get("SECRET_KEY", "super-secret-key"),
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[],
)

# -------------------- VIEW --------------------

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guruji - Wikipedia Cosmic Chat</title>
        <meta charset="utf-8">
    </head>
    <body style="background:#0a0e2a;color:white;text-align:center;padding:50px;font-family:Arial;">
        <h1>🌟 GURUJI - COSMIC WIKIPEDIA 🌟</h1>
        <h3>Powered by Wikipedia | Created by Sumit Haldar</h3>
        <form method="GET">
            <input type="text" name="query" placeholder="Ask something..." required
            style="padding:10px;width:300px;border-radius:20px;border:none;">
            <button type="submit"
            style="padding:10px 20px;border-radius:20px;border:none;background:gold;cursor:pointer;">
            Search</button>
        </form>
    """

    query = request.GET.get("query")

    if query:
        try:
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=5)

            html += f"""
            <div style="margin-top:30px;background:#111;padding:20px;border-radius:15px;">
                <h3>Result for: {query}</h3>
                <p style="text-align:left;max-width:800px;margin:auto;">{result}</p>
            </div>
            """
        except wikipedia.exceptions.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            html += f"""
            <div style="margin-top:30px;background:#222;padding:20px;border-radius:15px;">
                <h3>Multiple Results Found</h3>
                <p>{options}</p>
            </div>
            """
        except wikipedia.exceptions.PageError:
            html += """
            <div style="margin-top:30px;background:#222;padding:20px;border-radius:15px;">
                <h3>No Page Found</h3>
                <p>Try another query.</p>
            </div>
            """
        except Exception as e:
            html += f"""
            <div style="margin-top:30px;background:#222;padding:20px;border-radius:15px;">
                <h3>Error</h3>
                <p>{str(e)}</p>
            </div>
            """

    html += """
    </body>
    </html>
    """

    return HttpResponse(html)


# -------------------- URLS --------------------

urlpatterns = [
    path("", home),
]


# -------------------- WSGI APPLICATION --------------------

application = get_wsgi_application()


# -------------------- LOCAL RUN --------------------

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
