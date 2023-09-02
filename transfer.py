import ply.lex as lex
import ply.yacc as yacc
import sys

import ftplib


tokens = (
    'FTPCONNECT',
    'CWD',
    'UPLOAD',
    'REMOTELIST',
    'MKDIR',
    'QUIT',
    'STRING',
    'NUM'

)

t_ignore = ' \t'



def t_FTPCONNECT(t):
    "FTPCONNECT"
    return t

def t_CWD(t):
    "CWD"
    return t


def t_UPLOAD(t):
    "UPLOAD"
    return t


def t_REMOTELIST(t):
    "REMOTELIST"
    return t

t_QUIT = r'QUIT'
t_MKDIR=r'MKDIR'

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_NUM(t):
    r'[0-9]+'
    return t

def t_error(t):
    print("Unexpected character:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

class ParserState:
    def __init__(self):
        self.variables = {}

state = ParserState()

def p_new_ftp_connect(p):
    """statement : FTPCONNECT STRING NUM STRING STRING"""
    global state

    state.variables["FTPHOST"] = p[2]
    state.variables["FTPPORT"] = int(p[3])
    state.variables["FTPUSER"] = p[4]
    state.variables["FTPPWD"] = p[5]
    

    
    ftp = ftplib.FTP()
    ftp.connect(state.variables["FTPHOST"], state.variables["FTPPORT"])
    ftp.login(state.variables["FTPUSER"], state.variables["FTPPWD"])
    
    print("[*] Connected to " + state.variables["FTPHOST"])
    state.variables["FTPSESSION"] = ftp


def p_cwd(p):
    """statement : CWD STRING"""
    global state
    ftp=None
    if "FTPSESSION" in state.variables:
        ftp = state.variables["FTPSESSION"]
    else:
        print("Connect first (FTPCONNECTION)")
        sys.exit(1)
    
    remote_dir = p[2]
    print("[*] Changing directory to {} ".format(remote_dir))
    ftp.cwd(remote_dir)

def p_upload(p):
    """statement : UPLOAD STRING STRING"""
    global state
    ftp=None
    if "FTPSESSION" in state.variables:
        ftp = state.variables["FTPSESSION"]
    else:
        print("Connect first (FTPCONNECTION)")
        sys.exit(1)
    
    local_file = p[2]
    remote_file = p[3]
    print("[*] Uploading {} to {}".format(local_file, remote_file))
    with open(local_file, "rb") as file:
        ftp.storbinary("STOR {}".format(remote_file), file)

def p_mkdir(p):

    """statement : MKDIR STRING"""
    global state
    ftp=None
    if "FTPSESSION" in state.variables:
        ftp = state.variables["FTPSESSION"]
    else:
        print("Connect first (FTPCONNECTION)")
        sys.exit(1)
    
    remote_dir = p[2]
    print("[*] Creating directory {} to ".format(remote_dir))
    ftp.mkd(remote_dir)

def p_remotelist(p):
    """statement : REMOTELIST"""
    global state
    ftp=None
    if "FTPSESSION" in state.variables:
        ftp = state.variables["FTPSESSION"]
    else:
        print("Connect first (FTPCONNECTION)")
        sys.exit(1)

    files = ftp.nlst()
    for file in files:
        print(file)


def p_QUIT(p):
    """statement : QUIT"""
    global state
    
    if "FTPSESSION" in state.variables:
        ftp = state.variables["FTPSESSION"]
        ftp.close()
        print("[*] Disconnected")
        sys.exit()

def p_error(p):
    print("Syntax error at position:", p.lexpos)
    p.lexer.skip(1)

parser = yacc.yacc()
if len(sys.argv)>1:
    filein = sys.argv[1]
    fl = open(filein, 'r')
    while True:
        try:
            
            line = fl.readline()
            
            
        except Exception as ex:
            fl.close()
            break
        if not line: break
        line=line.strip()
        if line:
            result = parser.parse(line)
    