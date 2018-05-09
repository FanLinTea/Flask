from music import create_app


app = create_app('test')

if __name__ == '__main__':
    print app.url_map
    app.run()