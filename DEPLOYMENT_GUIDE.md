# Deployment Guide - Real Estate Analytics Dashboard

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is the easiest and free way to deploy your dashboard.

#### Prerequisites:
- GitHub account
- Your code in a GitHub repository

#### Steps:

1. **Prepare Your Repository**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - Real Estate Dashboard"
   
   # Create GitHub repo and push
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `dashboard.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://YOUR_USERNAME-YOUR_REPO_NAME.streamlit.app`

#### Important Notes:
- The Excel file (`data/real_estate_curation_project.xlsx`) will be included in deployment
- Free tier includes: 1 GB RAM, shared CPU
- App sleeps after inactivity but wakes up when accessed

---

### Option 2: Heroku (Paid)

#### Prerequisites:
- Heroku account
- Heroku CLI installed

#### Steps:

1. **Create Procfile**
   ```bash
   echo "web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

---

### Option 3: AWS EC2

#### Steps:

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.medium or larger (for ML models)
   - Open port 8503 in security group

2. **SSH into instance and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3-pip python3-venv -y
   
   # Clone your repo
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run with nohup
   nohup streamlit run dashboard.py --server.port=8503 --server.address=0.0.0.0 &
   ```

3. **Access at:** `http://your-ec2-ip:8503`

4. **Optional: Setup with systemd for auto-restart**
   ```bash
   sudo nano /etc/systemd/system/dashboard.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Real Estate Dashboard
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/YOUR_REPO_NAME
   Environment="PATH=/home/ubuntu/YOUR_REPO_NAME/venv/bin"
   ExecStart=/home/ubuntu/YOUR_REPO_NAME/venv/bin/streamlit run dashboard.py --server.port=8503 --server.address=0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable dashboard
   sudo systemctl start dashboard
   sudo systemctl status dashboard
   ```

---

### Option 4: Docker (Any Platform)

#### Steps:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8503
   
   CMD ["streamlit", "run", "dashboard.py", "--server.port=8503", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   docker build -t real-estate-dashboard .
   docker run -p 8503:8503 real-estate-dashboard
   ```

3. **Deploy to Docker Hub**
   ```bash
   docker tag real-estate-dashboard YOUR_USERNAME/real-estate-dashboard
   docker push YOUR_USERNAME/real-estate-dashboard
   ```

---

### Option 5: Azure App Service

#### Steps:

1. **Install Azure CLI**
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Login and Deploy**
   ```bash
   az login
   az webapp up --name your-app-name --runtime "PYTHON:3.11"
   ```

---

### Option 6: Google Cloud Run

#### Steps:

1. **Create Dockerfile** (same as Option 4)

2. **Deploy**
   ```bash
   gcloud run deploy real-estate-dashboard \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Excel file in `data/` folder
- [ ] `.gitignore` configured
- [ ] Test locally: `py -m streamlit run dashboard.py`
- [ ] Test models: `py test_models.py`
- [ ] Remove sensitive data (if any)
- [ ] Update README with deployment URL

---

## 🔧 Configuration Files

### requirements.txt
Already created with all dependencies:
- pandas
- openpyxl
- streamlit
- plotly
- scikit-learn
- statsmodels
- seaborn

### .streamlit/config.toml
Already created with theme and server settings

### runtime.txt
Specifies Python version for deployment

---

## 🌐 Custom Domain (Optional)

### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Update DNS records

### For Other Platforms:
1. Purchase domain (Namecheap, GoDaddy, etc.)
2. Point A record to your server IP
3. Setup SSL with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 📊 Monitoring & Maintenance

### Streamlit Cloud:
- Built-in analytics
- View logs in dashboard
- Auto-updates on git push

### Self-Hosted:
- Monitor with `htop` or `top`
- Check logs: `journalctl -u dashboard -f`
- Setup alerts with CloudWatch/Datadog

---

## 🔒 Security Best Practices

1. **Environment Variables**
   - Use `.streamlit/secrets.toml` for sensitive data
   - Never commit secrets to git

2. **Authentication** (if needed)
   ```python
   import streamlit as st
   
   def check_password():
       def password_entered():
           if st.session_state["password"] == "your_password":
               st.session_state["password_correct"] = True
           else:
               st.session_state["password_correct"] = False
       
       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           st.error("😕 Password incorrect")
           return False
       else:
           return True
   
   if check_password():
       # Your dashboard code here
       pass
   ```

3. **HTTPS**
   - Always use HTTPS in production
   - Streamlit Cloud provides this automatically

---

## 💰 Cost Estimates

### Streamlit Cloud (Community)
- **FREE**
- 1 GB RAM
- Shared CPU
- Perfect for this project

### Heroku
- **$7-25/month**
- Hobby/Basic tier

### AWS EC2
- **$10-50/month**
- t2.medium: ~$30/month
- t2.small: ~$15/month

### Google Cloud Run
- **Pay per use**
- ~$5-20/month for moderate traffic

### Azure App Service
- **$13-55/month**
- Basic tier

---

## 🚨 Troubleshooting

### Issue: App crashes on startup
**Solution:** Check logs, ensure all dependencies installed

### Issue: Models take too long to train
**Solution:** 
- Cache model training results
- Use smaller dataset for demo
- Upgrade server resources

### Issue: Excel file not found
**Solution:** Ensure `data/` folder is committed to git

### Issue: Out of memory
**Solution:**
- Reduce data size
- Upgrade to larger instance
- Optimize model training

---

## 📞 Support

For deployment issues:
1. Check Streamlit docs: https://docs.streamlit.io/
2. Streamlit forum: https://discuss.streamlit.io/
3. GitHub issues

---

## ✅ Quick Deploy (Streamlit Cloud)

**Fastest way to deploy:**

1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Click "New app"
4. Select repo and `dashboard.py`
5. Deploy!

**Done! Your dashboard is live! 🎉**
