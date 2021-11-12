gcloud builds submit --tag gcr.io/project2-20/cd-pipeline --project=project2-20

gcloud run deploy cd-pipeline --image gcr.io/project2-20/cd-pipeline --platform managed --region us-central1 --project=project2-20 --allow-unauthenticated