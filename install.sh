#!/bin/bash

# Verifica se o curl está instalado
if ! command -v curl &> /dev/null
then
    echo "curl não está instalado. Por favor, instale o curl e execute o script novamente."
    exit 1
fi

# Solicita o link do repositório do GitHub
# read -p "Informe o link do repositório do GitHub: " repo_url
repo_url="https://github.com/vmaicon/formacoes-esjud/archive/refs/heads/main.zip"

repo_dir="formacoes-esjud"

# Cria o diretório para o repositório
mkdir -p "$repo_dir"

cd $repo_dir

# Baixa o repositório do GitHub
echo "Baixando o repositório do GitHub..."
curl -L "$repo_url" -o repo.zip

echo "Extraindo o repositório..."
unzip repo.zip -d .

mv formacoes-esjud-main/* ./
rm -rf formacoes-esjud-main
rm repo.zip

# Verifica se o arquivo start.sh existe e adiciona permissões de execução
# if [ -f "start.sh" ]; then
#     chmod +x start.sh
#     echo "Permissões de execução adicionadas ao start.sh"
# else
#     echo "Arquivo start.sh não encontrado no repositório."
#     exit 1
# fi

# Executa o arquivo start.sh
# ./start.sh


# link do repositório https://github.com/vmaicon/formacoes-esjud/archive/refs/heads/main.zip


# Verifica se a versão do Python é superior a 3.10
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
required_version="3.10"

echo "Versão do python $python_version"

if [[ $(echo -e "$python_version\n$required_version" | sort -V | head -n1) == "$required_version" ]]; then
    echo "Versão do Python é $python_version"
else
    echo "A versão do Python é inferior a 3.10. Por favor, instale a versão 3.10 ou superior."
    exit 1
fi

# Instalar o virtualenv, criar e ativar o ambiente virtual
pip3 install virtualenv
virtualenv .venv
source .venv/bin/activate

# Atualizar o pip
pip install --upgrade pip

# Instalar os requisitos da aplicação
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "Requisitos instalados com sucesso."
        streamlit run home.py
    else
        echo "Falha na instalação dos requisitos."
        exit 1
    fi
else
    echo "Arquivo requirements.txt não encontrado."
    exit 1
fi
