# Criar o ambiente virtual

python -m virtualenv venv

# Ativar o ambiente virtual

source venv/Scripts/activate

# Instalar dependencias

pip install -r requirements.txt

# Rodar o flask em ambiente de dev(ativar o fast reload)

export FLASK_ENV=development
