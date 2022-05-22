from fabistrano import deploy

env.hosts = ["HOST"] # Replace with your host name or IP
env.base_dir = '/var/www' # Set to your app's directory
env.app_name = 'machine' # This will deploy the app to /www/app_name.com/
env.git_clone = 'GIT_PATH' # Your git url
