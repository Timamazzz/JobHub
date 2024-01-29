from JobHub.utils.ModelViewSet import ModelViewSet
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
    }
