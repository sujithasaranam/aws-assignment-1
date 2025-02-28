import json

def lambda_handler(event, context):
    try:
        order_data = json.loads(event["order"])
        
        if not order_data:
            return {"isValid": False, "reason": "Missing required fields"}
        
        return {"isValid": True, "order": order_data}
    
    except Exception as e:
        return {"isValid": False, "error_event": event, "reason": str(e)}