# -*- coding: UTF-8 -*- 
# Author: Zander_M
# Time: 七月, 22, 2018
# Title: SonyPy test 

import socket
import re
import requests


from .camera import Camera


SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900
SSDP_MX = 1


discovery_msg = ('M-SEARCH * HTTP/1.1\r\n'
                 'HOST: %s:%d\r\n'
                 'MAN: "ssdp:discover"\r\n'
                 'MX: %d\r\n'
                 'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n'
                 '\r\n')


dd_regex = ('<av:X_ScalarWebAPI_Service>\n\s*<av:X_ScalarWebAPI_ServiceType>(.*)<\/av:X_ScalarWebAPI_ServiceType>\n\s*<av:X_ScalarWebAPI_ActionList_URL>(.*)<\/av:X_ScalarWebAPI_ActionList_URL>\n\s*<av:X_ScalarWebAPI_AccessType\/>\n\s*<\/av:X_ScalarWebAPI_Service>')

class Discoverer(object):
    camera_class = Camera

    def _interface_addresses(self, family=socket.AF_INET):
        for info in socket.getaddrinfo('', None):
            if family == info[0]:
                addr = info[-1]
                yield addr

    def _parse_ssdp_response(self, data):
        lines = data.split('\r\n')
        lines.pop()
        lines.pop()
        print(lines)
        assert lines[0] == 'HTTP/1.1 200 OK'
        headers = {}
        for line in lines[1:]:
            key, val = line.split(': ', 1)
            headers[key.lower()] = val
        return headers

    def _ssdp_discover(self, timeout=1):
        socket.setdefaulttimeout(timeout)

        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM,
                             socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET,
                        socket.SO_REUSEADDR,
                        1)
        sock.setsockopt(socket.IPPROTO_IP,
                        socket.IP_MULTICAST_TTL,
                        2)
        for _ in range(2):
            msg = discovery_msg % (SSDP_ADDR, SSDP_PORT, SSDP_MX)
            sock.sendto(msg.encode(encoding = "utf8"), (SSDP_ADDR, SSDP_PORT))

        try:
            data = sock.recv(1024)
        except socket.timeout:
            print("SOCKET TIMEOUT")
            pass
        else:
            print("*****")
            print(data)
            yield self._parse_ssdp_response(str(data, encoding='utf8'))

    def _parse_device_definition(self, doc):
        """
        Parse the XML device definition file.
        """
        services = {}
        for m in re.findall(dd_regex, doc):
            services[m[0]] = m[1]
        return services

    def _read_device_definition(self, url):
        """
        Fetch and parse the device definition, and extract the URL endpoint for
        the camera API service.
        """
        r = requests.get(url)
        services = self._parse_device_definition(r.text)
        print(services)
        return services['camera']

    def discover(self):
        endpoints = []
        for resp in self._ssdp_discover():
            url = resp['location']
            endpoint = self._read_device_definition(url)
            print("endpoint: ",endpoint)
            endpoints.append(endpoint)
        return [self.camera_class(endpoint) for endpoint in endpoints]
