from flask import Flask, request, make_response, render_template,jsonify,redirect
import requests


app = Flask(__name__)
authen_url = 'http://authen-service:8008/'
author_url = 'http://authorization-service:8008/'
epochservice_url = 'http://epoch-service:8008/get_epoch_time'
quoteservice_url = 'http://quote-service:8008/random_quote'
max_retries=100

custom_log = []

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
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                return redirect("https://token.noteziee.cloud/users")
            else:
                break
    else:
        if request.method == 'POST':
            dataLogin = request.json
            for attempt in range(1, max_retries + 1):
                try:
                    response = requests.post(authen_login_url, json=dataLogin)
                    if response.ok:
                        print('POST request successful')
                        author_register_url= author_url + "token"
                        data = response.json()
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.post(author_register_url, json=data)
                                if response.ok:
                                    data = response.json()
                                    response_data = {"message": "token create"}
                                    response = make_response(jsonify(response_data), 200)
                                    response.set_cookie('token', value=data.get('token'))
                                    return response, 200
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

@app.route('/users', methods=['GET'])
def get_current_user():
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                token_data = {"token":token}

                author_register_url= author_url + "getusername"
                for attempt in range(1, max_retries + 1):
                    try:
                        response = requests.post(author_register_url, json=token_data)
                        if response.ok:
                            data = response.json()
                            username_from_server = data.get('username')
                            custom_log.append("username_from_server")
                            custom_log.append(username_from_server)
                            return render_template('authentication/user.html', username=username_from_server)
                        else:
                            data = response.json()
                            flag = data.get('isExpired')
                            if flag:
                                response = make_response('Token is fully expired')
                                response.set_cookie('token', value='NULL', expires = 0)
                                return response

                            return response, 400
                    except requests.exceptions.RequestException as e:
                        custom_log.append('Error in making the request:')
            else:
                custom_log.append('token cant be delivered')
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')
@app.route('/log', methods=['GET'])
def view_log():
    return custom_log,200
                
@app.route('/EpochService', methods=['GET'])
def returnEpoch():
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                author_check_url= author_url + "check"
                accessService = {"access":False}
                for attempt in range(1, max_retries + 1):
                    try:
                        data ={"token":token,"service":":EpochService"}
                        response = requests.post(author_check_url,json=data)
                        accessService = response.json()
                    except requests.exceptions.RequestException as e:
                        print('Error in making the request:', e)
                    if accessService.get('access') == True:
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.get(epochservice_url)
                                data = response.json()
                                response_data = data
                            except requests.exceptions.RequestException as e:
                                print('Error in making the request:', e)
                    else:
                        response_data = {"message": "Access Denied"}
                    response = make_response(jsonify(response_data), 200)
                    if accessService.get('token') == None or accessService.get('isExpired'):
                        response = make_response('Token is fully expired')
                        response.set_cookie('token', value='NULL', expires = 0)
                    else:
                        response.set_cookie('token', value=accessService.get('token'))
                    return response, 200
            else:
                custom_log.append('token cant be delivered')
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')

@app.route('/QuoteService', methods=['GET'])
def returnQuote():
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                author_check_url= author_url + "check"
                accessService = {"access":False}
                for attempt in range(1, max_retries + 1):
                    try:
                        data ={"token":token,"service":":EpochService"}
                        response = requests.post(author_check_url,json=data)
                        accessService = response.json()
                    except requests.exceptions.RequestException as e:
                        print('Error in making the request:', e)
                    if accessService.get('access') == True:
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.get(quoteservice_url)
                                data = response.json()
                                response_data = data
                            except requests.exceptions.RequestException as e:
                                print('Error in making the request:', e)
                    else:
                        response_data = {"message": "Access Denied"}
                    response = make_response(jsonify(response_data), 200)
                    if accessService.get('token') == None or accessService.get('isExpired'):
                        response = make_response('Token is fully expired')
                        response.set_cookie('token', value='NULL', expires = 0)
                    else:
                        response.set_cookie('token', value=accessService.get('token'))
                    return response, 200
            else:
                custom_log.append('token cant be delivered')
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')


if __name__ == '__main__':
    app.run(debug=True)
