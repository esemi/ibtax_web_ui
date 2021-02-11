"""All parts needed for handle requests."""

import logging
import pathlib

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from timing_asgi import TimingClient, TimingMiddleware
from timing_asgi.integrations import StarletteScopeToName

html_fir = pathlib.Path(__file__).parent.joinpath('templates').absolute()
html_templates = Jinja2Templates(directory=html_fir)


class PrintTimings(TimingClient):
    def timing(self, metric_name, timing, tags):
        logging.info(f'{metric_name=} {timing=}, {tags=}')


async def index_html(request):
    logging.info('index page request')

    return html_templates.TemplateResponse('index.html', {
        'request': request,
    })


routes = [
    Route('/', index_html, methods=['GET'], name='homepage'),
]

app = Starlette(debug=False, routes=routes)

app.add_middleware(
    TimingMiddleware,
    client=PrintTimings(),
    metric_namer=StarletteScopeToName(prefix='', starlette_app=app),
)

app_log = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)s %(levelname)s %(name)s %(message)s')  # noqa: WPS323
app_log.setFormatter(formatter)

logger = logging.getLogger()
logger.handlers = []
logger.addHandler(app_log)
logger.setLevel(logging.INFO)
