# -*- coding: utf-8 -*-
import http.client
import traceback
import urllib

HTTP_OK = 200
HTTP_AUTHORIZATION_ERROR = 401


class Client:
    domain = 'api.wmcloud.com'
    port = 443
    token = ''
    httpClient = None

    def __init__(self):
        self.httpClient = http.client.HTTPSConnection(self.domain, self.port)

    def __del__(self):
        if self.httpClient is not None:
            self.httpClient.close()

    def encodepath(self, path):
        # ת������ı���
        start = 0
        n = len(path)
        re = ''
        i = path.find('=', start)
        while i != -1:
            re += path[start:i + 1]
            start = i + 1
            i = path.find('&', start)
            if (i >= 0):
                for j in range(start, i):
                    if (path[j] > '~'):
                        re += urllib.quote(path[j])
                    else:
                        re += path[j]
                re += '&'
                start = i + 1
            else:
                for j in range(start, n):
                    if (path[j] > '~'):
                        re += urllib.quote(path[j])
                    else:
                        re += path[j]
                start = n
            i = path.find('=', start)
        return re

    def init(self, token):
        self.token = token

    def getData(self, path):
        result = None
        path = '/data/v1' + path
        path = self.encodepath(path)
        print(path)
        try:
            # set http header here
            self.httpClient.request('GET', path, headers={"Authorization": "Bearer " + self.token})
            # make request
            response = self.httpClient.getresponse()
            # read result
            if response.status == HTTP_OK:
                # parse json into python primitive object
                result = response.read()
            else:
                result = response.read()
            if (path.find('.csv?') == -1):
                result = result.decode('utf-8').encode('GB18030')
            return response.status, result
        except Exception as e:
            # traceback.print_exc()
            raise e
        return -1, result
