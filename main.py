from google.cloud import storage
from google.cloud import datastore
import os

datastore_kind = os.environ.get('KIND')
datastore_id = os.environ.get('ID')

def main(request):
    commits = request.get_json()["commits"]
    for commit in commits:
        added = commit["added"]
        commit_id = commit['id']
        url = commit['url']
        timestamp = commit['timestamp']
        for s in added:
            if s.endswith('.png'):
                print(f"PNG file found: {s}")
                png_url = url.replace('commit', 'blob')
                final_url = png_url + '/' + s
                print(f"Saving {final_url} to database")
                client = datastore.Client()
                key = client.key(datastore_kind, datastore_id)
                entity = datastore.Entity(key=key)
                entity.update({
                    'timestamp': timestamp,
                    'url': final_url
                })
                client.put(entity)
                print("URL saved the database.")
            else:
                print(f"Skipping file: {s}")