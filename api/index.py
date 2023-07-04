import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from Modules.website_content_scrape import Website_Scrape
from Modules.scrape_resume import Pdf_Scrape
from Modules.publications import Get_Published_Papers

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


ALLOWED_EXTENSIONS = set(["pdf"])
app.config["UPLOAD_FOLDER"] = "upload"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    # check if the post request has the file part
    if "file" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp
    file = request.files["file"]
    if file.filename == "":
        resp = jsonify({"message": "No file selected for uploading"})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], "resume.pdf"))
        d = Pdf_Scrape("./Resume.pdf", "./resume.txt")
        resume = d.scrape()
        # store this in the DB
        resp = jsonify({"message": "File successfully and read successfully"})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({"message": "Allowed file types are pdf only."})
        resp.status_code = 400
        return resp


@app.route("/read_professor_website", methods=["GET"])
def read_professor_website():
    url = request.args["url"]
    e = Website_Scrape(url, "./professor.txt")
    professors_website = e.scrape()
    professors_website = professors_website[
        :6000
    ]  # make a hard limit of 6000 characters
    # send this to database
    resp = jsonify({"message": "File successfully and read successfully"})
    resp.status_code = 201
    return resp


@app.route("/read_google_scholar", methods=["GET"])
def read_google_scholar():
    url = request.args["url"]
    c = Get_Published_Papers(url)
    publications = c.extract_papers()
    print(publications)
    # send this to database
    resp = jsonify({"message": "File successfully and read successfully"})
    resp.status_code = 201
    return resp

