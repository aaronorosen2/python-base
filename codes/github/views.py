from django.shortcuts import render
from github.models import Repo, RepoMember



# Create your views here.
@api_view(['POST'])
def create_repo(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    user = User.objects.get(id=token.user_id)
    repo = Repo()


