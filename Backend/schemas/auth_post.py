from fastapi import status
import httpx, requests, os
from dotenv import load_dotenv

load_dotenv()

role_env = os.getenv("ROLE")
admin_key = os.getenv("ADMIN_KEY")
post_token_available = ""

def permission(role=None, key=None):
    def decorator(func):
        # @wraps(func)
        def wrapper(*args, **kwargs):
            # print("Validate user...")
            if role != role_env or key != admin_key:
                # print({"error": "Unauthorized Access"})
                return {"error": "Unauthorized access"}, status.HTTP_401_UNAUTHORIZED
            return func(*args, **kwargs)
        return wrapper
    return decorator

@permission(role= role_env, key= admin_key)
def auth_post(post_token: str):
    if not isinstance(post_token, str) :
        return {"error": "Invalid parameter"}, status.HTTP_422_UNPROCESSABLE_ENTITY
    
    if post_token == post_token_available:
        return {"Request_status": "success"}, status.HTTP_200_OK






if __name__ == "__main__":
    auth_post()