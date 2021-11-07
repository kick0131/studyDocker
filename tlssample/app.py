from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World! I have been seen first times.\n'


if __name__ == "__main__":

    ENABLE_SSH = True

    if ENABLE_SSH:
        import ssl
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(
            'cert/hoge.cert', 'cert/hoge_key.pem'
        )
        app.run(host="0.0.0.0", debug=True, ssl_context=ssl_context)
    else:
        app.run(host="0.0.0.0", debug=True)
