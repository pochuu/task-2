import secrets
import string
from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uvicorn

# encoding coefficients
b_ = 7
c = 3
c_ = 65
d = 3

app = FastAPI()
security = HTTPBasic()


class Word(BaseModel):
    contents: str

@app.get('/user')
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "user")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}

# I got inspired from your hackme website, it is modified affine cipher(the b coefficient changes every iteration)
@app.post('/coding')
async def words_coding_post(word: Word, secure: str = Depends(get_current_username)):
    a = word.contents
    b = b_
    encode = []
    for e in a:
        encode.append((string.printable.index(e) * c + b) % 97)
        b = (b * d) % 97  # adding some randomness so the string made from the same letters is harder to decipher
    string_result = lambda x: [string.printable[s] for s in x]
    return {word.contents: ''.join(string_result(encode))}


@app.post('/decoding')
async def words_decoding_post(word: Word, secure: str = Depends(get_current_username)):
    a = word.contents
    b = b_
    decode = []
    for e in a:
        decode.append((c_ * (string.printable.index(e) - b)) % 97)
        b = (b * d) % 97
    string_result = lambda x: [string.printable[s] for s in x]
    return {word.contents: ''.join(string_result(decode))}

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')