# Setup & Installation

This section provides step-by-step instructions to help you set up the Automatic Timetable Generation System (ATGS) locally on your machine.

ATGS is made up of two main components:

- **Backend**: Built using Django and Django REST Framework
- **Frontend**: Built using Next.js

---

## 🛠 Prerequisites

Ensure the following are installed on your machine:

- Python 3.9+
- Node.js 16+
- Git
- pip (Python package installer)
- npm or yarn
- Redis (for background task handling or caching)
- Ngrok (for exposing your local server to the internet, useful for testing)

---

## 📦 Backend Setup (Django)

Follow these steps to set up the backend API server:

### 1. Clone the backend repository

```bash:```

```$ git clone https://github.com/ColinAdo/timeable-api.git```

```$ cd timeable-api```

### 2. Create and activate a virtual environment

```bash:```

```$ python -m venv env```

```$ source env/bin/activate - On Linux```

```$ env\Scripts\activate - On Windows```

### 3. Install Python dependencies

```bash:```

```$ pip install -r requirements.txt```

### 4. Create .env.local in the base directory

```Add these to .env.local```

```DEBUG='True'```

```SECRET_KEY=''```

```GROQ_API_KEY=''``` Visit the <a href="https://console.groq.com/keys" target="_blank" rel="noopener noreferrer">Grok Api</a> to generate them.

```DOMAIN='localhost:3000'```

```REDIRECT_URIS='http://localhost:3000/auth/google,http://localhost:3000/auth/github'```

```AWS_SES_FROM_EMAIL=''``` Visit the <a href="https://eu-north-1.signin.aws.amazon.com/oauth?client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&code_challenge=7rFuYmNJszy9M2y-UuLD5rHnQYlewbs96-N7LIXalfU&code_challenge_method=SHA-256&response_type=code&redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26nc2%3Dh_ct%26src%3Dheader-signin%26state%3DhashArgsFromTB_eu-north-1_02fb1af2057815b2"target="_blank" rel="noopener noreferrer">Amazon web service</a> to generate them.


```AWS_SES_ACCESS_KEY_ID=''```

```AWS_SES_SECRET_ACCESS_KEY=''```

```AWS_SES_REGION_NAME=''```

```GOOGLE_OAUTH_KEY=''``` Visit the <a href="https://console.cloud.google.com/welcome?pli=1&invt=AbuCOw&project=libo-421506" target="_blank" rel="noopener noreferrer">Google console</a> to generate them.

```GOOGLE_OAUTH_SECRET=''```

```GITHUB_OAUTH_KEY=''``` Visit the <a href="https://github.com/settings/developers" target="_blank" rel="noopener noreferrer">Github</a> to generate them.

```GITHUB_OAUTH_SECRET=''```

```MPESA_ENVIRONMENT='sandbox'```

```MPESA_CONSUMER_KEY=''``` Visit the <a href="https://developer.safaricom.co.ke/" target="_blank" rel="noopener noreferrer">Daraja</a> to generate them.

```MPESA_CONSUMER_SECRET=''```

```MPESA_PASSKEY=''```

```MPESA_EXPRESS_SHORTCODE='174379'```

### 5. Apply database migrations

```bash:```

```$ python manage.py migrate```

### 6. Run the backend server

```bash:```

```python manage.py runserver```

---

## 🌐 Frontend Setup (Next.js)

Follow these steps to set up the user interface:

### 1. Clone the frontend repository

```bash:```

```$ git clone https://github.com/ColinAdo/timeable-ui.git```

```$ cd timeable-ui```

### 2. Install frontend dependencies

```bash:```

```$ npm install or yarn install```

### 3. Create .env.local for API base URL

```Add these to.env.local:```

```NEXT_PUBLIC_HOST='http://localhost:8000'```

```NEXT_PUBLIC_WS_HOST='ws://localhost:8000'```

### 4. Start the frontend development server

```bash:```

```$ npm run dev or yarn dev```

---

## 🧪 Testing the Setup

Once both servers are running:

- Visit the frontend at `http://localhost:3000`
- Upload sample Excel file (unit code, unit name, academic year, e.g., Year and Semester (Y1S1))
- Generate timetable
- Download and review
