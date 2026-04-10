from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)


# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# DASHBOARD
@app.route('/')
def dashboard():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    return render_template("dashboard.html", products=products)


# ADD PRODUCT
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':

        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        conn = get_db()

        conn.execute(
            "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
            (name, quantity, price)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("add_product.html")


# SELL PRODUCT
@app.route('/sell', methods=['GET', 'POST'])
def sell_product():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':

        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        product = cursor.execute(
            "SELECT quantity, price FROM products WHERE id=?",
            (product_id,)
        ).fetchone()

        current_stock = product["quantity"]
        price = product["price"]

        new_stock = current_stock - quantity
        total = price * quantity

        cursor.execute(
            "UPDATE products SET quantity=? WHERE id=?",
            (new_stock, product_id)
        )

        cursor.execute(
            "INSERT INTO sales (product_id, quantity, total) VALUES (?, ?, ?)",
            (product_id, quantity, total)
        )

        conn.commit()

    products = cursor.execute("SELECT * FROM products").fetchall()
    conn.close()

    return render_template("sell_product.html", products=products)


# SALES HISTORY
@app.route('/sales')
def sales():

    conn = get_db()

    sales = conn.execute("""
        SELECT products.name, sales.quantity, sales.total, sales.date
        FROM sales
        JOIN products ON sales.product_id = products.id
        ORDER BY sales.date DESC
    """).fetchall()

    conn.close()

    return render_template("sales.html", sales=sales)


# API: Daily Revenue for Chart
@app.route('/api/daily_revenue')
def api_daily_revenue():
    conn = get_db()
    rows = conn.execute("SELECT date, SUM(total) FROM sales GROUP BY date ORDER BY date DESC LIMIT 7").fetchall()
    conn.close()
    # Reverse for chronological order
    rows = list(rows)[::-1]
    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    return jsonify({'labels': labels, 'values': values})


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)