# 💰 Dynamic Price Tracker

A modern, beautiful web application to track product prices across multiple e-commerce platforms and get notified when prices drop to your target.

## ✨ Features

- **🔍 Smart Product Search**: Search for products by name across multiple platforms
- **Multi-Platform Support**: Track prices from Amazon, Flipkart, Myntra, and Meesho
- **Real-time Monitoring**: Automatic price checking every 30 minutes
- **Smart Alerts**: Get notified when prices drop to your target
- **Price History**: View detailed price trends over time
- **Comparison Tool**: Compare prices across multiple products
- **Smart Recommendations**: AI-powered suggestions for best deals based on price and rating
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Excel Storage**: Simple data storage using Excel files

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd price-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   # Create .env file with your configuration
   cp .env.example .env
   # Edit .env with your email settings
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔍 New: Product Search Feature

### How It Works

1. **Go to Search Page**: Click "Search" in the navigation
2. **Enter Product Name**: Type what you're looking for (e.g., "iPhone 15", "Samsung Galaxy")
3. **Get Results**: View products found across all platforms with prices and ratings
4. **Smart Recommendations**: Get suggestions for best deals based on price and rating
5. **Track Products**: Click "Track" to add products to your price monitoring list

### Search Capabilities

- **Multi-Platform Search**: Searches Amazon, Flipkart, Myntra, and Meesho simultaneously
- **Price Comparison**: See prices across all platforms in one view
- **Rating Information**: View product ratings to make informed decisions
- **Smart Sorting**: Results sorted by relevance, price, and rating
- **One-Click Tracking**: Add products to your tracking list directly from search results

### Example Search Queries

- "iPhone 15 Pro"
- "Samsung Galaxy S24"
- "Nike Air Max"
- "MacBook Pro"
- "Sony Headphones"

## ⚙️ Configuration

Create a `.env` file in the root directory with the following settings:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Email Configuration (for price drop alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# Note: For Gmail, use App Password, not regular password
# Enable 2FA and generate App Password in Google Account settings
```

## 📱 Usage

### Product Search (New!)

1. Go to the Search page
2. Enter a product name
3. View results across all platforms
4. Get smart recommendations
5. Track products with one click

### Adding Products to Track

1. Go to the home page
2. Paste a product URL from supported platforms
3. Optionally set a target price for alerts
4. Click "Start Tracking"

### Supported Platforms

- **Amazon**: amazon.in, amazon.com
- **Flipkart**: flipkart.com
- **Myntra**: myntra.com
- **Meesho**: meesho.com

### Price History

- View detailed price changes over time
- See price trends and variations
- Track when prices hit your target

### Price Comparison

- Compare multiple products at once
- Get price analysis and insights
- Find the best deals across platforms

## 🏗️ Project Structure

```
price-tracker/
├── app/                    # Flask application
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   │   ├── search.html    # NEW: Product search page
│   │   ├── index.html     # Home page
│   │   ├── compare.html   # Price comparison
│   │   └── history.html   # Price history
│   ├── __init__.py        # App factory
│   └── routes.py          # Route definitions (NEW: search route)
├── core/                  # Core functionality
│   ├── tracker.py         # Price tracking logic
│   ├── comparator.py      # Price comparison & search (ENHANCED)
│   └── scheduler.py       # Background tasks
├── etl/                   # Data extraction
│   ├── base.py           # Base scraper
│   ├── amazon.py         # Amazon scraper
│   ├── flipkart.py       # Flipkart scraper
│   └── ...
├── notify/                # Notifications
│   └── emailer.py        # Email alerts
├── storage/               # Data storage
├── data/                  # Excel data files
├── run.py                 # Application entry point
└── requirements.txt       # Python dependencies
```

## 🔧 Development

### Running Tests

```bash
python -m pytest tests/
```

### Testing Search Functionality

```bash
python demo_search.py
```

### Code Style

The project follows PEP 8 style guidelines. Use a linter like `flake8` or `black` for code formatting.

### Adding New Platforms

1. Create a new scraper in the `etl/` directory
2. Implement the required methods
3. Add platform detection in `etl/base.py`
4. Add search function in `core/comparator.py`
5. Update the UI to show the new platform

## 📊 Data Storage

The application uses Excel files for data storage:

- `data/warehouse.xlsx`: Main product data
- `data/history.xlsx`: Price history records

## 🔔 Email Alerts

Configure email settings in your `.env` file to receive price drop notifications:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in your `.env` file

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
2. **Email Not Working**: Check your SMTP settings and App Password
3. **Scraping Fails**: Some websites may block automated requests
4. **Data Not Saving**: Ensure the `data/` directory exists and is writable
5. **Search Not Working**: Check if websites have changed their HTML structure

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask web framework
- Bootstrap for UI components
- Font Awesome for icons
- BeautifulSoup for web scraping
- Pandas for data manipulation

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Happy Price Tracking & Product Searching! 🎉🔍**
