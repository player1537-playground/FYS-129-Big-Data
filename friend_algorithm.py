#!/usr/bin/python

from __future__ import division
import pprint
import sqlite3

sqlite_db = None

def get_db():
    global sqlite_db
    if sqlite_db is None:
        sqlite_db = connect_db()
    return sqlite_db

def connect_db():
    return sqlite3.connect("friends.db")

def insert_friends(edges):
    def normalize_pair(p):
        return ( min(p), max(p) )
    
    db = get_db()
    for vertex_id in edges.keys():
        db.execute(('INSERT INTO vertices (id) VALUES (?)'),
                   [vertex_id])
    
    already_inserted = set()
    
    for first_id, second_id_set in edges.iteritems():
        for second_id in second_id_set:
            pair = normalize_pair((first_id, second_id))
            
            if pair not in already_inserted:
                db.execute(('INSERT INTO '
                            'edges (first_id, second_id) '
                            'VALUES (?, ?)'),
                           [pair[0], pair[1]])
                db.execute(('INSERT INTO '
                            'edges (first_id, second_id) '
                            'VALUES (?, ?)'),
                           [pair[1], pair[0]])
                already_inserted.update([pair])
    
    db.commit()

def is_determinable(person_id):
    db = get_db()
    
    cur = db.execute(('SELECT generated.id '
                      'FROM (SELECT edges2.second_id id, '
                      '             COUNT(*) c '
                      '      FROM edges '
                      '      JOIN edges AS edges2 '
                      '        ON edges.second_id = edges2.first_id '
                      '      WHERE edges.first_id = :person_id '
                      '      GROUP BY edges2.second_id '
                      '     ) AS generated '
                      'WHERE generated.c = (SELECT COUNT(*) '
                      '                     FROM edges '
                      '                     WHERE first_id = :person_id '
                      '                    ) '),
                     { "person_id": person_id })
    
    ids = [v[0] for v in cur]
    
    #print ids
    return len(ids) == 1

def accuracy_of_graph():
    db = get_db()
    
    cur = db.execute(('SELECT id FROM vertices'))
    person_ids = [v[0] for v in cur]
    
    num_determinable = 0
    for person_id in person_ids:
        if is_determinable(person_id):
            num_determinable += 1
    
    return (num_determinable, 
            len(person_ids), 
            num_determinable / len(person_ids) * 100)

def test_graph_1():
    friends = { 1: { 2, 3, 4 },
                2: { 1, 3 },
                3: { 1, 2, 5, 6 },
                4: { 1, 5, 6 },
                5: { 3, 4, 6 },
                6: { 3, 4, 5, 7 },
                7: { 6 },
                }

    insert_friends(friends)

def main():
    headings = ["Num determinable", "Total", "Percentage"]
    for desc, value in zip(headings,
                           accuracy_of_graph()):
        print "%*s %r" % (max(map(len, headings)), desc, value)
        

if __name__ == "__main__":
    main()
