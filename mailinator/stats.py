from .base import RequestData, RequestMethod
from .models import *

class GetTeamRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/team'
        super().__init__(RequestMethod.GET, url, Team)

class GetTeamStatsRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/team/stats/'
        super().__init__(RequestMethod.GET, url, Stats)

class GetTeamInfoRequest(RequestData):
    def __init__(self):
        url=f'{self._base_url}/teaminfo'
        super().__init__(RequestMethod.GET, url, TeamInfo)