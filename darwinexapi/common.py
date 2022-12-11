def not_successful(status_code, response_body):
    print('There was an error processing your request. Error code: {}. Description: {}'.format(status_code, response_body))
    return None