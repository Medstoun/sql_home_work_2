import sqlite3
import json
from flask import Flask, render_template, request, jsonify


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def db_connect(query):
        connection = sqlite3.connect('animal.db')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()

        return result

    @app.route('/animals/<int:idx>')
    def animals(idx):
        query = f"""
            SELECT 
            animals_final.id,
            animals_final.outcome_id,
            animals_final.name,
            animals_final.breed,
            animals_colors.*,
            colors.*,
            outcome.*
            FROM animals_final
            JOIN animals_colors
            ON animals_colors.animals_id = animals_final.id 
            JOIN colors
            ON colors.id = animals_colors.colors_id
            LEFT JOIN outcome
            ON outcome.id = animals_final.outcome_id
            WHERE animals_final.id = {idx}
            LIMIT 1
        """
        response = db_connect(query)
        response_json = []
        for i in response:
            response_json.append(i)
        return jsonify(response_json)

    app.run()


if __name__ == '__main__':
    main()
