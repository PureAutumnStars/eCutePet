# 作   者：林枭熠
# 开发时间:2024/6/10 下午8:29
from ninja import Redoc
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="e_CutePet API",
    description="一个宠物交流社区的API",
    urls_namespace="e-project",
)
api.auto_discover_controllers()
