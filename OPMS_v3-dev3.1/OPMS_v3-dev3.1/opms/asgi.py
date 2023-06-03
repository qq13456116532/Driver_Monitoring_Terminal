from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import Consumer.routings # 导入websocket的路由

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Consumer.routings.websocket_urlpatterns,  # 把websocket的路由注册进去
        )
    ),
})