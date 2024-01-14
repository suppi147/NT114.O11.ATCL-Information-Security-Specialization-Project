from flask import Flask, request, make_response, render_template
import requests

app = Flask(__name__)
authen_url = 'http://authen-service:8008/'
author_url = 'http://authorization-service:8008/'
max_retries=100

@app.route('/register', methods=['GET','POST'])
def authentication_register():
    if request.method == 'POST':
        authen_register_url= authen_url + "register"
        data = request.json
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(authen_register_url, json=data)
                if response.ok:
                    print('POST request successful')
                    return response.json(), 201
                else:
                    print('POST request failed. Status Code:', response.status_code)
                    return response.text, 400
            except requests.exceptions.RequestException as e:
                print('Error in making the request:', e)

    return render_template('authentication/register.html')

@app.route('/login', methods=['GET','POST'])
def authentication_login():
    authen_login_url= authen_url + "login"
    if request.method == 'POST':
        data = request.json
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(authen_login_url, json=data)
                if response.ok:
                    print('POST request successful')
                    author_register_url= author_url + "token"
                    data = response.json()
                    for attempt in range(1, max_retries + 1):
                        try:
                            response = requests.post(author_register_url, json=data)
                            if response.ok:
                                data = response.json()
                                response = make_response('token create')
                                response.set_cookie('token', value=data.get('token'))
                                return response
                            else:
                                print('POST request failed. Status Code:', response.status_code)
                                return response.text, 400
                        except requests.exceptions.RequestException as e:
                            print('Error in making the request:', e)

                else:
                    print('POST request failed. Status Code:', response.status_code)
                    return response.text, 400
            except requests.exceptions.RequestException as e:
                print('Error in making the request:', e)
    return render_template('authentication/login.html')

if __name__ == '__main__':
    app.run(debug=True)
