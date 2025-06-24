from flask  import Flask

sap=Flask(__name__)

@sap.route('/')
def home():
    return "Hello World"

if __name__=="__main__":
    sap.run(debug=True)
