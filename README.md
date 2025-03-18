# mahany.io Blog

This document describes the project structure, setup, and useful commands for maintaining and managing the Flask-based blog hosted at [mahany.io](https://mahany.io).

## Project Structure

```
/home/bloguser/blog 
├── app.py # Main Flask application 
├── articles/ # Markdown articles for the blog 
├── templates/ # Jinja2 HTML templates 
├── static/ # Static files (CSS, JS, images) 
├── logs/ # Application logs 
├── venv/ # Python virtual environment 
├── requirements.txt # Python dependencies 
├── run.sh # Simple script to run Gunicorn 
└── nginx.conf # Nginx configuration snippet
```

## Systemd Service Configuration

The blog is automatically managed by systemd using the following service file:

### `/etc/systemd/system/blog.service`

```ini
[Unit]
Description=Gunicorn instance to serve Flask blog
After=network.target nginx.service
Requires=nginx.service

[Service]
User=bloguser
Group=bloguser
WorkingDirectory=/home/bloguser/blog
ExecStart=/home/bloguser/blog/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
Restart=always
RestartSec=5
Environment="PATH=/home/bloguser/blog/venv/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

## Viewlong logs with journalctl
To see the application logs captured by systemd (very useful for debugging):
```
sudo journalctl -u blog.service -f
```

