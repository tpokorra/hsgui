
# Installation

    git clone https://github.com/tpokorra/hsgui
    cd hsgui
    export PIPENV_VENV_IN_PROJECT=1
    export ADMINDOMAIN=admin.meinedomain.de
    make init
    make create_superuser
    make restart
    make collectstatic
