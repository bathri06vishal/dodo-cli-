from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass


class SecurityManager:
    """Manages authentication, encryption, and secure data handling for DODO."""
    
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or Path.home() / ".dodo"
        self.config_dir.mkdir(exist_ok=True)
        self.users_file = self.config_dir / "users.json"
        self.session_file = self.config_dir / "session.json"
        self.salt_file = self.config_dir / "salt.key"
        
        # Initialize salt if not exists
        if not self.salt_file.exists():
            self.salt_file.write_bytes(secrets.token_bytes(32))
        
        self.salt = self.salt_file.read_bytes()
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())
    
    def _hash_password(self, password: str) -> str:
        """Hash password for storage."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000).hex()
    
    def create_user(self, username: str, password: str, email: str = None) -> bool:
        """Create a new user account."""
        users = self._load_users()
        
        if username in users:
            return False
        
        users[username] = {
            "password_hash": self._hash_password(password),
            "email": email,
            "created_at": str(os.times()),
            "api_key": self._generate_api_key(),
            "role": "user"
        }
        
        self._save_users(users)
        return True
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data."""
        users = self._load_users()
        
        if username not in users:
            return None
        
        user = users[username]
        stored_hash = user["password_hash"]
        input_hash = self._hash_password(password)
        
        if not hmac.compare_digest(stored_hash, input_hash):
            return None
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        session_data = {
            "username": username,
            "session_token": session_token,
            "expires_at": os.times()[4] + 3600  # 1 hour
        }
        
        self.session_file.write_text(json.dumps(session_data))
        return user
    
    def logout(self) -> bool:
        """Logout current user."""
        if self.session_file.exists():
            self.session_file.unlink()
            return True
        return False
    
    def get_current_user(self) -> Optional[str]:
        """Get currently logged in user."""
        if not self.session_file.exists():
            return None
        
        try:
            session_data = json.loads(self.session_file.read_text())
            current_time = os.times()[4]
            
            if session_data["expires_at"] < current_time:
                self.logout()
                return None
            
            return session_data["username"]
        except (json.JSONDecodeError, KeyError):
            return None
    
    def verify_session(self, session_token: str) -> bool:
        """Verify session token."""
        if not self.session_file.exists():
            return False
        
        try:
            session_data = json.loads(self.session_file.read_text())
            current_time = os.times()[4]
            
            if session_data["expires_at"] < current_time:
                return False
            
            return hmac.compare_digest(
                session_data["session_token"], 
                session_token
            )
        except (json.JSONDecodeError, KeyError):
            return False
    
    def _generate_api_key(self) -> str:
        """Generate secure API key."""
        return f"dodo_{secrets.token_urlsafe(32)}"
    
    def get_user_api_key(self, username: str) -> Optional[str]:
        """Get user's API key."""
        users = self._load_users()
        return users.get(username, {}).get("api_key")
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """Verify API key and return username."""
        if not api_key.startswith("dodo_"):
            return None
        
        users = self._load_users()
        for username, user_data in users.items():
            if user_data.get("api_key") == api_key:
                return username
        return None
    
    def encrypt_data(self, data: str, password: str) -> bytes:
        """Encrypt data with password."""
        key = self._derive_key(password)
        fernet = Fernet(Fernet(key))
        return fernet.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes, password: str) -> str:
        """Decrypt data with password."""
        key = self._derive_key(password)
        fernet = Fernet(Fernet(key))
        return fernet.decrypt(encrypted_data).decode()
    
    def _load_users(self) -> Dict[str, Any]:
        """Load users database."""
        if not self.users_file.exists():
            return {}
        
        try:
            return json.loads(self.users_file.read_text())
        except json.JSONDecodeError:
            return {}
    
    def _save_users(self, users: Dict[str, Any]) -> None:
        """Save users database."""
        self.users_file.write_text(json.dumps(users, indent=2))
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password."""
        users = self._load_users()
        
        if username not in users:
            return False
        
        stored_hash = users[username]["password_hash"]
        input_hash = self._hash_password(old_password)
        
        if not hmac.compare_digest(stored_hash, input_hash):
            return False
        
        users[username]["password_hash"] = self._hash_password(new_password)
        self._save_users(users)
        return True
    
    def delete_user(self, username: str, password: str) -> bool:
        """Delete user account."""
        users = self._load_users()
        
        if username not in users:
            return False
        
        stored_hash = users[username]["password_hash"]
        input_hash = self._hash_password(password)
        
        if not hmac.compare_digest(stored_hash, input_hash):
            return False
        
        del users[username]
        self._save_users(users)
        
        # Logout if this was the current user
        if self.get_current_user() == username:
            self.logout()
        
        return True


# Global security manager instance
security_manager = SecurityManager()


def require_auth(func):
    """Decorator to require authentication for a function."""
    def wrapper(*args, **kwargs):
        current_user = security_manager.get_current_user()
        if not current_user:
            raise PermissionError("Authentication required. Please run 'dodo login' first.")
        return func(*args, **kwargs)
    return wrapper


def verify_api_key(api_key: str) -> Optional[str]:
    """Verify API key and return username."""
    return security_manager.verify_api_key(api_key)
