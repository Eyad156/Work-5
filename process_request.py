from insta import Insta
from face import Facebook

# def update_logs(message,campaignId):
#     try:
#         url = "http://127.0.0.1:3000/api/updatedata"
#         data = {"campaignId": campaignId,
#                 "userId": "65c0b0ff6ef53ae8d0659d77",
#                 "message":message}  # Replace with your actual data
#         response = requests.put(url, json=data)

#         print(response.status_code)
#     except Exception as e:
#         print(f'FAILED TO UPDATE STATUS : {str(e)}')


def process_facebook_request(configuration):
    print(configuration)                
    inst = Facebook()

    try:
        inst.login_fb(configuration['username'],configuration['password'],configuration['campaignId'])
    except Exception as e:
        print(f'Error while logging in : {str(e)}')            
        return {'message':'failed to login'}

    if 'publish' in configuration:
        try:
            file_status = False
            # current_directory = os.getcwd()
            # save_file_path = os.path.join(current_directory, 'pic.png')
            save_file_path = ''
            # print(current_directory)
            if 'filename' in configuration:                  
                file_status = True
                save_file_path = f'/home/junaid/bot/{configuration["filename"]}'

            inst.publish_post(configuration['publish'],configuration['groupId'],configuration['campaignId'],file_status,save_file_path)
        except Exception as e:    
            print(f'Error while publishing : {str(e)}')                          
            return {'message':'failed to publish'}

    if 'comment' in configuration:
        try:
            file_status = False
            # current_directory = os.getcwd()
            # save_file_path = os.path.join(current_directory, 'pic.png')
            save_file_path = ''
            # print(current_directory)
            if 'filename' in configuration:                  
                file_status = True
                save_file_path = f'/home/junaid/bot/{configuration["filename"]}'


            inst.write_comment(int(configuration['limit']),configuration['comment'],file_status,save_file_path,configuration['groupId'],configuration['campaignId'])
        except Exception as e:
            print(f'Error while commenting : {str(e)}')             
            return {'message':'failed to comment'}

            
    elif 'private messages' in configuration:
        try:                    
            inst.sendMessage(configuration['private messages'],int(configuration['limit']),configuration['groupId'],configuration['campaignId'])
        except Exception as e:                
            print(f'Error while sending private message : {str(e)}')
            return {'message':'failed to send private messages'}    
    

def process_instagram_request(configuration):
        inst = Insta()
        try:
            inst.login(configuration['username'],configuration['password'],configuration['campaignId'])
        except Exception as e:
            print(f'Error while logging in : {str(e)}')  
            return {'Message':'Login Failed'}
        
        try:
            inst.search_by_hashtag(configuration['hashtag'].replace('#',''))
        except Exception as e:
            print(f'Error while searching hashtag : {str(e)}')  

        if 'comment' and 'privateMessage' in configuration:

            try:
                inst.comment_post(1,int(configuration['limit']),configuration['comment'],1,configuration['privateMessage'],configuration['campaignId'])
            except Exception as e:
                print(f'Error while commenting and sending private message on post: {str(e)}')              
                return {'Comment + Private Message':str(e)}
                

        elif 'comment' in configuration:
            try:
                inst.comment_post(1,int(configuration['limit']),configuration['comment'],0,'None',configuration['campaignId'])
            except Exception as e:          
                print(f'Error while commenting on post: {str(e)}')     
                return {'Comment + Private Message':str(e)}
                

        elif 'privateMessage' in configuration:
            try:
                inst.comment_post(0,int(configuration['limit']),'None',1,configuration['privateMessage'])
            except Exception as e:
                print(f'Error while sending private message post: {str(e)}')             
                return {'Comment + Private Message':str(e)}
                
