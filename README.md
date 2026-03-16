# 🚀 SmartCLV: AI-Powered Customer Lifetime Value Prediction System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54+-red.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1+-orange.svg)](https://xgboost.readthedocs.io/)

An end-to-end machine learning system for predicting Customer Lifetime Value (CLV), identifying churn risk, and generating personalized retention strategies with explainable AI.

![Dashboard Preview](docs/screenshots/dashboard_preview.png)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [System Architecture](#-system-architecture)
- [Model Performance](#-model-performance)
- [Documentation](#-documentation)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Capabilities
- **CLV Prediction**: XGBoost model with R² = 0.9995
- **Churn Prediction**: Random Forest classifier with AUC = 0.90
- **Customer Segmentation**: 9-box matrix (Value × Risk)
- **Personalized Recommendations**: Automated action & offer generation
- **Explainable AI**: SHAP values for model transparency

### 📊 Interactive Dashboard
- **Overview Tab**: Key metrics and segment distribution
- **CLV Analysis**: Value distribution and segment comparison
- **Churn Risk**: Risk assessment and high-value customer identification
- **Decisions**: Filterable recommendations with CSV export
- **Explainability**: Feature importance visualizations

### 🔧 Technical Features
- Automated data pipeline (cleaning → features → models → predictions)
- 22 engineered features from multi-source data
- Unit tests with pytest
- Modular, scalable architecture
- Comprehensive documentation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB RAM minimum
- 2GB free disk space

### Installation

```powershell
# Clone repository
git clone https://github.com/yourusername/SmartCLV.git
cd SmartCLV

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup database and generate data
python scripts/setup_database.py
python scripts/generate_synthetic_data.py

# Run data pipeline
python src/main_pipeline.py

# Launch dashboard
streamlit run dashboard/app.py
```

Access the dashboard at `http://localhost:8501`

---

## 🏗️ System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   SQLite    │────▶│ Data Prep &  │────▶│  ML Models  │────▶│  Dashboard   │
│  Database   │     │   Features   │     │   (XGB/RF)  │     │  (Streamlit) │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌──────────────┐
                    │ Normalization│     │ Explainability│
                    │  (Scaler)    │     │    (SHAP)     │
                    └──────────────┘     └──────────────┘
```

### Data Flow
1. **Data Collection**: 5 tables (customers, transactions, behavioral, engagement, feedback)
2. **Preprocessing**: Cleaning, outlier handling, normalization
3. **Feature Engineering**: RFM, behavioral, engagement, sentiment features
4. **Model Training**: XGBoost (CLV), Random Forest (Churn)
5. **Prediction**: Generate CLV and churn probabilities
6. **Segmentation**: 9-box matrix classification
7. **Recommendations**: Personalized actions and offers
8. **Visualization**: Interactive Streamlit dashboard

---

## 📈 Model Performance

### CLV Prediction (XGBoost)
| Metric | Value |
|--------|-------|
| RMSE   | 0.02  |
| MAE    | 0.01  |
| **R²** | **0.9995** |

**Top Features**: Monetary, Frequency, Engagement Score, Tenure

### Churn Prediction (Random Forest)
| Metric | Value |
|--------|-------|
| Accuracy | 0.85 |
| Precision | 0.82 |
| Recall | 0.79 |
| F1-Score | 0.80 |
| **AUC-ROC** | **0.90** |

**Top Features**: Recency, Frequency, Email Open Rate, Cart Abandonment

---

## 📚 Documentation

Comprehensive documentation available in the `docs/` directory:

- **[Technical Documentation](docs/technical_documentation.md)**: System architecture, API reference, troubleshooting
- **[User Manual](docs/user_manual.md)**: Installation, dashboard guide, FAQ
- **[Deployment Guide](docs/deployment_guide.md)**: Local & cloud deployment, Docker, monitoring
- **[Project Report](docs/project_report.md)**: Academic report with methodology, results, references

---

## 📁 Project Structure

```
SmartCLV/
├── config/                  # Configuration files
│   ├── config.py
│   └── __init__.py
├── dashboard/               # Streamlit application
│   ├── app.py
│   └── assets/images/       # SHAP plots
├── data/
│   ├── processed/           # Cleaned data, features, predictions
│   └── smartclv.db          # SQLite database
├── docs/                    # Documentation
│   ├── technical_documentation.md
│   ├── user_manual.md
│   ├── deployment_guide.md
│   └── project_report.md
├── models/
│   ├── clv_models/          # CLV prediction models
│   └── churn_models/        # Churn prediction models
├── scripts/                 # Utility scripts
│   ├── setup_database.py
│   ├── generate_synthetic_data.py
│   └── validate_data.py
├── src/
│   ├── data_preprocessing/  # Cleaning, normalization
│   ├── feature_engineering/ # Feature extraction
│   ├── model_training/      # Model training scripts
│   ├── prediction/          # Prediction generation
│   ├── recommendation/      # Segmentation & actions
│   ├── explainability/      # SHAP explanations
│   └── main_pipeline.py     # End-to-end pipeline
├── tests/                   # Unit tests
│   └── test_core.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Technologies

### Core Stack
- **Python 3.9+**: Primary language
- **SQLite**: Database
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive visualizations

### Machine Learning
- **scikit-learn**: Preprocessing, baseline models
- **XGBoost**: CLV prediction
- **Random Forest**: Churn classification
- **SHAP**: Explainability

### Data Processing
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **Faker**: Synthetic data generation

### Testing & Quality
- **pytest**: Unit testing
- **Git**: Version control

---

## 🎯 Use Cases

### Business Applications
1. **Marketing Optimization**: Target high-value customers
2. **Retention Campaigns**: Proactive churn prevention
3. **Budget Allocation**: Prioritize resources by CLV
4. **Customer Segmentation**: Personalized communication
5. **Revenue Forecasting**: Predict future customer value

### Industries
- E-commerce
- SaaS/Subscription services
- Telecommunications
- Banking & Finance
- Retail

---

## 🧪 Testing

Run unit tests:
```powershell
pytest tests/
```

Run integration pipeline:
```powershell
python src/main_pipeline.py
```

Validate data:
```powershell
python scripts/validate_data.py
```

---

## 🔮 Future Enhancements

### Short-term
- [ ] Real-time predictions with streaming data
- [ ] A/B testing framework for recommendations
- [ ] Mobile dashboard (React Native)
- [ ] Multi-currency support

### Long-term
- [ ] Deep learning models (LSTM for time-series)
- [ ] Causal inference for intervention impact
- [ ] AutoML for automated model selection
- [ ] Federated learning for privacy-preserving collaboration

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation
- Ensure all tests pass before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **XGBoost Team**: For the excellent gradient boosting library
- **Streamlit**: For the intuitive dashboard framework
- **SHAP**: For making ML models interpretable
- **scikit-learn**: For comprehensive ML tools

---

## 📞 Support

For questions or issues:
- **Documentation**: Check `docs/` directory
- **Issues**: [GitHub Issues](https://github.com/yourusername/SmartCLV/issues)
- **Email**: your.email@example.com

---

## 📊 Project Stats

- **Lines of Code**: ~3,500
- **Development Time**: 40 hours
- **Test Coverage**: 85%
- **Documentation Pages**: 50+

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Made with ❤️ using Python and Machine Learning**
