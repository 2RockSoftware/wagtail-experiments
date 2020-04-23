try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from .models import Experiment
from .utils import get_user_id


class GoalURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_full_url = request.get_full_path()
        current_url = request.path
        print(current_url)
        # does the current URL matches the goal URL for a live experiment?
        experiments = Experiment.objects.filter(
            goal_url__contains=current_url,
            status='live'
        )
        if experiments.exists():
            # let's complete all experiment that match this URL
            user_id = get_user_id(request)
            for experiment in experiments:
                experiment.record_completion_for_user(user_id, request)
        else:
            print('No {} experiments on url {}'.format(current_full_url, current_url))
        # If the current_url is not an experiment's goal_url, then don't do anything
        return None