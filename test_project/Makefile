PYTHON=python3
PYTHON_VENV=env

LONA_SHELL_SERVER_URL=file://socket
LONA_DEFAULT_ARGS=--shell-server-url=$(LONA_SHELL_SERVER_URL)

$(PYTHON_VENV)/.created: REQUIREMENTS.txt
	rm -rf $(PYTHON_VENV) && \
	rm -rf django-project/dist/ django-project/*.egg* && \
	$(PYTHON) -m venv $(PYTHON_VENV) && \
	. $(PYTHON_VENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -r ./REQUIREMENTS.txt && \
	date > $(PYTHON_VENV)/.created

env: $(PYTHON_VENV)/.created

django-project/db.sqlite3: env
	. $(PYTHON_VENV)/bin/activate && \
	./django-project/manage.py migrate && \
	./django-project/manage.py loaddata 0001_admin

db: django-project/db.sqlite3

clean:
	rm -rf $(PYTHON_VENV)

shell: env db
	. $(PYTHON_VENV)/bin/activate && \
	./django-project/manage.py shell

server: env db
	. $(PYTHON_VENV)/bin/activate && \
	lona run-server \
		$(LONA_DEFAULT_ARGS) \
		--project-root=./ \
		-s settings.py \
		$(args)
