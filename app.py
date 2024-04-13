from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import plotly.express as px

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    portfolios = Portfolio.query.all()
    bills = Bill.query.all()

    total_portfolio_value = sum([portfolio.amount for portfolio in portfolios])
    total_bills_amount = sum([bill.amount for bill in bills])
    total_expenses = total_bills_amount

    monthly_income = request.args.get('monthly_income', type=float, default=0)
    desired_savings = request.args.get('desired_savings', type=float, default=0)
    remaining_money = monthly_income - total_expenses

    # Calculate percentage of income spent and saved
    spent_percentage = (total_expenses / monthly_income) * 100 if monthly_income else 0
    savings_percentage = ((monthly_income - total_expenses - desired_savings) / monthly_income) * 100 if monthly_income else 0

    # AI advice (plcaeholder: will try to call an external API here)
    advice = "Try to reduce your non-essential expenses to increase your savings." if savings_percentage < 20 else "Good job on your savings!"

    table_data = [{'Portfolio': portfolio.name, 'Amount': portfolio.amount} for portfolio in portfolios]
    table_data.extend([{'Bill': bill.name, 'Amount': bill.amount, 'Due Date': bill.due_date} for bill in bills])

    expense_labels = [bill.name for bill in bills]
    expense_values = [bill.amount for bill in bills]

    fig = px.pie(names=expense_labels, values=expense_values, title='Monthly Expenses')
    graph_html = fig.to_html(full_html=False)

    return render_template('index.html', portfolios=portfolios, bills=bills,
                           total_portfolio_value=total_portfolio_value,
                           total_expenses=total_expenses, remaining_money=remaining_money,
                           spent_percentage=spent_percentage, savings_percentage=savings_percentage,
                           advice=advice, table_data=table_data, graph_html=graph_html)



@app.route('/add_portfolio', methods=['POST'])
def add_portfolio():
    name = request.form['portfolio_name']
    amount = float(request.form['portfolio_amount'])

    new_portfolio = Portfolio(name=name, amount=amount)
    db.session.add(new_portfolio)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_bill', methods=['POST'])
def add_bill():
    name = request.form['bill_name']
    amount = float(request.form['bill_amount'])
    due_date = datetime.strptime(request.form['bill_due_date'], '%Y-%m-%d').date()

    new_bill = Bill(name=name, amount=amount, due_date=due_date)
    db.session.add(new_bill)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

