from src.resources.auth import UserAuthResource, UserRegistrationResource
from src.resources.user import UserResource
from src.resources.transaction import TranctionResource

def initialize_routes(api):

    api.add_resource(UserRegistrationResource, 'user/registor/', methods=['POST'], endpoint="register_user")
    api.add_resource(UserAuthResource, 'user/login/', methods=['POST'], endpoint="login_user")
    api.add_resource(UserAuthResource, 'user/logout/', methods=['DELETE'], endpoint="logout_user")

    api.add_resource(UserResource, 'user/', methods=['GET'], endpoint="get_user")

    api.add_resource(TranctionResource, 'transactions/', methods=['GET'], endpoint="get_user_transactions")
    api.add_resource(TranctionResource, 'transaction/', methods=['POST'], endpoint="create_transactions")
    api.add_resource(TranctionResource, 'transaction/', methods=['PUT'], endpoint="transfer_transactions")