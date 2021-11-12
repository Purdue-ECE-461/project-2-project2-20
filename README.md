gcloud builds submit --tag gcr.io/project2-20/cd-pipeline --project=project2-20

gcloud run deploy cd-pipeline --image gcr.io/project2-20/cd-pipeline --platform managed --region us-central1 --project=project2-20 --allow-unauthenticated




# Switching service accounts

1. gcloud iam service-accounts list

The account you just created should be listed there.

2. gcloud iam service-accounts keys create ./NAME-OF-KEY-FILE.json --iam-account team20-service@project2-20.iam.gserviceaccount.com

If you store it in your app directory, make sure to add it to your .gitignore file.

3. gcloud auth activate-service-account --key-file=NAME-OF-KEY-FILE.json

This way, you can run commands as the service account.

4. gcloud auth list

To go back to account:
1. gcloud config set account YOUR-EMAIL-ADDRESS