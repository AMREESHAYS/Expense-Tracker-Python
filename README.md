# Expense Tracker That Yells at You

A modern, user-friendly desktop application for tracking expenses, managing budgets, and visualizing spending habits. Built with Python, Tkinter, and ttkbootstrap for a beautiful, responsive UI. Includes premium features like OCR receipt scanning and customizable settings.

---

## Features

- **Expense Management**: Add, view, and categorize your expenses with ease.
- **Budgeting**: Set monthly budgets for each category and get notified if you overspend.
- **Reports & Analytics**: Visualize your spending by category with interactive pie charts.
- **Premium UI**: Clean, modern interface with theme and currency selection.
- **Category Management**: Add or remove categories as you wish.
- **OCR Receipt Scanning**: Extract text from receipts using built-in OCR (premium feature).
- **Persistent Settings**: All preferences and categories are saved for future sessions.

---

## Screenshots

![image](https://github.com/user-attachments/assets/6229e709-5de1-4934-aa08-23add097f5af)
![image](https://github.com/user-attachments/assets/ac41c597-8be0-4700-84f1-02c31a4392a7)
![image](https://github.com/user-attachments/assets/8bc05d91-f3cf-4319-a876-8e4e11dd8007)


---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd expense-tracker
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

### Running the App
```sh
python main.py
```

---

## Usage

- **Expenses Tab**: Add new expenses by entering the date, amount, category, and description. All expenses are listed in a table.
- **Budgets Tab**: Set a budget for any category. The app will notify you if you exceed your budget.
- **Reports Tab**: Click "Generate Report" to see a pie chart of your spending by category.
- **Settings Tab**:
  - Change currency and theme.
  - Add or remove categories.
  - Use the OCR feature to scan receipts and extract text.

---

## Configuration & Data
- **config.json**: Stores your selected currency and categories.
- **expenses.db**: SQLite database for all expenses and budgets.
- **assets/**: Place for icons and images.

---

## OCR Feature
- Click "Scan Receipt" in the Settings tab.
- Select an image file (JPG, PNG, JPEG).
- Extracted text will be shown in a popup.

---

## Customization
- **Themes**: Choose between auto, light, or dark mode in Settings.
- **Categories**: Add or remove categories as needed. All changes are saved.
- **Currency**: Select your preferred currency symbol.

---

## Troubleshooting
- If you see a database or SQL error, ensure you are using Python 3.8+ and have the correct permissions.
- For OCR, make sure you have the required packages installed (see `requirements.txt`).
- If the UI does not display correctly, try updating `ttkbootstrap` and `tkinter`.

---

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the MIT License.

---

## Credits
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [pytesseract](https://github.com/madmaze/pytesseract) (for OCR)

---

Enjoy tracking your expenses with a little extra motivation!
