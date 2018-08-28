# Data Ingestion and Publication Service: Data Service for NSW Crime Statistics
Designed an API interface to search for crime statistics across the NSW


// README.txt 
Name: Yuyou Xu

Overview:
A data service API that allows a client to read and store some publicly available crime statistics data, and publish the content in a standard Web data publication format. A pyhton script client is given as well.

Dependencies
1. Python 3.6
2. Flask-RESTful
3. Pycharm
4. Please refer to requirements files to install the python libs needed


Installation Guide 
- How to compile, deploy the service code:
1. unzip the server.zip and client.zip.
2. use Pycharm to import them, and use the 'requirements' file to install all the libs needed.
3. make the server on-line by running views.py.
4. if you want to use the client, 5 python scripts are provided for different goals:
	-post_requests.py: run this script to POST by name or postcode (admin-allowed).
	-get_single_collection.py: run this script to GET specific collection by name-searching.
	-get_collections.py: run this script to GET all existed collections in the database.
	-delete_requests.py: run this script to DELETE specific collection in database by name-searching (admin-		allowed).
	-filter_requests.py: run this script to GET specific collection by following rules mentioned in this file.
	note: you do NOT need to manually run authentication.py to get authentication, because it is imported by 		scripts that need the token such as post_requests.py and delete_requests.py.


- Specification:
For client side:
	1. input examples are given with necessary description in every test script.
	2. for POST and DELETE, you need to input your username and password to get token first. If not passed, 		further operation will contribute to '401 unauthorized' warning.
	3. the response may contain json information or ATOM information with a validated feed.
	4. For GET, no authentication process existed since it is available for all users. 
	5. It is defined that if a person is not admin(i.e., use 'admin' as both username and password), he/she 		must be a guest no matter what are the inputs for username and password.

For server side:
	1. necessary comments are given in all python files.
	2. all operations are available with both the provided Client and Restlet Client.
	3. the mLab database is empty now.

Additions:
	Atom validation: https://validator.w3.org/feed/#validate_by_input
	mLab database: https://mlab.com/databases/9321test 	
	for login to mLab: username:yuyoux password:
	
