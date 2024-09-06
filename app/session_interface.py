# Before creating our own interface, we need to create our own object.
import uuid #to give a unique id
import json
from itsdangerous import signer, BadSignature, want_bytes
from flask.sessions import SessionMixin, SessionInterface
from itsdangerous import Signer, BadSignature, want_bytes

class MySession(dict,SessionMixin): #MySession sınıfı
    def __init__(self, initial=None,sessionId=None):
        self.initial=initial
        self.sessionId=sessionId
        super(MySession,self).__init__(initial or ())
        
    def __setitem__(self, key, value):
        super(MySession, self).__setitem__(key, value)


    def __getitem__(self,item):
        return super(MySession,self).__getitem__(item)

    def __delitem__(self,key):
        super(MySession,self).__delitem__(key)

class MySessionInterface(SessionInterface):
    session_class=MySession
    salt='my-session'
    #parantez koymadık çünkü parantez ornegini veriyor
    #ben adresini vermek istediğim için no parantez


    #ben bu degerleri bir sozlukte kaydedicem
    container=dict()
    def __init__(self):
        pass
    def open_session(self,app,request):
        #bize requesti verdiği için cookie den id yi alalım
        signer=Signer(app.secret_key, salt=self.salt,key_derivation='hmac' )
        signedSessionId = request.cookies.get(app.config['SESSION_COOKIE_NAME'])
        if not signedSessionId: #eger yoksa
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)

        try: 
            sessionId=signer.unsign(signedSessionId).decode()
        except BadSignature:
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)
        initialSessionValueAsJson= self.container.get(sessionId)
        
        try:
            initialSessionValue=json.loads(initialSessionValueAsJson)
        except:
            sessionId=str(uuid.uuid4())
            return self.session_class(sessionId=sessionId)
        return self.session_class(initialSessionValue,sessionId=sessionId)

    def save_session(self,app,session,response):
        if session is not None and hasattr(session, 'sessionId'):
            sessionAsJson= json.dumps(dict(session)) #save in json mode
            self.container[session.sessionId]=sessionAsJson
            signer=Signer(app.secret_key,salt=self.salt, key_derivation='hmac')
            signedSessionId=signer.sign(session.sessionId).decode()
            response.set_cookie(app.config['SESSION_COOKIE_NAME'],signedSessionId)#key,value
        else:
            pass
