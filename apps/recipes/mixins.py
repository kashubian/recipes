from django.http import HttpResponseForbidden


class OwnerMixin:
    """
    Forbidden error appears if user is not an owner of resource.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if self.request.user != obj.owner:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
    