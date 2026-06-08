from flask import Flask, render_template, redirect, url_for, request, flash
from email_validator import validate_email, EmailNotValidError
from app.database import create_db, login_user, new_user, user_things
app = Flask(__name__)

app.secret_key = 'chaveultrasecretanãoreveleparaninguem'

# Verifica se o email é verdadeiro
def check_email(email):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        return False
    return True

#-Rotas-#

# Rota original
@app.route('/')
def template():
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')

        # Verifica de email é verdadeiro
        if not check_email(email):
            flash('Email ou Senha incorretos')
            return redirect(url_for('login'))
        
        result = login_user(email, pw)
        
        if result == 'Check':
            # Login
            flash('Acesso Concedido')
            return redirect(url_for('login'))
        else:
            # Retorna uma mensagem de erro
            flash(result)
            return redirect(url_for('login'))

    return render_template('login.html')

# Cadastro
@app.route('/cadastro', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('nome')
        password = request.form.get('password')
        email = request.form.get('email')
        estado = request.form.get('estado')

        # Email inválido
        if not check_email(email):
            flash('O email inserido não é válido. Tente novamente com um email válido')
            return redirect(url_for('register'))
        result = new_user(name,password,email,estado)
        if not result:
            flash('O email inserido ja está cadastrado. Tente novamente com outro email')
            return redirect(url_for('register'))
    
        return '''
<script>
    alert("Conta criada com sucesso!");
    window.location.href = "/login";
</script>
'''
    return render_template('newuser.html')

# Executar app
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
