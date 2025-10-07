from models import*
from database import*
from auth import*
from services.user_service import*
from fastapi import Depends, FastAPI


my_dict = {
    1:	'.,?!:',
    2:	'ABC',
    3:	'DEF',
    4:	'GHI',
    5:	'JKL',
    6:	'MNO',
    7:	'PQRS',
    8:	'TUV',
    9:	'WXYZ',
    0:	' '
}

print(dict([("key1", "value1"), ("key2", "value2")]))