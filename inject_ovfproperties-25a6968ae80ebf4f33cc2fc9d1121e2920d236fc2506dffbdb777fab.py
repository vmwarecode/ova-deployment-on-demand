import json

def handler(context, inputs):

    outputs = {}
    outputs["customProperties"] = {}
    outputs["customProperties"]['ovf.prop:va-ssh-enabled'] = 'false' # update ovf property
    dict = {"user": "smak"} 
    outputs["customProperties"]["dict"] = json.dumps(dict) # add; only string type is accepted
    
    url = '/deployment/api/deployments/' + inputs['deploymentId']
    resp = context.request(url, 'GET', '')
    print('Tango proxy call executed.')
    print(resp['content'])
    #print(resp['headers'])
    
    json_resp = {}
    try:
        json_resp = json.loads(resp['content'])
    except json.decoder.JSONDecodeError as ex:
        print("Error occured while parsing json response: ")
        print(ex)
        return outputs
        
    ovfProperties = json_resp['inputs']['ovfProperties']
    imageRef = json_resp['inputs']['imageRef']
    url = '/provisioning/uerp/provisioning/mgmt/ovf-info?url=' + imageRef
    resp = context.request(url, 'GET', '')
    print('Tango proxy call executed.')
    print(resp['content'])
    #print(resp['headers'])
    json_resp = {}
    try:
        json_resp = json.loads(resp['content'])
    except json.decoder.JSONDecodeError as ex:
        print("Error occured while parsing json response: ")
        print(ex)
    
    prefix = 'ovf.prop:'  # ovf property prefix
    for k, v in json_resp.items():
      print(k)
      for item in ovfProperties:
        #print(item)
        if k == item['key']: 
          print('key: ' + prefix + k + '; value: ' + item['value'])     
          outputs['customProperties'][prefix + k] = item['value'] # override with user input
        else:
          outputs['customProperties'][prefix + k] = json.dumps(v) # convert to string
    return outputs
