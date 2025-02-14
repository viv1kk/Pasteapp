from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Set your passcode here
PASSCODE = "mysecret"

# In-memory storage for texts; keys are IDs and values are the text content
notes = {}
next_id = 1  # Simple counter for note IDs

# HTML templates using render_template_string for simplicity

login_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Enter Passcode</h2>
    <form method="POST" action="{{ url_for('login') }}">
        <input type="password" name="passcode" placeholder="Passcode" required>
        <button type="submit">Login</button>
    </form>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

main_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Text Manager</title>
</head>
<body>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Text Manager</h2>
        <form method="POST" action="{{ url_for('logout') }}">
            <button type="submit">Logout</button>
        </form>
    </div>
    <form method="POST" action="{{ url_for('create') }}">
        <textarea name="content" placeholder="Enter text here" required></textarea><br>
        <button type="submit">Add Text</button>
    </form>
    <h3>Saved Texts</h3>
    <ul>
        {% for id, content in notes.items() %}
            <li>
                {{ content }}
                <form method="POST" action="{{ url_for('delete') }}" style="display:inline;">
                    <input type="hidden" name="id" value="{{ id }}">
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template_string(main_page_html, notes=notes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        passcode = request.form.get('passcode')
        if passcode == PASSCODE:
            session['authenticated'] = True
            return redirect(url_for('home'))
        else:
            error = 'Incorrect passcode.'
    return render_template_string(login_page_html, error=error)

@app.route('/create', methods=['POST'])
def create():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    global next_id
    content = request.form.get('content')
    if content:
        notes[next_id] = content
        next_id += 1
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    note_id = request.form.get('id')
    if note_id:
        note_id = int(note_id)
        notes.pop(note_id, None)
    return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the app with HTTPS enabled using a self-signed certificate
    # app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
    app.run()