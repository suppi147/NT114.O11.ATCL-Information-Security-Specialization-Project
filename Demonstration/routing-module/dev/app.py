from flask import Flask, request, make_response, render_template,jsonify,redirect
import requests
from log import Logger

app = Flask(__name__)
authen_url = 'http://authen-service:8008/'
author_url = 'http://authorization-service:8008/'
session_management_url = 'http://session-management-service:8008/'
epochservice_url = 'http://epoch-service:8008/get_epoch_time'
quoteservice_url = 'http://quote-service:8008/random_quote'
max_retries=100

custom_log = []

@app.route('/register', methods=['GET','POST'])
def authentication_register():
    if request.method == 'POST':
        authen_register_url= authen_url + "register"
        data = request.json
        logger = Logger("routing_log.txt")
        logger.log(f"|routing-module|app.py|authentication_register()|data recieve from browser{data}|")
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(authen_register_url, json=data)
                if response.ok:
                    logger.log(f"|routing-module|app.py|authentication_register()|post request with data: {data} successfully send to {authen_register_url}|")
                    return response.json(), 201
                else:
                    logger.log(f"|routing-module|app.py|authentication_register()|post request FAILED with data: {data} send to {authen_register_url} {response.status_code}|")
                    return response.text, 400
            except requests.exceptions.RequestException as e:
                logger.log(f"|routing-module|app.py|authentication_register()|Error in making the request:{e}|")
        logger.log(f"|routing-module|app.py|authentication_register()|rendering to register.html|")
    return render_template('authentication/register.html')

@app.route('/login', methods=['GET','POST'])
def authentication_login():
    routing_login_url= authen_url + "login"
    cookie_header = request.headers.get('Cookie')
    logger = Logger("routing_log.txt")
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                logger.log(f"|routing-module|app.py|authentication_login()|token{cookie} exist in browser|")
                return redirect("https://token.noteziee.cloud/users")
            else:
                logger.log(f"|routing-module|app.py|authentication_login()|token NOT exist in browser|")
                break
    else:
        if request.method == 'POST':
            dataLogin = request.json
            for attempt in range(1, max_retries + 1):
                try:
                    response = requests.post(routing_login_url, json=dataLogin)
                    if response.ok:
                        logger.log(f"|routing-module|app.py|authentication_login()|success login with {dataLogin} with authen link {routing_login_url}|")
                        author_register_url= author_url + "token"
                        data = response.json()
                        logger.log(f"|routing-module|app.py|authentication_login()|request data {data} with author link {author_register_url}|")
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.post(author_register_url, json=data)
                                if response.ok:
                                    data = response.json()
                                    response_data = {"message": "token create"}
                                    response = make_response(jsonify(response_data), 200)
                                    response.set_cookie('token', value=data.get('token'))
                                    logger.log(f"|routing-module|app.py|authentication_login()|returning token {data.get('token')} to browser|")
                                    return response, 200
                                else:
                                    logger.log(f"|routing-module|app.py|authentication_login()|request to {author_register_url} post FAILED|")
                                    return response.text, 400
                            except requests.exceptions.RequestException as e:
                                logger.log(f"|routing-module|app.py|authentication_login()|error in making request to {author_register_url} {e}|")

                    else:
                        logger.log(f"|routing-module|app.py|authentication_login()|POST request failed. Status Code:, {response.status_code}|")
                        return response.text, 400
                except requests.exceptions.RequestException as e:
                    logger.log(f"|routing-module|app.py|authentication_login()|Error in making the request: {e}|")
    return render_template('authentication/login.html')

@app.route('/users', methods=['GET'])
def get_current_user():
    logger = Logger("routing_log.txt")
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                token_data = {"token":token}
                logger.log(f"|routing-module|app.py|get_current_user()|extract token: {token_data}|")
                author_register_url= author_url + "getusername"
                for attempt in range(1, max_retries + 1):
                    try:
                        response = requests.post(author_register_url, json=token_data)
                        if response.ok:
                            data = response.json()
                            username_from_server = data.get('username')
                            logger.log(f"|routing-module|app.py|get_current_user()|request to {author_register_url} with token {token_data} is oke|")
                            logger.log(f"|routing-module|app.py|get_current_user()|get user name {username_from_server}|")
                            return render_template('authentication/user.html', username=username_from_server)
                        else:
                            data = response.json()
                            logger.log(f"|routing-module|app.py|get_current_user()|request to {author_register_url} with token {token_data} is NOT oke with data response {data}|")
                            flag = data.get('isExpired')
                            if flag:
                                response = make_response('Token is fully expired')
                                logger.log(f"|routing-module|app.py|get_current_user()|token is expired|")
                                response.set_cookie('token', value='NULL', expires = 0)
                                return response

                            return response, 400
                    except requests.exceptions.RequestException as e:
                        logger.log(f"|routing-module|app.py|get_current_user()|Error in making the request:{e}|")
                        
            else:
                logger.log(f"|routing-module|app.py|get_current_user()|token can NOT be extracted in browser|")
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')
@app.route('/log', methods=['GET'])
def view_log():
    return custom_log,200
                
@app.route('/EpochService', methods=['GET'])
def returnEpoch():
    logger = Logger("routing_log.txt")
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                session_management_check_url= session_management_url + "check"
                logger.log(f"|session-management-module|app.py|returnEpoch()|token:{token} exist in browser|")
                accessService = {"access":False}
                for attempt in range(1, max_retries + 1):
                    try:
                        data ={"token":token,"service":"EpochService"}
                        response = requests.post(session_management_check_url,json=data)
                        accessService = response.json()
                        logger.log(f"|session-management-module|app.py|returnEpoch()|send request:{data} to url: {session_management_check_url}|")
                        logger.log(f"|session-management-module|app.py|returnQuote()|recieve data {accessService}|")
                    except requests.exceptions.RequestException as e:
                        logger.log(f"|session-management-module|app.py|returnEpoch()|Error in making the request:{e}|")
                    if accessService.get('access') == True:
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.get(epochservice_url)
                                data = response.json()
                                logger.log(f"|session-management-module|app.py|returnEpoch()|access {epochservice_url} and recieve {data}|")
                                response = make_response(jsonify(data), 200)
                                response.set_cookie('token', value=accessService.get('token'))
                            except requests.exceptions.RequestException as e:
                                logger.log(f"|session-management-module|app.py|returnEpoch()|Error in making the request:{e}|")
                    elif accessService.get('token') == None:
                        response = make_response('Token is fully expired')
                        response.set_cookie('token', value='NULL', expires = 0)
                    else:
                        response_data = {"message": "Access Denied"}
                        response = make_response(jsonify(response_data), 200)
                    return response, 200
            else:
                logger.log(f"|session-management-module|app.py|returnEpoch()|token cant be delivered|")
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')

@app.route('/QuoteService', methods=['GET'])
def returnQuote():
    logger = Logger("routing_log.txt")
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                session_management_check_url= session_management_url + "check"
                logger.log(f"|session-management-module|app.py|returnQuote()|token:{token} exist in browser|")
                accessService = {"access":False}
                for attempt in range(1, max_retries + 1):
                    try:
                        data ={"token":token,"service":"QuoteService"}
                        response = requests.post(session_management_check_url,json=data)
                        accessService = response.json()
                        logger.log(f"|session-management-module|app.py|returnQuote()|send request:{data} to url: {session_management_check_url}|")
                        logger.log(f"|session-management-module|app.py|returnQuote()|recieve data {accessService}|")
                    except requests.exceptions.RequestException as e:
                        logger.log(f"|session-management-module|app.py|returnQuote()|Error in making the request:{e}|")
                    if accessService.get('access') == True:
                        for attempt in range(1, max_retries + 1):
                            try:
                                response = requests.get(quoteservice_url)
                                data = response.json()
                                logger.log(f"|session-management-module|app.py|returnQuote()|access {quoteservice_url} and recieve {data}|")
                                response = make_response(jsonify(data), 200)
                                response.set_cookie('token', value=accessService.get('token'))
                            except requests.exceptions.RequestException as e:
                                logger.log(f"|session-management-module|app.py|returnQuote()|Error in making the request:{e}|")
                    elif accessService.get('token') == None:
                        response = make_response('Token is fully expired')
                        response.set_cookie('token', value='NULL', expires = 0)
                    else:
                        response_data = {"message": "Access Denied"}
                        response = make_response(jsonify(response_data), 200)
                    return response, 200
            else:
                logger.log(f"|session-management-module|app.py|returnQuote()|token cant be delivered|")
                return redirect('https://token.noteziee.cloud/login')
    else:
        custom_log.append('token cant be delivered')
        return redirect('https://token.noteziee.cloud/login')

if __name__ == '__main__':
    app.run(debug=True)
