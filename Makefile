DATABASE = friends.db
SCHEMA = schema.sql
FRIEND_ALGORITHM = friend_algorithm
FRIEND_ALGORITHM_PY = $(FRIEND_ALGORITHM).py

all: | create-db load-data

.PHONY: clean-db
clean-db:
	rm -f $(DATABASE)

.PHONY: create-db
create-db: clean-db
	sqlite3 $(DATABASE) <$(SCHEMA)
	python -c 'from $(FRIEND_ALGORITHM) import test_graph_1; test_graph_1()'

.PHONY: test-db
test-db: create-db
	python -c 'from $(FRIEND_ALGORITHM) import main; main()'



