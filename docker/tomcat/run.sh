docker run -it -d --restart unless-stopped -p 8080:8080 --name tomcat -v tomcat_db:/usr/local/tomcat/ tomcat
