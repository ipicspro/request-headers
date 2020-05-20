# -*- coding: utf-8 -*-

# from . import useragents, proxies, referers, screensizes, random_list
from . import request_headers

# from . import ConnectionError, ReadTimeout, Timeout
# from . import web_test_list, UA_List, SS_List
# from . import UserAgent, fake_setttings, FakeUserAgentError

useragents = request_headers.useragents()
proxies = request_headers.proxies()
referers = request_headers.referers()
screensizes = request_headers.screensizes()
randomseeds = request_headers.random_list

ConnectionError = request_headers.ConnectionError
ReadTimeout = request_headers.ReadTimeout
Timeout = request_headers.Timeout
UserAgent = request_headers.UserAgent
fake_setttings = request_headers.fake_setttings
FakeUserAgentError = request_headers.FakeUserAgentError

rf_list = request_headers.rf().l
ua_list = request_headers.ua().l
ss_list = request_headers.ss().l

# depricated
# USERAGENTS = useragents
# PROXIES = proxies
# REFERERS = referers
# SCREENSIZES = screensizes
# RANDOMSEEDS = random_list
