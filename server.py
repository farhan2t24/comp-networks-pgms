from flask import Flask, request, jsonify, render_template, abort, session, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import uuid
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Required for session management

# In-memory storage for users and messages
USERS = {}  # {user_id: {"username": str, "password": str}}
STORE = {}  # {msg_id: {key, iv, ciphertext, plaintext, sender_id, receiver_id}}
STORE = {}

def encrypt_message(plaintext: str):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return key, cipher.iv, ct

def decrypt_message(key: bytes, iv: bytes, ciphertext: bytes):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pt.decode('utf-8')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', 
                         username=USERS[session['user_id']]['username'],
                         users=[{'id': uid, 'username': data['username']} 
                               for uid, data in USERS.items() 
                               if uid != session['user_id']])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'missing username or password'}), 400
        
        # Check if username exists
        if any(u['username'] == data['username'] for u in USERS.values()):
            return jsonify({'error': 'username already exists'}), 400
        
        user_id = str(uuid.uuid4())
        USERS[user_id] = {
            'username': data['username'],
            'password': data['password']  # In production, hash the password!
        }
        return jsonify({'success': True, 'user_id': user_id})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'missing username or password'}), 400
        
        # Find user by username
        user_id = next((uid for uid, u in USERS.items() 
                       if u['username'] == data['username'] 
                       and u['password'] == data['password']), None)
        
        if user_id is None:
            return jsonify({'error': 'invalid credentials'}), 401
        
        session['user_id'] = user_id
        return jsonify({'success': True})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/search_user', methods=['GET'])
def search_user():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    query = request.args.get('username', '').lower()
    if not query:
        return jsonify({'users': []})
    
    # Search for users whose usernames contain the query
    matching_users = [
        {'id': uid, 'username': data['username']}
        for uid, data in USERS.items()
        if query in data['username'].lower() and uid != session['user_id']
    ]
    return jsonify({'users': matching_users})

@app.route('/send', methods=['POST'])
def send():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    data = request.get_json()
    if not data or 'message' not in data or 'username' not in data:
        return jsonify({'error': 'missing message or username'}), 400
    
    # Find receiver by username
    receiver_id = next(
        (uid for uid, udata in USERS.items() 
         if udata['username'].lower() == data['username'].lower()),
        None
    )
    
    if not receiver_id:
        return jsonify({'error': 'user not found'}), 404
    
    if receiver_id == session['user_id']:
        return jsonify({'error': 'cannot send message to yourself'}), 400
    
    message = data['message']
    key, iv, ct = encrypt_message(message)
    message_id = str(uuid.uuid4())
    
    STORE[message_id] = {
        'key': base64.b64encode(key).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'ciphertext': base64.b64encode(ct).decode('utf-8'),
        'plaintext': message,
        'sender_id': session['user_id'],
        'receiver_id': data['receiver_id']
    }
    
    return jsonify({
        'id': message_id,
        'ciphertext': STORE[message_id]['ciphertext'],
        'receiver': USERS[data['receiver_id']]['username']
    })

@app.route('/messages')
def list_messages():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    # Get messages where user is sender or receiver
    user_messages = {
        msg_id: {
            'id': msg_id,
            'sender': USERS[msg['sender_id']]['username'],
            'receiver': USERS[msg['receiver_id']]['username'],
            'is_sender': msg['sender_id'] == session['user_id']
        }
        for msg_id, msg in STORE.items()
        if msg['sender_id'] == session['user_id'] 
        or msg['receiver_id'] == session['user_id']
    }
    
    return jsonify({'messages': list(user_messages.values())})

@app.route('/message/<message_id>', methods=['GET'])
def get_message(message_id):
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    entry = STORE.get(message_id)
    if not entry:
        abort(404)
    
    # Only sender or receiver can view the message
    if session['user_id'] not in [entry['sender_id'], entry['receiver_id']]:
        abort(403)
    
    key = base64.b64decode(entry['key'])
    iv = base64.b64decode(entry['iv'])
    ct = base64.b64decode(entry['ciphertext'])
    plaintext = decrypt_message(key, iv, ct)
    
    return jsonify({
        'id': message_id,
        'message': plaintext,
        'sender': USERS[entry['sender_id']]['username'],
        'receiver': USERS[entry['receiver_id']]['username']
    })

@app.route('/raw/<message_id>', methods=['GET'])
def get_raw(message_id):
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    entry = STORE.get(message_id)
    if not entry:
        abort(404)
    
    # Only sender or receiver can view the raw message
    if session['user_id'] not in [entry['sender_id'], entry['receiver_id']]:
        abort(403)
    
    return jsonify({
        'id': message_id,
        'ciphertext': entry['ciphertext'],
        'iv': entry['iv'],
        'sender': USERS[entry['sender_id']]['username'],
        'receiver': USERS[entry['receiver_id']]['username']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
