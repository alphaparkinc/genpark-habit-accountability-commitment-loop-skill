import sys
import json
import time
from client import HabitAccountabilityLoop

loop = HabitAccountabilityLoop()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-habit-accountability-commitment-loop-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "register_habit",
                        "description": "Register a new habit commitment with weekly target and accountability partner",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "habit_id": {"type": "string"},
                                "title": {"type": "string"},
                                "target_days_per_week": {"type": "number"},
                                "accountability_partner": {"type": "string"}
                            },
                            "required": ["habit_id", "title"]
                        }
                    },
                    {
                        "name": "checkin",
                        "description": "Record daily completion checkin for a habit",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "habit_id": {"type": "string"}
                            },
                            "required": ["habit_id"]
                        }
                    },
                    {
                        "name": "evaluate_accountability",
                        "description": "Evaluate habit status and generate check-in nudge message",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "habit_id": {"type": "string"}
                            },
                            "required": ["habit_id"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "register_habit":
            loop.register_habit(args["habit_id"], args["title"], args.get("target_days_per_week", 5), args.get("accountability_partner"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Habit registered successfully"}]}}
        elif tool_name == "checkin":
            res = loop.checkin(args["habit_id"], time.time())
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "evaluate_accountability":
            res = loop.evaluate_accountability(args["habit_id"], time.time())
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
