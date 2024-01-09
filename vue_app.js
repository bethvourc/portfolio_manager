new Vue({
    el: '#app',
    data: {
        portfolios: [], // Assuming portfolios is initially empty
        bills: [],      // Assuming bills is initially empty
        total_portfolio_value: 0,
        total_expenses: 0,
        remaining_money: 0,
        newPortfolio: {
            name: '',
            amount: 0
        },
        newBill: {
            name: '',
            amount: 0,
            due_date: ''
        },
        monthlyIncome: 0,
        table_data: [],
        graph_html: ''
    },
    methods: {
        addPortfolio: function () {
            // Assuming you have a route for adding a portfolio through an API
            // You need to update this part based on your backend API structure
            axios.post('/add_portfolio', this.newPortfolio)
                .then(response => {
                    // Assuming the API returns the updated list of portfolios
                    this.portfolios = response.data.portfolios;
                    this.newPortfolio = { name: '', amount: 0 };
                })
                .catch(error => {
                    console.error('Error adding portfolio:', error);
                });
        },
        addBill: function () {
            // Assuming you have a route for adding a bill through an API
            // You need to update this part based on your backend API structure
            axios.post('/add_bill', this.newBill)
                .then(response => {
                    // Assuming the API returns the updated list of bills
                    this.bills = response.data.bills;
                    this.newBill = { name: '', amount: 0, due_date: '' };
                })
                .catch(error => {
                    console.error('Error adding bill:', error);
                });
        },
        calculateExpenses: function () {
            // Assuming you have a route for calculating expenses through an API
            // You need to update this part based on your backend API structure
            axios.get('/', { params: { monthly_income: this.monthlyIncome } })
                .then(response => {
                    this.total_expenses = response.data.total_expenses;
                    this.remaining_money = response.data.remaining_money;
                })
                .catch(error => {
                    console.error('Error calculating expenses:', error);
                });
        }
    },
    mounted: function () {
        // Fetch initial data when the component is mounted
        axios.get('/')
            .then(response => {
                this.portfolios = response.data.portfolios;
                this.bills = response.data.bills;
                this.total_portfolio_value = response.data.total_portfolio_value;
                this.total_expenses = response.data.total_expenses;
                this.remaining_money = response.data.remaining_money;
                this.table_data = response.data.table_data;
                this.graph_html = response.data.graph_html;
            })
            .catch(error => {
                console.error('Error fetching initial data:', error);
            });
    }
});
