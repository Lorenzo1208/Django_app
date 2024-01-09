
import time
from app.models import RequestLog

class RequestMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    start_time = time.time()
    response = self.get_response(request)
    duration = time.time() - start_time

    RequestLog.objects.create(path=request.path, duration=duration)

    return response
