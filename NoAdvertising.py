"""
/*
 * Copyright (C) 2013 Romain Estievenart <blenderviking@live.be>
 * 
 * NoAdvertising is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * NoAdvertising is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NoAdvertising.  If not, see <http://www.gnu.org/licenses/>.
 */
"""
# -*- coding: utf-8 -*-
import requests
import itertools


class NoAdvertising(object):

    def _write_host_list_in_file(self, hosts_list):
        with open('host.txt', 'wb') as file:
            content = '127.0.0.1\t' + '\r\n127.0.0.1\t'.join(hosts_list)
            file.write(content)

    def _get_web_host(self, url):
        response = ''
        try:
            response = requests.get(url).text
        except ConnectionError as e:
            print 'Network error with ' + url
        except HTTPError as e:
            print 'HTTP error with ' + url
        except Timeout as e:
            print 'Timeout with ' + url
        except TooManyRedirects as e:
            print 'TooManyRedirects with ' + url
        except requests.exceptions.RequestException as e:
            print 'RequestException with ' + url
        return response

    def _get_list_host(self, host_list):
        hosts = []
        for host in host_list:
            if host and host.strip():
                if host[0:1] == '#':
                    continue
                hosts.append(host.strip())
        return hosts

    def _merge_host_list(self, *lists):
        merged_list = []
        merged_list.extend(itertools.chain.from_iterable(lists))
        return merged_list

    def _get_list_url(self):
        urls = []
        with open('url.txt') as file:
            for url in file:
                urls.append(url.strip())
        return urls

    def fetch_all_web_host(self):
        urls = self._get_list_url()
        host_list = []
        for url in urls:
            print 'Get host list from : ' + url
            responses = self._get_web_host(url)
            if not responses:
                continue
            responses = responses.replace('0.0.0.0','').replace('127.0.0.1','')
            host = self._get_list_host(responses.split('\n'))
            host_list = self._merge_host_list(host_list, host)
        host_list = set(host_list)
        self._write_host_list_in_file(host_list)

if __name__ == "__main__":
    NoAdvertising().fetch_all_web_host()
