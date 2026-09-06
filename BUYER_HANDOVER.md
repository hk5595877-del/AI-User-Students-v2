# StudentGPA AI — Buyer Handover Guide

## 1. Purpose

This document provides a technical handover guide for a future owner or authorized maintainer of StudentGPA AI.

It describes the main project assets, services, configuration requirements, and recommended transfer process.

---

## 2. Project

Project name:

StudentGPA AI

Application type:

Streamlit machine learning web application

Primary purpose:

Estimate student Post-Semester GPA using academic, study-habit, and Generative AI usage characteristics.

---

## 3. Main Assets

The project includes the following important assets:

- Application source code
- Machine learning model
- Model training script
- Dataset
- Model evaluation metrics
- Streamlit deployment configuration
- Authentication integration
- Analytics integration
- Technical documentation
- Legal and licensing documentation

---

## 4. Core Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main application |
| `train_model.py` | Model training pipeline |
| `model.joblib` | Trained machine learning model |
| `model_metrics.json` | Model evaluation metrics |
| `ai_student_impact_dataset.csv` | Training dataset |
| `requirements.txt` | Runtime dependencies |
| `pyproject.toml` | Project configuration |
| `Dockerfile` | Container deployment |
| `sample-input.json` | Example input |
| `README.md` | Project overview |

---

## 5. Documentation

The repository contains additional documentation covering:

- System architecture
- Machine learning model
- Deployment
- Dataset licensing
- Third-party licenses
- Intellectual property
- Privacy
- Terms of service
- Project authorship

Important documentation files include:

- `ARCHITECTURE.md`
- `MODEL_DOCUMENTATION.md`
- `DEPLOYMENT.md`
- `PROJECT_AUTHORS.md`
- `THIRD_PARTY_NOTICES.md`
- `DATASET_NOTICE.md`
- `IP_AND_OWNERSHIP.md`
- `PRIVACY_POLICY.md`
- `TERMS_OF_SERVICE.md`

---

## 6. Machine Learning Model

The application uses a locally stored CatBoost regression model.

Model file:

`model.joblib`

Training script:

`train_model.py`

Evaluation metrics:

`model_metrics.json`

The model predicts:

`Post_Semester_GPA`

The model should be tested in the buyer's environment before being used in production.

---

## 7. Dataset

The project uses the AI Student Impact Dataset.

The dataset is identified as CC0 / Public Domain on its Kaggle dataset page.

The project does not claim exclusive ownership of the underlying third-party dataset.

The buyer should review the dataset notice and applicable licensing information before redistributing the dataset independently of the application.

---

## 8. Authentication

The application uses Supabase for authentication.

The buyer should establish control of the appropriate Supabase project or create a new project.

The buyer should verify:

- Authentication settings
- Email/password authentication
- User registration
- User login
- User logout
- Any database configuration used by the application
- Security policies

Credentials should be regenerated or securely transferred.

They should never be stored in GitHub source code.

---

## 9. Analytics

The application may use Google Analytics to measure application activity and selected events.

The buyer should create or obtain control of the appropriate analytics property or replace the existing configuration.

The buyer should verify:

- Measurement ID
- Data stream
- Event tracking
- Analytics privacy settings
- Ownership/access permissions

---

## 10. Streamlit Deployment

The application can be deployed using Streamlit Community Cloud.

The buyer should verify ownership/control of the deployment after acquisition.

The deployment configuration includes:

- GitHub repository
- Application entry point
- Python dependencies
- Streamlit secrets
- Required third-party service configuration

---

## 11. Secrets and Credentials

The following types of information must not be committed to the repository:

- Supabase keys
- Passwords
- API keys
- Private tokens
- Service-account credentials
- Private certificates
- Other authentication secrets

The buyer should receive access through secure account-transfer procedures or regenerate credentials.

---

## 12. Recommended Transfer Process

A technical transfer should generally follow this sequence:

### Step 1 — Repository

Transfer or provide appropriate access to the GitHub repository.

Verify:

- Repository access
- Branches
- Commit history
- Issues
- Deployment configuration

### Step 2 — Application Deployment

Transfer or recreate the Streamlit deployment.

Verify that the application starts successfully.

### Step 3 — Authentication

Transfer or recreate the Supabase configuration.

Verify registration and login.

### Step 4 — Analytics

Transfer or recreate the Google Analytics configuration.

Verify tracked events.

### Step 5 — Machine Learning

Verify:

- `model.joblib`
- `train_model.py`
- `model_metrics.json`
- Dataset
- Required Python dependencies

### Step 6 — Testing

Perform complete application testing.

### Step 7 — Documentation

Review all project documentation with the new owner.

---

## 13. Post-Transfer Testing

The buyer should test the following functionality:

### Authentication

- Account creation
- Login
- Logout
- Invalid login handling

### Student Prediction

- Valid input
- Invalid input
- Prediction generation
- Result display

### Institute Prediction

- CSV upload
- Required-column validation
- Batch prediction
- Result generation

### SSC / HSSC Prediction

- Percentage input
- GPA conversion
- Prediction
- Percentage output

### Analytics

- Application visits
- Relevant tracked events
- Analytics reporting

---

## 14. Intellectual Property

The seller represents only those rights that the seller actually owns or is legally entitled to transfer.

Original project materials are subject to the applicable project license and ownership documentation.

Third-party software, datasets, libraries, services, and other materials remain subject to their respective licenses and terms.

The buyer should review:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `DATASET_NOTICE.md`
- `IP_AND_OWNERSHIP.md`

before commercial redistribution.

---

## 15. Third-Party Dependencies

The application relies on third-party technologies and services.

These may include:

- Streamlit
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- Joblib
- Supabase
- Google Analytics
- Streamlit Community Cloud

These technologies are not claimed as proprietary assets of the project author.

Their respective licenses and service terms continue to apply.

---

## 16. Reference Materials

During development, external repositories and resources may have been consulted for general reference, architecture, development patterns, or implementation ideas.

The project's ownership documentation should be reviewed for the distinction between independently developed project materials and third-party materials.

Third-party code should remain subject to its applicable license where applicable.

---

## 17. Known Configuration Requirements

Before deployment, the buyer should verify:

- Python version
- Dependency versions
- Streamlit configuration
- Supabase credentials
- Analytics configuration
- Model file
- Dataset
- Required secrets
- CSV input format

---

## 18. Recommended Security Review

After acquisition, the buyer should perform a security review covering:

- Git history
- Repository secrets
- Authentication
- Supabase policies
- Uploaded-file handling
- Analytics configuration
- Dependency vulnerabilities
- Application logs
- Access permissions

Any credentials previously used by the seller should be rotated when appropriate.

---

## 19. Recommended Product Review

The buyer should independently evaluate:

- Prediction accuracy
- Dataset quality
- Model generalization
- User experience
- Authentication security
- Privacy compliance
- Scalability
- Infrastructure costs
- Commercial viability

The model's historical validation metrics should not be treated as a guarantee of future performance.

---

## 20. Commercial Expansion Opportunities

Potential future product opportunities include:

- Premium student accounts
- Institute subscriptions
- Advanced student analytics
- Prediction history
- Personalized academic coaching
- Institute dashboards
- Administrative reporting
- Subscription plans
- Custom institutional deployments
- Custom domains
- Additional predictive models

These are potential future opportunities and are not necessarily current application functionality.

---

## 21. Final Handover Checklist

Before considering the technical transfer complete:

- [ ] GitHub access transferred
- [ ] Streamlit deployment transferred/recreated
- [ ] Supabase access transferred/recreated
- [ ] Analytics access transferred/recreated
- [ ] Required secrets configured
- [ ] Model verified
- [ ] Dataset verified
- [ ] Dependencies installed
- [ ] Student prediction tested
- [ ] Institute prediction tested
- [ ] SSC/HSSC prediction tested
- [ ] Authentication tested
- [ ] Analytics tested
- [ ] Documentation reviewed
- [ ] Security review completed
- [ ] Buyer confirms successful deployment

---

## 22. Important Notice

This document is a technical handover guide and does not itself constitute a transfer of intellectual property, ownership, accounts, licenses, or contractual rights.

Any acquisition or transfer should be documented through a separate written agreement appropriate to the transaction.

---

## 23. Current Public Application

Current application:

https://studentgpa-ai.streamlit.app/

The deployment URL may change following a transfer of ownership or infrastructure.
