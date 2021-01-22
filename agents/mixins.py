from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
# create our own mixin to handle the processing of the user type


class OrganizerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organiser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizer:
            # return self.handle_no_permission() - instead of raising an error we will redirect to leads
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)
