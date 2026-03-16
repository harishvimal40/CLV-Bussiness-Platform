# SmartCLV Deployment Guide

## Local Deployment

### Quick Start

**1. System Requirements**
- Operating System: Windows 10/11, macOS, or Linux
- Python: 3.8 or higher
- RAM: 8GB minimum (16GB recommended)
- Storage: 2GB free space

**2. Installation Steps**

```powershell
# Navigate to project directory
cd SmartCLV

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**3. Database Setup**

```powershell
# Create database schema
python scripts/setup_database.py

# Generate synthetic data (10,000 customers)
python scripts/generate_synthetic_data.py

# Validate data integrity
python scripts/validate_data.py
```

**4. Run Data Pipeline**

```powershell
# Execute full pipeline (data → models → predictions)
python src/main_pipeline.py
```

This will:
- Clean data
- Engineer features
- Train models
- Generate predictions
- Create recommendations
- Generate SHAP explanations

**5. Launch Dashboard**

```powershell
streamlit run dashboard/app.py
```

Access at: `http://localhost:8501`

---

## Production Deployment

### Option 1: Heroku Deployment

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**

1. **Create Heroku App**
```bash
heroku create smartclv-app
```

2. **Add Buildpack**
```bash
heroku buildpacks:set heroku/python
```

3. **Create Procfile**
```
web: streamlit run dashboard/app.py --server.port=$PORT --server.address=0.0.0.0
```

4. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

5. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

6. **Open App**
```bash
heroku open
```

---

### Option 2: AWS EC2 Deployment

**1. Launch EC2 Instance**
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t2.medium (4GB RAM)
- Security Group: Allow ports 22 (SSH), 8501 (Streamlit)

**2. Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**3. Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

**4. Clone Repository**
```bash
git clone <your-repo-url>
cd SmartCLV
```

**5. Setup Application**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**6. Run with PM2 (Process Manager)**
```bash
# Install PM2
sudo npm install -g pm2

# Create ecosystem file
pm2 start "streamlit run dashboard/app.py" --name smartclv

# Save PM2 config
pm2 save
pm2 startup
```

**7. Setup Nginx (Optional)**
```bash
sudo apt install nginx -y

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/smartclv
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/smartclv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 3: Docker Deployment

**1. Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**2. Create .dockerignore**
```
venv/
__pycache__/
*.pyc
.git/
.env
data/smartclv.db
```

**3. Build Image**
```bash
docker build -t smartclv:latest .
```

**4. Run Container**
```bash
docker run -p 8501:8501 -v $(pwd)/data:/app/data smartclv:latest
```

**5. Docker Compose (Optional)**

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  smartclv:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## Environment Configuration

### Environment Variables

Create `.env` file:
```
# Database
DB_PATH=data/smartclv.db

# Model Paths
CLV_MODEL_PATH=models/clv_models/best_model.pkl
CHURN_MODEL_PATH=models/churn_models/best_churn_model.pkl

# Data Paths
DATA_DIR=data/processed/
IMAGES_DIR=dashboard/assets/images/

# Application
DEBUG=False
LOG_LEVEL=INFO
```

### Configuration Management

Use `config/config.py`:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).parent.parent
    DB_PATH = os.getenv('DB_PATH', 'data/smartclv.db')
    MODEL_DIR = BASE_DIR / 'models'
    DATA_DIR = BASE_DIR / 'data' / 'processed'
    
config = Config()
```

---

## Database Migration

### From SQLite to PostgreSQL (Production)

**1. Install PostgreSQL**
```bash
sudo apt install postgresql postgresql-contrib
```

**2. Create Database**
```sql
CREATE DATABASE smartclv;
CREATE USER smartclv_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smartclv TO smartclv_user;
```

**3. Update Connection String**
```python
# In scripts/setup_database.py
import psycopg2

conn = psycopg2.connect(
    dbname="smartclv",
    user="smartclv_user",
    password="your_password",
    host="localhost"
)
```

**4. Migrate Data**
```bash
# Export from SQLite
sqlite3 data/smartclv.db .dump > dump.sql

# Import to PostgreSQL
psql smartclv < dump.sql
```

---

## Monitoring & Logging

### Application Logging

Add to `dashboard/app.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Performance Monitoring

Use Streamlit's built-in profiler:
```python
import streamlit as st

@st.cache_data
def expensive_computation():
    # Your code here
    pass
```

---

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to git
2. **Database Credentials**: Use secrets management (AWS Secrets Manager, HashiCorp Vault)
3. **HTTPS**: Use SSL certificates (Let's Encrypt)
4. **Authentication**: Add login system for production
5. **Input Validation**: Sanitize all user inputs
6. **Rate Limiting**: Prevent API abuse
7. **Regular Updates**: Keep dependencies updated

---

## Backup & Recovery

### Database Backup

**Automated Backup Script:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# Backup database
cp data/smartclv.db $BACKUP_DIR/smartclv_$DATE.db

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz models/

# Keep only last 7 days
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

**Schedule with Cron:**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, AWS ALB)
- Deploy multiple Streamlit instances
- Share database across instances

### Vertical Scaling
- Increase EC2 instance size
- Add more RAM for larger datasets
- Use GPU for model training (AWS p2/p3 instances)

### Caching Strategy
- Redis for session data
- CDN for static assets
- Database query caching

---

## Troubleshooting Deployment

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 8501
lsof -i :8501
# Kill process
kill -9 <PID>
```

**Permission Denied:**
```bash
# Fix file permissions
chmod +x scripts/*.py
```

**Module Not Found:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

**Database Locked:**
```bash
# Check for active connections
fuser data/smartclv.db
# Kill if necessary
```

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review application logs
- Check disk space
- Monitor memory usage

**Monthly:**
- Update dependencies
- Retrain models with new data
- Review and optimize queries

**Quarterly:**
- Security audit
- Performance optimization
- Backup verification

---

## Support & Resources

- **Documentation**: `docs/`
- **Issues**: GitHub Issues
- **Community**: Stack Overflow tag `smartclv`
- **Updates**: Check releases for new features
