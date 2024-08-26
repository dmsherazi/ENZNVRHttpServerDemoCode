#!/usr/bin/env python
import http.client
import json
import hashlib

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    #'Referer': '/degist/frmUserLogin',
    'Accept-Language': 'zh-CN',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Host': '10.8.0.198',
    #'Content-Length': '27',
    'Connection': 'Keep-Alive',
    'Cache-Control': 'no-cache'
}

g_data_cmd = {
    "Type": 0,
    "Ch": 0,
    "Data":{}
}

data_cmd = {
    "Type": 0,
    "Ch": 0,
    "Data":{}
}

g_username = 'admin'
g_password = '1'
g_ipaddr = '10.8.0.35'
g_port = 80
g_cmd ='frmUserLogin'
json_recv = ''
s_hash = ''
c_hash = ''
x_hash = ''

def get_auth_str(src_str,find_str):
    #print("src %s  find %s" %(src_str,find_str))
    npos = src_str.find(find_str)
    #print(npos)
    split_str = src_str[npos + len(find_str):]
   # print(split_str)
    npos = split_str.find('"')
   # print(npos)
   # print(split_str[0:npos])
    return split_str[0:npos]

def login_device(save_json_recv):
    conn = http.client.HTTPConnection(g_ipaddr, g_port)
    #print(g_data_cmd)
    # cmd_str = json.dumps(data_cmd).encode()
    #cmd_str = json.dumps(g_data_cmd)
    if save_json_recv == 0:
        cmd_str = json.dumps(data_cmd)
    else:
        cmd_str = g_data_cmd

    print(cmd_str)
    #degisturi = 'http://10.8.0.198//digest//frmUserLogin'
    degisturi = '//digest//frmUserLogin'
    Referer = '//degist//frmUserLogin'
    Host = g_ipaddr
    headers.clear()
    headers.setdefault('Accept', '*/*')
    headers.setdefault('Content-Type', 'application/json')
    headers.setdefault('Referer', Referer)
    headers.setdefault('Accept-Language', 'zh-CN')
    headers.setdefault('Accept-Encoding', 'gzip, deflate')
    headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
    headers.setdefault('Host', Host)
    headers.setdefault('Content-Length', len(cmd_str))
    headers.setdefault('Cache-Control', 'no-cache')
    print(headers)
    method = 'POST'
    try:
        conn.request(method, degisturi, cmd_str, headers)
    except Exception as ex:
        print("出现如下异常%s" % ex)
        conn.close()
        return -1

    response = conn.getresponse()
    print(response.status, response.reason)
    print(response.headers)

    if response.status == 401:
        #print(response.headers)
        #print(response.getheader('WWW-Authenticate'))
        auth = response.getheader('WWW-Authenticate')
        # 获取 realm
        realm = get_auth_str(auth, 'realm="')
        print(realm)
        domain = get_auth_str(auth, 'domain="')
        print(domain)
        qop = get_auth_str(auth, 'qop="')
        print(qop)
        nonce = get_auth_str(auth, 'nonce="')
        print(nonce)
        opaque = get_auth_str(auth, 'opaque="')
        print(opaque)

        # HA1 username:realm:password
        HA1_str = g_username + ':' + realm + ':' + g_password
        print(HA1_str)
        HA1 = hashlib.md5(HA1_str.encode('utf-8')).hexdigest()
        print(HA1)

        # HA1 method:degisturi
        HA2_str = method + ':' + degisturi
        print(HA2_str)
        HA2 = hashlib.md5(HA2_str.encode('utf-8')).hexdigest()
        print(HA2)

        # nc 和 cnonce 是客户端自己随机生成， 在发送给服务端的时候需要带上
        nc = "00000002"
        cnonce = "08368223322de35"
        # HA1:nonce:nc:cnonce:qop:HA2

        result_str = HA1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + HA2
        print(result_str)
        result = hashlib.md5(result_str.encode('utf-8')).hexdigest()
        print(result)

        Authorization_str = 'X-Digest username="' + g_username + '", '
        Authorization_str += 'realm="' + realm + '", '
        Authorization_str += 'nonce="' + nonce + '", '
        Authorization_str += 'uri="' + degisturi + '", '
        Authorization_str += 'response="' + result + '", '
        Authorization_str += 'opaque="' + opaque + '", '
        Authorization_str += 'qop=' + qop + ', '
        Authorization_str += 'nc=' + nc + ', '
        Authorization_str += 'cnonce="' + cnonce + '",'
        print(Authorization_str)
        headers.setdefault('Authorization', Authorization_str)
        conn.close()
        conn = http.client.HTTPConnection(g_ipaddr, g_port)
        try:
            conn.request(method, degisturi, cmd_str, headers)
        except Exception as ex:
            print("出现如下异常%s" % ex)
            conn.close()
            return -1

        response = conn.getresponse()
        print(response.status, response.reason)
        print(response.headers)
        #degist 认证中 只有登录接口才会返回 S-HASH C-HASH' X-HASH
        #后续其它操作都需要在http头里面带上这个三个信息 否则认证不会通过
        global s_hash
        global c_hash
        global x_hash
        print(response.getheader('S-HASH'))
        s_hash = response.getheader('S-HASH')
        print(response.getheader('C-HASH'))
        c_hash = response.getheader('C-HASH')
        print(response.getheader('X-HASH'))
        x_hash = response.getheader('X-HASH')
        data = response.read().decode('utf-8')
        # print(data)


        if save_json_recv == 1:
            global json_recv
            json_recv = data
    else:
        print(response.status)
        conn.close()
        return -1

    conn.close()
    return 0

def logout_device(save_json_recv):
    print(g_ipaddr)
    print(g_port)
    conn = http.client.HTTPConnection(g_ipaddr, g_port)
    #print(g_data_cmd)
    # cmd_str = json.dumps(data_cmd).encode()
    if save_json_recv == 0:
        cmd_str = json.dumps(data_cmd)
    else:
        cmd_str = g_data_cmd
   # print(cmd_str)
   # degisturi = 'http://10.8.0.198//digest//frmUserLogout'
    degisturi = '//digest//frmUserLogout'
    Referer = '//degist//frmUserLogout'
    Host = g_ipaddr
    headers.clear()
    headers.setdefault('Accept', '*/*')
    headers.setdefault('Content-Type', 'application/json')
    headers.setdefault('Referer', Referer)
    headers.setdefault('Accept-Language', 'zh-CN')
    headers.setdefault('Accept-Encoding', 'gzip, deflate')
    headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
    headers.setdefault('Host', Host)
    headers.setdefault('Content-Length', len(cmd_str))
    headers.setdefault('Cache-Control', 'no-cache')
    headers.setdefault('Cache-Control', 'no-cache')
    headers.setdefault('S-HASH', s_hash)
    headers.setdefault('C-HASH', c_hash)
    headers.setdefault('X-HASH', x_hash)

    print(headers)
    method = 'POST'
    try:
        conn.request(method, degisturi, cmd_str, headers)
    except Exception as ex:
        print("出现如下异常%s" % ex)
        conn.close()
        return -1

    response = conn.getresponse()
    print(response.status, response.reason)
    if response.status == 401:
        #print(response.headers)
        #print(response.getheader('WWW-Authenticate'))
        auth = response.getheader('WWW-Authenticate')
        # 获取 realm
        realm = get_auth_str(auth, 'realm="')
        print(realm)
        domain = get_auth_str(auth, 'domain="')
        print(domain)
        qop = get_auth_str(auth, 'qop="')
        print(qop)
        nonce = get_auth_str(auth, 'nonce="')
        print(nonce)
        opaque = get_auth_str(auth, 'opaque="')
        print(opaque)

        # HA1 username:realm:password
        HA1_str = g_username + ':' + realm + ':' + g_password
        print(HA1_str)
        HA1 = hashlib.md5(HA1_str.encode('utf-8')).hexdigest()
        print(HA1)

        # HA1 method:degisturi
        HA2_str = method + ':' + degisturi
        print(HA2_str)
        HA2 = hashlib.md5(HA2_str.encode('utf-8')).hexdigest()
        print(HA2)

        # nc 和 cnonce 是客户端自己随机生成， 在发送给服务端的时候需要带上
        nc = '00000002'
        cnonce = "08368223322de35"
        # HA1:nonce:nc:cnonce:qop:HA2

        result_str = HA1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + HA2
        print(result_str)
        result = hashlib.md5(result_str.encode('utf-8')).hexdigest()
        print(result)

        Authorization_str = 'X-Digest username="' + g_username + '", '
        Authorization_str += 'realm="' + realm + '", '
        Authorization_str += 'nonce="' + nonce + '", '
        Authorization_str += 'uri="' + degisturi + '", '
        Authorization_str += 'response="' + result + '", '
        Authorization_str += 'opaque="' + opaque + '", '
        Authorization_str += 'qop=' + qop + ', '
        Authorization_str += 'nc=' + nc + ', '
        Authorization_str += 'cnonce="' + cnonce + '",'
        print(Authorization_str)
        headers.setdefault('Authorization', Authorization_str)
        conn.close()
        conn = http.client.HTTPConnection(g_ipaddr, g_port)
        try:
            conn.request(method, degisturi, cmd_str, headers)
        except Exception as ex:
            print("出现如下异常%s" % ex)
            conn.close()
            return -1

        response = conn.getresponse()
        print(response.status, response.reason)
        print(response.headers)
        data = response.read().decode('utf-8')
        #print(data)
        if save_json_recv == 1:
            global json_recv
            json_recv = data
    else:
        print(response.status)
        conn.close()
        return -1

    conn.close()
    return 0

def send_http_request(username, password, ip, port, cmd, cmd_data):
    global g_username
    global g_password
    global g_ipaddr
    global g_port
    global g_cmd
    global g_data_cmd
    g_username = username
    g_password = password
    g_ipaddr = ip
    g_port = port
    g_cmd = cmd
    g_data_cmd = cmd_data
    global login_success
    login_success = -1
    if cmd == 'frmUserLogin':
        login_success = login_device(1)
        if login_success != 0 :
            return False

        if login_success == 0:
            logout_device(0)
        return True

    if cmd == 'frmUserLogout':
        login_success = login_device(0)
        logout_device(1)
        return True
    #g_data_cmd = cmd_data
    login_success = login_device(0)
    conn = http.client.HTTPConnection(g_ipaddr, g_port)
    print(cmd_data)
    #cmd_str = json.dumps(cmd_data).encode()
    #cmd_str = json.dumps(cmd_data)
    cmd_str = cmd_data
    print(cmd_str)
    #degisturi = 'http://10.8.0.198//digest//' + cmd
    degisturi = '//digest//' + cmd
    Referer = '//degist/' + cmd
    Host = g_ipaddr
    headers.clear()
    headers.setdefault('Accept', '*/*')
    headers.setdefault('Content-Type', 'application/json')
    headers.setdefault('Referer', Referer)
    headers.setdefault('Accept-Language', 'zh-CN')
    headers.setdefault('Accept-Encoding', 'gzip, deflate')
    headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
    headers.setdefault('Host', Host)
    headers.setdefault('Content-Length', len(cmd_str))
    headers.setdefault('Cache-Control', 'no-cache')
    headers.setdefault('S-HASH', s_hash)
    headers.setdefault('C-HASH', c_hash)
    headers.setdefault('X-HASH', x_hash)
    print(headers)
    method = 'POST'
    try:
        conn.request(method, degisturi, cmd_str, headers)
    except Exception as ex:
        print("出现如下异常%s" % ex)
        conn.close()
        if login_success == 0:
            logout_device(0)
        return False

    response = conn.getresponse()
    print("jinll")
    print(response)
    print(response.status, response.reason)
    if response.status == 401:
        # print(response.headers)
        # print(response.getheaders())
        # print(response.getheader('WWW-Authenticate'))
        auth = response.getheader('WWW-Authenticate')
        # 获取 realm
        realm = get_auth_str(auth, 'realm="')
        print(realm)
        domain = get_auth_str(auth, 'domain="')
        print(domain)
        qop = get_auth_str(auth, 'qop="')
        print(qop)
        nonce = get_auth_str(auth, 'nonce="')
        print(nonce)
        opaque = get_auth_str(auth, 'opaque="')
        print(opaque)

        # HA1 username:realm:password
        HA1_str = g_username + ':' + realm + ':' + g_password
        print(HA1_str)
        HA1 = hashlib.md5(HA1_str.encode('utf-8')).hexdigest()
        print(HA1)

        # HA1 method:degisturi
        HA2_str = method + ':' + degisturi
        print(HA2_str)
        HA2 = hashlib.md5(HA2_str.encode('utf-8')).hexdigest()
        print(HA2)

        # nc 和 cnonce 是客户端自己随机生成， 在发送给服务端的时候需要带上
        nc = "00000002"
        cnonce = "08368223322de35"
        # HA1:nonce:nc:cnonce:qop:HA2

        result_str = HA1 + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + HA2
        print(result_str)
        result = hashlib.md5(result_str.encode('utf-8')).hexdigest()
        print(result)

        Authorization_str = 'X-Digest username="' + g_username + '", '
        Authorization_str += 'realm="' + realm + '", '
        Authorization_str += 'nonce="' + nonce + '", '
        Authorization_str += 'uri="' + degisturi + '", '
        Authorization_str += 'response="' + result + '", '
        Authorization_str += 'opaque="' + opaque + '", '
        Authorization_str += 'qop=' + qop + ', '
        Authorization_str += 'nc=' + nc + ', '
        Authorization_str += 'cnonce="' + cnonce + '",'

        print(Authorization_str)
        headers.setdefault('Authorization', Authorization_str)
        conn.close()
        conn = http.client.HTTPConnection(g_ipaddr, g_port)
        try:
            conn.request(method, degisturi, cmd_str, headers)
        except Exception as ex:
            print("出现如下异常%s" % ex)
            conn.close()
            if login_success == 0:
                logout_device(0)
            return False

        response = conn.getresponse()
        print(response.status, response.reason)
        #data = response.read().decode('utf-8')
        #global json_recv
        #json_recv = data
        #print(json_recv)
    else:
        data = response.read().decode('utf-8')
        global json_recv
        json_recv = data
        print(json_recv)
        #print(response.status)
        #conn.close()
       # if login_success == 0:
       #     logout_device(0)
       # return False

    conn.close()
    if login_success == 0:
        logout_device(0)
    return True

#接收回复 回复以字典的方式回复dirt = {'recv':''}
def get_recv(dirt):
    global json_recv
    if json_recv == '':
        recv_datas=''
        dirt['recv'] = recv_datas
        return False
    else:
        print('json_recv = ', json_recv)
        recv_datas = json_recv
        dirt['recv'] = recv_datas
        json_recv = ''
        return True