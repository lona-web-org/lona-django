from lona import LonaView


class HomeView(LonaView):
    def handle_request(self, request):
        return """
            <h1>Lona Django Test Project</h1>
            <ul>
                <li><a href="/admin/">Django Admin</a></li>
                <li><a href="/login-required/">Login Required</a></li>
                <li><a href="/template-based-form/">Template Based Form</a></li>
            </ul>
        """  # NOQA
