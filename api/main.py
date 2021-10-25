from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
import uvicorn
from pydantic import BaseModel
import secrets
import string

app = FastAPI()
security = HTTPBasic()


class Word(BaseModel):
    contents: str
b = 7
c = 3
c_ = 65
d = 3


@app.get('/user')
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "username")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}


@app.post('/coding')
def words_coding_post(word: Word, secure: str = Depends(get_current_username)):
    result = lambda x: [string.printable[s] for s in x]
    return {"coded": ''.join(result(encode_word(word)))}


@app.post('/decoding')
def words_decoding_post(word: Word, secure: str = Depends(get_current_username)):
    result = lambda x: [string.printable[s] for s in x]
    return {"decoded": ''.join(result(decode_word(word)))}


def decode_word(word):
    decode = []
    b_ = b
    for char in word.contents:
        decode.append((c_ * (string.printable.index(char) - b_)) % 97)
        b_ = (b_ * d) % 97
    return decode


def encode_word(word):
    '''
    I got inspired from your hackme page, it is modified affine cipher(the b coefficient changes every iteration)
    '''
    b_ = b
    encode = []
    for char in word.contents:
        if char not in string.printable:
            return {"Unknown": "character"}
        encode.append((string.printable.index(char) * c + b_) % 97)
        b_ = (b_ * d) % 97  # adding some randomness so the string made from the same letters is harder to decipher
    return encode


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
