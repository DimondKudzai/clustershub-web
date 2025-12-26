#web: gunicorn app:app
# Source - https://stackoverflow.com/a
# Posted by ACL, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-26, License - CC BY-SA 4.0

gunicorn app:app \
   --workers 1 \
   --worker-class uvicorn.workers.UvicornWorker \
   --bind 0.0.0.0:8443 \
   --timeout 600
