* Download python search this in browser

      https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe

* Install some prerequisites
   Opem terminal or command prompt

      pip install flask
  
      pip install opencv-python
  
      pip install opencv-contrib-python
  
      pip install numpy
  
      pip install pysqlite3
  
      pip install flask-sqlalchemy
  
      pip install opencv-contrib-python==4.5.5.64
      
* Clone the repository:
  Open a terminal or command prompt.
  Use the git clone command followed by the URL of the GitHub repository to clone the code to your local machine:

      git clone -b Aditya_Raj https://github.com/springboardmentor0328/Image_Recognition_System_Infosys_Internship_Oct2024.git

* Navigate to the project directory:

      cd Image_Recognition_System_Infosys_Internship_Oct2024

* Create a virtual environment:

      python -m venv venv

* Activate the virtual environment:

  On Windows:

      venv\Scripts\activate

  On macOS and Linux:

      source venv/bin/activate

* Install dependencies:

      pip install -r requirements.txt

* Set the Flask application environment:

  On Windows:

      set FLASK_APP=app.py

  On macOS and Linux:

      export FLASK_APP=app.py
  
* Run the Flask app:
    flask run
