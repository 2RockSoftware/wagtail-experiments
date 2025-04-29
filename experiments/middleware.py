from .models import Experiment
from .utils import get_user_id


class GoalURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = request.path
        experiments = Experiment.objects.filter(
            goal_url__contains=current_url,
            status='live'
        )
        if experiments.exists():
            # let's complete all experiment that match this URL
            user_id = get_user_id(request)
            for exp in experiments:
                exp.record_completion_for_user(user_id, request)

        response = self.get_response(request)
        return response