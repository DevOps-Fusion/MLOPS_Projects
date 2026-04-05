Overview: Built an ML-based DevOps Issue Prediction system using FastAPI, Docker, and Kubernetes,
capable of classifying common infrastructure issues and providing debugging and resolution steps.

###. Architecture

  User → UI (HTML)
        ↓
    FastAPI
        ↓
    ML Model
        ↓
    Dataset Lookup
        ↓
    Full Response


# 1. Install Dependencies
     pip install -r requirements.txt

# 2. Train ML Model
     python/python3 train.py
    # This will create 
       model.pkl
       vectorizer.pkl
# 3. Build API (FastAPI)
     Run API Locally

     cd app
     uvicorn main:app --reload
 
     Open:
     http://127.0.0.1:8000/doc

     Test:
    /predict?issue=crashloopbackoff
    

# 4. Dockerize the App
     docker build -t devops-ml-app .

     docker run -p 8000:80 devops-ml-app

     Open:
     http://localhost:8000/doc


# 5. Port Forward
  kubectl port-forward pod/prometheus 9090:9090 -n monitoring  ----> Promethus
  kubectl port-forward pod/grafana 3001:3000 -n monitoring     ----> Grafana
  kubectl port-forward svc/devops-ml-service 8090:80 -n default ----> Application
# 6. Access 
     http://localhost:8090/ui -------- Application
     http://localhost:3001 ----> Grafana
     http://localhost:9090 ----> Promethus

