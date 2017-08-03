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
from collections import defaultdict

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
        url_params = {'zip': zip_search, 'api_key': 'gvaqgra59ma2sxhjmcx9ccqk', 'startDate': date_search}
        movie_response = urllib2.urlopen(base_url + urllib.urlencode(url_params)).read()
        parsed_movie_dictionary = json.loads(movie_response)
        # movies = {'movies' : parsed_movie_dictionary[:10]}

        for movie in parsed_movie_dictionary[:15]:
            theatre_dict = defaultdict(list)
            for theatre in movie['showtimes']:
                theatre_name = theatre['theatre']['name']
                theatre_dict[theatre_name].append(theatre['dateTime'])
            movie['special_showtimes'] = theatre_dict

            # time to get the poster image for this movie
            img_base_url = "https://api.themoviedb.org/3/search/movie?"
            img_url_params = {'query': movie['title'], 'api_key': '15d2ea6d0dc1d476efbca3eba2b9bbfb'}
            img_response = urllib2.urlopen(img_base_url + urllib.urlencode(img_url_params)).read()
            parsed_img_dictionary = json.loads(img_response)
            image_url = "http://image.tmdb.org/t/p/w500//qquEFkFbQX1i8Bal260EgGCnZ0f.jpg"
            if len(parsed_img_dictionary['results']) > 0:
                image_url = "http://image.tmdb.org/t/p/w500/" + parsed_img_dictionary['results'][0]['poster_path']
            movie['special_poster'] = image_url

        movies_we_disp = []
        for movie in parsed_movie_dictionary[:15]:
            if "3D" not in movie["title"] and "3d" not in movie["title"]:
                movies_we_disp.append(movie)

        self.response.write(template.render({'movies' : movies_we_disp}))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
