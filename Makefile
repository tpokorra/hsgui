PIPENV := PIPENV_VENV_IN_PROJECT=1 pipenv run 
PAC := `id -nu`
DOMAIN := ${ADMINDOMAIN}
SECRETDJANGOKEY = `${PIPENV} python -c "import secrets; print(secrets.token_urlsafe())"`
INITIAL_USERNAME := admin
INITIAL_PASSWORD := `${PIPENV} python -c "import secrets; import string; alphabet = string.ascii_letters + string.digits; print(''.join(secrets.choice(alphabet) for i in range(16)))"`
PYTHON_VERSION := 3.10.9

all:
	@echo "help:"
	@echo "  make init"


create_pipenv:
	echo "PIPENV_VENV_IN_PROJECT=1" >> ${HOME}/.profile
	PIPENV_VENV_IN_PROJECT=1 pipenv install

setup_domain:
	if [ ! -d ${HOME}/doms/${DOMAIN} ]; then hsscript -u ${PAC} -e "domain.add({set:{name:'${DOMAIN}', user:'${PAC}'}})"; fi
	echo "from hsgui.wsgi import application" > ${HOME}/doms/${DOMAIN}/app-ssl/passenger_wsgi.py
	rm -Rf ${HOME}/doms/${DOMAIN}/subs-ssl/www/index.html
	rm -Rf ${HOME}/doms/${DOMAIN}/htdocs-ssl/.htaccess
	rm -f ${HOME}/doms/${DOMAIN}/htdocs-ssl/static
	ln -s /home/pacs/${PAC}/hsgui/static ${HOME}/doms/${DOMAIN}/htdocs-ssl/static
	echo "PassengerFriendlyErrorPages off" > ${HOME}/doms/${DOMAIN}/.htaccess
	echo "PassengerPython /home/pacs/${PAC}/hsgui/.venv/bin/python" >> ${HOME}/doms/${DOMAIN}/.htaccess
	echo "SetEnv PYTHONPATH /home/pacs/${PAC}/hsgui" >> ${HOME}/doms/${DOMAIN}/.htaccess
	echo "ALLOWED_HOSTS = [ '${DOMAIN}' ]" > /home/pacs/${PAC}/hsgui/hsgui/settings_local.py
	echo "DEBUG = False" >> /home/pacs/${PAC}/hsgui/hsgui/settings_local.py
	echo "SECRET_KEY = '${SECRETDJANGOKEY}'" >> /home/pacs/${PAC}/hsgui/hsgui/settings_local.py

create_superuser:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('${INITIAL_USERNAME}', 'admin@${DOMAIN}', '${INITIAL_PASSWORD}')" | ${PIPENV} python manage.py shell
	echo "login with username ${INITIAL_USERNAME} and password ${INITIAL_PASSWORD}"

migrate:
	${PIPENV} python manage.py migrate

collectstatic:
	${PIPENV} python manage.py collectstatic --no-input

restart:
	mkdir -p ${HOME}/doms/${DOMAIN}/app-ssl/tmp && touch ${HOME}/doms/${DOMAIN}/app-ssl/tmp/restart.txt

hsadmin_properties:
	@/bin/bash -c 'if [ -f ~/.hsadmin.properties ]; then echo "Die Datei ~/.hsadmin.properties existiert bereits"; else echo "Es wird die Datei .hsadmin.properties mit dem Passwort für den Benutzer ${PAC} angelegt, um automatisierte Aufgaben zu ermöglichen" && read -p "Bitte Password für ${PAC} eingeben: " -s pac_password && echo "${PAC}.passWord=$$pac_password" >> ~/.hsadmin.properties; echo; echo "Erfolg: die Datei wurde angelegt."; fi'

# Ansible requires Python >= 3.8; on Debian Buster we have Python 3.7.3
install_ansible:
	mkdir -p ${HOME}/opt
	mkdir -p ${HOME}/build
	cd ${HOME}/build; wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
	cd ${HOME}/build; tar xzf Python-${PYTHON_VERSION}.tgz
	cd ${HOME}/build/Python-${PYTHON_VERSION}; ./configure --enable-optimizations --prefix=/home/pacs/${PAC}/opt; make; make install
	rm -rf ${HOME}/build
	echo 'export PATH=$$HOME/opt/bin:$$HOME/.local/bin:$$PATH' >> ${HOME}/.profile
	. ${HOME}/.profile; python3 -m pip install --user --upgrade pip pipenv
	mkdir -p ${HOME}/ansible
	cd ${HOME}/ansible; . ${HOME}/.profile; PIPENV_VENV_IN_PROJECT=1 pipenv install ansible
	
	


init: create_pipenv setup_domain migrate

