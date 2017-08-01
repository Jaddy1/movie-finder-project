#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
import json
import urllib2
import urllib
import logging

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("hello from the get")
        template = jinja_environment.get_template('templates/search_zip.html')
        self.response.write(template.render())
    def post(self):
        template = jinja_environment.get_template('templates/movie-showings.html')
        zip_search = self.request.get('zip_code_input')
        date_search = self.request.get('date_input')

        base_url = "http://data.tmsapi.com/v1.1/movies/showings?"
<<<<<<< HEAD
        url_params = {'zip': zip_search, 'api_key': 'gvaqgra59ma2sxhjmcx9ccqk', 'startDate': '2017-08-01'}
=======
        url_params = {'zip': zip_search, 'api_key': 'qvhrjfxsk6j6bgcedpugeg35', 'startDate': date_search}
>>>>>>> 5bdeb32067572a61e23deb258bf8507e1bb8a8c4
        movie_response = urllib2.urlopen(base_url + urllib.urlencode(url_params)).read()
        parsed_movie_dictionary = json.loads(movie_response)
        movies = parsed_movie_dictionary[:5]

        self.response.write(template.render(movies))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
