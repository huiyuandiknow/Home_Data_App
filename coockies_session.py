import hashlib
from flask.sessions import SessionInterface, SessionMixin, session_json_serializer, SecureCookieSession, \
    URLSafeTimedSerializer, total_seconds, BadSignature


class ChunkedSecureCookieSessionInterface(SessionInterface):
    """The default session interface that stores sessions in signed cookies
    through the :mod:`itsdangerous` module.
    """
    #: the salt that should be applied on top of the secret key for the
    #: signing of cookie based sessions.
    salt = 'cookie-session_ha'
    #: the hash function to use for the signature.	The default is sha1
    digest_method = staticmethod(hashlib.sha1)
    #: the name of the itsdangerous supported key derivation.  The default
    #: is hmac.
    key_derivation = 'hmac'
    #: A python serializer for the payload.	 The default is a compact
    #: JSON derived serializer with support for some extra Python types
    #: such as datetime objects or tuples.
    serializer = session_json_serializer
    session_class = SecureCookieSession

    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None

        cookie_vals = {}
        for cookie_name in request.cookies:
            if cookie_name.startswith(app.session_cookie_name):
                cookie_vals[cookie_name] = request.cookies.get(cookie_name)
        vals = []
        for cookie_name in sorted(cookie_vals.keys()):
            vals.append(cookie_vals[cookie_name])
        val = ''.join(vals)

        if not val:
            return self.session_class()
        max_age = total_seconds(app.permanent_session_lifetime)
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            print ('bad_signature')
            return self.session_class()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session:
            if session.modified:
                for cookie_idx in range(10):
                    response.delete_cookie('%s:%s' % (app.session_cookie_name, cookie_idx),
                                           domain=domain, path=path)
            return
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))

        chunks, chunk_size = len(val), int(len(val) / 9)
        vals = [val[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

        for i in range(10):
            try:
                val = vals[i]
            except:
                val = ''
            response.set_cookie('%s:%s' % (app.session_cookie_name, i), val,
                                expires=expires, httponly=httponly,
                                domain=domain, path=path, secure=secure)

#by RJ Patawaran can be used freely for anything you like and edited by Mikle Gorbunov