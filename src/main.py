import web


from ctrl.ctrl import Controller
from ctrl.notfound import NotFound


        
urls = (
#     '/notfound/tt', 'NotFound',
    '/(.*)', 'Controller'
)
    

app = web.application(urls, globals())


if __name__ == "__main__":
    app.run()