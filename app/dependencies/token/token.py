from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from joserfc import jwe, jwk, jwt, jws
from ...settings import config


class TokenHandler:
    def __init__(self):
        self.secret_key = jwk.OctKey.import_key(bytes.fromhex(config.SECRET_KEY))
        self.jwe_registry = jwe.JWERegistry()
        self.jws_registry = jws.JWSRegistry()
        self.claims = jwt.JWTClaimsRegistry()

    def generate_jwt(
        self, payload: dict, expire_minutes: int, is_encrypted: bool = False
    ):
        expire_date = datetime.now() + timedelta(minutes=expire_minutes)

        if is_encrypted:
            registry = self.jwe_registry
            header = {"alg": "dir", "enc": "A256GCM"}
        else:
            registry = self.jws_registry
            header = {"alg": "HS256"}

        claims = {
            "exp": int(expire_date.timestamp()),
        }
        claims.update(payload)

        token = jwt.encode(
            header=header, claims=claims, key=self.secret_key, registry=registry
        )

        return token

    def decode_jwt(self, encoded_token: str, is_encrypted: bool = False):
        if is_encrypted:
            registry = self.jwe_registry
        else:
            registry = self.jws_registry

        token = jwt.decode(value=encoded_token, key=self.secret_key, registry=registry)

        try:
            self.claims.validate(token.claims)
            return token
        except:
            raise


def get_token_handler():
    return TokenHandler()


token_dependency = Annotated[TokenHandler, Depends(get_token_handler)]
