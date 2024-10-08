from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from .shared import db
from .user_type import UserType


class User(db.Model):
    bcrypt = Bcrypt()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    _type = db.Column(db.String(20), nullable=False)

    @property
    def type(self) -> UserType:
        return UserType(self._type)

    @type.setter
    def type(self, value):
        try:
            self._type = UserType(value).value
        except ValueError:
            raise ValueError("Invalid user type")

    @property
    def password(self):
        raise AttributeError("password not readable")

    @password.setter
    def password(self, password: str):
        self.password_hash = self.bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password: str) -> bool:
        """
        Check if the password is correct

        Parameters
        ----------
        password: str
            The password to check

        Returns
        -------
        bool
            True if the password is correct, False otherwise
        """
        return self.bcrypt.check_password_hash(self.password_hash, password)

    def create_access_token(self) -> str:
        """
        Create an access token for the user

        Returns
        -------
        str
            The access token
        """
        return create_access_token(identity=self.email)

    def is_admin(self) -> bool:
        """
        Check if the user is an admin

        Returns
        -------
        bool
            True if the user is an admin, False otherwise
        """
        return self.type == UserType.ADMIN

    def has_password(self) -> bool:
        """
        Check if the user has a password

        Returns
        -------
        bool
            True if the user has a password, False otherwise
        """
        return self.password_hash is not None
