from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import HTTPException, status
import jwt

from app.core.settings import get_settings
from app.core.exceptions import BAD_REQUEST


settings = get_settings()


class MojixJWT:
    """Mojix JWT
    A class for creating access and refresh tokens for users.
    Inspired by `djangorestframework-simplejwt`.
    """

    def __init__(
        self,
        secret: str,
        algorithm: str = "HS512",
        access_expire_time: timedelta = timedelta(seconds=3600),
        refresh_expire_time: timedelta = timedelta(seconds=86400),
        user_id_claim: str = "sub",
        user_id_field: str = "id",
    ) -> None:
        """Initialize configs

        Parameters
        --------
        secret: str
            JWT signing key.
        algorithm: str
            JWT signing algorithm. Defaults to "HS256".
        access_expire_time: timedelta
            how long access token is valid. Defaults to 1 hour.
        refresh_expire_time: timedelta
            how long refresh token is valid. Defaults to 1 day.
        user_id_claim: str
            user identifier claim in JWT. Defaults to "sub".
        user_id_field: str
            name of the field that we use to fetch user from db. Defaults to "id".
        --------

        Returns
        --------
        None
        --------
        """
        self.secret = secret
        self.algorithm = algorithm
        self.access_expire_time = access_expire_time
        self.refresh_expire_time = refresh_expire_time
        self.user_id_claim = user_id_claim
        self.user_id_field = user_id_field

    def _create_access_token(self, user_id_claim_value: str) -> str:
        """Creates access token

        Parameters
        --------
        user_id_claim_value: str
            user_id_claim value that identifies user.
        --------

        Returns
        --------
        str
            access token
        --------
        """
        expire = datetime.utcnow() + self.access_expire_time
        to_encode = {
            self.user_id_claim: user_id_claim_value,
            "exp": expire,
            "token_type": "access",
        }
        token = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token

    def _create_refresh_token(self, user_id_claim_value: str) -> str:
        """Creates refresh token

        Parameters
        --------
        user_id_claim_value: str
            user_id_claim value that identifies user.
        --------

        Returns
        --------
        str
            refresh token
        --------
        """
        expire = datetime.utcnow() + self.refresh_expire_time
        to_encode = {
            self.user_id_claim: user_id_claim_value,
            "exp": expire,
            "token_type": "refresh",
        }
        token = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token

    def user_login_response(self, user_id_claim_value: str) -> Dict[str, str]:
        """Response for user login

        Parameters
        --------
        user_id_claim_value: str
            user_id_claim value that identifies user.
        --------

        Returns
        --------
        Dict[str, str]
            a dict including `access_token`, `refresh_token` and `token_type`.
        --------
        """
        return {
            "access_token": self._create_access_token(user_id_claim_value),
            "refresh_token": self._create_refresh_token(user_id_claim_value),
            "token_type": "bearer",
        }

    def create_token_from_refresh(self, refresh_token: str) -> Dict[str, str]:
        """Creates access token from refresh token

        Parameters
        --------
        refresh_token: str
        --------

        Returns
        --------
        Dict[str, str]
            a dict including `access_token` and `token_type`.
        --------
        """
        try:
            payload = self.decode_token(refresh_token)
            if payload["token_type"] != "refresh":
                raise BAD_REQUEST
            token = self._create_access_token(payload[self.user_id_claim])
            return {
                "access_token": token,
                "token_type": "bearer",
            }
        except:
            raise BAD_REQUEST

    def decode_token(self, token: str) -> Dict[str, Any]:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])


jwt_manager = MojixJWT(
    secret=settings.SECRET_KEY,
    access_expire_time=settings.JWT_ACCESS_EXPIRE_TIME,
    refresh_expire_time=settings.JWT_REFRESH_EXPIRE_TIME,
)
