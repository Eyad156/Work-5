from flask import Flask, request , jsonify
from flask_cors import CORS
import process_request
import threading
import os
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)
# Allow all origins during development, tighten this in production
CORS(app,supports_credentials=True)

@app.route("/",methods=["GET", "POST"])
def read_root():
    print('hello world')
    return 'Hello this is Junaid'

@app.route("/instagram",methods=["GET", "POST"])
def instagram():
    print('GOT INSTAGRAM REQUEST')
    try:        
        data = request.json          
        print(data)        
        executor.submit(process_request.process_instagram_request, data)      
        # send status request
        return jsonify({"message":"Recieved request at server"})
    except Exception as e:
        return jsonify({"message":f"Exception in campaign {str(e)}"})

# {'username': 'Junaid ', 'password': 'aslijunaid', 'hashtag': '#alksnc', 'comment': 'kansc', 'privateMessage': 'acns'}
# {'username': 'junaid', 'password': 'aslijunadi', 'limit': '20', 'hashtag': '#acn', 'comment': 'klnacs', 'privateMessage': 'lacnslkanc'}
@app.route("/facebook",methods=["GET", "POST"])
def facebook():
    print('GOT FACEBOOK REQUEST')
    try:
        print(request.form)
        configuration = {
            'username':request.form['username'],
            'password':request.form['password'],
            'groupId':request.form['groupId'].split(','),
            'campaignId':request.form['campaignId']
        }

        if 'publishText' in request.form:
            configuration['publish'] = request.form['publishText']
            if 'imageUrl' in request.files:                
                f = request.files.get('imageUrl')
                print(f.filename)
                configuration['filename'] = f.filename
                try:                
                    f.save(os.path.join('/home/junaid/bot/',f.filename))
                except Exception as e:
                    print(f'Saving file failed : {str(e)}')
                    return jsonify({'message','failed to save file'})

        elif 'comment' in request.form:
            configuration['comment'] = request.form['comment']
            configuration['limit'] = request.form['limit']            
            if 'imageUrl' in request.files:                
                f = request.files.get('imageUrl')
                print(f.filename)
                configuration['filename'] = f.filename
                try:                
                    f.save(os.path.join('/home/junaid/bot/',f.filename))
                except Exception as e:
                    print(f'Saving file failed : {str(e)}')
                    return jsonify({'message','failed to save file'})

        elif 'privateMessage' in request.form:
            configuration['private messages'] = request.form['privateMessage']
            configuration['limit'] = request.form['limit']

        executor.submit(process_request.process_facebook_request, configuration)

        
        return jsonify({"message":"Recieved request at server"})
    
    except Exception as e:        
        return jsonify({"message":f"Exception in campaign {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

# {'username': 'junaid', 'password': 'alsbcjasb', 'groupId': [98236482, 92374092734, 98236482364], 'publish': 'Hello'}
# {'username': 'lksdv', 'password': 'lksnd', 'groupId': [937378, 2929, 296328], 'comment': '5'}
# {'username': 'junaid', 'password': 'alnckasc', 'groupId': [98233, 342, 234], 'private messages': '5'}
