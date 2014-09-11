SHELL = /bin/bash

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

.PHONY: load-db
load-db: load-db/1

.PHONY: load-db/%
load-db/%: create-db
	python -c 'from $(FRIEND_ALGORITHM) import test_graph_$*; test_graph_$*()'

.PHONY: test-db
test-db: test-db/1

.PHONY: test-db/%
test-db/%: load-db/%
	diff --side-by-side --width=80 --suppress-common-lines \
		<(python -c 'from $(FRIEND_ALGORITHM) import show_accuracy_test; show_accuracy_test()') \
		t/$@

.PHONY: visualize-db
visualize-db: visualize-db/1

.PHONY: visualize-db/%
visualize-db/%: load-db/%
	bash visualize.bash $(DATABASE)






