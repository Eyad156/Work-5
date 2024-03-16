import requests

def update_logs(message,campaignId):
    try:
        url = "https://fb-auto-testing.vercel.app/api/updatedata"
        data = {"campaignId": campaignId,
                "userId": "65c3573ad2648786108a7c4e",
                "message":message}  # Replace with your actual data
        response = requests.put(url, json=data)

        print(response.status_code)
    except Exception as e:
        print(f'FAILED TO UPDATE STATUS : {str(e)}')

