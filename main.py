#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


hair2 = {"CCAGCAATCGC":'black', "GCCAGTGCCG":'brown', "TTAGCTATCGC":'carrot'}
facial_shape2 = {"GCCACGG":'square', "ACCACAA":'round', "AGGCCTCA":'oval'}
eye_color2 = {"TTGTGGTGGC":'blue', "GGGAGGTGGC":'green', "AAGTAGTGAC":'brown'}
gender2 = {"TGAAGGACCTTC":'female', "TGCAGGAACTTC":'male'}
race2 = {"AAAACCTCA":'white', "CGACTACAG":'black', "CGCGGGCCG":'asian'}

def search(list, entry):
    for k in list:
         if k in entry:
                return list.get(k)
    else:
        return "Not detected"


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("dna.html")

    def post(self):
        entry = self.request.get("vnos")

        sporocilo = {"hair": search(hair2, entry), "facial_shape": search(facial_shape2, entry),"eye_color": search(eye_color2, entry),"gender": search(gender2, entry),"race":search(race2, entry)}
        return self.render_template("dna.html", params=sporocilo)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
