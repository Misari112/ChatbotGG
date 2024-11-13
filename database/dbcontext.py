import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Firebase:
    _instance: Optional['Firebase'] = None
    _initialized = False

    def __new__(cls) -> 'Firebase':
        if cls._instance is None:
            cls._instance = super(Firebase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Firebase._initialized:
            self._initialize_firebase()
            Firebase._initialized = True

    def _load_config(self):
        """Load and validate Firebase configuration from environment variables"""
        config = {
            'apiKey': os.getenv('APIKEY'),
            'authDomain': os.getenv('AUTHDOMAIN'),
            'projectId': os.getenv('PROJECTID'),
            'databaseURL': os.getenv('DATABASEURL'),
            'storageBucket': os.getenv('STORAGEBUCKET'),
            'messagingSenderId': os.getenv('MESSAGINGSENDERID'),
            'appId': os.getenv('APPID')
        }

        # Validate required configuration
        if not config['databaseURL']:
            raise ValueError("DATABASEURL environment variable is not set")

        # Remove None values
        return {k: v for k, v in config.items() if v is not None}

    def _initialize_firebase(self):
        """Initialize both Firebase Admin SDK and Pyrebase with error handling"""
        try:
            # Load and validate configuration
            firebase_config = self._load_config()
            database_url = firebase_config['databaseURL']

            # Initialize Firebase Admin SDK
            cred_path = 'chatbotgladys-firebase-adminsdk-2ftoy-80c998945b.json'
            if not os.path.exists(cred_path):
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

            cred = credentials.Certificate(cred_path)
            
            # Initialize with explicit database URL
            self.admin_app = firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })

            # Initialize Pyrebase with validated config
            self.pyrebase_app = pyrebase.initialize_app(firebase_config)
            
            # Initialize auth and database references
            self.auth = self.pyrebase_app.auth()
            self.db = db.reference('/')  # Initialize with root path

        except ValueError as e:
            print(f"Configuration error: {str(e)}")
            raise
        except firebase_admin.exceptions.FirebaseError as e:
            print(f"Firebase Admin SDK error: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    @property
    def database(self):
        """Get database reference"""
        return self.db

    @property
    def authentication(self):
        """Get authentication instance"""
        return self.auth

# Create a single instance to be imported by other modules
firebase = Firebase()